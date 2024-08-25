from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Conversation, Message
from django.core import serializers
from django.db.models import Q, Count




@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()

    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    # Mark all messages from the other user as read
    conversation.messages.filter(sender=other_user, is_read=False).update(is_read=True)

    messages = conversation.messages.all()

    return render(request, 'chat/chat.html', {'conversation': conversation, 'messages': messages, 'other_user': other_user})

@require_POST
@login_required
def send_message(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    message = request.POST.get('message')

    if message:
        Message.objects.create(conversation=conversation, sender=request.user, text=message)
        return JsonResponse({'status': 'ok'})

    return JsonResponse({'status': 'fail'})

@login_required
def get_messages(request, conversation_id):
    conversation = get_object_or_404(Conversation, id=conversation_id)
    messages = conversation.messages.all()
    data = serializers.serialize('json', messages)
    return JsonResponse({'messages': data})

@login_required
def chat_list_view(request):
    conversations = Conversation.objects.filter(participants=request.user).annotate(
        unread_count=Count('messages', filter=Q(messages__is_read=False, messages__sender__ne=request.user))
    )
    
    return render(request, 'chat/chat_list.html', {'conversations': conversations})