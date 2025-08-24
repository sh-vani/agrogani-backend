# from .models import UserActivity

# def log_activity(user, action_type, description):
#     UserActivity.objects.create(
#         user=user,
#         action_type=action_type,
#         description=description
#     )




# accounts/utils.py

from .models import ActivityLog
from django.utils.timezone import now

def log_activity(user, event_type, module, description, icon_type=None, details=None):
    """
    A helper function to easily create an activity log entry.

    Args:
        user: The user instance performing the action.
        event_type (str): The title of the event (e.g., 'Task Completed').
        module (str): The app module (e.g., 'Tasks').
        description (str): A user-friendly description of the activity.
        icon_type (str, optional): An identifier for a frontend icon.
        details (dict, optional): Extra JSON data about the event.
    """
    if not user or not user.is_authenticated:
        # Do not log activities for anonymous users
        return

    ActivityLog.objects.create(
        user=user,
        event_type=event_type,
        module=module,
        description=description,
        icon_type=icon_type,
        details=details or {},
        timestamp=now()
    )