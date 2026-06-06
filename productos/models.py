from django.db import models


class Producto(models.Model):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre


class Orden(models.Model):
    ESTADOS= [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('cancelada', 'Cancelada')
    ]

    nombre_cliente = models.CharField(max_length=200, default='SIN NOMBRE')
    documento_cliente = models.CharField(max_length=200, default='0')
    total = models.DecimalField(max_digits=10, decimal_places=2)
    estado = models.CharField(max_length=50, choices=ESTADOS, default='pendiente')
    fecha = models.DateTimeField(auto_now_add=True)
    unidades = models.IntegerField(default=0)

    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        default=0
    )

    token_dispensar = models.CharField(max_length=10, blank=True, default='')

    def __str__(self):
        return f"Orden {self.id} - {self.nombre_cliente}"


class Pago(models.Model):
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('cancelada', 'Cancelada')
    ]

    orden = models.OneToOneField(Orden, on_delete=models.CASCADE)
    stripe_payment_intent_id = models.CharField(max_length=255, null=True, blank=True)
    monto = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # ← agregar
    estado = models.CharField(max_length=50, choices=ESTADOS, default='pendiente')
    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.id}"