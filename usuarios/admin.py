from django.contrib import admin

# Register your models here.
from .models import Usuario, Juego, Sesion

admin.site.register(Usuario)
admin.site.register(Juego)
admin.site.register(Sesion)
