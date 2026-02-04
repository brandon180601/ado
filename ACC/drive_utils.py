import os
import io
import socket
from django.conf import settings
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

# ================================
# Forzar que todas las conexiones usen IPv4
# ================================
old_getaddrinfo = socket.getaddrinfo

def getaddrinfo_ipv4(host, port, *args, **kwargs):
    return [x for x in old_getaddrinfo(host, port, *args, **kwargs) if x[0] == socket.AF_INET]

socket.getaddrinfo = getaddrinfo_ipv4

# ================================
# Configuración Drive
# ================================
SCOPES = ["https://www.googleapis.com/auth/drive"]
TOKEN_FILE = str(settings.GOOGLE_DRIVE_TOKEN_FILE)  # Asegúrate de que esto existe
ROOT_FOLDER_NAME = str(settings.GOOGLE_DRIVE_ROOT_FOLDER)  # Nombre de tu carpeta raíz

# ================================
# Servicio de Google Drive
# ================================
def get_drive_service():
    """
    Devuelve un servicio de Google Drive usando token OAuth.
    """
    if not os.path.exists(TOKEN_FILE):
        raise Exception(f"No se encontró token en {TOKEN_FILE}. Ejecuta obtener_token.py primero.")

    creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # Refrescar token si está expirado
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, "w") as token_file:
            token_file.write(creds.to_json())

    # Construir servicio normalmente (IPv4 ya está forzado por socket.getaddrinfo)
    return build("drive", "v3", credentials=creds)

# ================================
# Carpeta raíz
# ================================
def get_root_folder_id():
    service = get_drive_service()

    query = (
        f"name='{ROOT_FOLDER_NAME}' "
        "and mimeType='application/vnd.google-apps.folder' "
        "and trashed=false"
    )

    results = service.files().list(q=query, fields="files(id, name)").execute()
    folders = results.get("files", [])

    if not folders:
        raise Exception("No se encontró la carpeta raíz en Drive")

    return folders[0]["id"]

# ================================
# Crear carpeta
# ================================
def create_drive_folder(folder_name, parent_id=None):
    service = get_drive_service()

    if parent_id is None:
        parent_id = get_root_folder_id()

    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
        "parents": [parent_id],
    }

    folder = service.files().create(body=file_metadata, fields="id, webViewLink").execute()
    return {"id": folder["id"], "url": folder["webViewLink"]}

# ================================
# Subir archivo
# ================================
def upload_file_to_drive(file_obj, filename, folder_id):
    service = get_drive_service()

    file_metadata = {"name": filename, "parents": [folder_id]}
    media = MediaIoBaseUpload(io.BytesIO(file_obj.read()), mimetype=file_obj.content_type, resumable=True)

    file = service.files().create(body=file_metadata, media_body=media, fields="id, webViewLink").execute()

    # Hacer archivo público (lectura)
    service.permissions().create(fileId=file["id"], body={"type": "anyone", "role": "reader"}).execute()

    return {"id": file["id"], "url": file["webViewLink"]}
