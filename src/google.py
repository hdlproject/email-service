from __future__ import print_function
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials


class GoogleAPIClient:
    SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

    def __init__(self):
        self.creds = None

    def login(self):
        creds = None

        if os.path.exists('../token.json'):
            creds = Credentials.from_authorized_user_file('../token.json', self.SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file('../client_secret.json', self.SCOPES)
                creds = flow.run_local_server()

            with open('../token.json', 'w') as token:
                token.write(creds.to_json())

        self.creds = creds
