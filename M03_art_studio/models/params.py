from django.db import models
from django.contrib.postgres.fields import ArrayField


class Param(models.Model):
    """
    Tüm parametre tipleri için ortak havuz:
    shape, palette, effect, border, fontset, iconset vb.
    """

    PARAM_GROUPS = [
        ("shape", "Shape"),
        ("palette", "Color Palette"),
        ("effect", "Effect / Shadow"),
        ("border", "Border / Radius"),
        ("fontset", "Font Set"),
        ("iconset", "Icon Set"),
        ("pattern", "Pattern / Texture"),
    ]

    group = models.CharField(max_length=32, choices=PARAM_GROUPS)
    code = models.SlugField(max_length=64)
    name = models.CharField(max_length=120)

    data = models.JSONField(default=dict, blank=True)
    tags = ArrayField(models.CharField(max_length=50), default=list, blank=True)

    is_active = models.BooleanField(default=True)
    order_index = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("group", "code")
        ordering = ["group", "order_index", "code"]
        verbose_name = "Design Param"
        verbose_name_plural = "Design Params"

    def __str__(self):
        return f"{self.group} | {self.name}"
