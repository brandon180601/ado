import os
import io
import socket
from django.conf import settings
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google_auth_oauthlib.flow import InstalledAppFlow

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
CREDENTIALS_FILE = settings.GOOGLE_DRIVE_CREDENTIALS

# ================================
# Servicio de Google Drive
# ================================
def get_drive_service():
    """
    Devuelve un servicio autenticado de Google Drive.
    Si no existe token, lo genera automáticamente.
    """

    creds = None

    # 1️⃣ Si existe token, lo cargamos
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    # 2️⃣ Si no hay credenciales válidas, generarlas
    if not creds or not creds.valid:

        # Si el token existe pero expiró → refrescar
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            # Si no existe token → crear flujo nuevo
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Guardar token nuevo o actualizado
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    # 3️⃣ Construir servicio
    service = build("drive", "v3", credentials=creds)

    return service

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
