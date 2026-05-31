import json
import stripe
from django.http import JsonResponse
from .models import Producto, Orden, Pago
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from decouple import config


stripe.api_key = stripe.api_key = config('STRIPE_SECRET_KEY')

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

@csrf_exempt
def crear_pago(request):
    if request.method == 'POST':
        body = json.loads(request.body)
        orden_id = body.get('orden_id')

        try:
            orden = Orden.objects.get(id=orden_id)
        except Orden.DoesNotExist:
            return JsonResponse({"error": "Orden no encontrada"}, status=404)

        payment_link = stripe.PaymentLink.create(
            line_items=[{
                'price_data': {
                    'currency': 'cop',
                    'product_data': {
                        'name': f'Orden #{orden.id} - {orden.nombre_cliente}',
                    },
                    'unit_amount': int(orden.total * 100),
                },
                'quantity': 1,
            }],
        )

        Pago.objects.create(
            orden=orden,
            stripe_payment_intent_id=payment_link.id,
            monto=orden.total,
            estado='pendiente'
        )

        return JsonResponse({
            "link": payment_link.url,
            "orden_id": orden.id
        })
    
@csrf_exempt
@csrf_exempt
def webhook_stripe(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = config('STRIPE_WEBHOOK_SECRET')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=400)

    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        
        # acceder como atributo, no como diccionario
        payment_link_id = session.payment_link

        try:
            pago = Pago.objects.get(stripe_payment_intent_id=payment_link_id)
            pago.estado = 'pagada'
            pago.save()

            pago.orden.estado = 'pagada'
            pago.orden.save()
        except Pago.DoesNotExist:
            pass

    return JsonResponse({"status": "ok"})