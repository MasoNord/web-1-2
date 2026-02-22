import os
from pathlib import Path

import magic

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, HttpError

from harmony_hound.application.common.utils import get_project_root

ROOT_DIR = get_project_root()
SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/drive.file"
]

class GoogleDriveService:
    def __init__(self):
        self.cred = self.__get_creds()

    def upload_file(self, file_path: Path):
        try:
            with build('drive', 'v3', credentials=self.cred) as service:
                basename = os.path.basename(file_path)
                mime = magic.Magic(mime=True)

                file_metadata = {
                    "name": basename
                }

                media = MediaFileUpload(str(file_path), mime.from_file(str(file_path)))

                file = (
                    service.files()
                    .create(
                        supportsAllDrives=True,
                        body=file_metadata,
                        media_body=media,
                        fields="id"
                    )
                    .execute()
                )
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

        return file.get("id")


    def get_web_view_link(self, file_id):
        """
        Fetch file_url info by file_id from a Google Drive
        :param file_id:
        :return: webViewLink which will be used in RecognitionService
        """
        try:
            with build('drive', 'v3', credentials=self.cred) as service:
                file = (
                    service.files()
                    .get(
                        fileId=file_id,
                        fields="id, name, webViewLink, webContentLink",
                        supportsAllDrives=True
                    )
                    .execute()
                )
        except HttpError as error:
            print(f"An error occurred: {error}")
            return None

        web_view_link = file['webViewLink']
        web_view_link = web_view_link.replace("usp=drivesdk", "usp=drive_link")

        print(f"file_id: {file_id}")
        print(f"webViewLink: {web_view_link}")

        return web_view_link

    def delete_file_by_id(self, file_id):
        try:
            with build('drive', 'v3', credentials=self.cred) as service:
                service.files().delete(
                    fileId=file_id
                ).execute()
            return True
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

    def apply_share_flag(self, file_id):
        user_permission = {
            'type': 'anyone',
            'role': 'reader'
        }

        try:
            with build('drive', 'v3', credentials=self.cred) as service:
                service.permissions().create(
                    fileId = file_id,
                    body=user_permission
                ).execute()
        except HttpError as error:
            print(f"An error occurred: {error}")
            return False

        return True


    def __get_creds(self):
        if os.path.exists(os.path.join(ROOT_DIR, "important", "token.json")):
            creds = Credentials.from_authorized_user_file(os.path.join(ROOT_DIR, "important", "token.json"), SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    os.path.join(ROOT_DIR, "important", "credentials.json"), SCOPES
                )
                creds = flow.run_local_server(port=0)
            with open(os.path.join(ROOT_DIR, "important", "token.json"), "w") as token:
                token.write(creds.to_json())

        return creds