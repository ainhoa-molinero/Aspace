from django.urls import path, include
from . import views

urlpatterns = [
    path('perfiles', views.perfiles, name ='perfiles'),
    path('subir_sesion', views.subir_sesion, name ='subir_sesion'),
    path('u/<str:id_usuario>', views.perfil_usuario, name ='perfil_usuario'),
    path('show_games', views.show_games, name ='show_games'),
    path('juegos/<str:id_juego>', views.juegos, name ='juegos'),



]

# if.settings.DEBUG:
#     urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
