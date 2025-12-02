# M02_settings/urls.py
from django.urls import path
from M02_settings.views.test_theme import theme_preview

urlpatterns = [
    # Tema test / preview sayfası
    path("theme-preview/", theme_preview, name="theme_preview"),
]
