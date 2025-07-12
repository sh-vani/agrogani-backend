
        
from rest_framework.permissions import BasePermission
from datetime import date

class IsPaidUser(BasePermission):
    def has_permission(self, request, view):
        try:
            user_plan = request.user.userplan
            if user_plan.end_date and user_plan.end_date < date.today():
                return False
            return user_plan.plan.name != 'Free'
        except:
            return False
