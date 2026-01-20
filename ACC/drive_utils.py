import os
import io
import json
from django.conf import settings
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

SCOPES = ["https://www.googleapis.com/auth/drive"]

# TOKEN_FILE = os.path.join(settings.BASE_DIR, "token_drive.json")
TOKEN_FILE = os.getenv("GOOGLE_TOKEN_JSON")


def get_drive_service():
    creds = None

    # --- NUEVO: leer token desde variable de entorno ---
    token_env = os.getenv("GOOGLE_TOKEN_JSON")
    if token_env:
        creds = Credentials.from_authorized_user_info(
            json.loads(token_env), SCOPES
        )

    # Si no hay credenciales válidas, pedimos login (igual que antes)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_config(
                json.loads(os.getenv("GOOGLE_CLIENT_JSON")),
                scopes=SCOPES,
                redirect_uri="http://localhost:8080/"
            )
            creds = flow.run_local_server(port=8080)

        # Guardamos el token SOLO para tu máquina local
        with open("token_drive.json", "w") as token:
            token.write(creds.to_json())

    return build("drive", "v3", credentials=creds)


def get_root_folder_id():
    service = get_drive_service()

    query = (
        f"name='{settings.GOOGLE_DRIVE_ROOT_FOLDER}' "
        "and mimeType='application/vnd.google-apps.folder' "
        "and trashed=false"
    )

    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])

    if not folders:
        raise Exception("No se encontró la carpeta raíz en Drive")

    return folders[0]["id"]


def create_drive_folder(folder_name, parent_id=None):
    service = get_drive_service()

    if parent_id is None:
        parent_id = get_root_folder_id()

    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }

    folder = (
        service.files()
        .create(body=file_metadata, fields="id, webViewLink")
        .execute()
    )

    return {
        "id": folder["id"],
        "url": folder["webViewLink"],
    }


def upload_file_to_drive(file_obj, filename, folder_id):
    service = get_drive_service()

    file_metadata = {
        "name": filename,
        "parents": [folder_id],
    }

    media = MediaIoBaseUpload(
        io.BytesIO(file_obj.read()),
        mimetype=file_obj.content_type,
        resumable=True,
    )

    file = (
        service.files()
        .create(body=file_metadata, media_body=media, fields="id, webViewLink")
        .execute()
    )

    # Hacer archivo público (lectura)
    service.permissions().create(
        fileId=file["id"],
        body={"type": "anyone", "role": "reader"},
    ).execute()

    return {
        "id": file["id"],
        "url": file["webViewLink"],
    }
