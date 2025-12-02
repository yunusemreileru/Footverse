# M02_settings/views/test_theme.py
from django.shortcuts import render, redirect
from M02_settings.models import ThemeSelection
from M02_settings.utils.theme_registry import get_available_themes


def theme_preview(request):
    # Tema seçimi POST ile geliyorsa kaydet
    if request.method == "POST":
        theme_code = request.POST.get("theme_code")
        if request.user.is_authenticated and theme_code:
            ThemeSelection.objects.update_or_create(
                user=request.user,
                defaults={"theme_code": theme_code}
            )
        return redirect("theme_preview")

    # Dinamik preset listesi (code + name)
    presets = get_available_themes()

    return render(request, "main/theme_preview.html", {
        "presets": presets,
        # active_theme context processor'dan geliyor
    })
