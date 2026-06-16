from django.contrib.auth import get_user_model
from messaging.models import Conversation, Message

User = get_user_model()


def unread_messages(request):
    if not request.user.is_authenticated:
        return {'unread_messages_count': 0}
    if request.user.is_staff:
        count = Message.objects.filter(is_read=False, is_from_admin=False).count()
    else:
        count = Message.objects.filter(
            conversation__user=request.user,
            is_read=False,
            is_from_admin=True,
        ).count()
    return {'unread_messages_count': count}
