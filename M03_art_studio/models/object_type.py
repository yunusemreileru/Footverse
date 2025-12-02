from django.db import models

class ObjectType(models.Model):
    """Object tipleri: badge, trophy, card, stadium_object vb."""

    code = models.SlugField(max_length=64, unique=True)
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["code"]
        verbose_name = "Design Object Type"
        verbose_name_plural = "Design Object Types"

    def __str__(self):
        return self.name
