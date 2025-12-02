# M02_settings/models/theme.py

from django.conf import settings
from django.db import models

class ThemeSelection(models.Model):
    """
    Kullanıcının seçtiği temayı tutar.
    Theme içeriği JSON dosyalarından okunur,
    burada sadece theme_code saklanır.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="theme_selection"
    )
    theme_code = models.CharField(max_length=50)  # Örn: "footverse_default"

    def __str__(self):
        return f"{self.user} → {self.theme_code}"


class AdminThemeSetting(models.Model):
    """
    Admin tarafından seçilen varsayılan tema.
    Sitede kullanıcı seçimi yoksa bu tema yüklenir.
    Eğer bu da yoksa sistemin kendi default preset'i uygulanır.
    """
    theme_code = models.CharField(max_length=50)  # Örn: "dark", "gold_premium"
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Admin Tema Ayarı"
        verbose_name_plural = "Admin Tema Ayarları"

    def __str__(self):
        return f"Admin Default Theme → {self.theme_code}"
