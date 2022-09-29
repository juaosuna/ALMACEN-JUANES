from django.contrib import admin

# Register your models here.
from .models import Carrito,Producto

admin.site.register(Producto)
admin.site.register(Carrito)
