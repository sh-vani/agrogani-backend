# expenses/permissions.py
from rest_framework import permissions
from plan.utils import is_paid_user

class IsPaidUserPlan(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and is_paid_user(request.user)
