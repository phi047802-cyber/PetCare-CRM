app_name = "petcare_crm"
app_title = "PetCare CRM"
app_publisher = "PetCare Team"
app_description = "PetCare CRM - Complete Pet Care Customer Lifecycle & Automation"
app_email = "team@petcare.com"
app_license = "MIT"
app_version = "1.0.0"

# Default home page
home_page = "index"

# ─────────────────────────────────────────────────────────────────────
# FIXTURES (Finding-08 Fix: Role & Permissions Export)
# ─────────────────────────────────────────────────────────────────────
fixtures = [
    {
        "doctype": "Role",
        "filters": [
            [
                "name",
                "in",
                [
                    "PetCare Front Desk",
                    "PetCare Veterinarian",
                    "PetCare Groomer",
                    "PetCare Manager",
                    "PetCare Sales",
                    "PetCare Analyst",
                    "PetCare Customer Portal",
                ],
            ]
        ],
    }
]

# Migration & Install Hooks
after_migrate = "petcare_crm.setup.install.setup_petcare_crm"

# ─────────────────────────────────────────────────────────────────────
# SCHEDULER EVENTS (Prompt 7)
# ─────────────────────────────────────────────────────────────────────
scheduler_events = {
    "daily": [
        "petcare_crm.tasks.daily_petcare_scan"
    ],
    "hourly": [
        "petcare_crm.tasks.hourly_workflow_check"
    ],
}

# List View customization
doctype_list_js = {
    "Care Recommendation": "petcare_crm/doctype/care_recommendation/care_recommendation.js",
    "Customer Membership": "petcare_crm/doctype/customer_membership/customer_membership.js",
}
