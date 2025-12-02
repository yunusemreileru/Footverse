import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..services.renderer import Renderer
from ..utils.template_logic import merge_params


@csrf_exempt
def render_svg(request):
    """
    POST:
    {
        "base_params": {...},
        "override_params": {...}
    }
    """
    if request.method != "POST":
        return JsonResponse({"error": "POST required"}, status=405)

    data = json.loads(request.body.decode("utf-8"))

    base_params = data.get("base_params", {})
    override_params = data.get("override_params", {})

    final_params = merge_params(base_params, override_params)

    svg = Renderer._render(final_params)

    return JsonResponse({
        "svg": svg,
        "params": final_params
    })
