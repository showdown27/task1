from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender_name")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver_name")
    content = models.TextField()
    timeStamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender} - {self.receiver}"