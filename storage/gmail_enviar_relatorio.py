import os
import pickle
import base64
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from email.mime.text import MIMEText

from logs.logger_config import logger

SCOPES = ['https://www.googleapis.com/auth/gmail.send']
TOKEN_PICKLE = 'token.pickle'

def authenticate_gmail(creds_path: str):
    logger.info("Autenticando Gmail API")
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

def create_message(sender: str, to: str, subject: str, body: str) -> dict:
    msg = MIMEText(body, _charset="utf-8")
    msg['to'] = to
    msg['from'] = sender
    msg['subject'] = subject
    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    return {'raw': raw}

def send_summary_email(service, sender: str, to: str, report: str):
    logger.info(f"Enviando relatório de teste para {to}")
    msg = create_message(sender, to, "[TESTE] Relatório de NPS", report)
    sent = service.users().messages().send(userId="me", body=msg).execute()
    logger.info(f"E-mail enviado com ID {sent['id']}")
