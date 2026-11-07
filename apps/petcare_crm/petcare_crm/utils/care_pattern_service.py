"""
Care Pattern Intelligence & Analytics Engine (Rule-based).
Conforms to Single Responsibility Principle (SRP) and Clean Architecture:
- CarePatternAnalyzer: Statistical analysis of visit intervals (IQR outlier detection, EWMA, deltas).
- VisitPredictionService: Rule-based next visit prediction with qualitative confidence levels.
- RiskDetectionService: Due Soon & At Risk absence ratio evaluation with explainability.
- CarePatternService: Unified facade maintaining 100% backward compatibility.
"""

from datetime import date, datetime, timedelta
import statistics
from typing import Any, Dict, List, Optional, Tuple, Union

from petcare_crm.utils.config import (
    AT_RISK_RATIO,
    DUE_SOON_THRESHOLD_DAYS,
    MIN_VISITS_FOR_INTERVAL,
    get_service_thresholds,
)
from petcare_crm.utils.models import (
    AtRiskResult,
    DueSoonResult,
    PatternResult,
    PredictionResult,
    RiskEvaluationResult,
)


def _extract_date(val: Any) -> Optional[date]:
    """Extract datetime.date from date, datetime, string, or object."""
    if val is None:
        return None
    if isinstance(val, datetime):
        return val.date()
    if isinstance(val, date):
        return val
    if isinstance(val, str):
        try:
            return datetime.strptime(val[:10], "%Y-%m-%d").date()
        except Exception:
            return None
    return None


def _get_field(obj: Any, key: str, default: Any = None) -> Any:
    """Helper to get field from object, dict, or primitive."""
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _filter_iqr_outliers(deltas: List[int]) -> List[int]:
    """
    Filters out Statistical Outliers using Interquartile Range (IQR) method when len >= 4.
    Fences: [Q1 - 1.5*IQR, Q3 + 1.5*IQR] (Standard inclusive quartile interpolation).
    """
    clean, _, _, _ = CarePatternAnalyzer.filter_outliers_iqr(deltas)
    return clean


def _calculate_ewma(deltas: List[int], alpha: float = 0.6) -> float:
    """
    Calculates Exponentially Weighted Moving Average (EWMA) giving higher weight to recent deltas.
    """
    return CarePatternAnalyzer.calculate_ewma(deltas, alpha)


class CarePatternAnalyzer:
    """
    Pure statistical and pattern analyzer for pet service visits.
    Responsible for:
    - Segregating visits by (pet, service_type)
    - Computing raw intervals (deltas)
    - Handling same-day visits (delta=0)
    - Identifying and filtering statistical outliers via IQR
    - Calculating typical interval via EWMA (recency-weighted) and Arithmetic Mean/Median
    - Determining data sufficiency and qualitative confidence
    """

    @staticmethod
    def extract_visit_deltas(
        pet: str,
        service_type: str,
        visits: List[Any],
    ) -> Tuple[List[Any], List[int], List[int], int]:
        """
        Filters and sorts visits for the specific pet and service type.
        Returns:
            (matching_visits, raw_deltas, positive_deltas, same_day_count)
        """
        pet_str = str(pet).strip()
        service_str = str(service_type).strip().lower()

        matching_visits = []
        for v in visits:
            v_pet = _get_field(v, "pet")
            v_service = _get_field(v, "service_type") or _get_field(v, "service") or ""

            if str(v_pet).strip() == pet_str and str(v_service).strip().lower() == service_str:
                d = _extract_date(_get_field(v, "visit_date"))
                if d is not None:
                    matching_visits.append((d, v))

        # Sort chronologically by visit_date
        matching_visits.sort(key=lambda x: x[0])
        sorted_visits = [x[1] for x in matching_visits]
        visit_dates = [x[0] for x in matching_visits]

        raw_deltas: List[int] = []
        for i in range(1, len(visit_dates)):
            delta_days = (visit_dates[i] - visit_dates[i - 1]).days
            raw_deltas.append(delta_days)

        positive_deltas = [d for d in raw_deltas if d > 0]
        same_day_count = sum(1 for d in raw_deltas if d == 0)

        return sorted_visits, raw_deltas, positive_deltas, same_day_count

    @staticmethod
    def filter_outliers_iqr(
        deltas: List[int],
    ) -> Tuple[List[int], List[int], float, float]:
        """
        Identifies and separates statistical outliers using Interquartile Range (IQR).
        Requires at least 4 observations to compute meaningful quartiles.
        Fences: [Q1 - 1.5 * IQR, Q3 + 1.5 * IQR]
        Returns:
            (clean_deltas, outliers_detected, lower_fence, upper_fence)
        """
        if len(deltas) < 4:
            return list(deltas), [], 0.0, 0.0

        try:
            q1, _, q3 = statistics.quantiles(deltas, n=4, method="inclusive")
            iqr = q3 - q1
            lower_fence = q1 - 1.5 * iqr
            upper_fence = q3 + 1.5 * iqr

            clean_deltas = [d for d in deltas if lower_fence <= d <= upper_fence]
            outliers = [d for d in deltas if d < lower_fence or d > upper_fence]

            # If all deltas were filtered out, preserve originals
            if not clean_deltas:
                return list(deltas), [], lower_fence, upper_fence

            return clean_deltas, outliers, lower_fence, upper_fence
        except Exception:
            return list(deltas), [], 0.0, 0.0

    @staticmethod
    def calculate_ewma(deltas: List[int], alpha: float = 0.6) -> float:
        """
        Computes Exponentially Weighted Moving Average (EWMA).
        Alpha in [0.0, 1.0] controls responsiveness to recent intervals.
        """
        if not deltas:
            return 0.0
        if len(deltas) == 1:
            return float(deltas[0])

        ewma = float(deltas[0])
        for d in deltas[1:]:
            ewma = alpha * d + (1.0 - alpha) * ewma

        return round(ewma, 2)

    @classmethod
    def analyze_pattern(
        cls,
        pet: str,
        service_type: str,
        visits: List[Any],
        use_ewma: bool = True,
        filter_outliers: bool = True,
        min_visits_for_stable: int = MIN_VISITS_FOR_INTERVAL,
    ) -> PatternResult:
        """
        Performs end-to-end service cycle pattern analysis for (Pet, Service Type).
        """
        sorted_visits, raw_deltas, positive_deltas, same_day_count = cls.extract_visit_deltas(
            pet, service_type, visits
        )
        total_visits = len(sorted_visits)
        last_visit_date = _extract_date(_get_field(sorted_visits[-1], "visit_date")) if sorted_visits else None

        # Case 0: No visits at all
        if total_visits == 0:
            return PatternResult(
                pet=pet,
                service_type=service_type,
                number_of_visits=0,
                last_visit_date=None,
                data_sufficiency="INSUFFICIENT",
                confidence="NONE",
                insufficient_data=True,
                reason="Chưa có lượt sử dụng dịch vụ nào cho thú cưng này.",
            )

        # Case 1: Exactly 1 visit (distance cannot be measured)
        if total_visits == 1:
            return PatternResult(
                pet=pet,
                service_type=service_type,
                number_of_visits=1,
                last_visit_date=last_visit_date,
                data_sufficiency="INSUFFICIENT",
                confidence="NONE",
                insufficient_data=True,
                reason="Chỉ có 1 lượt sử dụng dịch vụ. Cần ít nhất 2 lượt để đo khoảng cách chu kỳ.",
            )

        # Case 2: Visits occurred but all were same-day (deltas == 0)
        if not positive_deltas:
            return PatternResult(
                pet=pet,
                service_type=service_type,
                number_of_visits=total_visits,
                last_visit_date=last_visit_date,
                raw_deltas=raw_deltas,
                data_sufficiency="INSUFFICIENT",
                confidence="NONE",
                insufficient_data=True,
                reason=f"Có {total_visits} lượt sử dụng nhưng toàn bộ diễn ra cùng ngày ({same_day_count} lượt trùng). Chưa hình thành chu kỳ phân biệt.",
            )

        # Filter statistical outliers using IQR when data sufficiency allows
        clean_deltas, outliers, _, _ = cls.filter_outliers_iqr(positive_deltas) if filter_outliers else (list(positive_deltas), [], 0.0, 0.0)

        # Compute intervals: EWMA, arithmetic mean, median
        ewma_val = cls.calculate_ewma(clean_deltas, alpha=0.6)
        mean_val = round(statistics.mean(clean_deltas), 2)
        median_val = round(float(statistics.median(clean_deltas)), 2)

        typical_interval = ewma_val if use_ewma else mean_val

        # Assess data sufficiency & qualitative confidence
        if total_visits == 2:
            data_sufficiency = "MINIMAL"
            confidence = "LOW"
            insufficient_data = total_visits < min_visits_for_stable
            reason = (
                f"Có 2 lượt sử dụng (1 khoảng cách = {positive_deltas[0]} ngày). "
                f"Chu kỳ sơ bộ, độ tin cậy thấp."
            )
        elif total_visits < 5:
            data_sufficiency = "SUFFICIENT"
            confidence = "MEDIUM"
            insufficient_data = False
            reason = (
                f"Đã có {total_visits} lượt sử dụng ({len(clean_deltas)} khoảng cách). "
                f"Chu kỳ ổn định, độ tin cậy vừa."
            )
        else:
            data_sufficiency = "SUFFICIENT"
            confidence = "HIGH"
            insufficient_data = False
            outlier_info = f", đã loại {len(outliers)} ngoại lai" if outliers else ""
            reason = (
                f"Đã có {total_visits} lượt sử dụng ({len(clean_deltas)} khoảng cách{outlier_info}). "
                f"Chu kỳ trưởng thành với bộ lọc IQR, độ tin cậy cao."
            )

        return PatternResult(
            pet=pet,
            service_type=service_type,
            number_of_visits=total_visits,
            last_visit_date=last_visit_date,
            raw_deltas=raw_deltas,
            filtered_deltas=clean_deltas,
            outliers_detected=outliers,
            typical_interval=typical_interval,
            arithmetic_mean=mean_val,
            median_interval=median_val,
            data_sufficiency=data_sufficiency,
            confidence=confidence,
            insufficient_data=insufficient_data,
            reason=reason,
        )


class SeasonalAdjustmentHelper:
    """
    Evaluates seasonal impact on pet care intervals (Prompt 10 / Limitation 2.1 Extension).
    Accounts for tropical/subtropical seasonal changes in Vietnam:
    - Spring Shedding (Mar-Apr): factor 0.85 (shorter grooming/spa cycle due to shedding season)
    - Summer/Monsoon Humidity (May-Aug): factor 0.80 (shorter cycle for hygiene, dermatology, tick/bath care)
    - Autumn Pre-Winter Molting (Sep-Oct): factor 0.88 (shedding preparation)
    - Winter (Nov-Feb): factor 1.05 (slightly longer bathing cycle to prevent cold, unless medical hygiene requires)
    """

    @staticmethod
    def get_seasonal_factor(month: int, service_type: str = "") -> float:
        st = str(service_type).lower()
        # Primary impact on grooming, spa, hygiene, bath care
        if not any(k in st for k in ["groom", "spa", "tắm", "cắt tỉa", "vệ sinh", "da", "nail"]):
            return 1.0

        if month in (3, 4):  # Spring shedding
            return 0.85
        elif month in (5, 6, 7, 8):  # Hot/rainy season
            return 0.80
        elif month in (9, 10):  # Autumn shedding
            return 0.88
        elif month in (11, 12, 1, 2):  # Winter
            return 1.05
        return 1.0


class PetAgeAdjustmentHelper:
    """
    Evaluates age-based development impact on pet care cycle (Limitation 2.1 Extension):
    - Puppy/Kitten (< 12 months): fast fur growth, hygiene habituation, higher vaccination frequency (factor 0.85)
    - Adult (12 - 84 months / 1-7 yrs): standard maintenance (factor 1.0)
    - Senior (> 84 months / > 7 yrs): lower self-grooming, higher susceptibility to joint/skin issues (factor 0.80)
    """

    @staticmethod
    def get_age_factor(age_months: Optional[int], service_type: str = "") -> float:
        if age_months is None or age_months < 0:
            return 1.0
        if age_months < 12:
            return 0.85
        elif age_months > 84:
            return 0.80
        return 1.0

    @staticmethod
    def calculate_age_months(
        birth_date: Optional[Union[str, date]],
        target_date: Optional[date] = None,
    ) -> Optional[int]:
        bdate = _extract_date(birth_date)
        if not bdate:
            return None
        tdate = target_date or date.today()
        if bdate > tdate:
            return 0
        diff_days = (tdate - bdate).days
        return int(diff_days // 30.4375)


class VisitPredictionService:
    """
    Rule-based prediction service for next pet service visit.
    Formula: predicted_next_visit = last_visit_date + timedelta(days=round(typical_interval * seasonal_factor * age_factor))
    Includes explicit qualitative confidence ratings and rule-based estimation disclaimer.
    """

    @classmethod
    def predict_next_visit(
        cls,
        pet: str,
        service_type: str,
        visits: List[Any],
        current_date: Optional[date] = None,
        pet_age_months: Optional[int] = None,
        pet_birth_date: Optional[Union[str, date]] = None,
        enable_seasonal_adjustment: bool = False,
        enable_age_adjustment: bool = False,
    ) -> PredictionResult:
        """
        Generates next visit prediction based on analyzed pattern.
        Optionally applies seasonal shedding factor and pet developmental age factor.
        """
        pattern = CarePatternAnalyzer.analyze_pattern(pet, service_type, visits)

        if pattern.typical_interval is None or pattern.last_visit_date is None:
            return PredictionResult(
                pet=pet,
                service_type=service_type,
                predicted_next_visit=None,
                average_interval=pattern.typical_interval,
                last_visit_date=pattern.last_visit_date,
                number_of_visits=pattern.number_of_visits,
                confidence=pattern.confidence,
                insufficient_data=True,
                reason=pattern.reason,
            )

        ref_date = current_date or pattern.last_visit_date
        s_factor = 1.0
        if enable_seasonal_adjustment:
            ref_month = ref_date.month if ref_date else date.today().month
            s_factor = SeasonalAdjustmentHelper.get_seasonal_factor(ref_month, service_type)

        a_factor = 1.0
        if enable_age_adjustment:
            calc_age = pet_age_months
            if calc_age is None and pet_birth_date:
                calc_age = PetAgeAdjustmentHelper.calculate_age_months(pet_birth_date, ref_date)
            a_factor = PetAgeAdjustmentHelper.get_age_factor(calc_age, service_type)

        combined_factor = s_factor * a_factor
        adjusted_interval = round(pattern.typical_interval * combined_factor, 2)
        days_forward = max(1, int(round(adjusted_interval)))
        predicted_date = pattern.last_visit_date + timedelta(days=days_forward)

        # Build informative reason string
        reason_notes = []
        if enable_seasonal_adjustment and s_factor != 1.0:
            reason_notes.append(f"hệ số mùa vụ={s_factor:.2f}")
        if enable_age_adjustment and a_factor != 1.0:
            reason_notes.append(f"hệ số độ tuổi={a_factor:.2f}")

        note_str = f" ({', '.join(reason_notes)})" if reason_notes else ""
        reason = (
            f"Dự đoán ngày {predicted_date} dựa trên chu kỳ điển hình {adjusted_interval:.1f} ngày"
            f"{note_str} kể từ lần khám gần nhất {pattern.last_visit_date}."
        )

        return PredictionResult(
            pet=pet,
            service_type=service_type,
            predicted_next_visit=predicted_date,
            average_interval=pattern.typical_interval,
            last_visit_date=pattern.last_visit_date,
            number_of_visits=pattern.number_of_visits,
            confidence=pattern.confidence,
            insufficient_data=pattern.insufficient_data,
            is_rule_based_estimate=True,
            disclaimer="Dự đoán mang tính chất tham khảo dựa trên tần suất lịch sử, không phải lịch hẹn đã xác nhận.",
            reason=reason,
            seasonal_factor=s_factor,
            age_factor=a_factor,
            adjusted_interval=adjusted_interval if (enable_seasonal_adjustment or enable_age_adjustment) else None,
        )


class RiskDetectionService:
    """
    Evaluates pet care risk:
    - Due Soon: predicted date approaching within threshold (not triggered on visit day)
    - At Risk: absence ratio = days_since_last_visit / typical_interval >= threshold (e.g. 1.5)
    High explainability with localized reason text.
    """

    @classmethod
    def detect_due_soon(
        cls,
        pet: str,
        service_type: str,
        visits: List[Any],
        current_date: Optional[date] = None,
        threshold_days: Optional[int] = None,
    ) -> DueSoonResult:
        """
        Detects if pet is due soon for service.
        """
        if current_date is None:
            current_date = date.today()
        else:
            current_date = _extract_date(current_date) or date.today()

        service_defaults = get_service_thresholds(service_type)
        if threshold_days is None:
            threshold_days = service_defaults["due_soon_days"]

        pred = VisitPredictionService.predict_next_visit(pet, service_type, visits, current_date)
        if pred.insufficient_data or pred.predicted_next_visit is None or pred.last_visit_date is None:
            return DueSoonResult(
                pet=pet,
                service_type=service_type,
                status="UNKNOWN",
                is_due_soon=False,
                threshold_days=threshold_days,
                effective_threshold=threshold_days,
                reason="Chưa đủ dữ liệu lịch sử để dự đoán ngày đến hạn.",
            )

        avg_interval = pred.average_interval or 0.0
        days_until_due = (pred.predicted_next_visit - current_date).days
        days_since_last_visit = (current_date - pred.last_visit_date).days

        # Dynamic cap: threshold cannot exceed 40% of typical interval
        effective_threshold = min(threshold_days, max(1, int(round(avg_interval * 0.4))))

        # Pet visited today or in future is NEVER due soon
        is_due_soon = (days_since_last_visit > 0) and (0 <= days_until_due <= effective_threshold)

        if is_due_soon:
            status = "DUE_SOON"
            reason = f"Còn {days_until_due} ngày tới ngày dự kiến ({pred.predicted_next_visit}), nằm trong ngưỡng cảnh báo {effective_threshold} ngày."
        elif days_until_due < 0:
            status = "OVERDUE"
            reason = f"Đã quá ngày dự kiến {abs(days_until_due)} ngày ({pred.predicted_next_visit})."
        else:
            status = "NOT_DUE"
            reason = f"Chưa đến hạn chăm sóc (còn {days_until_due} ngày, ngưỡng: {effective_threshold} ngày)."

        return DueSoonResult(
            pet=pet,
            service_type=service_type,
            status=status,
            is_due_soon=is_due_soon,
            predicted_date=pred.predicted_next_visit,
            days_until_due=days_until_due,
            days_since_last_visit=days_since_last_visit,
            threshold_days=threshold_days,
            effective_threshold=effective_threshold,
            reason=reason,
        )

    @classmethod
    def detect_at_risk(
        cls,
        pet: str,
        service_type: str,
        visits: List[Any],
        current_date: Optional[date] = None,
        at_risk_ratio_threshold: Optional[float] = None,
    ) -> AtRiskResult:
        """
        Detects if customer/pet is at risk based on absence ratio.
        absence_ratio = days_since_last_visit / typical_interval
        """
        if current_date is None:
            current_date = date.today()
        else:
            current_date = _extract_date(current_date) or date.today()

        service_defaults = get_service_thresholds(service_type)
        if at_risk_ratio_threshold is None:
            at_risk_ratio_threshold = service_defaults["at_risk_ratio"]

        pattern = CarePatternAnalyzer.analyze_pattern(pet, service_type, visits)
        if pattern.insufficient_data or pattern.typical_interval is None or pattern.typical_interval <= 0 or pattern.last_visit_date is None:
            return AtRiskResult(
                pet=pet,
                service_type=service_type,
                status="UNKNOWN",
                is_at_risk=False,
                threshold_ratio=at_risk_ratio_threshold,
                reason="Chưa đủ dữ liệu lịch sử để tính tỷ lệ vắng mặt.",
            )

        days_since_last_visit = (current_date - pattern.last_visit_date).days
        absence_ratio = round(days_since_last_visit / pattern.typical_interval, 2)
        is_at_risk = absence_ratio >= at_risk_ratio_threshold

        status = "AT_RISK" if is_at_risk else "NOT_AT_RISK"
        if is_at_risk:
            reason = (
                f"Pet đã vắng mặt {days_since_last_visit} ngày, tỷ lệ vắng mặt {absence_ratio:.2f}x "
                f"vượt ngưỡng cảnh báo {at_risk_ratio_threshold:.2f}x (chu kỳ thông thường: {pattern.typical_interval:.1f} ngày)."
            )
        else:
            reason = (
                f"Tỷ lệ vắng mặt {absence_ratio:.2f}x ({days_since_last_visit} ngày) "
                f"vẫn trong giới hạn an toàn so với chu kỳ {pattern.typical_interval:.1f} ngày."
            )

        return AtRiskResult(
            pet=pet,
            service_type=service_type,
            status=status,
            is_at_risk=is_at_risk,
            average_interval=pattern.typical_interval,
            days_since_last_visit=days_since_last_visit,
            absence_ratio=absence_ratio,
            last_visit_date=pattern.last_visit_date,
            threshold_ratio=at_risk_ratio_threshold,
            reason=reason,
        )

    @classmethod
    def evaluate_care_risk(
        cls,
        pet: str,
        service_type: str,
        visits: List[Any],
        current_date: Optional[date] = None,
    ) -> RiskEvaluationResult:
        """
        Evaluates overall care risk synthesizing Pattern, Prediction, Due Soon, and At Risk.
        """
        pattern = CarePatternAnalyzer.analyze_pattern(pet, service_type, visits)
        pred = VisitPredictionService.predict_next_visit(pet, service_type, visits, current_date)
        due_soon = cls.detect_due_soon(pet, service_type, visits, current_date)
        at_risk = cls.detect_at_risk(pet, service_type, visits, current_date)

        if pattern.insufficient_data:
            overall_status = "INSUFFICIENT_DATA"
        elif at_risk.is_at_risk:
            overall_status = "AT_RISK"
        elif due_soon.status == "OVERDUE":
            overall_status = "OVERDUE"
        elif due_soon.is_due_soon:
            overall_status = "DUE_SOON"
        else:
            overall_status = "NOT_DUE"

        return RiskEvaluationResult(
            pet=pet,
            service_type=service_type,
            overall_status=overall_status,
            due_soon=due_soon,
            at_risk=at_risk,
            pattern=pattern,
            prediction=pred,
        )


class CarePatternService:
    """
    Unified facade class for backward compatibility.
    Exposes familiar methods returning dicts while delegating directly to SRP classes.
    """

    @classmethod
    def calculate_average_interval(
        cls,
        pet: str,
        service_type: str,
        visits: List[Any],
        use_ewma: bool = True,
        filter_outliers: bool = True,
    ) -> Dict[str, Any]:
        """Calculates interval pattern and returns dictionary."""
        p = CarePatternAnalyzer.analyze_pattern(
            pet=pet,
            service_type=service_type,
            visits=visits,
            use_ewma=use_ewma,
            filter_outliers=filter_outliers,
        )
        return {
            "average_interval": p.typical_interval,
            "number_of_visits": p.number_of_visits,
            "last_visit_date": p.last_visit_date,
            "service_type": p.service_type,
            "insufficient_data": p.insufficient_data,
            "reason": p.reason,
            "raw_deltas": p.raw_deltas,
            "filtered_deltas": p.filtered_deltas,
            "outliers_removed": len(p.outliers_detected),
            "data_sufficiency": p.data_sufficiency,
            "confidence": p.confidence,
            "arithmetic_mean": p.arithmetic_mean,
            "median_interval": p.median_interval,
        }

    @classmethod
    def predict_next_visit(
        cls,
        pet: str,
        service_type: str,
        visits: List[Any],
        current_date: Optional[date] = None,
        pet_age_months: Optional[int] = None,
        pet_birth_date: Optional[Union[str, date]] = None,
        enable_seasonal_adjustment: bool = False,
        enable_age_adjustment: bool = False,
    ) -> Dict[str, Any]:
        """Predicts next visit date and returns dictionary."""
        pred = VisitPredictionService.predict_next_visit(
            pet=pet,
            service_type=service_type,
            visits=visits,
            current_date=current_date,
            pet_age_months=pet_age_months,
            pet_birth_date=pet_birth_date,
            enable_seasonal_adjustment=enable_seasonal_adjustment,
            enable_age_adjustment=enable_age_adjustment,
        )
        return {
            "predicted_next_visit": pred.predicted_next_visit,
            "average_interval": pred.average_interval,
            "last_visit_date": pred.last_visit_date,
            "number_of_visits": pred.number_of_visits,
            "service_type": pred.service_type,
            "insufficient_data": pred.insufficient_data,
            "confidence": pred.confidence,
            "is_rule_based_estimate": pred.is_rule_based_estimate,
            "disclaimer": pred.disclaimer,
            "reason": pred.reason,
            "seasonal_factor": pred.seasonal_factor,
            "age_factor": pred.age_factor,
            "adjusted_interval": pred.adjusted_interval,
        }

    @classmethod
    def detect_due_soon(
        cls,
        pet: str,
        service_type: str,
        visits: List[Any],
        current_date: Optional[date] = None,
        threshold_days: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Detects due soon and returns dictionary."""
        ds = RiskDetectionService.detect_due_soon(
            pet=pet,
            service_type=service_type,
            visits=visits,
            current_date=current_date,
            threshold_days=threshold_days,
        )
        return {
            "status": ds.status,
            "is_due_soon": ds.is_due_soon,
            "predicted_date": ds.predicted_date,
            "days_until_due": ds.days_until_due,
            "days_since_last_visit": ds.days_since_last_visit,
            "service_type": ds.service_type,
            "threshold_days": ds.threshold_days,
            "effective_threshold": ds.effective_threshold,
            "reason": ds.reason,
        }

    @classmethod
    def detect_at_risk(
        cls,
        pet: str,
        service_type: str,
        visits: List[Any],
        current_date: Optional[date] = None,
        at_risk_ratio_threshold: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Detects at risk and returns dictionary."""
        ar = RiskDetectionService.detect_at_risk(
            pet=pet,
            service_type=service_type,
            visits=visits,
            current_date=current_date,
            at_risk_ratio_threshold=at_risk_ratio_threshold,
        )
        return {
            "status": ar.status,
            "is_at_risk": ar.is_at_risk,
            "average_interval": ar.average_interval,
            "days_since_last_visit": ar.days_since_last_visit,
            "absence_ratio": ar.absence_ratio,
            "last_visit_date": ar.last_visit_date,
            "service_type": ar.service_type,
            "threshold_ratio": ar.threshold_ratio,
            "reason": ar.reason,
        }
