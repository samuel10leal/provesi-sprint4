from django.db import models


class TraceEvent(models.Model):
    order_id = models.IntegerField()  # id del pedido
    status = models.CharField(max_length=50)
    location = models.CharField(max_length=100, blank=True)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_id} - {self.status}"
