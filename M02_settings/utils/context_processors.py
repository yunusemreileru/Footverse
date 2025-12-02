# M02_settings/utils/context_processors.py
from .theme_loader import get_active_theme


def theme_context(request):
    """
    Tüm sayfalara 'active_theme' sözlüğünü gönderir.
    """
    return {
        "active_theme": get_active_theme(request)
    }
