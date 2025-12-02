from django.contrib import admin
from M02_settings.models import ThemeSelection, AdminThemeSetting
from M02_settings.utils.theme_registry import get_available_themes


class ThemeCodeChoiceMixin:
    """Admin panelindeki theme_code alanını dynamic dropdown yapar."""

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name == "theme_code":
            choices = [(t, t) for t in get_available_themes()]
            kwargs["widget"] = admin.widgets.AdminRadioSelect(choices=choices)
        return super().formfield_for_dbfield(db_field, **kwargs)


@admin.register(AdminThemeSetting)
class AdminThemeSettingAdmin(ThemeCodeChoiceMixin, admin.ModelAdmin):
    list_display = ("theme_code", "is_active")
    list_editable = ("is_active",)
    list_filter = ("is_active",)
    search_fields = ("theme_code",)


@admin.register(ThemeSelection)
class ThemeSelectionAdmin(ThemeCodeChoiceMixin, admin.ModelAdmin):
    list_display = ("user", "theme_code")
    search_fields = ("user__username", "theme_code")
    list_filter = ("theme_code",)
