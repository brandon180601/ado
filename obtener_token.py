from ACC.drive_utils import get_drive_service, get_root_folder_id, create_drive_folder

service = get_drive_service()
print("Conectado a Drive correctamente")

root_id = get_root_folder_id()
print("ID carpeta raíz:", root_id)

folder = create_drive_folder("Prueba desde Django", parent_id=root_id)
print("Carpeta creada:", folder)
