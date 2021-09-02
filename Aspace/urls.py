from django.contrib import admin
from django.urls import path, include
from login import views
from usuarios import views

from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login/', include('login.urls')),
    path('usuarios/', include('usuarios.urls')),
    path('graficas/', include('graficas.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
