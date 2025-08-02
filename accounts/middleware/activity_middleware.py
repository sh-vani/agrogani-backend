from accounts.models import ActivityLog
from django.utils.timezone import now
import re

class UserActivityMiddleware:
    IGNORED_PATHS = [
        '/api/account/recent-activities/',
        '/api/token/',
        '/api/auth/',
        '/api/user/profile/'
    ]

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            path = request.path
            method = request.method
            if not any(path.startswith(p) for p in self.IGNORED_PATHS):
                ActivityLog.objects.create(
                    user=request.user,
                    event_type=self.get_event_type(path, method, request.user),
                    module=self.get_module_from_path(path),
                    description=self.get_description_from_path(path, method, request.user),
                    icon_type=""  # No icon used
                )

        return response

    def get_module_from_path(self, path):
        mapping = {
            "crop": "Crop",
            "expense": "Expense",
            "task": "Task",
            "sales": "Sales",
            "report": "Report",
            "income": "Income",
            "buyer": "Buyer",
            "labour": "Labour",
            "seller": "Seller",
            "ledger": "Ledger",
            "advisory": "Advisory",
            "userprofile": "Profile",
            "plan":"Plan",
        }
        for key in mapping:
            if key in path.lower():
                return mapping[key]
        return "General"

    def get_event_type(self, path, method, user):
        path_lower = path.lower().rstrip("/")

        if "crop/add" in path_lower and method == "POST":
            return "Crop Added"
        if "crop/my-crops" in path_lower and method == "GET":
            return "Crop View"
        if "expense" in path_lower and method == "POST":
            return "Expense Recorded"
        if "task/complete" in path_lower and method == "POST":
            return "Task Completed"
        if "sales/add" in path_lower and method == "POST":
            return "Sale Added"
        if "report" in path_lower and method == "GET":
            return "Report Viewed"
        if "buyer/add" in path_lower and method == "POST":
            return "Buyer Added"
        if "labour/add" in path_lower and method == "POST":
            return "Labour Added"
        if "ledger" in path_lower and method == "GET":
            return "Ledger Viewed"
        if "advisory/advisories/list" in path_lower and method == "GET":
            return "Advisory Viewed"
        if "userprofile/profile" in path_lower and method == "GET":
            return "Profile Viewed"
        if "plan/plans" in path_lower and method == "GET":
            return "Plan Viewed"
                   # For shop list
        if "shop/list" in path_lower and method == "GET":
            return " viewed the shop list"
   
        if "detailed-sale/add" in path_lower and method == "POST":
             return "Detailed Sale Added"

        return f"{method} {path}"

    def get_description_from_path(self, path, method, user):
        full_name = getattr(user, "full_name", None) or getattr(user, "get_full_name", lambda: None)() or getattr(user, "username", "User")
        path_lower = path.lower().rstrip("/")

        if "crop/add" in path_lower and method == "POST":
            return f"{full_name} added a new crop"
        if "expense" in path_lower and method == "POST":
            return f"{full_name} recorded an expense"
        if "task/complete" in path_lower and method == "POST":
            return f"{full_name} marked a task as complete"
        if "sales/add" in path_lower and method == "POST":
            return f"{full_name} added a sale record"
        if "detailed-sale/add" in path_lower and method == "POST":
            return f"{full_name} added a detailed sale record"
        if "shop/list" in path_lower and method == "GET":
         return f"{full_name} viewed the shop list"
        if "crop/my-crops" in path_lower and method == "GET":
            return "Crop View"
        if "report" in path_lower and method == "GET":
            return f"{full_name} viewed a report"
        if "buyer/add" in path_lower and method == "POST":
            return f"{full_name} added a new buyer"
        if "labour/add" in path_lower and method == "POST":
            return f"{full_name} added a labour record"
        if "ledger" in path_lower and method == "GET":
            return f"{full_name} viewed ledger details"
        if "advisory/advisories/list" in path_lower and method == "GET":
            return f"{full_name} viewed advisory contacts"
        if "userprofile/profile" in path_lower and method == "GET":
            return f"{full_name} viewed profile"
        if "plan/plans" in path_lower and method == "GET":
            return "Plan Viewed"
     

# For detailed sale
        if "detailed-sale/add" in path_lower and method == "POST":
             return "Detailed Sale Added"

        return f"{full_name} performed {method} on {path}"

    def extract_id(self, path, keyword):
        match = re.search(rf'{keyword}/(\d+)/', path)
        return match.group(1) if match else "?"

    def get_model_name(self, obj_id, app_label, model_name):
        try:
            from django.apps import apps
            model = apps.get_model(app_label, model_name)
            return getattr(model.objects.get(id=obj_id), "name", f"{model_name} #{obj_id}")
        except Exception:
            return f"{model_name} #{obj_id}"
