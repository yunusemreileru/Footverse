# M02_settings/utils/theme_loader.py
from .theme_registry import load_theme_json


def get_active_theme(request):
    """
    1) Kullanıcının seçtiği tema
    2) Admin default tema
    3) Sistem default (footverse_default)
    sırasıyla döner.
    """
    from M02_settings.models import ThemeSelection, AdminThemeSetting

    # 1 - Kullanıcı teması
    if request and hasattr(request, "user") and request.user.is_authenticated:
        ts = ThemeSelection.objects.filter(user=request.user).first()
        if ts:
            return load_theme_json(ts.theme_code)

    # 2 - Admin default tema
    admin_theme = AdminThemeSetting.objects.filter(is_active=True).first()
    if admin_theme:
        return load_theme_json(admin_theme.theme_code)

    # 3 - Sistem default
    return load_theme_json("footverse_default")
