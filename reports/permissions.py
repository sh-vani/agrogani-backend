from rest_framework import permissions
from accounts.models import UserPlan  # assuming ye model bana hua hai

class IsPaidMember(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            user_plan = UserPlan.objects.get(user=request.user)
            return user_plan.plan.name.lower() != "free"
        except UserPlan.DoesNotExist:
            return False
