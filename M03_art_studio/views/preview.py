# M03_art_studio/views/preview.py

import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_POST

from ..models.template_model import TemplateModel
from ..models.object import Object
from ..services.renderer import Renderer


def preview_template(request, template_id):
    template = get_object_or_404(TemplateModel, id=template_id)
    svg = Renderer.render_template(template)

    return render(request, "M03_art_studio/preview_panel.html", {
        "svg": svg,
        "mode": "template",
        "item": template,
    })


def preview_object(request, object_id):
    obj = get_object_or_404(Object, id=object_id)
    svg = Renderer.render_object(obj)

    return render(request, "M03_art_studio/preview_panel.html", {
        "svg": svg,
        "mode": "object",
        "item": obj,
    })


@require_POST
def template_live_preview(request):
    """
    Template formundan gelen params JSON + checkbox flag'lerle
    canlı SVG preview döndürür (JSON response: { "svg": "<svg ...>" }).
    """
    # Body JSON ise onu dene, değilse POST'u kullan
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        payload = request.POST

    raw_params = payload.get("params") or {}

    # params string geldiyse parse et
    if isinstance(raw_params, str):
        try:
            params = json.loads(raw_params)
        except json.JSONDecodeError:
            params = {}
    elif isinstance(raw_params, dict):
        params = raw_params
    else:
        params = {}

    def to_bool(value):
        if isinstance(value, bool):
            return value
        if value is None:
            return False
        value = str(value).lower()
        return value in ("1", "true", "on", "yes")

    show_stars = to_bool(payload.get("show_stars"))
    show_platform = to_bool(payload.get("show_platform"))
    show_icon = to_bool(payload.get("show_icon"))

    # Renderer.render_template'in beklediği interface'i sağlayan
    # küçük bir dummy template objesi oluşturuyoruz.
    class DummyTemplate:
        pass

    dummy = DummyTemplate()
    dummy.params = params
    dummy.show_stars = show_stars
    dummy.show_platform = show_platform
    dummy.show_icon = show_icon

    svg = Renderer.render_template(dummy)

    return JsonResponse({"svg": svg})
