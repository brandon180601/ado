from django.db import models

# Create your models here.

class Autobus(models.Model):
    id_autobus = models.AutoField(primary_key=True)
    economico = models.CharField(max_length=50)
    no_obra = models.CharField(max_length=50)
    serie = models.CharField(max_length=100)
    seams = models.CharField(max_length=50, null=True, blank=True)
    placas = models.CharField(max_length=20)
    tipo = models.CharField(max_length=20) 

    class Meta:
        db_table = 'autobusTabla'

    def __str__(self):
        return f"{self.economico} - {self.placas}"


class Conductor(models.Model):
    id_conductor = models.AutoField(primary_key=True)
    clave = models.CharField(max_length=20, unique=True)
    nombres = models.CharField(max_length=100)
    a_paterno = models.CharField(max_length=100)
    a_materno = models.CharField(max_length=100)

    class Meta:
        db_table = 'conductorTabla'

    def __str__(self):
        return f"{self.nombres} {self.a_paterno}"


class Tipo_Cargo(models.Model):
    id_tipo_cargo = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150)

    class Meta:
        db_table = 'tipo_cargoTabla'

    def __str__(self):
        return self.descripcion


class Proveedor(models.Model):
    id_proveedor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=150)

    class Meta:
        db_table = 'proveedorTabla'

    def __str__(self):
        return self.nombre


class Tipo_Dano(models.Model):
    id_tipo_dano = models.AutoField(primary_key=True)
    descripcion = models.CharField(max_length=150)

    class Meta:
        db_table = 'tipo_danoTabla'

    def __str__(self):
        return self.descripcion

class Accidente(models.Model):

    autobus = models.ForeignKey('Autobus', on_delete=models.CASCADE)
    conductor = models.ForeignKey('Conductor', on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)

    tipo_dano = models.ForeignKey('Tipo_Dano', on_delete=models.CASCADE)
    tipo_cargo = models.ForeignKey('Tipo_Cargo', on_delete=models.CASCADE)

    descripcion = models.TextField()

    # ==== Carpetas Drive ====
    carpeta_base = models.CharField(max_length=100)
    carpeta_evidencia_inicial = models.URLField()
    carpeta_evidencia_final = models.URLField(null=True, blank=True)

    # ==== Campos que se llenan AL FINAL ====
    proveedor = models.CharField(max_length=150, null=True, blank=True)
    costo = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    codigo_acc = models.CharField(max_length=30, unique=True, null=True, blank=True)
    comentarios_cierre = models.TextField(null=True, blank=True)

    # ==== TUS ESTADOS ====
    ESTADOS = [
        ('EN_PROCESO', 'En proceso'),
        ('EN_REPARACION', 'En reparación'),
        ('FINALIZADO', 'Finalizado'),
    ]

    estado = models.CharField(
        max_length=15,
        choices=ESTADOS,
        default='EN_PROCESO'
    )

    class Meta:
        db_table = 'accidenteTabla'
