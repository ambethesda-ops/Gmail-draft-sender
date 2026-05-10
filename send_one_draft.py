import os
import json
import base64
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

CLIENT_ID = os.environ["GMAIL_CLIENT_ID"]
CLIENT_SECRET = os.environ["GMAIL_CLIENT_SECRET"]
REFRESH_TOKEN = os.environ["GMAIL_REFRESH_TOKEN"]
USER_EMAIL = "kateandtom2027@gmail.com"

def get_service():
    creds = Credentials(
        token=None,
        refresh_token=REFRESH_TOKEN,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        token_uri="https://oauth2.googleapis.com/token"
    )
    return build("gmail", "v1", credentials=creds)

def get_oldest_draft(service):
    result = service.users().drafts().list(userId=USER_EMAIL).execute()
    drafts = result.get("drafts", [])
    if not drafts:
        print("No drafts remaining.")
        return None
    # Get full details for all drafts to find oldest
    detailed = []
    for d in drafts:
        full = service.users().drafts().get(userId=USER_EMAIL, id=d["id"]).execute()
        internal_date = int(full["message"].get("internalDate", 0))
        detailed.append((internal_date, d["id"]))
    detailed.sort(key=lambda x: x[0])
    return detailed[0][1]

def send_draft(service, draft_id):
    service.users().drafts().send(
        userId=USER_EMAIL,
        body={"id": draft_id}
    ).execute()
    print(f"Sent draft {draft_id}")

def main():
    service = get_service()
    draft_id = get_oldest_draft(service)
    if draft_id:
        send_draft(service, draft_id)

if __name__ == "__main__":
    main()
