"""
Object Factory
--------------
Template'ten gerçek DesignObject üretimi burada yapılır.
"""

from ..models.object import Object
from ..models.object_type import ObjectType
from ..utils.template_logic import merge_params


class ObjectFactory:
    """
    DesignObject üretimi:
    - Template parametrelerini alır
    - Object override parametrelerini birleştirir
    """

    @staticmethod
    def create_from_template(template, object_type_code: str, name: str, override_params=None):
        """
        Template + override kombinasyonundan Object üretir.
        """
        obj_type = ObjectType.objects.get(code=object_type_code)

        # Parametre birleştirme
        final_params = merge_params(template.params, override_params or {})

        return Object.objects.create(
            template=template,
            object_type=obj_type,
            name=name,
            params=final_params
        )
