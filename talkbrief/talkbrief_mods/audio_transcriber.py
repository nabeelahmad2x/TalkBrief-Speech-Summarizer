

import assemblyai as aai
aai.settings.api_key = "6d9209c01dd54857b60536e9dba78bb1"

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