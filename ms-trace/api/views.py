from django.http import JsonResponse
from django.views.decorators.http import require_GET
from api.models import TraceEvent


@require_GET
def trace_list(request):
    """
    Devuelve la lista de eventos de trazabilidad de un pedido.
    Endpoint: GET /trace?order_id=1
    """
    order_id = request.GET.get("order_id")

    if not order_id:
        return JsonResponse(
            {"error": "Se requiere el parámetro order_id"},
            status=400,
        )

    events = TraceEvent.objects.filter(order_id=order_id).order_by("created_at")

    data = []
    for ev in events:
        data.append(
            {
                "order_id": ev.order_id,
                "status": ev.status,
                "location": ev.location,
                "comment": ev.comment,
                "created_at": ev.created_at.isoformat(),
            }
        )

    return JsonResponse(data, safe=False, status=200)
