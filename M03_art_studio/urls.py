# M03_art_studio/urls.py

from django.urls import path

from .views.studio import template_studio_home
from .views.preview import preview_template, preview_object, template_live_preview

from .views.template_type_views import (
    template_type_list,
    template_type_detail,
    template_type_create,
    template_type_edit,
    template_type_delete,
)

from .views.template_views import (
    template_list,
    template_detail,
    template_create,
    template_edit,
    template_delete,
)

app_name = "art_studio"

urlpatterns = [
    # Studio ana workspace
    path("home/", template_studio_home, name="studio_home"),

    # ==== TEMPLATE TYPES ====
    path("template-types/", template_type_list, name="template_type_list"),
    path("template-types/add/", template_type_create, name="template_type_create"),
    path("template-types/<int:pk>/", template_type_detail, name="template_type_detail"),
    path("template-types/<int:pk>/edit/", template_type_edit, name="template_type_edit"),
    path("template-types/<int:pk>/delete/", template_type_delete, name="template_type_delete"),


    # ==== TEMPLATE DESIGN ====
    path("template-design/", template_list, name="template_list"),
    path("template-design/add/", template_create, name="template_create"),
    path("template-design/<int:pk>/", template_detail, name="template_detail"),
    path("template-design/<int:pk>/edit/", template_edit, name="template_edit"),
    path("template-design/<int:pk>/delete/", template_delete, name="template_delete"),

    # Canlı preview endpoint'i (JSON)
    path(
        "template-design/live-preview/",
        template_live_preview,
        name="template_live_preview",
    ),

    # Preview ekranları
    path("preview/template/<int:template_id>/", preview_template, name="preview_template"),
    path("preview/object/<int:object_id>/", preview_object, name="preview_object"),
]
