from django.contrib import admin
from .models import Orden, Producto, Pago

admin.site.register(Producto)
admin.site.register(Orden)
admin.site.register(Pago)