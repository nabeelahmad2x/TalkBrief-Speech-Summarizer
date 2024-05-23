from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
#from.models import Transcription, Summary
from django.http import HttpResponse
from.forms import RegisterForm, AuthenticationForm
from.forms import TranscriptionForm, SummaryForm
import assemblyai as aai

def home(request):
    return render(request, 'talkbrief/home.html')

def about(request):
    return render(request, 'talkbrief/about.html')

def contact(request):
    return render(request, 'talkbrief/contact.html')


# def register(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#             form.save()
#             username = form.cleaned_data.get('username')
#             raw_password = form.cleaned_data.get('password1')
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)
#             return redirect('home')
#     else:
#         form = RegisterForm()
#     return render(request, 'talkbrief/register.html', {'form': form})
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']  # Ensure email is saved
            user.save()
            # Automatically logs the user in
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'talkbrief/register.html', {'form': form})




# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 form = LoginForm()    
#     return render(request, 'talkbrief/login.html', {'form': form})
#this view is written for built in authentication form..
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



aai.settings.api_key = "6d9209c01dd54857b60536e9dba78bb1"

# def transcribe(request):
#     if request.method == 'POST':
#         # Initialize the transcriber
#         transcriber = aai.Transcriber()
        
#         # Check if a file was uploaded
#         if 'audio_video_file' in request.FILES:
#             file = request.FILES['audio_video_file']
#             # Save the file temporarily to get its local path
#             temp_path = f"/tmp/{file.name}"
#             with open(temp_path, 'wb+') as destination:
#                 for chunk in file.chunks():
#                     destination.write(chunk)
#             # Transcribe the local file
#             transcript = transcriber.transcribe(temp_path)
            
#         # Check if a URL was entered
#         elif 'url' in request.POST:
#             url = request.POST['url']
#             # Transcribe the URL
#             transcript = transcriber.transcribe(url)
        
#         else:
#             return HttpResponse("No file or URL provided.")
        
#         # Render the transcription result in the template
#         return render(request, 'talkbrief/transcribe.html', {'transcript': transcript.text})
    
#     else:
#         return render(request, 'home.html')

# def transcribe_view(request):
#     if request.method == 'POST':
#         av_url_or_file = None
        
#         if 'av_url' in request.POST:
#             # User entered a URL
#             av_url_or_file = request.POST['av_url']
#         elif 'file' in request.FILES:
#             # User uploaded a file
#             av_url_or_file = request.FILES['file']
        
#         if av_url_or_file:
#             transcriber = aai.Transcriber()
#             if isinstance(av_url_or_file, str):
#                 # It's an online link
#                 transcript = transcriber.transcribe(av_url_or_file)
#             else:
#                 # It's a local file
#                 with open(av_url_or_file.name, 'rb') as f:
#                     transcript = transcriber.transcribe(f.read())
            
#             return render(request, 'transcribe.html', {'transcript': transcript.text})
    
#     return render(request, 'home.html')

# def display_transcription_view(request):
#     return render(request, 'transcribe.html')

# views.py

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
            # User entered a URL
            av_url_or_file = request.POST['av_url']
        elif 'file' in request.FILES:
            # User uploaded a file
            av_url_or_file = request.FILES['file']
        
        if av_url_or_file:
            transcriber = aai.Transcriber()
            if isinstance(av_url_or_file, str):
                # It's an online link
                transcript = transcriber.transcribe(av_url_or_file)
            else:
                # It's a local file
                with open(av_url_or_file.name, 'rb') as f:
                    transcript = transcriber.transcribe(f.read())
            
            # Redirect to transcribe.html with the transcription result
            return render(request, 'talkbrief/transcribe.html', {'transcript': transcript.text})
        # Render home.html if the form hasn't been submitted yet
   # return render(request, 'talkbrief/home.html')

def summarize(request):
    if request.method == "POST":
        form = SummaryForm(request.POST)
        if form.is_valid():
            summary = form.save(commit=False)
            summary.user = request.user  # Assign the current user
            summary.save()
            return redirect('home')
    else:
        form = SummaryForm()
    return render(request, 'talkbrief/summarize.html', {'form': form})


