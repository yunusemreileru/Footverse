from django.db import models
from .object_type import ObjectType
from .template_model import TemplateModel


class Object(models.Model):
    """
    Template'ten türetilen gerçek obje.
    Kullanıcıya atanabilir, oyunda kullanılabilir.
    """

    template = models.ForeignKey(
        TemplateModel,
        on_delete=models.PROTECT,
        related_name="template_objects"   # ✅ ESKİ: "objects"
    )

    object_type = models.ForeignKey(
        ObjectType,
        on_delete=models.PROTECT,
        related_name="type_objects"       # ✅ ESKİ: "objects"
    )

    name = models.CharField(max_length=120)
    params = models.JSONField(default=dict, blank=True)

    is_active = models.BooleanField(default=True)

    # timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["object_type__code", "template__code", "id"]
        verbose_name = "Design Object"
        verbose_name_plural = "Design Objects"

    def __str__(self):
        return f"{self.name} ({self.object_type.code})"
