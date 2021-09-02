from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django_tables2 import RequestConfig
from django.contrib import messages
from .models import Usuario, UsuariosTable, Sesion, SesionTable, Juego
from .forms import FileForm
import io
import csv
import datetime


from django.core.files.storage import FileSystemStorage

@login_required(login_url="/login/login")
def home(request):
    juegos = Juego.objects.all()
    return render(request, 'usuarios/home.html', {'juegos':juegos})

@login_required(login_url="/login/login")
def perfiles(request):
    usuarios = Usuario.objects.all()

    table_usuario = UsuariosTable(usuarios)
    RequestConfig(request).configure(table_usuario)
    table_usuario.paginate(page=request.GET.get("page", 1), per_page=50)

    return render(request, 'usuarios/perfiles.html', {'usuarios':usuarios, 'table_usuario':table_usuario})

@login_required(login_url="/login/login")
def perfil_usuario(request, id_usuario):
    usuario = Usuario.objects.get(id_usuario=id_usuario)
    sesiones = Sesion.objects.filter(id_usuario=id_usuario)
    # sesiones_pirata = sesiones.filter(id_juego_id__nombre_juego='Sumas de piratas')

    table_sesion = SesionTable(sesiones)
    RequestConfig(request).configure(table_sesion)
    table_sesion.paginate(page=request.GET.get("page", 1), per_page=50)

    # table_sesion_pirata = SesionTable(sesiones_pirata)
    # RequestConfig(request).configure(table_sesion_pirata)
    # table_sesion_pirata.paginate(page=request.GET.get("page", 1), per_page=50)

    return render(request, 'usuarios/perfilusuario.html', {'usuario':usuario,  'table_sesion':table_sesion})



# @login_required(login_url="/login/login")
# def subir_sesion(request):
#     if request.method=='POST':
#         form = forms.FileForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#Archivo
#             return render(request, 'usuarios/subir_sesion.html', {'form':form})

@login_required(login_url="/login/login")
def subir_sesion(request):
    context ={}
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['document']
            data = uploaded_file.read().decode('UTF-8')
            io_string = io.StringIO(data)
            # fieldnames = ['NOMBRE USUARIO', 'FECHA', 'ACIERTOS', 'FALLOS', 'RONDAS', 'TIEMPO MEDIO', 'NIVEL ELEGIDO']
            fieldnames = io_string.readline().strip().split(',')
            reader = csv.DictReader(io_string, fieldnames=fieldnames)
            for line in reader:
                nombre_completo = line.get('NOMBRE USUARIO')
                juego = line.get('JUEGO')
                fecha = line.get('FECHA')
                aciertos = line.get('ACIERTOS')
                fallos = line.get('FALLOS')
                rondas = line.get('RONDAS')
                tiempo_medio = line.get('TIEMPO MEDIO')
                nivel = line.get('NIVEL ELEGIDO')

                try:
                    nombre, apellido = nombre_completo.split(' ')
                except:
                    # arreglar en caso de que no tengan ambos
                    pass

                usuario, created = Usuario.objects.get_or_create(nombre = nombre, apellido = apellido)
                juego, created = Juego.objects.get_or_create(nombre_juego=juego)
                sesion, created = Sesion.objects.update_or_create(
                    id_usuario = usuario,
                    id_juego = juego,
                    fecha = fecha,
                    defaults = {
                        'id_usuario': usuario,
                        'id_juego': juego,
                        'fecha': fecha,
                        'aciertos': aciertos,
                        'fallos': fallos,
                        'rondas': rondas,
                        'tiempo_medio': tiempo_medio,
                        'nivel': nivel
                    }
                )
                print(line)
                print(created)

            messages.success(request, 'Archivos subidos a la base de datos!')
        except:
            messages.warning(request, 'Ha habido un error. ¿Has seleccionado algún archivo?')


    return render(request, 'usuarios/subir_sesion.html', context)




@login_required(login_url="/login/login")
def show_games(request):
    return render(request, 'usuarios/juegos.html')




# @login_required(login_url="/login/login")
# def perfil_juego(request, id_juego):
#
#     juego = Juego.objects.get(id_juego=id_juego)
#     return render(request, 'usuarios/juegos.html', {'perfil_juego':perfil_juego})


@login_required(login_url="/login/login")
def juegos(request, id_juego):

    juego = Juego.objects.get(id_juego=id_juego)
    return render(request, 'usuarios/juegos.html', {'juego':juego})
