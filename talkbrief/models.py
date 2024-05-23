from django.db import models
from django.contrib.auth.models import User
#from django_guest_user.models import GuestUser

class Transcription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #guest_user = models.ForeignKey(GuestUser, on_delete=models.CASCADE, null=True, blank=True)
    audio_file = models.FileField(upload_to='audio/')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Summary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    #guest_user = models.ForeignKey(GuestUser, on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField()
    summary = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

