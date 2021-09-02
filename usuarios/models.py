from django.db import models
from django.contrib.auth.models import User
import django_tables2 as tables
import django_filters
from django_tables2.utils import A
import datetime
import pytz
from django.utils import timezone

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    apellido = models.CharField(max_length=255)
    fecha_nacimiento = models.DateTimeField(null=True, blank=True)
    foto =  models.ImageField(upload_to = 'images/', default='images/icono.png')

    def __str__(self):
        return str(self.nombre)+' '+str(self.apellido)


    def get_last_sesion_date(self):

        try:
            fecha = Usuario.objects.filter(sesion__id_usuario=self.id_usuario).order_by('-sesion__fecha').values_list('sesion__fecha',flat=True)[0]
            print(fecha)
            # return(fecha)
            actual = datetime.datetime.now(datetime.timezone.utc)
            print(fecha)

            print(actual)

            dias = (actual-fecha).days
            print('dias',dias)
            if dias==0:
                return 'Última sesión hoy'
            elif dias>0 and dias<31:
                return f'Útima sesión hace {dias} días'
            elif dias>=31:
                dias = round((actual-fecha).days/31)
                if dias == 1:
                    return f'Útima sesión hace {dias} mes'
                if dias>1:

                    return f'Útima sesión hace {dias} meses'


        except Exception as e:
            print(e)
            return('Sin sesiones')

class Juego(models.Model):
    id_juego = models.AutoField(primary_key=True)
    nombre_juego = models.CharField(max_length=255)
    descripcion = models.TextField(max_length=600, null=True, blank=True)
    img_juego = models.ImageField(upload_to = 'images/',blank=True)
    url = models.URLField(max_length=255, null=True, blank=True)
    icono = models.ImageField(upload_to = 'images/',blank=True)
    def __str__(self):
        return self.nombre_juego


class Sesion(models.Model):
    id_sesion = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.DO_NOTHING)
    id_juego =  models.ForeignKey(Juego, on_delete=models.DO_NOTHING)
    fecha = models.DateTimeField(null=True, blank=True)
    aciertos = models.IntegerField(null=True, blank=True)
    fallos = models.IntegerField(null=True, blank=True)
    rondas = models.IntegerField(null=True, blank=True)
    tiempo_medio = models.IntegerField(null=True, blank=True)
    nivel =  models.CharField(max_length=255, null=True, blank=True)
    fichero = models.FileField(upload_to="media/", null=True, blank=True)
    def __str__(self):
        return str(self.id_usuario)+' - '+str(self.id_juego)+' - '+str(self.fecha)


class UsuariosTable(tables.Table):
    id_usuario = tables.LinkColumn("perfil_usuario", args=[A('id_usuario')])
    nombre = tables.LinkColumn("perfil_usuario", args=[A('id_usuario')])
    class Meta:
        model = Usuario
        # fields = ('id_usuario')
        template_name = "table_template.html"


class JuegosTable(tables.Table):
    class Meta:
        model = Juego
        # fields = ('id_usuario')
        template_name = "table_template.html"


class SesionTable(tables.Table):
    # id_sesion = tables.LinkColumn("perfil_usuario", args=[A('id_usuario')])
    # nombre_juego = tables.LinkColumn("perfil_usuario", args=[A('id_usuario')])
    id_usuario = tables.Column(verbose_name='Nombre')
    id_juego = tables.Column(verbose_name='Juego')
    class Meta:
        model = Sesion
        # fields = ('id_usuario')
        template_name = "table_template.html"
