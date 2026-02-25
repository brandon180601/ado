from django.shortcuts import render
from django.http import JsonResponse
from .models import *
from django.utils import timezone
from django.utils.timezone import now
from .drive_utils import *
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from decimal import Decimal
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils.dateparse import parse_date
from django.template.loader import render_to_string
from weasyprint import HTML
from django.http import HttpResponse
import json

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # o tu dashboard
        else:
            messages.error(request, "Usuario o contraseña incorrectos")
    return render(request, 'ACC/login.html')

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")  # o la vista que quieras

    return redirect("dashboard")

@login_required
def dashboard(request):
    # Conteo de accidentes por tipo de autobús
    accidentes_gl = Accidente.objects.filter(autobus__tipo='GL').count()
    accidentes_pl = Accidente.objects.filter(autobus__tipo='PL').count()

    # Conteo total de accidentes
    total_accidentes = Accidente.objects.count()

    context = {
        'accidentes_gl': accidentes_gl,
        'accidentes_pl': accidentes_pl,
        'total_accidentes': total_accidentes,
    }
    return render(request, 'ACC/dashboard.html', context)

@login_required
def accidentes(request):
    # --- Consulta base ---
    accidentes = Accidente.objects.select_related(
        "autobus", "conductor", "tipo_dano"
    ).all()

    accidentes_qs = Accidente.objects.select_related(
        "autobus", "conductor", "tipo_dano"
    ).all().order_by("-fecha")

    total = Accidente.objects.all()

    # --- FILTROS ---
    # Estado
    estado = request.GET.get("estado")
    if estado and estado != "TODOS":
        accidentes = accidentes.filter(estado=estado)

    # Tipo de unidad
    tipo = request.GET.get("tipo")
    if tipo and tipo != "TODOS":
        accidentes = accidentes.filter(autobus__tipo=tipo)

    # Rango de fechas
    fecha_desde = request.GET.get("fecha_desde")
    fecha_hasta = request.GET.get("fecha_hasta")
    if fecha_desde:
        fecha_desde_obj = parse_date(fecha_desde)
        if fecha_desde_obj:
            accidentes = accidentes.filter(fecha__date__gte=fecha_desde_obj)
    if fecha_hasta:
        fecha_hasta_obj = parse_date(fecha_hasta)
        if fecha_hasta_obj:
            accidentes = accidentes.filter(fecha__date__lte=fecha_hasta_obj)

    # Búsqueda por unidad, conductor o código
    q = request.GET.get("q")
    if q:
        accidentes = accidentes.filter(
            Q(autobus__economico__icontains=q) |
            Q(conductor__nombres__icontains=q) |
            Q(conductor__a_paterno__icontains=q) |
            Q(conductor__a_materno__icontains=q) |
            Q(codigo_acc__icontains=q)
        )

    # --- PAGINACIÓN ---
    mostrar = request.GET.get("mostrar", 50)  # valor predeterminado
    try:
        mostrar = int(mostrar)
    except ValueError:
        mostrar = 50

    # Mostrar todos si se pone 0
    if mostrar == 0:
        page_obj = accidentes
    else:
        paginator = Paginator(accidentes.order_by("-fecha"), mostrar)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

    # Obtener fechas para el calendario
    fecha_min = accidentes_qs.order_by("fecha").first().fecha if accidentes_qs.exists() else None
    fecha_max = now().date()  # fecha actual

    context = {
        "accidentes": page_obj,
        "paginator": paginator if mostrar != 0 else None,
        "estado": estado or "TODOS",
        "tipo": tipo or "TODOS",
        "fecha_desde": fecha_desde or "",
        "fecha_hasta": fecha_hasta or "",
        "mostrar": mostrar,
        "q": q or "",
        "fecha_min": fecha_min,
        "today": fecha_max,
        "total": total,
    }

    return render(request, "ACC/accidentes.html", context)

@login_required
def gestion(request):
    return render(request, 'ACC/gestion.html')

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

def listar_proveedores(request):
    proveedores = list(
        Proveedor.objects.values("id_proveedor", "nombre")
    )
    return JsonResponse({"proveedores": proveedores})

def registrar_accidente(request):
    if request.method != "POST":
        return JsonResponse({"error": "Solo POST permitido"}, status=400)

    data = request.POST
    archivos = request.FILES.getlist("imagenes")

    if not archivos:
        return JsonResponse({"error": "Debes subir al menos una imagen"}, status=400)

    try:
        autobus = Autobus.objects.get(economico=data["economico"])
        conductor = Conductor.objects.get(clave=data["clave_conductor"])
        tipo_dano = Tipo_Dano.objects.get(id_tipo_dano=data["tipo_dano"])
        tipo_cargo = Tipo_Cargo.objects.get(id_tipo_cargo=data["tipo_cargo"])
    except Exception as e:
        return JsonResponse({"error": f"Dato inválido: {str(e)}"}, status=400)

    # === Crear carpeta ===
    fecha = timezone.localtime().strftime("%d%m%Y")
    carpeta_base = f"ACC_{autobus.economico}_{fecha}"
    carpeta_inicial = f"{carpeta_base}_INICIAL"

    try:
        resultado_drive = create_drive_folder(carpeta_inicial)
    except Exception as e:
        return JsonResponse({"error": f"Error Drive: {str(e)}"}, status=500)

    # === Crear accidente ===
    accidente = Accidente.objects.create(
        autobus=autobus,
        conductor=conductor,
        tipo_dano=tipo_dano,
        tipo_cargo=tipo_cargo,
        descripcion=data["descripcion"],
        carpeta_base=carpeta_base,
        carpeta_evidencia_inicial=resultado_drive["url"],
        carpeta_evidencia_inicial_id=resultado_drive["id"],
        estado="EN_PROCESO"
    )

    # === Subir imágenes ===
    try:
        for archivo in archivos:
            upload_file_to_drive(archivo, archivo.name, resultado_drive["id"])
    except Exception as e:
        return JsonResponse({"error": f"Error al subir imágenes: {str(e)}"}, status=500)

    return JsonResponse({
        "success": True,
        "accidente_id": accidente.id
    })

def delete_drive_folder(folder_id):

    service = get_drive_service()

    service.files().delete(
        fileId=folder_id
    ).execute()

    return True

@login_required
@require_POST
def eliminar_accidente(request, accidente_id):

    if request.method != "POST":
        return JsonResponse({
            'success': False,
            'error': 'Método no permitido'
        }, status=405)

    accidente = get_object_or_404(Accidente, id=accidente_id)

    if accidente.estado == 'FINALIZADO':
        return JsonResponse({
            'success': False,
            'error': 'No se puede eliminar un accidente finalizado'
        })

    # eliminar carpeta inicial
    try:
        if accidente.carpeta_evidencia_inicial_id:
            delete_drive_folder(accidente.carpeta_evidencia_inicial_id)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'Error eliminando carpeta inicial: {str(e)}'
        })

    # eliminar registro
    accidente.delete()

    return JsonResponse({
        'success': True
    })

@csrf_exempt
def asignar_proveedor(request, accidente_id):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=400)

    try:
        data = json.loads(request.body)
        proveedor_id = data.get("proveedor")

        accidente = Accidente.objects.get(id=accidente_id)

        if accidente.estado != "EN_PROCESO":
            return JsonResponse({"error": "Estado inválido"}, status=400)
        
        proveedor = Proveedor.objects.get(id_proveedor=proveedor_id)
        accidente.proveedor = proveedor
        accidente.estado = "EN_REPARACION"
        accidente.save()

        return JsonResponse({"success": True})

    except Accidente.DoesNotExist:
        return JsonResponse({"error": "Accidente no encontrado"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def actualizar_accidente(request, accidente_id):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    try:
        data = json.loads(request.body)
        accidente = get_object_or_404(Accidente, id=accidente_id)

        # ================= AUTOBÚS =================
        economico = data.get("economico")
        if economico and economico != accidente.autobus.economico:
            accidente.autobus = Autobus.objects.get(economico=economico)

        # ================= CONDUCTOR =================
        clave = data.get("clave_conductor")
        if clave and clave != accidente.conductor.clave:
            accidente.conductor = Conductor.objects.get(clave=clave)

        # ================= TIPO DAÑO =================
        tipo_dano_id = data.get("tipo_dano")
        if tipo_dano_id is not None:
            tipo_dano_id = int(tipo_dano_id)
            if tipo_dano_id != accidente.tipo_dano_id:
                accidente.tipo_dano_id = tipo_dano_id

        # ================= TIPO CARGO =================
        tipo_cargo_id = data.get("tipo_cargo")
        if tipo_cargo_id is not None:
            tipo_cargo_id = int(tipo_cargo_id)
            if tipo_cargo_id != accidente.tipo_cargo_id:
                accidente.tipo_cargo_id = tipo_cargo_id

        # ================= PROVEEDOR =================
        proveedor_id = data.get("proveedor")
        if proveedor_id:
            proveedor_id = int(proveedor_id)
        else:
            proveedor_id = None

        if proveedor_id != accidente.proveedor_id:
            accidente.proveedor_id = proveedor_id

        # ================= DESCRIPCIÓN =================
        descripcion = data.get("descripcion")
        if descripcion is not None:
            accidente.descripcion = descripcion

        accidente.save()
        return JsonResponse({"success": True})

    except Autobus.DoesNotExist:
        return JsonResponse({"error": "El autobús no existe"}, status=400)

    except Conductor.DoesNotExist:
        return JsonResponse({"error": "El conductor no existe"}, status=400)

    except ValueError:
        return JsonResponse({"error": "Datos inválidos"}, status=400)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

def detalle_accidente(request, accidente_id):
    accidente = get_object_or_404(Accidente, id=accidente_id)

    return JsonResponse({
        "id": accidente.id,
        "descripcion": accidente.descripcion,

        "autobus": {
            "economico": accidente.autobus.economico,
            "tipo": accidente.autobus.tipo,
            "seams": accidente.autobus.seams,
            "no_obra": accidente.autobus.no_obra,
            "serie": accidente.autobus.serie,
            "placas": accidente.autobus.placas,
        },

        "conductor": {
            "clave": accidente.conductor.clave,
            "nombre": f"{accidente.conductor.nombres} {accidente.conductor.a_paterno} {accidente.conductor.a_materno}"
        },

        "tipo_dano_id": accidente.tipo_dano_id,
        "tipo_cargo_id": accidente.tipo_cargo_id,
        "proveedor_id": accidente.proveedor_id
    })

def finalizar_accidente(request, accidente_id):
    if request.method != "POST":
        return JsonResponse({"error": "Solo POST permitido"}, status=400)

    accidente = get_object_or_404(Accidente, id=accidente_id)

    # 🔒 No permitir doble finalización
    if accidente.estado == "FINALIZADO":
        return JsonResponse(
            {"error": "Este accidente ya fue finalizado"},
            status=400
        )

    data = request.POST
    archivos = request.FILES.getlist("imagenes")

    # ===== VALIDACIONES =====
    campos_requeridos = [
        "economico", "clave_conductor", "tipo_dano", "tipo_cargo",
        "proveedor", "descripcion", "codigo_acc", "costo", "comentarios"
    ]

    for campo in campos_requeridos:
        if not data.get(campo):
            return JsonResponse(
                {"error": f"Falta el campo {campo}"},
                status=400
            )

    if not archivos:
        return JsonResponse(
            {"error": "Debes subir al menos una imagen"},
            status=400
        )

    # ===== VALIDAR RELACIONES =====
    try:
        autobus = Autobus.objects.get(economico=data["economico"])
        conductor = Conductor.objects.get(clave=data["clave_conductor"])
        tipo_dano = Tipo_Dano.objects.get(id_tipo_dano=data["tipo_dano"])
        tipo_cargo = Tipo_Cargo.objects.get(id_tipo_cargo=data["tipo_cargo"])
        proveedor = Proveedor.objects.get(id_proveedor=data["proveedor"])
    except Exception as e:
        return JsonResponse(
            {"error": f"Dato inválido: {str(e)}"},
            status=400
        )

    # ===== VALIDAR CÓDIGO ÚNICO =====
    codigo_acc = data["codigo_acc"].strip()

    if Accidente.objects.exclude(id=accidente.id).filter(codigo_acc=codigo_acc).exists():
        return JsonResponse(
            {"error": "El código de accidente ya existe"},
            status=400
        )

    # ===== CREAR CARPETA FINAL =====
    carpeta_final = f"{accidente.carpeta_base}_FINAL"

    try:
        resultado_drive = create_drive_folder(carpeta_final)
    except Exception as e:
        return JsonResponse(
            {"error": f"Error al crear carpeta en Drive: {str(e)}"},
            status=500
        )

    # ===== SUBIR IMÁGENES =====
    try:
        for archivo in archivos:
            upload_file_to_drive(
                archivo,
                archivo.name,
                resultado_drive["id"]
            )
    except Exception as e:
        return JsonResponse(
            {"error": f"Error al subir imágenes: {str(e)}"},
            status=500
        )

    # ===== ACTUALIZAR ACCIDENTE =====
    accidente.autobus = autobus
    accidente.conductor = conductor
    accidente.tipo_dano = tipo_dano
    accidente.tipo_cargo = tipo_cargo
    accidente.proveedor = proveedor
    accidente.descripcion = data["descripcion"]

    accidente.codigo_acc = codigo_acc
    accidente.costo = Decimal(data["costo"])
    accidente.comentarios_cierre = data["comentarios"]
    accidente.carpeta_evidencia_final = resultado_drive["url"]
    accidente.fecha_finalizado = timezone.now()
    accidente.estado = "FINALIZADO"

    accidente.save()

    return JsonResponse({
        "success": True,
        "mensaje": "Accidente finalizado correctamente"
    })

def get_drive_images(folder_id):

    service = get_drive_service()

    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
        fields="files(id, name, mimeType)",
        orderBy="createdTime asc"
    ).execute()

    files = results.get("files", [])

    imagenes = []

    for file in files:

        imagenes.append({
            "id": file["id"],
            "nombre": file["name"],
            "url": f"https://lh3.googleusercontent.com/d/{file['id']}=w1200"
        })

    return imagenes

def vista_accidente(request, accidente_id):

    accidente = get_object_or_404(
        Accidente.objects.select_related(
            'autobus',
            'conductor',
            'tipo_dano',
            'tipo_cargo',
            'proveedor'
        ),
        id=accidente_id
    )

    imagenes = []

    if accidente.carpeta_evidencia_inicial_id:
        imagenes = get_drive_images(
            accidente.carpeta_evidencia_inicial_id
        )

    return JsonResponse({

        "id": accidente.id,

        "fecha": timezone.localtime(accidente.fecha).strftime("%d/%m/%Y"),

        "descripcion": accidente.descripcion,

        "estado": accidente.estado,

        "imagenes": imagenes,

        "autobus": {
            "economico": accidente.autobus.economico,
            "tipo": accidente.autobus.tipo,
            "seams": accidente.autobus.seams,
            "no_obra": accidente.autobus.no_obra,
            "serie": accidente.autobus.serie,
            "placas": accidente.autobus.placas,
        },

        "conductor": {
            "clave": accidente.conductor.clave,
            "nombre": f"{accidente.conductor.nombres} {accidente.conductor.a_paterno} {accidente.conductor.a_materno}"
        },

        "tipo_dano": accidente.tipo_dano.descripcion,

        "tipo_cargo": accidente.tipo_cargo.descripcion,

        "proveedor": accidente.proveedor.nombre if accidente.proveedor else "Sin asignar",

    })


def extraer_folder_id(url):
    if not url:
        return None
    
    if "folders/" in url:
        return url.split("folders/")[1].split("?")[0]
    
    return url

def obtener_imagenes_drive(folder_url):

    service = get_drive_service()

    folder_id = extraer_folder_id(folder_url)

    results = service.files().list(
        q=f"'{folder_id}' in parents and mimeType contains 'image/' and trashed=false",
        fields="files(id, name, mimeType)",
        orderBy="createdTime asc"
    ).execute()

    files = results.get("files", [])

    imagenes = []

    for file in files:
        imagenes.append(
            f"https://drive.google.com/uc?export=view&id={file['id']}"
        )

    return imagenes

def generar_pdf_accidente(request, id):

    accidente = Accidente.objects.select_related(
        'autobus',
        'conductor',
        'proveedor'
    ).get(id=id)


    evidencia_inicial = obtener_imagenes_drive(
        accidente.carpeta_evidencia_inicial_id
    )


    evidencia_final = []

    if accidente.carpeta_evidencia_final:
        evidencia_final = obtener_imagenes_drive(
            accidente.carpeta_evidencia_final
        )


    html_string = render_to_string(
        "ACC/pdf/reporte_accidente.html",
        {
            "accidente": accidente,
            "evidencia_inicial": evidencia_inicial,
            "evidencia_final": evidencia_final
        }
    )


    pdf = HTML(string=html_string).write_pdf()


    response = HttpResponse(pdf, content_type="application/pdf")

    response['Content-Disposition'] = \
        f'inline; filename="Accidente_{accidente.codigo_acc}.pdf"'


    return response