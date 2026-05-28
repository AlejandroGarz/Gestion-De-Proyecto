import json
from django.http import JsonResponse
from .models import Producto


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

