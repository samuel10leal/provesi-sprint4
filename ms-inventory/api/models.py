from django.db import models


class InventoryItem(models.Model):
    order_id = models.IntegerField()  # id del pedido asociado
    sku = models.CharField(max_length=50)  # código de producto
    product_name = models.CharField(max_length=100)
    warehouse = models.CharField(max_length=100)
    quantity = models.IntegerField()
    available = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.product_name} (order {self.order_id})"
