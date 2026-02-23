import os
import django

# Inicializar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
from google_auth_oauthlib.flow import InstalledAppFlow

# Permisos de Drive
SCOPES = ['https://www.googleapis.com/auth/drive']

# Crear flujo de autenticación
flow = InstalledAppFlow.from_client_secrets_file(
    settings.GOOGLE_DRIVE_CREDENTIALS,
    SCOPES
)

# Abrir navegador para autenticar
creds = flow.run_local_server(port=0)

# Guardar token
with open(settings.GOOGLE_DRIVE_TOKEN_FILE, 'w') as token:
    token.write(creds.to_json())

print("✅ Token generado correctamente en:")
print(settings.GOOGLE_DRIVE_TOKEN_FILE)