"""
FULL Render Engine - Stage 1 (Base + Gradient + Shadow + Glow + Border + Layers)
-----------------------------------------------------------------------------
Bu motor, Art Studio'nun çekirdek SVG renderer'ıdır.
Badge / Trophy / Card vb. her şey buradan render edilir.
"""

from ..utils.svg_shapes import build_shape
from ..utils.color_utils import build_gradient, apply_fill_and_stroke, build_filters
from ..utils.template_logic import merge_params
from django.templatetags.static import static

class Renderer:

    @staticmethod
    def render_template(template):
        """
        Template seviyesindeki flag'leri (show_stars, show_icon, show_platform)
        params içine uygular, sonra render eder.
        """
        # template.params'i kopyala ki orijinali bozulmasın
        params = dict(template.params or {})

        # Eğer stars param'ı varsa ve template.show_stars False ise kapat
        stars = params.get("stars")
        if hasattr(template, "show_stars") and stars is not None and not template.show_stars:
            stars["enabled"] = False

        # Icon flag
        icon = params.get("icon")
        if hasattr(template, "show_icon") and icon is not None and not template.show_icon:
            icon["enabled"] = False

        # Platform param'ı ileride eklenecek; şimdilik varsa enabled kapatıyoruz
        platform = params.get("platform")
        if hasattr(template, "show_platform") and platform is not None and not template.show_platform:
            platform["enabled"] = False

        return Renderer._render(params)


    @staticmethod
    def render_object(obj):
        params = obj.params
        return Renderer._render(params)

    @staticmethod
    def _render(params: dict) -> str:
        """
        MASTER RENDER PIPELINE
        1) viewBox / root hazırlığı
        2) defs: gradient, filters
        3) layers render
        4) main shape render
        5) icon render (ADIM 6.3)
        """

        layout = params.get("layout", {})
        size = layout.get("size", 256)
        padding = layout.get("padding", 0)

        view_size = size + padding * 2

        # === SVG ROOT ===
        svg_parts = [
            f'<svg width="{view_size}" height="{view_size}" viewBox="0 0 {view_size} {view_size}"',
            'xmlns="http://www.w3.org/2000/svg">',
            "<defs>"
        ]

        # === GRADIENTS ===
        gradient_def = build_gradient(params.get("gradient", {}))
        if gradient_def:
            svg_parts.append(gradient_def)

        # === FILTERS === (shadow, glow)
        filter_def = build_filters(params)
        if filter_def:
            svg_parts.append(filter_def)

        svg_parts.append("</defs>")

        # === MULTI-LAYER ===
        for layer in params.get("layers", []):
            svg_parts.append(Renderer._render_layer(layer, layout))

        # === MAIN SHAPE ===
        svg_parts.append(Renderer._render_main_shape(params))

        # ICON LAYER
        icon_layer = Renderer._render_icon_layer(params.get("icon", {}))
        if icon_layer:
            svg_parts.append(icon_layer)

        # RARITY / STAR LAYERS
        stars_layer = Renderer._render_star_layers(params.get("stars", {}), params.get("layout", {}))
        if stars_layer:
            svg_parts.append(stars_layer)

        svg_parts.append("</svg>")
        return "".join(svg_parts)

    @staticmethod
    def _render_layer(layer, layout):
        layer_shape = layer.get("shape", {})
        layer_colors = layer.get("colors", {})
        layer_gradient = layer.get("gradient", {})
        layer_shadow = layer.get("shadow", {})
        layer_glow = layer.get("glow", {})

        shape_svg = build_shape(layer_shape)

        # Fill / stroke uygulama
        shape_svg = apply_fill_and_stroke(
            shape_svg,
            layer_colors,
            layer_gradient,
            layer_shadow,
            layer_glow
        )

        return shape_svg

    @staticmethod
    def _render_main_shape(params):
        shape = params.get("shape", {})
        colors = params.get("colors", {})
        gradient = params.get("gradient", {})
        shadow = params.get("shadow", {})
        glow = params.get("glow", {})

        base_shape = build_shape(shape)

        base_shape = apply_fill_and_stroke(
            base_shape,
            colors,
            gradient,
            shadow,
            glow
        )

        return base_shape

    @staticmethod
    def _render_icon_layer(icon: dict):
        if not icon.get("enabled"):
            return ""

        src = icon.get("src")
        if not src:
            return ""

        size = icon.get("size", 64)
        ox = icon.get("offset_x", 0)
        oy = icon.get("offset_y", 0)
        opacity = icon.get("opacity", 1.0)

        # Static path resolve
        static_path = static(f"M03_art_studio/img/icons/{src}")

        return (
            f'<image href="{static_path}" '
            f'x="{ox}" y="{oy}" '
            f'width="{size}" height="{size}" '
            f'opacity="{opacity}" />'
        )
    
    @staticmethod
    def _render_star_layers(stars: dict, layout: dict):
        """
        Gelişmiş yıldız motoru:
        - filled / outline / mixed
        - auto-center veya manual offset_x
        - boyut, gap, opacity
        """
        if not stars or not stars.get("enabled"):
            return ""

        count = int(stars.get("count", 0))
        if count <= 0:
            return ""

        size = stars.get("size", 32)
        gap = stars.get("gap", 8)
        offset_y = stars.get("offset_y", 0)
        offset_x = stars.get("offset_x")  # None ise auto-center
        opacity = stars.get("opacity", 1.0)

        star_type = stars.get("type", "filled")  # filled | outline | mixed
        filled_count = int(stars.get("filled_count", count))

        icon_filled_name = stars.get("icon_filled", "star_filled.png")
        icon_outline_name = stars.get("icon_outline", "star_outline.png")

        static_filled = static(f"M03_art_studio/img/icons/{icon_filled_name}")
        static_outline = static(f"M03_art_studio/img/icons/{icon_outline_name}")

        canvas_size = layout.get("size", 256)

        total_width = count * size + (count - 1) * gap

        if offset_x is None:
            start_x = (canvas_size - total_width) / 2
        else:
            start_x = offset_x

        svg = ""

        for i in range(count):
            x = start_x + i * (size + gap)

            # Hangi ikon? filled / outline / mixed
            if star_type == "outline":
                href = static_outline
            elif star_type == "mixed":
                href = static_filled if i < filled_count else static_outline
            else:  # filled
                href = static_filled

            svg += (
                f'<image href="{href}" '
                f'x="{x}" y="{offset_y}" '
                f'width="{size}" height="{size}" '
                f'opacity="{opacity}" />'
            )

        return svg

