from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path("logout/", views.logout_view, name="logout"),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('accidentes/', views.accidentes, name='accidentes'),
    path('gestion/', views.gestion, name='gestion'),
    path("buscar-autobus/", views.buscar_autobus, name="buscar_autobus"),
    path("buscar-conductor/", views.buscar_conductor, name="buscar_conductor"),
    path("listar-tipo-cargo/", views.listar_tipo_cargo, name="listar_tipo_cargo"),
    path("listar-tipo-danio/", views.listar_tipo_danio, name="listar_tipo_danio"),
    path('listar-proveedores/', views.listar_proveedores, name='listar_proveedores'),
    path("registrar-accidente/", views.registrar_accidente, name="registrar_accidente"),
    path('accidente/eliminar/<int:accidente_id>/', views.eliminar_accidente, name='eliminar_accidente'),
    path('accidente/asignar-proveedor/<int:accidente_id>/',views.asignar_proveedor,name='asignar_proveedor'),
    path('accidente/detalle/<int:accidente_id>/',views.detalle_accidente,name='detalle_accidente'),
    path('accidente/actualizar/<int:accidente_id>/',views.actualizar_accidente,name='actualizar_accidente'),
    path("accidente/finalizar/<int:accidente_id>/",views.finalizar_accidente,name="finalizar_accidente"),

]
