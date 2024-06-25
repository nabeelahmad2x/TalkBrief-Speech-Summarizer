# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.

from django.db import models
from django.contrib.auth.models import User
#from django_guest_user.models import GuestUser

class UserInfo(models.Model):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)

class Transcriptions(models.Model):
    transcription_id = models.AutoField(primary_key=True)
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userid')
    file_name_link = models.CharField(max_length=255, blank=True, null=True)
    transcription = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'transcriptions'

class Summaries(models.Model):
    summary_id = models.AutoField(primary_key=True)
    transcription = models.ForeignKey('Transcriptions', models.DO_NOTHING)
    summary = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'summaries'


### this is old chunk of models that was used with db.sqlite3..
### new models are imoirted from postgresql
# from django.db import models
# from django.contrib.auth.models import User
# #from django_guest_user.models import GuestUser

# class Transcription(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     #guest_user = models.ForeignKey(GuestUser, on_delete=models.CASCADE, null=True, blank=True)
#     audio_file = models.FileField(upload_to='audio/')
#     text = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

# class Summary(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     #guest_user = models.ForeignKey(GuestUser, on_delete=models.CASCADE, null=True, blank=True)
#     text = models.TextField()
#     summary = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)