import os
import mimetypes

from googleapiclient.http import MediaFileUpload

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError


SCOPES = ["https://www.googleapis.com/auth/drive"]
FILES = "https://www.googleapis.com/drive/v3/files"


"""
Connect to google docs api 
Requies a credentals.json file which contains the 
"""


def connect_to_api():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return creds


"""
Search and return the folderId 
Args: folder_name 
"""


def search_folder(service, folder_name):

    page_token = None
    res = (
        service.files()
        .list(
            q=f"mimeType = 'application/vnd.google-apps.folder' and name = '{folder_name}'",
            spaces="drive",
            fields="nextPageToken, files(id, name)",
            pageToken=page_token,
        )
        .execute()
    )

    files = res.get("files", [])
    if len(files) == 1:
        return {"id": files[0].get("id"), "name": files[0].get("name")}


def upload_folder(folder_path, service, parent_id):

    if not os.path.isdir(folder_path):
        print("Not a folder path")
        return
    folder_metadata = {
        "name": os.path.basename(folder_path),
        "mimeType": "application/vnd.google-apps.folder",
    }

    if parent_id is not None:
        folder_metadata.update({"parents": [parent_id]})

    # create folder
    print(f"Creating Folder {os.path.basename(folder_path)}")
    folder = service.files().create(body=folder_metadata, fields="id").execute()

    # get file path in the folder and mime
    files = os.listdir(folder_path)
    files_path = []
    mime_types = []
    for file in files:
        path = f"{folder_path}/{file}"
        mime = mimetypes.guess_type(path)
        files_path.append(path)
        mime_types.append(mime[0])

    # upload files and folders in the directory
    for i in range(len(files_path)):
        print(f"going through {files_path[i]}")
        if os.path.isfile(files_path[i]):
            upload_file(files_path[i], mime_types[i], folder.get("id"), service)
        else:
            upload_folder(files_path[i], service, folder.get("id"))

    return


"""
Upload a file to drive
"""


def upload_file(file_path, mime_type, folder_id, service):
    file_metadata = {"name": os.path.basename(file_path), "parents": [folder_id]}

    if mime_type is None:
        media = MediaFileUpload(
            file_path, mimetype="application/octet-stream", resumable=True
        )
    else:
        media = MediaFileUpload(file_path, mimetype=mime_type, resumable=True)

    print(f"UPLOADING FILE {file_path}")
    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id")
        .execute()
    )
