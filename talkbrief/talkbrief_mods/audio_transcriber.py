import assemblyai as aai
from.keys import AAI_key


aai.settings.api_key = AAI_key

def extract_audio(av_url_or_file):

    if av_url_or_file:
        transcriber = aai.Transcriber()

    
    if isinstance(av_url_or_file, str):
        # It's an online link
        transcript = transcriber.transcribe(av_url_or_file)
        
    else:
        # It's a local file
        with open(av_url_or_file.name, 'rb') as f:
            transcript = transcriber.transcribe(f.read())

    return transcript