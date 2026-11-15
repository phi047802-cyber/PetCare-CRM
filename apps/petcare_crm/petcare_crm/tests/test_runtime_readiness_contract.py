"""Static runtime-readiness contracts for Frappe schema, API and RBAC wiring."""

import ast
import importlib
import json
import sys
import types
import unittest
from pathlib import Path


APP_ROOT = Path("apps/petcare_crm/petcare_crm")
DOCTYPE_ROOT = APP_ROOT / "petcare_crm" / "doctype"
sys.path.insert(0, str(Path("apps/petcare_crm").resolve()))
STANDARD_FIELDS = {
    "name", "owner", "creation", "modified", "modified_by", "docstatus", "idx",
    "parent", "parentfield", "parenttype", "_user_tags", "_comments", "_assign",
    "_liked_by",
}


def load_schemas():
    schemas = {}
    for path in DOCTYPE_ROOT.glob("*/*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        if data.get("doctype") == "DocType":
            schemas[data["name"]] = (path, data)
    return schemas


def call_name(node):
    parts = []
    while isinstance(node, ast.Attribute):
        parts.append(node.attr)
        node = node.value
    if isinstance(node, ast.Name):
        parts.append(node.id)
    return ".".join(reversed(parts))


def literal_string(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def literal_fields(node):
    if isinstance(node, (ast.List, ast.Tuple)):
        return [
            item.value for item in node.elts
            if isinstance(item, ast.Constant) and isinstance(item.value, str)
        ]
    value = literal_string(node)
    return [part.strip() for part in value.split(",")] if value else []


class TestRuntimeReadinessContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.schemas = load_schemas()

    def test_01_python_sources_compile(self):
        failures = []
        for path in APP_ROOT.rglob("*.py"):
            try:
                compile(path.read_text(encoding="utf-8"), str(path), "exec")
            except SyntaxError as exc:
                failures.append(f"{path}:{exc.lineno}: {exc.msg}")
        self.assertEqual(failures, [])

    def test_02_doctype_json_and_field_order_are_consistent(self):
        issues = []
        for doctype, (path, data) in self.schemas.items():
            fields = [field.get("fieldname") for field in data.get("fields", [])]
            order = data.get("field_order", [])
            if len(fields) != len(set(fields)):
                issues.append(f"{doctype}: duplicate fieldname")
            missing = set(order) - set(fields)
            unordered = set(fields) - set(order)
            if missing or unordered:
                issues.append(
                    f"{doctype}: missing_fields={sorted(missing)}, unordered={sorted(unordered)}"
                )
        self.assertEqual(issues, [], "\n".join(issues))

    def test_03_literal_frappe_queries_only_use_real_fields(self):
        allowed = {
            name: {
                field.get("fieldname") for field in data.get("fields", [])
                if field.get("fieldname")
            } | STANDARD_FIELDS
            for name, (_, data) in self.schemas.items()
        }
        supported = {
            "frappe.db.get_list", "frappe.db.get_all", "frappe.get_all",
            "frappe.db.get_value", "frappe.db.exists",
        }
        issues = []
        for path in APP_ROOT.rglob("*.py"):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if not isinstance(node, ast.Call) or call_name(node.func) not in supported:
                    continue
                doctype = literal_string(node.args[0]) if node.args else None
                if doctype not in allowed:
                    continue
                used = []
                if call_name(node.func).endswith("get_value") and len(node.args) > 2:
                    used.extend(literal_fields(node.args[2]))
                for keyword in node.keywords:
                    if keyword.arg in {"fields", "fieldname"}:
                        used.extend(literal_fields(keyword.value))
                    if keyword.arg == "filters" and isinstance(keyword.value, ast.Dict):
                        used.extend(
                            value for key in keyword.value.keys
                            if (value := literal_string(key))
                        )
                for field in used:
                    base = field.split(" as ")[0].strip().split(".")[0]
                    if "(" not in base and base not in allowed[doctype]:
                        issues.append(f"{path}:{node.lineno}: {doctype}.{field}")
        self.assertEqual(issues, [], "\n".join(issues))

    def test_04_literal_document_payloads_match_doctype_schema(self):
        field_maps = {
            name: {field["fieldname"]: field for field in data.get("fields", [])}
            for name, (_, data) in self.schemas.items()
        }
        issues = []

        def validate_payload(payload, doctype, path, line):
            if doctype not in field_maps:
                return
            values = {
                key.value: value
                for key, value in zip(payload.keys, payload.values)
                if isinstance(key, ast.Constant) and isinstance(key.value, str)
            }
            for fieldname, value in values.items():
                if fieldname == "doctype":
                    continue
                meta = field_maps[doctype].get(fieldname)
                if not meta:
                    issues.append(f"{path}:{line}: unknown {doctype}.{fieldname}")
                    continue
                if meta.get("fieldtype") == "Select":
                    literal = literal_string(value)
                    options = set(str(meta.get("options", "")).splitlines())
                    if literal is not None and literal not in options:
                        issues.append(
                            f"{path}:{line}: invalid {doctype}.{fieldname}={literal!r}"
                        )
                if meta.get("fieldtype") == "Table" and isinstance(value, ast.List):
                    for child in value.elts:
                        if isinstance(child, ast.Dict):
                            validate_payload(child, meta.get("options"), path, line)

        for path in APP_ROOT.rglob("*.py"):
            source = path.read_text(encoding="utf-8")
            tree = ast.parse(source)
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and call_name(node.func) == "frappe.get_doc"
                    and node.args
                    and isinstance(node.args[0], ast.Dict)
                ):
                    payload = node.args[0]
                    values = {
                        key.value: value
                        for key, value in zip(payload.keys, payload.values)
                        if isinstance(key, ast.Constant) and isinstance(key.value, str)
                    }
                    doctype = literal_string(values.get("doctype"))
                    validate_payload(payload, doctype, path, node.lineno)
        self.assertEqual(issues, [], "\n".join(issues))

    def test_05_whitelisted_api_has_explicit_authorization_contract(self):
        path = APP_ROOT / "api.py"
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
        expected_guest = {
            "get_available_plans", "submit_website_lead", "payment_webhook",
            "owner_portal_get_pets", "owner_portal_get_health_timeline",
            "owner_portal_get_membership_wallet", "owner_portal_book_appointment",
            "woocommerce_order_webhook",
        }
        actual_guest = set()
        unguarded = []
        guard_calls = {
            "check_role_permission", "require_any_role", "_verify_owner_portal_access",
        }
        for node in tree.body:
            if not isinstance(node, ast.FunctionDef):
                continue
            whitelisted = False
            guest = False
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Call) and call_name(decorator.func) == "frappe.whitelist":
                    whitelisted = True
                    guest = any(
                        keyword.arg == "allow_guest"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value is True
                        for keyword in decorator.keywords
                    )
                elif call_name(decorator) == "frappe.whitelist":
                    whitelisted = True
            if not whitelisted:
                continue
            if guest:
                actual_guest.add(node.name)
                continue
            calls = {
                call_name(child.func).split(".")[-1]
                for child in ast.walk(node)
                if isinstance(child, ast.Call)
            }
            if not calls.intersection(guard_calls) and node.name != "reset_demo_dataset":
                unguarded.append(f"{node.lineno}:{node.name}")
        self.assertEqual(actual_guest, expected_guest)
        self.assertEqual(unguarded, [])

    def test_06_no_administrator_impersonation_or_default_secrets(self):
        source = (APP_ROOT / "api.py").read_text(encoding="utf-8")
        payment_source = (APP_ROOT / "utils" / "payment_gateway.py").read_text(
            encoding="utf-8"
        )
        self.assertNotIn('frappe.set_user("Administrator")', source)
        self.assertNotIn("petcare_webhook_secret_key_2026", payment_source)
        self.assertNotIn("petcare-owner-portal-secret", source)
        self.assertIn("MIN_WEBHOOK_SECRET_LENGTH", payment_source)
        self.assertIn("owner_portal_secret", source)
        repository_text = "\n".join(
            path.read_text(encoding="utf-8", errors="ignore")
            for path in Path(".").rglob("*")
            if path.is_file()
            and ".git" not in path.parts
            and path.suffix.lower() in {".py", ".md", ".json", ".ps1", ".yml", ".yaml"}
        )
        self.assertNotIn("admin" + "123", repository_text)
        self.assertNotIn("SANDBOX_SECRET_KEY_" + "PETCARE_2026", repository_text)

    def test_07_rbac_matrix_matches_doctype_permissions(self):
        fake_frappe = types.ModuleType("frappe")
        fake_frappe._ = lambda value: value
        original_frappe = sys.modules.get("frappe")
        sys.modules["frappe"] = fake_frappe
        try:
            security = importlib.import_module("petcare_crm.utils.security")
            security = importlib.reload(security)
            matrix = security.ROLE_PERMISSIONS
        finally:
            if original_frappe is None:
                sys.modules.pop("frappe", None)
            else:
                sys.modules["frappe"] = original_frappe

        operations = {"read", "write", "create", "delete", "cancel", "report", "export"}
        issues = []
        for doctype, (_, data) in self.schemas.items():
            for permission in data.get("permissions", []):
                role = permission.get("role")
                if role not in matrix:
                    continue
                metadata_ops = {op for op in operations if permission.get(op)}
                matrix_ops = matrix[role].get(doctype, set())
                if metadata_ops != matrix_ops:
                    issues.append(
                        f"{doctype}/{role}: meta={sorted(metadata_ops)}, matrix={sorted(matrix_ops)}"
                    )
        self.assertEqual(issues, [], "\n".join(issues))

    def test_08_all_custom_roles_are_installed_and_exported(self):
        metadata_roles = {
            permission["role"]
            for _, data in self.schemas.values()
            for permission in data.get("permissions", [])
            if str(permission.get("role", "")).startswith("PetCare ")
        }
        install_source = (APP_ROOT / "setup" / "install.py").read_text(encoding="utf-8")
        hooks_source = (APP_ROOT / "hooks.py").read_text(encoding="utf-8")
        missing_install = sorted(role for role in metadata_roles if role not in install_source)
        missing_fixture = sorted(role for role in metadata_roles if role not in hooks_source)
        self.assertEqual(missing_install, [])
        self.assertEqual(missing_fixture, [])


if __name__ == "__main__":
    unittest.main()
