from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.lista_productos),

    path('productos/<int:id>/', views.detalle_producto),

    path('productos/crear', views.crear_producto),

    path('orden/crear', views.crear_orden),

   
]