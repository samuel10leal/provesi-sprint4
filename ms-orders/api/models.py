from django.db import models


class Order(models.Model):
    STATUS_CHOICES = [
        ("TRANSITO", "En tránsito"),
        ("ALISTAMIENTO", "En alistamiento"),
        ("POR_VERIFICAR", "Por verificar"),
        ("VERIFICADO", "Verificado"),
        ("EMPACADO", "Empacado"),
        ("DESPACHADO", "Despachado"),
        ("ENTREGADO", "Entregado"),
        ("DEVUELTO", "Devuelto"),
    ]

    customer_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    warehouse = models.CharField(max_length=50)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pedido #{self.id} - {self.customer_name}"
