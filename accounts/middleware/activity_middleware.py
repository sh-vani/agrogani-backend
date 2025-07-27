# accounts/middleware/activity_middleware.py
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
            if not any(path.startswith(p) for p in self.IGNORED_PATHS):
                ActivityLog.objects.create(
                    user=request.user,
                    event_type=self.get_event_type(path, request.method),
                    module=self.get_module_from_path(path),
                    description=self.get_description_from_path(path, request.method, request.user),
                    icon_type=self.get_icon(path, request.method)
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
            "seller": "Seller"
        }
        for key in mapping:
            if key in path:
                return mapping[key]
        return "General"

    def get_event_type(self, path, method):
        if "complete" in path and "task" in path:
            return "Completed Task"
        elif "expense" in path and method == "POST":
            return "Created Expense"
        elif "report" in path:
            return "Viewed Report"
        elif "crop" in path and method == "PUT":
            return "Updated Crop"
        elif "income" in path and method == "POST":
            return "Recorded Income"
        elif "buyer" in path and method == "POST":
            return "Added Buyer"
        elif "seller" in path and method == "POST":
            return "Added Seller"
        elif "labour" in path and method == "POST":
            return "Logged Labour Activity"
        return f"{method} {path}"

    def get_icon(self, path, method):
        if "complete" in path:
            return "✅"
        elif "expense" in path:
            return "💰"
        elif "report" in path:
            return "📊"
        elif "crop" in path:
            return "🌾"
        elif "sales" in path:
            return "🛒"
        elif "income" in path:
            return "📥"
        elif "buyer" in path:
            return "🧑‍🌾"
        elif "seller" in path:
            return "🏪"
        elif "labour" in path:
            return "🧱"
        return "🧭"

    def get_description_from_path(self, path, method, user):
        full_name = user.full_name


        if "tasks" in path and "complete" in path:
            task_id = self.extract_id(path, "tasks")
            task_name = self.get_model_name(task_id, "task", "Task")
            return f'Task "{task_name}" (ID #{task_id}) marked complete by {full_name} ✅'

        elif "expense" in path and method == "POST":
            return f'{full_name} added a new expense entry 💸'

        elif "report" in path:
            report_type = path.split("/")[-1].replace("-", " ").title()
            return f'{full_name} viewed the "{report_type}" report 📈'

        elif "crop" in path and method == "PUT":
            return f'{full_name} updated crop data 🌾'

        elif "income" in path and method == "POST":
            return f'{full_name} recorded a new income entry 📥'

        elif "sales" in path and method == "POST":
            return f'{full_name} created a new sales transaction 🛒'

        elif "buyer" in path and method == "POST":
            buyer_id = self.extract_id(path, "buyer")
            buyer_name = self.get_model_name(buyer_id, "buyer", "Buyer")
            return f'{full_name} added a new buyer: "{buyer_name}" 🧑‍🌾'

        elif "seller" in path and method == "POST":
            seller_id = self.extract_id(path, "seller")
            seller_name = self.get_model_name(seller_id, "seller", "Seller")
            return f'{full_name} added a new seller: "{seller_name}" 🏪'

        elif "labour" in path and method == "POST":
            return f'{full_name} logged labour activity 🧱'

        return f'{full_name} accessed {path} via {method} 🧭'

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
