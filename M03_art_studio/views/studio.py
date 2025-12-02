# M03_art_studio/views/studio.py

from django.shortcuts import render


def template_studio_home(request):
    """
    Art Studio ana çalışma alanı:
    Üstte Template/Object/Asset menü barı,
    altta 3 kolonluk çalışma alanı (liste / editor / preview).

    Şimdilik sadece iskelet, menü aksiyonlarını adım adım ekleyeceğiz.
    """
    return render(request, "M03_art_studio/template_studio.html")
