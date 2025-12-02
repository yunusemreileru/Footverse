from django.contrib import admin
from django.urls import path, include
from .views import dashboard


urlpatterns = [
    path("admin/", admin.site.urls),

    # Ana sayfa
    path("", dashboard, name="dashboard"),

    # M02 Settings modülü
    path("settings/", include("M02_settings.urls")),

    # M03 Art Studio modülü
    path("art-studio/", include("M03_art_studio.urls")),
]
