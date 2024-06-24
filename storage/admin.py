from django.contrib import admin
from django.contrib.admin import site
from .models import Folder, File

# Register your models here.

site.register(File)
site.register(Folder)