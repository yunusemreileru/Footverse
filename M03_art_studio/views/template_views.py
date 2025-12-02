from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from M03_art_studio.models.template_model import TemplateModel
from M03_art_studio.models.template_type_model import TemplateTypeModel
from M03_art_studio.forms.template_form import TemplateForm

import logging
import os

logger = logging.getLogger("django")


# ============================================================
# Yardımcı fonksiyonlar
# ============================================================

def _get_current_type_from_request(request, selected=None):
    """
    URL'den veya formdan gelen template_type bilgisini okur.
    Hiçbiri yoksa:
      - seçili kaydın template_type'ını
      - ya da aktif ilk TemplateType kaydını döndürür.
    """
    type_id = (
        request.GET.get("type")
        or request.POST.get("template_type")
        or request.POST.get("template_type_id")
    )

    if type_id:
        try:
            return TemplateTypeModel.objects.get(pk=type_id)
        except TemplateTypeModel.DoesNotExist:
            logger.warning("TemplateType %s bulunamadı, fallback kullanılacak.", type_id)

    if selected is not None:
        return selected.template_type

    return TemplateTypeModel.objects.filter(is_active=True).order_by("code").first()


def _get_templates_for_type(current_type):
    """
    Seçili template type'a göre TemplateModel listesini döndür.
    """
    qs = TemplateModel.objects.all().select_related("template_type")
    if current_type:
        qs = qs.filter(template_type=current_type)
    return qs.order_by("code", "id")


def _get_icon_files():
    """
    static/M03_art_studio/img/icons altındaki PNG dosyalarının listesini döndürür.
    Sadece dosya isimleri (örn. 'trophy_gold.png') döner.
    """
    base_dir = getattr(settings, "BASE_DIR", None)
    if not base_dir:
        return []

    icons_dir = os.path.join(base_dir, "static", "M03_art_studio", "img", "icons")
    if not os.path.isdir(icons_dir):
        logger.warning("İkon klasörü bulunamadı: %s", icons_dir)
        return []

    files = []
    for name in os.listdir(icons_dir):
        if not name.lower().endswith(".png"):
            continue
        full_path = os.path.join(icons_dir, name)
        if os.path.isfile(full_path):
            files.append(name)

    return sorted(files)


# ============================================================
# Ortak layout renderer
# ============================================================

def _render_panel(
    request,
    mode,
    templates=None,
    selected=None,
    form=None,
    current_type=None,
):
    """
    Ortak layout renderer.

    - Solda liste için template queryset
    - Sağ panel için seçili kayıt / form
    - Üst dropdown için template type listesi
    - Icon sekmesi için ikon dosya isimleri
    """
    logger.debug(
        "🟦 _render_panel çağrıldı mode=%s current_type=%s selected=%s",
        mode,
        current_type,
        selected,
    )

    template_types = TemplateTypeModel.objects.filter(is_active=True).order_by("code")

    # current_type yoksa, isteğe veya seçili kayda göre belirle
    if current_type is None:
        current_type = _get_current_type_from_request(request, selected=selected)

    # Liste datası
    if templates is None:
        templates = _get_templates_for_type(current_type)
    else:
        # güvenli şekilde select_related uygula (queryset değilse dokunma)
        try:
            templates = templates.select_related("template_type")
        except AttributeError:
            pass

    # Seçili kayıt yoksa, listeden ilkini otomatik seç
    if selected is None and templates.exists():
        selected = templates.first()

    # Form yoksa mode'a göre oluştur
    if form is None:
        if mode in ("edit", "delete") and selected is not None:
            form = TemplateForm(instance=selected)
        else:
            initial = {}
            if current_type is not None:
                initial["template_type"] = current_type
            form = TemplateForm(initial=initial)

    context = {
        "templates": templates,
        "selected": selected,
        "form": form,
        "mode": mode,
        "current_type": current_type,
        "template_types": template_types,
        "icon_files": _get_icon_files(),
    }
    return render(request, "M03_art_studio/templates/layout.html", context)


# ============================================================
# View fonksiyonları
# ============================================================

def template_list(request):
    """
    Template Studio ana ekranı.
    Sadece liste + ilk kaydın detayını gösterir.
    """
    current_type = _get_current_type_from_request(request)
    templates = _get_templates_for_type(current_type)
    selected = templates.first() if templates.exists() else None
    return _render_panel(
        request,
        mode="list",
        templates=templates,
        selected=selected,
        current_type=current_type,
    )


def template_detail(request, pk):
    """
    Belirli bir template kaydının detayını (ve formunu) gösterir.
    """
    selected = get_object_or_404(TemplateModel, pk=pk)
    current_type = _get_current_type_from_request(request, selected=selected)
    templates = _get_templates_for_type(current_type)

    return _render_panel(
        request,
        mode="detail",
        templates=templates,
        selected=selected,
        current_type=current_type,
    )


def template_create(request):
    """
    Yeni template oluşturma ekranı.
    """
    current_type = _get_current_type_from_request(request)

    if request.method == "POST":
        form = TemplateForm(request.POST)
        if form.is_valid():
            obj = form.save()
            # Oluşturduktan sonra edit ekranına git
            try:
                url = reverse("art_studio:template_edit", kwargs={"pk": obj.pk})
            except Exception:
                # URL name henüz tanımlı değilse path'e göre fallback
                url = f"/art-studio/template-design/{obj.pk}/"
            return redirect(url)
    else:
        initial = {}
        if current_type is not None:
            initial["template_type"] = current_type
        form = TemplateForm(initial=initial)

    templates = _get_templates_for_type(current_type)

    return _render_panel(
        request,
        mode="create",
        templates=templates,
        selected=None,
        form=form,
        current_type=current_type,
    )


def template_edit(request, pk):
    """
    Mevcut bir template'i düzenleme ekranı.
    """
    selected = get_object_or_404(TemplateModel, pk=pk)
    current_type = _get_current_type_from_request(request, selected=selected)

    if request.method == "POST":
        form = TemplateForm(request.POST, instance=selected)
        if form.is_valid():
            obj = form.save()
            try:
                url = reverse("art_studio:template_edit", kwargs={"pk": obj.pk})
            except Exception:
                url = f"/art-studio/template-design/{obj.pk}/"
            return redirect(url)
    else:
        form = TemplateForm(instance=selected)

    templates = _get_templates_for_type(current_type)

    return _render_panel(
        request,
        mode="edit",
        templates=templates,
        selected=selected,
        form=form,
        current_type=current_type,
    )


def template_delete(request, pk):
    """
    Template silme.
    GET → onay ekranı
    POST → sil & template listesine dön
    """
    selected = get_object_or_404(TemplateModel, pk=pk)
    current_type = selected.template_type

    if request.method == "POST":
        type_id = current_type.id if current_type else None
        selected.delete()

        # Silindikten sonra aynı type filtresiyle listeye dön
        if type_id:
            return redirect(f"/art-studio/template-design/?type={type_id}")

        try:
            return redirect("art_studio:template_list")
        except Exception:
            return redirect("/art-studio/template-design/")

    return _render_panel(request, mode="delete", selected=selected, current_type=current_type)
