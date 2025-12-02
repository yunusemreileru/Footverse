from django.shortcuts import render, get_object_or_404, redirect
from M03_art_studio.models.template_type_model import TemplateTypeModel
from M03_art_studio.forms.template_type_form import TemplateTypeForm


def _render_panel(request, mode, types=None, selected=None, form=None):
    """Tek merkezli render helper – tekrarları bitirir."""
    if types is None:
        types = TemplateTypeModel.objects.all()

    return render(request, "M03_art_studio/template_types/layout.html", {
        "types": types,
        "selected": selected,
        "form": form,
        "mode": mode,
    })


def template_type_list(request):
    return _render_panel(request, mode="empty")


def template_type_detail(request, pk):
    selected = get_object_or_404(TemplateTypeModel, pk=pk)
    return _render_panel(request, mode="detail", selected=selected)


def template_type_create(request):
    if request.method == "POST":
        form = TemplateTypeForm(request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect("art_studio:template_type_detail", obj.id)
    else:
        form = TemplateTypeForm()

    return _render_panel(request, mode="create", form=form)


def template_type_edit(request, pk):
    selected = get_object_or_404(TemplateTypeModel, pk=pk)

    if request.method == "POST":
        form = TemplateTypeForm(request.POST, instance=selected)
        if form.is_valid():
            form.save()
            return redirect("art_studio:template_type_detail", pk)
    else:
        form = TemplateTypeForm(instance=selected)

    return _render_panel(request, mode="edit", selected=selected, form=form)


def template_type_delete(request, pk):
    selected = get_object_or_404(TemplateTypeModel, pk=pk)

    if request.method == "POST":
        selected.delete()
        return redirect("art_studio:template_type_list")

    return _render_panel(request, mode="delete", selected=selected)
