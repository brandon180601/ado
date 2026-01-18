from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accidentes/', views.accidentes, name='accidentes'),
    path("buscar-autobus/", views.buscar_autobus, name="buscar_autobus"),
    path("buscar-conductor/", views.buscar_conductor, name="buscar_conductor"),
    path("listar-tipo-cargo/", views.listar_tipo_cargo, name="listar_tipo_cargo"),
    path("listar-tipo-danio/", views.listar_tipo_danio, name="listar_tipo_danio"),
    path("registrar-accidente/", views.registrar_accidente, name="registrar_accidente"),
    path("subir-evidencia/", views.subir_evidencia, name="subir_evidencia"),
]
