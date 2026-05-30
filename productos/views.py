import json
from django.http import JsonResponse
from .models import Producto, Orden
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


def lista_productos(request):

    productos = Producto.objects.all()

    data = []

    for p in productos:
        data.append({
            "id": p.id,
            "nombre": p.nombre,
            "descripcion": p.descripcion,
            "precio": str(p.precio),
            "stock": p.stock
        })

    return JsonResponse(data, safe=False)


def detalle_producto(request, id):

    producto = Producto.objects.get(id=id)

    data = {
        "id": producto.id,
        "nombre": producto.nombre,
        "descripcion": producto.descripcion,
        "precio": str(producto.precio),
        "stock": producto.stock
    }

    return JsonResponse(data)

#temporalmente mientras se construye la API
@csrf_exempt 
def crear_producto(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        nombre = body.get('nombre')
        descripcion = body.get('descripcion')
        precio = body.get('precio')
        stock = body.get('stock')

        producto = Producto.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            stock=stock
        )

        return JsonResponse({
            "id": producto.id,
            "nombre": producto.nombre,
            "mensaje": "Producto creado con éxito"
        }, status=201)
    
    return JsonResponse({"error": "Método no permitido"}, status=405)


# temporal
@csrf_exempt
def crear_orden(request):
    if request.method == 'POST':
        body = json.loads(request.body)

        nombre_cliente = body.get('nombre_cliente')
        documento_cliente = body.get('documento_cliente')
        unidades = body.get('unidades')
        producto_id = body.get('producto_id')

        try:
            producto = Producto.objects.get(id=producto_id)
        except:
            return JsonResponse({"error": "Producto no encontrado"}, status=404)

        total = producto.precio * unidades

        orden = Orden.objects.create(
            nombre_cliente=nombre_cliente,
            documento_cliente=documento_cliente,
            unidades=unidades,
            producto_id=producto_id,
            total=total,
            estado='pendiente'

        )

        return JsonResponse({
            "mensaje": "Su orden ha sido creada con éxito",
            "orden_id": orden.id,
            "total": str(total)

        }, status=201)
