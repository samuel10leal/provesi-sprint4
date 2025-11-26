from django.http import JsonResponse
from django.views.decorators.http import require_GET
from api.models import InventoryItem


@require_GET
def inventory_list(request):
    """
    Devuelve el inventario asociado a un pedido.
    Endpoint: GET /inventory?order_id=1
    """
    order_id = request.GET.get("order_id")

    if not order_id:
        return JsonResponse(
            {"error": "Se requiere el parámetro order_id"},
            status=400,
        )

    items = InventoryItem.objects.filter(order_id=order_id)

    data = []
    for item in items:
        data.append(
            {
                "order_id": item.order_id,
                "sku": item.sku,
                "product_name": item.product_name,
                "warehouse": item.warehouse,
                "quantity": item.quantity,
                "available": item.available,
                "last_updated": item.last_updated.isoformat(),
            }
        )

    return JsonResponse(data, safe=False, status=200)
