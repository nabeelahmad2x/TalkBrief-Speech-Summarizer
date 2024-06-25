# myapp/forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from.models import Transcriptions, Summaries

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

# class TranscriptionForm(forms.ModelForm):
#     class Meta:
#         model = Transcriptions
#         fields = ['audio_file', 'text']

class TranscriptionForm(forms.ModelForm):
    class Meta:
        model = Transcriptions
        fields = ['file_name_link', 'transcription', 'userid']



# class SummaryForm(forms.ModelForm):
#     class Meta:
#         model = Summaries
#         fields = ['text', 'summary']
from django import forms
from .models import Summaries

class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summaries
        fields = ['transcription', 'summary']


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    # def save(self, commit=True):
    #     user = super(RegisterForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user

class MediaForm(forms.Form):
    # audio_url = forms.URLField(required=False)
    # file = forms.FileField(required=False)
    audio_video_file = forms.FileField(widget=forms.FileInput(attrs={'accept': 'audio/*,video/*'}))
    url = forms.URLField()