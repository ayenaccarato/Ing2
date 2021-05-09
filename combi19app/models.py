from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class Usuario_Manager(BaseUserManager):
    def create_user(self, email, dni, nombre, apellido, direccion, telefono, password=None):
        us = self.model(
            email= self.normalize_email(email),
            dni=dni,
            nombre = nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono
        )
        us.set_password(password)
        us.save(using=self._db)
        return us

    def create_superuser(self, password, email, dni, nombre, apellido, direccion, telefono):
        us = self.create_user(
            password=password,
            email=email,
            dni=dni,
            nombre = nombre,
            apellido=apellido,
            direccion=direccion,
            telefono=telefono
        )
        # us.super_usuario = True
        us.is_admin = True
        us.is_superuser = True
        us.is_active= True
        us.tipo_usuario= 1
        us.save(using=self._db)
        return us


class Usuario(AbstractBaseUser, PermissionsMixin):
    #usuario = models.CharField(max_length=15, unique=True)
    #contraseña = models.CharField(max_length=3000)
    dni = models.BigIntegerField(primary_key = True)
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=20)
    email = models.EmailField( max_length=254, unique=True)
    direccion = models.CharField(max_length=20)
    telefono = models.IntegerField()
    #is_active = models.BooleanField(default= True)
    #staff = models.BooleanField(default= False)
    #admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True, verbose_name='account is activated')
    is_admin = models.BooleanField(default=False, verbose_name='staff account')
    # super_usuario = models.BooleanField(default=False)
    tipo_usuario = models.IntegerField(default = 3)
    objects = Usuario_Manager()

    USERNAME_FIELD = 'dni'
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido', 'direccion', 'telefono']

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.dni)

#    @property
#    def is_admin(self):
#        return self.is_admin

    @property
    def is_staff(self):
        return self.is_admin
    #class Meta:
    #    verbose_name = "Usuario"
    #    verbose_name_plural = "Usuarios"


class Vehiculo (models.Model):
    patente = models.CharField(max_length=10, primary_key=True)
    marca = models.CharField(max_length=50)
    modelo = models.CharField(max_length=4)
    capacidad = models.IntegerField( verbose_name="Cantidad de asientos")
    premium = models.BooleanField()


    def publish(self):
            self.save()

    def __str__(self):
        return self.patente

class Ciudad (models.Model):
    nombre = models.CharField(max_length=30)
    provincia = models.CharField(max_length=25)
    codigo_postal = models.IntegerField(primary_key=True)
    pais = models.CharField(max_length=20, default="Argentina")

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.codigo_postal)


class Ruta (models.Model):
    origen = models.CharField(max_length=30)
    destino = models.CharField(max_length=30)
    nombre = models.CharField(max_length=30, primary_key=True)
    km = models.IntegerField()
    duracion = models.IntegerField()
    duracion_en = models.CharField(max_length=10)

    def publish(self):
        self.save()

    def __str__(self):
        return self.nombre

class Viaje (models.Model):
    fecha_salida = models.DateTimeField()
    fecha_llegada = models.DateTimeField('%m/%d/%Y %H:%M') # fijarse si es ida y vuelta
    hora_salida = models.CharField(max_length=20)
    hora_llegada = models.CharField(max_length=20)
    ruta = models.ForeignKey(Ruta, related_name='+', on_delete=models.PROTECT)
    ciudad_origen = models.ForeignKey(Ciudad, related_name='+', on_delete=models.PROTECT)
    ciudad_destino = models.ForeignKey(Ciudad, related_name='+',on_delete=models.PROTECT)
    chofer = models.ForeignKey(Usuario, related_name='+', on_delete=models.PROTECT)
    vehiculo = models.ForeignKey(Vehiculo, related_name='+', on_delete=models.PROTECT)
    asientos_total = models.IntegerField(default=0)
    asientos_disponibles = models.IntegerField(default=0)
    vendidos = models.IntegerField()

    def publish(self):
        self.save()

class Tarjeta(models.Model):
    nro = models.BigIntegerField()
    banco = models.CharField(max_length=20)
    entidad = models.CharField(max_length=20)

class Pasajes(models.Model):
    dni = models.ForeignKey(Usuario, on_delete=models.PROTECT)
    nro_viaje = models.ForeignKey(Viaje, on_delete=models.PROTECT)
    estado = models.CharField(max_length=20)
    tarjeta = models.ForeignKey(Tarjeta, on_delete=models.PROTECT)
