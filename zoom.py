import requests

class ZoomClient:
    def __init__(self, account_id, client_id, client_secret):
        self.account_id = account_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.get_access_token()

    def get_access_token(self):
        url = "https://zoom.us/oauth/token"
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }
        response = requests.post(url, data=data)
        if response.status_code == 200:
            return response.json()['access_token']
        else:
            raise Exception(f"Failed to retrieve access token: {response.text}")

    def get_recordings(self):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        url = "https://api.zoom.us/v2/accounts/{self.account_id}/recordings"
        response = requests.get(url, headers=headers)
        return response.json()

    def get_download_url(self, meeting_id):
        headers = {
            "Authorization": f"Bearer {self.access_token}"
        }
        url = f"https://api.zoom.us/v2/meetings/{meeting_id}/recordings"
        response = requests.get(url, headers=headers)
        recordings = response.json()
        
        download_url = None
        for file in recordings['recording_files']:
            if file['recording_type'] == 'audio_only':
                download_url = file['download_url']
                break
        
        if download_url:
            download_link = f"{download_url}?access_token={self.access_token}&playback_access_token={recordings['password']}"
            return download_link
        else:
            return "Audio-only recording not found or download link not available."

# Ejemplo de uso
if __name__ == "__main__":
    account_id = "tu_account_id"
    client_id = "tu_client_id"
    client_secret = "tu_client_secret"

    zoom_client = ZoomClient(account_id, client_id, client_secret)
    recordings = zoom_client.get_recordings()
    print("Listado de grabaciones:")
    print(recordings)

    meeting_id = "ID_de_la_reunión"
    download_url = zoom_client.get_download_url(meeting_id)
    print(f"Enlace de descarga del audio de la reunión {meeting_id}:")
    print(download_url)
