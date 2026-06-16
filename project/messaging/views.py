from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Prefetch

from .models import Conversation, Message
from .forms import MessageForm, ContactForm


def _annotate_conversations(conversations, user):
    for conv in conversations:
        if user.is_staff:
            conv.unread_count = conv.messages.filter(is_read=False, is_from_admin=False).count()
        else:
            conv.unread_count = conv.messages.filter(is_read=False, is_from_admin=True).count()
        conv.last_message = conv.messages.order_by('-created_at').first()
    return conversations


@login_required
def chat_list(request):
    if request.user.is_staff:
        conversations = Conversation.objects.select_related('user', 'user__profile').prefetch_related(
            Prefetch('messages', queryset=Message.objects.select_related('sender').order_by('-created_at')[:1])
        )
    else:
        conversations = Conversation.objects.filter(user=request.user).prefetch_related(
            Prefetch('messages', queryset=Message.objects.select_related('sender').order_by('-created_at')[:1])
        )
    conversations = _annotate_conversations(conversations, request.user)
    return render(request, 'messaging/chat_list.html', {'conversations': conversations})


@login_required
def chat_detail(request, pk):
    conversation = get_object_or_404(
        Conversation.objects.select_related('user', 'user__profile'),
        pk=pk,
    )
    if not request.user.is_staff and conversation.user != request.user:
        messages.error(request, 'غير مصرح لك بالوصول.')
        return redirect('messaging:chat_list')

    if request.method == 'POST':
        form = MessageForm(request.POST, request.FILES)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.conversation = conversation
            msg.sender = request.user
            msg.is_from_admin = request.user.is_staff
            msg.save()
            return redirect('messaging:chat_detail', pk=pk)
    else:
        form = MessageForm()

    unread = conversation.messages.filter(is_read=False)
    if request.user.is_staff:
        unread.filter(is_from_admin=False).update(is_read=True)
    else:
        unread.filter(is_from_admin=True).update(is_read=True)

    chat_messages = conversation.messages.select_related('sender').all()

    if request.user.is_staff:
        chat_partner = conversation.user
        chat_title = conversation.user.full_name
        chat_subtitle = conversation.user.phone
    else:
        chat_partner = None
        chat_title = 'الإدارة'
        chat_subtitle = 'ماركو Academy'

    return render(request, 'messaging/chat_detail.html', {
        'conversation': conversation,
        'chat_messages': chat_messages,
        'form': form,
        'chat_partner': chat_partner,
        'chat_title': chat_title,
        'chat_subtitle': chat_subtitle,
    })


@login_required
def chat_poll(request, pk):
    conversation = get_object_or_404(Conversation, pk=pk)
    if not request.user.is_staff and conversation.user != request.user:
        return JsonResponse({'error': 'forbidden'}, status=403)

    last_id = int(request.GET.get('last_id', 0))
    new_messages = conversation.messages.filter(id__gt=last_id).select_related('sender')
    payload = []
    for msg in new_messages:
        payload.append({
            'id': msg.id,
            'content': msg.content,
            'image': msg.image.url if msg.image else '',
            'time': msg.created_at.strftime('%H:%M'),
            'is_mine': msg.sender_id == request.user.id,
            'sender': msg.sender.full_name,
        })

    if request.user.is_staff:
        conversation.messages.filter(is_read=False, is_from_admin=False).update(is_read=True)
    else:
        conversation.messages.filter(is_read=False, is_from_admin=True).update(is_read=True)

    return JsonResponse({'messages': payload})


@login_required
def chat_start(request):
    # المطلوب: المستخدم هو الذي يبدأ المراسلة. منع الأدمن من إنشاء محادثة جديدة لنفسه.
    if request.user.is_staff:
        messages.info(request, 'يمكنك الرد على رسائل الطلاب من قائمة المحادثات.')
        return redirect('messaging:chat_list')
    conversation, _ = Conversation.objects.get_or_create(
        user=request.user,
        defaults={'subject': 'محادثة مع الإدارة'},
    )
    return redirect('messaging:chat_detail', pk=conversation.pk)


@require_POST
def contact_submit(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        form.save()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'تم إرسال رسالتك بنجاح!'})
        messages.success(request, 'تم إرسال رسالتك بنجاح! سنتواصل معك قريباً.')
    else:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        messages.error(request, 'يرجى التحقق من البيانات المدخلة.')
    return redirect('pages:home')
