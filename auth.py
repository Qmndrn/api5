import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

CLIENT_SECRET_FILE = (
    "/home/mndrn/Рабочий стол/vscode/api5/"
    "client_secret_470315497650-2tkgjmbpu00nkcpv1hdkj8d1rpfqd7f0.apps."
    "googleusercontent.com.json"
)

API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ['https://www.googleapis.com/auth/drive']
TOKEN_FILE = "token_drive"


def create_service():
    creds = None

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRET_FILE,
                SCOPES,
            )
            creds = flow.run_local_server()

        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)

    service = build(API_NAME, API_VERSION, credentials=creds)
    print(API_NAME, "service created successfully")
    return service


