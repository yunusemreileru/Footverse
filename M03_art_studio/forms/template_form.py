from django import forms
from M03_art_studio.models.template_model import TemplateModel
from M03_art_studio.models.template_type_model import TemplateTypeModel


class TemplateForm(forms.ModelForm):
    class Meta:
        model = TemplateModel
        fields = [
            "template_type",
            "code",
            "name",
            "description",
            "version",
            "params",
            "is_active",
            "show_stars",
            "show_platform",
            "show_icon",
            "show_effects",
        ]

        widgets = {
            "template_type": forms.Select(attrs={
                "class": "fv-input",
            }),
            "code": forms.TextInput(attrs={
                "class": "fv-input",
                "placeholder": "Örn: badge_default / trophy_elite"
            }),
            "name": forms.TextInput(attrs={
                "class": "fv-input",
                "placeholder": "Görünen template adı"
            }),
            "description": forms.Textarea(attrs={
                "class": "fv-textarea",
                "rows": 3,
                "placeholder": "Bu template’in açıklaması"
            }),
            "version": forms.TextInput(attrs={
                "class": "fv-input",
                "placeholder": "Örn: v1, v1.1"
            }),
            "params": forms.Textarea(attrs={
                "class": "fv-textarea fv-textarea--mono",
                "rows": 6,
                "placeholder": "{\n  \"base_shape\": \"circle\",\n  \"palette\": \"gold\",\n  \"font\": \"Oswald\"\n}"
            }),
        }
