from django import forms
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from.models import UserInfo, Transcriptions, Summaries

# class UserForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password']

# class TranscriptionForm(forms.ModelForm):
#     class Meta:
#         model = Transcriptions
#         fields = ['audio_file', 'text']


# class RegisterForm(UserCreationForm):
#     email = forms.EmailField(required=True)

#     class Meta:
#         model = UserInfo
#         fields = ("username", "email", "password1", "password2")

    # def save(self, commit=True):
    #     user = super(RegisterForm, self).save(commit=False)
    #     user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #     return user

class RegisterForm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    class Meta:
        model = UserInfo
        fields = ('username', 'email')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1!= password2:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        
        if commit:
            user.save()
        return user



class TranscriptionForm(forms.ModelForm):
    class Meta:
        model = Transcriptions
        fields = ['file_name_link', 'transcription', 'userid']


class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summaries
        fields = ['transcription', 'summary']

# class FileUploadForm(forms.Form):
#     file = forms.FileField()


class MediaForm(forms.Form):
    audio_video_file = forms.FileField(widget=forms.FileInput(attrs={'accept': 'audio/*,video/*'}))
    url = forms.URLField()