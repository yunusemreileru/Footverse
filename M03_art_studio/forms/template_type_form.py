from django import forms
from M03_art_studio.models.template_type_model import TemplateTypeModel


class TemplateTypeForm(forms.ModelForm):
    class Meta:
        model = TemplateTypeModel
        fields = ["code", "name", "description", "is_active"]

        widgets = {
            "code": forms.TextInput(attrs={
                "class": "fv-input",
                "placeholder": "Örn: badge / trophy / card_base"
            }),
            "name": forms.TextInput(attrs={
                "class": "fv-input",
                "placeholder": "Görünen isim"
            }),
            "description": forms.Textarea(attrs={
                "class": "fv-textarea",
                "rows": 3,
                "placeholder": "Bu template tipinin açıklaması"
            }),
            "is_active": forms.CheckboxInput(attrs={
                "class": "fv-checkbox"
            }),
        }
