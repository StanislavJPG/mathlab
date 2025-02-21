from django.contrib.auth import get_user_model
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='sent_message', on_delete=models.CASCADE)
    receiver = models.ForeignKey(get_user_model(), related_name='received_message', on_delete=models.CASCADE)
    message = models.TextField(max_length=500)
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Sender: {self.sender}, while Receiver: {self.receiver}'

    class Meta:
        indexes = [models.Index(fields=('receiver', 'sender'))]
