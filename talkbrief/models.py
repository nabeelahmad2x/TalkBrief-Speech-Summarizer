from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
#from django.contrib.auth.models import User
#from django_guest_user.models import GuestUser

# Custom user manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('The Username field must be set')
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)

# Updated UserInfo model
class UserInfo(AbstractBaseUser, PermissionsMixin):
    userid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=128)  # Adjusted for security reasons
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email',]

    def __str__(self):
        return self.username

class Transcriptions(models.Model):
    transcription_id = models.AutoField(primary_key=True)
    userid = models.ForeignKey('UserInfo', models.DO_NOTHING, db_column='userid')
    file_name_link = models.CharField(max_length=255, blank=True, null=True)
    transcription = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'transcriptions'

class Summaries(models.Model):
    summary_id = models.AutoField(primary_key=True)
    transcription = models.ForeignKey('Transcriptions', models.DO_NOTHING)
    summary = models.TextField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    class Meta:
        managed = True
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