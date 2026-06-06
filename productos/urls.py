from django.urls import path
from . import views

urlpatterns = [
    path('productos/', views.lista_productos),

    path('productos/<int:id>/', views.detalle_producto),

    path('productos/crear', views.crear_producto),

    path('orden/crear', views.crear_orden),

    path('pagos/crear/', views.crear_pago),

    path('pagos/webhook/', views.webhook_stripe),

    path('ordenes/generar-token/', views.generar_token),
    
    path('ordenes/verificar-token/', views.verificar_token),

   
]