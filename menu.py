import os
import assemblyai as aai
from dotenv import load_dotenv
from zoom import ZoomClient
 
load_dotenv()

ZOOM_ACCOUNT_ID = os.environ.get('ZOOM_ACCOUNT_ID')
ZOOM_CLIENT_ID = os.environ.get('ZOOM_CLIENT_ID')
ZOOM_CLIENT_SECRET = os.environ.get('ZOOM_CLIENT_SECRET') 
aai.settings.api_key = os.environ.get('ASSEMBLYAI_API_KEY')

transcriber = aai.Transcriber()

client = ZoomClient(account_id=ZOOM_ACCOUNT_ID,
                    client_id=ZOOM_CLIENT_ID,
                    client_secret=ZOOM_CLIENT_SECRET)

recs = client.get_recordings()

if recs['meetings']:
    rec_id = recs['meetings'][0]['id']
    my_url = client.get_download_url(rec_id)
    try:
        transcript = transcriber.transcribe(my_url)
        print(transcript.text)
        with open('transcript.txt', 'w') as f:
            f.write(transcript.text)
    except Exception as e:
        print(f"Error al transcribir: {e}")
else:
    print('No hay reuniones para descargar.')
