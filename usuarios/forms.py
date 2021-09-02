from django import forms
import django_filters
from django.db.models.base import Model
from django.db.models import Q
from .models import  Sesion


class FileForm(forms.Form):
    archivo_sesion = forms.FileField()
