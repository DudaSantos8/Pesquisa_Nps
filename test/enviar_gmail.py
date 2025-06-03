import os
import pickle
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_PICKLE = 'token.pickle'


def authenticate_gmail(creds_path: str):
    creds = None
    if os.path.exists(TOKEN_PICKLE):
        with open(TOKEN_PICKLE, 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PICKLE, 'wb') as f:
            pickle.dump(creds, f)
    return build('gmail', 'v1', credentials=creds)


def send_email_gmail(service, sender: str, subject: str,
                     body_text: str, body_html: str, charset: str = 'UTF-8') -> dict:
    try:
        msg = MIMEMultipart('alternative')
        msg['To'] = sender
        msg['From'] = sender
        msg['Subject'] = subject

        part1 = MIMEText(body_text, 'plain', _charset=charset)
        part2 = MIMEText(body_html, 'html', _charset=charset)

        msg.attach(part1)
        msg.attach(part2)

        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode()
        message = {'raw': raw_message}

        sent = service.users().messages().send(userId='me', body=message).execute()
        return {'status': 'S', 'response': sent['id']}
    except Exception as e:
        return {'status': 'E', 'response': str(e)}
    