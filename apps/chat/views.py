from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Message
from django.db.models import Q

# Create your views here.
@login_required
def chatRoom(request, username):
    r = User.objects.filter(username = username).first()
    messages = Message.objects.filter(
        (Q(sender = request.user) & Q(receiver = r)) | (Q(sender = r) & Q(receiver = request.user))
    ).order_by("timeStamp")

    if request.method == "POST":
        msg = request.POST.get('msg')
        if msg:
            Message.objects.create(
                sender = request.user,
                receiver = r,
                content = msg
            )
    return render (request, "chat/chat.html", {"r": r, "messages": messages})