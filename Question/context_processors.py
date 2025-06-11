from .models import Notification

def notifications_processor(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(is_read=False)
        return {
            'notifications':notifications,
            'notifications_count' : notifications.count()
        }
    return {}

def unread_notifications(request):
    if request.user.is_authenticated:
        notifications = request.user.notifications.filter(is_read=False)
    else:
        notifications = []
    return {
        'notifications': notifications
    }