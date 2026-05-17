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
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden {self.id}"


class Pago(models.Model):
    orden = models.OneToOneField(
        Orden,
        on_delete=models.CASCADE
    )

    metodo_pago = models.CharField(max_length=100)

    estado = models.CharField(max_length=50)

    fecha_pago = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pago {self.id}"