from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Autobus)
admin.site.register(Conductor)
admin.site.register(Tipo_Cargo)
admin.site.register(Proveedor)
admin.site.register(Tipo_Dano)
admin.site.register(Accidente)
