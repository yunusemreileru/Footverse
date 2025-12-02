"""
Template Logic
--------------
Parametre birleştirme / override sistemleri
"""

def merge_params(base: dict, override: dict) -> dict:
    """
    Template params + Object override params = final params
    Derin birleştirme.
    """
    result = base.copy()

    for key, value in override.items():
        if isinstance(value, dict) and key in result and isinstance(result[key], dict):
            # İç içe sözlük kombinasyonu
            result[key] = merge_params(result[key], value)
        else:
            result[key] = value

    return result
