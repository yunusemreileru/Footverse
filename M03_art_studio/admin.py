from django.contrib import admin
from .models.template_type_model import TemplateTypeModel
from .models.object_type import ObjectType
from .models.params import Param
from .models.template_model import TemplateModel
from .models.object import Object


@admin.register(TemplateTypeModel)
class TemplateTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active", "created_at")
    search_fields = ("code", "name")
    list_filter = ("is_active",)
    ordering = ("code",)


@admin.register(ObjectType)
class ObjectTypeAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "is_active", "created_at")
    search_fields = ("code", "name")
    list_filter = ("is_active",)
    ordering = ("code",)


@admin.register(Param)
class ParamAdmin(admin.ModelAdmin):
    list_display = ("group", "code", "name", "is_active", "order_index")
    search_fields = ("group", "code", "name")
    list_filter = ("group", "is_active")
    ordering = ("group", "order_index", "code")


@admin.register(TemplateModel)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "template_type", "show_stars", "show_platform", "show_icon", "show_effects", "is_active", "updated_at")
    search_fields = ("code", "name")
    list_filter = ("template_type", "is_active")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("template_type__code", "code")

    fieldsets = (
        ("General Info", {
            "fields": ("template_type", "code", "name", "description", "version", "is_active")
        }),
        ("Show", {
            "fields": ("show_stars", "show_platform", "show_icon", "show_effects")
        }),
        ("Parameters", {
            "classes": ("collapse",),
            "fields": ("params",),
        }),
        ("Timestamps", {
            "classes": ("collapse",),
            "fields": ("created_at", "updated_at"),
        }),
    )


@admin.register(Object)
class ObjectAdmin(admin.ModelAdmin):
    list_display = ("name", "template", "object_type", "is_active", "created_at")
    search_fields = ("name", "template__name", "template__code")
    list_filter = ("object_type", "is_active")
    ordering = ("object_type__code", "template__code")

    fieldsets = (
        ("General Info", {
            "fields": ("template", "object_type", "name", "is_active")
        }),
        ("Parameters (Overrides)", {
            "classes": ("collapse",),
            "fields": ("params",),
        }),
        ("Timestamps", {
            "classes": ("collapse",),
            "fields": ("created_at",),
        }),
    )
