from googleapiclient.http import MediaFileUpload
from .Google import Create_Service

def send_video(title, description, video):

  SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
  SECRET_FILE = 'utils/token.json'
  API_NAME = 'youtube'
  API_VERSION = 'v3'
  service = Create_Service(SECRET_FILE, API_NAME, API_VERSION, SCOPES)

  request_body = {
    'snippet': {
      'categoryI': 19,
      'title': f'{title}',
      'description': f'{description}',
      'tags': ['Travel', 'test']
    },
    'status': {
      'privateStatus': 'public',
      'selfDeclaredMadeForKids': False,
    },
    'notifySubscribers': True
  } 
  media_file = MediaFileUpload(video)

  response_upload = service.videos().insert(
    part = 'snippet, status',
    body=request_body,
    media_body = media_file
  ).execute()

  return response_upload