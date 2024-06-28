import os
#from django.http import HttpResponse
#from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout

from.models import UserInfo, Transcriptions, Summaries
from.forms import RegisterForm

from django.contrib.auth.forms import AuthenticationForm
from datetime import datetime

from talkbrief.talkbrief_mods.text_summarizer import extract_summary
from talkbrief.talkbrief_mods.audio_transcriber import extract_audio




# views..
def home(request):
    return render(request, 'talkbrief/home.html')

def about(request):
    return render(request, 'talkbrief/about.html')

def contact(request):
    return render(request, 'talkbrief/contact.html')


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


####for testing if file is reaching view
#from django.http import HttpResponse
# def transcribe(request):
#     if request.method == 'POST':
#         # Check if a file was uploaded
#         if 'audio_video_file' in request.FILES:
#             file = request.FILES['audio_video_file']
#             # Process the file here (e.g., save it, transcribe it)
#             return HttpResponse("File received.")
        
#         # Check if a URL was entered
#         elif 'url' in request.POST:
#             url = request.POST['url']
#             # Process the URL here (e.g., fetch content, transcribe it)
#             return HttpResponse("URL received.")
        
#         else:
#             return HttpResponse("No file or URL provided.")
    
#     else:
#         return render(request, 'home.html')

def transcribe(request):
    if request.method == 'POST':
        av_url_or_file = None
        
        if 'av_url' in request.POST:
            # User entered a URL or PATH
            av_url_or_file = request.POST['av_url']
        elif 'file' in request.FILES:
            av_url_or_file = request.FILES['file']


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
        else:
            text = ''            
        
        # Retrieve the selected summary length percentage
        summary_length = request.POST.get('summary_length', '')
        
        if text:
            summary = extract_summary(text, summary_length)


            return render(request, 'talkbrief/summarize.html', {'summary': summary})
        else:
            return render(request, 'talkbrief/summarize.html', {'error': 'No text provided.'})
    else:
        return render(request, 'talkbrief/transcribe.html') 

    #to check if view is recieving data from transcribe template
    # if request.method == 'POST':
    #     transcription = request.POST.get('transcription', '')
    #     # Process the transcription here
    #     return HttpResponse("Transcription received.")
    # else:
    #     return HttpResponse("Invalid request.")
    
