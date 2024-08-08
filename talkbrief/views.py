import os
#import shutil
from datetime import datetime
#from django.http import HttpResponse
#from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.storage import FileSystemStorage
from django.conf import settings  # Import settings

from.models import UserInfo, Transcriptions, Summaries
from.forms import RegisterForm

from talkbrief.talkbrief_mods.text_summarizer import extract_summary
from talkbrief.talkbrief_mods.audio_transcriber import extract_audio




def home(request):
    return render(request, 'talkbrief/home.html')

def about(request):
    return render(request, 'talkbrief/about.html')

def contact(request):
    return render(request, 'talkbrief/contact.html')

def howto(request):
     return render(request, 'talkbrief/howto.html')

def whyus(request):
     return render(request, 'talkbrief/whyus.html')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            # The save method now takes care of setting the password,
            # so we just call save() directly.
            user = form.save()
            
            # Automatically logs the user in
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    
    return render(request, 'talkbrief/register.html', {'form': form})



def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'talkbrief/login_view.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


def history(request):
    if request.user.is_authenticated:
        user_instance = UserInfo.objects.get(userid=request.user.userid)
        
        # Fetch the transcriptions of the authenticated user
        transcriptions = Transcriptions.objects.filter(userid=user_instance).order_by('-time')
        
        # Fetch summaries related to these transcriptions
        summaries = Summaries.objects.filter(transcription__in=transcriptions)
        
        # Prepare the data to pass to the template
        history_data = []
        for transcription in transcriptions:
            summary = summaries.filter(transcription=transcription).first()
            history_data.append({
                'transcription': transcription,
                'summary': summary
            })
        
        return render(request, 'talkbrief/history.html', {'history_data': history_data})
    else:
        return render(request, 'talkbrief/history.html', {'error': 'You need to be logged in to view your history.'})


def transcribe(request):
    if request.method == 'POST':
        av_url_or_file = None
        
        if 'av_url' in request.POST:
            # User entered a URL or PATH
            av_url_or_file = request.POST['av_url']
        elif 'file' in request.FILES and request.FILES['file']:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(uploaded_file.name, uploaded_file)
            av_url_or_file = fs.url(filename)
            av_url_or_file = av_url_or_file[1:]
            # print(av_url_or_file)


        # calling function in audio_transcriber module to transcrbe the audio/video..
        transcript = extract_audio(av_url_or_file)

        
        if request.user.is_authenticated:
            # Fetch the user instance using the user ID
            user_instance = UserInfo.objects.get(userid=request.user.userid)        
        
            # Save the transcription to the database
            Transcriptions.objects.create(
            userid=user_instance,  # Assign the user instance, not just the ID
            file_name_link=av_url_or_file,
            transcription=transcript.text,
            time=datetime.now(),  # Current timestamp
            )
        else:
            pass




        # delete the uploaded file in project directory after transcription
        if av_url_or_file:
            file_path = os.path.join(settings.MEDIA_ROOT, av_url_or_file)
            if os.path.exists(file_path):
                os.remove(file_path)


                
        # redirect to transcribe.html with the transcription result
        return render(request, 'talkbrief/transcribe.html', {'transcript': transcript.text})
    # will render home.html if the form hasn't been submitted yet
    return render(request, 'talkbrief/home.html')

def summarize(request):
    if request.method == 'POST':
        if 'transcription' in request.POST:
            text = request.POST['transcription']
        elif 'user_text' in request.POST:
            text = request.POST['user_text']
        
            # saving text in db..
            if request.user.is_authenticated:
                # Fetch the user instance using the user ID
                user_instance = UserInfo.objects.get(userid=request.user.userid)        
        
              # Save the transcription to the database
                Transcriptions.objects.create(
                userid=user_instance,  # Assign the user instance, not just the ID
                file_name_link='text input',
                transcription=text,
                time=datetime.now(),  # Current timestamp
                )
            else:
                pass
        
        # Retrieve the selected summary length percentage
        summary_length = request.POST.get('summary_length', '')      
        
        # Extract the summary
        summary = extract_summary(text, summary_length)

        if text:
            # Get the last transcription saved in the database
            last_transcription = Transcriptions.objects.latest('transcription_id')       
                   
            # Save the summary to the database
            Summaries.objects.create(
                transcription=last_transcription,  # Associate with the latest transcription
                summary=summary,
                time=datetime.now(),  # Current timestamp
            )           
        
        
        if text:
           
            return render(request, 'talkbrief/summarize.html', {'summary': summary})
        else:
            return render(request, 'talkbrief/summarize.html', {'error': 'No text provided.'})
    else:
        return render(request, 'talkbrief/home.html')     
