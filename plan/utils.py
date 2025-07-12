# plans/utils.py
from datetime import date
from accounts.models import UserPlan

def is_paid_user(user):
    today = date.today()
    active_plan = UserPlan.objects.filter(
        user=user,
        start_date__lte=today,
        end_date__gte=today
    ).order_by('-end_date').first()
    
    if active_plan and active_plan.plan.name.lower() != 'free':
        return True
    return False
