from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.utils.timezone import now
from .drive_utils import *

def login(request):
    return render(request, 'ACC/login.html')

def dashboard(request):
    return render(request, 'ACC/dashboard.html')

def accidentes(request):
    return render(request, 'ACC/accidentes.html')

def buscar_autobus(request):
    economico = request.GET.get("economico", "").strip()

    try:
        autobus = Autobus.objects.get(economico=economico)
        
        data = {
            "existe": True,
            "tipo_unidad": autobus.tipo,
            "no_obra": autobus.no_obra,
            "serie": autobus.serie,
            "seams": autobus.seams or "",
            "placas": autobus.placas,
        }


    except Autobus.DoesNotExist:
        data = {"existe": False}

    return JsonResponse(data)

def buscar_conductor(request):
    clave = request.GET.get("clave", "").strip()

    try:
        c = Conductor.objects.get(clave=clave)

        nombre_completo = f"{c.nombres} {c.a_paterno} {c.a_materno}"

        data = {
            "existe": True,
            "nombre_completo": nombre_completo
        }

    except Conductor.DoesNotExist:
        data = {"existe": False}

    return JsonResponse(data)

def listar_tipo_cargo(request):
    cargos = list(
        Tipo_Cargo.objects.values("id_tipo_cargo", "descripcion")
    )

    return JsonResponse({"cargos": cargos})

def listar_tipo_danio(request):
    danios = list(
        Tipo_Dano.objects.values("id_tipo_dano", "descripcion")
    )
    return JsonResponse({"danios": danios})

def registrar_accidente(request):
    if request.method != "POST":
        return JsonResponse({"error": "Solo POST permitido"}, status=400)

    data = request.POST

    try:
        autobus = Autobus.objects.get(economico=data["economico"])
        conductor = Conductor.objects.get(clave=data["clave_conductor"])
        tipo_dano = Tipo_Dano.objects.get(id_tipo_dano=data["tipo_dano"])
        tipo_cargo = Tipo_Cargo.objects.get(id_tipo_cargo=data["tipo_cargo"])

    except Exception as e:
        return JsonResponse({"error": f"Dato inválido: {str(e)}"}, status=400)

    descripcion = data["descripcion"]

    # === Crear nombre de carpeta ===
    fecha = now().strftime("%d%m%Y")
    carpeta_base = f"ACC_{autobus.economico}_{fecha}"
    carpeta_inicial = f"{carpeta_base}_INICIAL"

    # === Crear carpeta en Drive ===
    resultado_drive = create_drive_folder(carpeta_inicial)

    # === Crear registro en BD ===
    accidente = Accidente.objects.create(
        autobus=autobus,
        conductor=conductor,
        tipo_dano=tipo_dano,
        tipo_cargo=tipo_cargo,
        descripcion=descripcion,
        carpeta_base=carpeta_base,
        carpeta_evidencia_inicial=resultado_drive["url"],
        estado="EN_PROCESO"
    )

    return JsonResponse({
        "mensaje": "Accidente registrado",
        "accidente_id": accidente.id,
        "folder_id": resultado_drive["id"]
    })

def subir_evidencia(request):
    if request.method != "POST":
        return JsonResponse({"error": "Solo POST permitido"}, status=400)

    folder_id = request.POST.get("folder_id")
    archivos = request.FILES.getlist("imagenes")

    # --- Validaciones más claras (evitan errores raros) ---
    if not folder_id:
        return JsonResponse({"error": "No se recibió folder_id"}, status=400)

    if not archivos or len(archivos) == 0:
        return JsonResponse({"error": "No se enviaron imágenes"}, status=400)

    urls = []

    try:
        for archivo in archivos:
            resultado = upload_file_to_drive(
                archivo,
                archivo.name,
                folder_id
            )
            urls.append(resultado["url"])

        return JsonResponse({
            "mensaje": "Imágenes subidas correctamente",
            "urls": urls
        })

    except Exception as e:
        return JsonResponse({
            "error": f"Error al subir imágenes: {str(e)}"
        }, status=500)
