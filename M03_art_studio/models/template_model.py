from django.db import models
from .template_type_model import TemplateTypeModel

class TemplateModel(models.Model):
    """
    Temel Template modeli.
    Badge / Trophy / Card / Stadium / Banner vb. hepsi bu modeli kullanır.
    """

    template_type = models.ForeignKey(
        TemplateTypeModel,
        on_delete=models.PROTECT,
        related_name="design_templates"
    )

    code = models.SlugField(max_length=80, unique=True)
    name = models.CharField(max_length=120)

    # PARAMETRELER
    params = models.JSONField(default=dict, blank=True)

    # Template metadata
    description = models.TextField(blank=True, default="")
    version = models.CharField(max_length=32, blank=True, default="v1")
    is_active = models.BooleanField(default=True)

    show_stars = models.BooleanField("Yıldızlar görünsün", default=False)
    show_platform = models.BooleanField("Platform bandı görünsün", default=False)
    show_icon = models.BooleanField("Merkez ikon görünsün", default=False)
    show_effects = models.BooleanField("Efektler görünsün", default=False)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["template_type__code", "code"]
        verbose_name = "Design Template"
        verbose_name_plural = "Design Templates"

    def __str__(self):
        return f"{self.name} ({self.template_type.code})"
