from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Conversation, Message



@login_required
def chat_view(request, user_id):
    other_user = get_object_or_404(User, id=user_id)
    conversation = Conversation.objects.filter(participants=request.user).filter(participants=other_user).first()
    
    if not conversation:
        conversation = Conversation.objects.create()
        conversation.participants.add(request.user, other_user)

    if request.method == "POST":
        message = request.POST.get('message')
        if message:
            Message.objects.create(conversation=conversation, sender=request.user, text=message)

    messages = conversation.messages.all().order_by('timestamp')
    return render(request, 'chat/chat.html', {'conversation': conversation, 'messages': messages, 'other_user': other_user})
