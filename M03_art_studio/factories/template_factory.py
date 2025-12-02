"""
Template Factory
----------------
DesignTemplate oluşturma veya güncelleme sürecinde kullanılacak
yardımcı fonksiyonlar.
"""

from ..models.template_model import TemplateModel
from ..models.template_type_model import TemplateTypeModel
from ..utils.template_logic import merge_params


class TemplateFactory:
    """
    DesignTemplate oluşturma, parametre seti hazırlama,
    varsayılan parametreleri yükleme gibi işlemler burada.
    """

    @staticmethod
    def create_template(template_type_code: str, code: str, name: str, params: dict = None):
        """
        Yeni bir template oluşturur.
        """
        template_type = TemplateTypeModel.objects.get(code=template_type_code)

        return TemplateModel.objects.create(
            template_type=template_type,
            code=code,
            name=name,
            params=params or {}
        )

    @staticmethod
    def update_params(template: TemplateModel, new_params: dict):
        """
        Template parametrelerini birleştirir (override).
        """
        merged = merge_params(template.params, new_params)
        template.params = merged
        template.save()
        return template
