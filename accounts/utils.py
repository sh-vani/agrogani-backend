from .models import UserActivity

def log_activity(user, action_type, description):
    UserActivity.objects.create(
        user=user,
        action_type=action_type,
        description=description
    )
