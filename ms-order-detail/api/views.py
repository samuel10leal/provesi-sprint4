import logging
import requests

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)


def _call_service(url: str):
    """
    Llama a un microservicio externo vía HTTP GET.
    Devuelve (json, error). Si error es None, salió bien.
    """
    try:
        resp = requests.get(url, timeout=settings.EXTERNAL_TIMEOUT)
        resp.raise_for_status()
        return resp.json(), None
    except requests.exceptions.RequestException as e:
        logger.exception("Error llamando al servicio externo: %s", url)
        return None, str(e)


@csrf_exempt
@require_GET
def order_full_detail(request, order_id: int):
    """
    ESTE es el endpoint del microservicio de latencia.
    - Llama a ms-orders (pedidos)
    - Llama a ms-trace (trazabilidad)  [aún no existe, por eso ponemos valores vacíos]
    - Llama a ms-inventory (inventario) [igual]
    y junta todo en un solo JSON.
    """

    # 1. Construir URLs hacia cada microservicio
    url_order = f"{settings.PATH_ORDERS}/{order_id}"
    url_trace = f"{settings.PATH_TRACE}?order_id={order_id}"
    url_inv   = f"{settings.PATH_INVENTORY}?order_id={order_id}"

    # 2. Llamar a ms-orders (si esto falla, devolvemos error)
    order_data, err_order = _call_service(url_order)
    if err_order or not order_data:
        return JsonResponse(
            {
                "error": "No se pudo obtener la información del pedido",
                "detail": err_order,
            },
            status=502,
        )

    # 3. Llamar a ms-trace (si falla, seguimos pero avisamos)
    trace_data, err_trace = _call_service(url_trace)
    if err_trace:
        trace_data = []
        logger.warning(
            "No se pudo obtener trazabilidad para pedido %s: %s",
            order_id,
            err_trace,
        )

    # 4. Llamar a ms-inventory (si falla, seguimos pero avisamos)
    inv_data, err_inv = _call_service(url_inv)
    if err_inv:
        inv_data = {}
        logger.warning(
            "No se pudo obtener inventario para pedido %s: %s",
            order_id,
            err_inv,
        )

    # 5. Armar respuesta consolidada
    response_payload = {
        "order": order_data,
        "trace": trace_data,
        "inventory": inv_data,
    }

    return JsonResponse(response_payload, status=200, safe=False)

