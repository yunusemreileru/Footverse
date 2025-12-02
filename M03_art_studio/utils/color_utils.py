"""
Color & Gradient Engine
-----------------------
fill/stroke, gradient, shadow, glow
"""

import uuid


def build_gradient(gradient: dict) -> str:
    if not gradient.get("enabled"):
        return ""

    gid = f"grad_{uuid.uuid4().hex[:6]}"
    gtype = gradient.get("type", "linear")
    angle = gradient.get("angle", 0)

    stops = gradient.get("stops", [])

    if gtype == "linear":
        x1 = 0
        y1 = 0
        x2 = 1
        y2 = 1
        return (
            f'<linearGradient id="{gid}" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
            + "".join([f'<stop offset="{p[1]*100}%" stop-color="{p[0]}" />' for p in stops])
            + "</linearGradient>"
        )

    if gtype == "radial":
        return (
            f'<radialGradient id="{gid}">'
            + "".join([f'<stop offset="{p[1]*100}%" stop-color="{p[0]}" />' for p in stops])
            + "</radialGradient>"
        )

    return ""


def build_filters(params: dict) -> str:
    """
    Build shadow + glow filters in <defs>.
    """
    shadow = params.get("shadow", {})
    glow = params.get("glow", {})

    # no filter required
    if not shadow.get("enabled") and not glow.get("enabled"):
        return ""

    fid = f"f_{uuid.uuid4().hex[:6]}"
    parts = [f'<filter id="{fid}">']

    # === SHADOW ===
    if shadow.get("enabled"):
        ox = shadow.get("offset_x", 0)
        oy = shadow.get("offset_y", 0)
        blur = shadow.get("blur", 4)
        color = shadow.get("color", "rgba(0,0,0,0.4)")

        parts.append(f'<feDropShadow dx="{ox}" dy="{oy}" stdDeviation="{blur}" flood-color="{color}" />')

    # === GLOW ===
    if glow.get("enabled"):
        blur = glow.get("blur", 4)
        color = glow.get("color", "#ffffff")

        parts.append(
            f'<feGaussianBlur stdDeviation="{blur}" result="coloredBlur" />'
            f'<feMerge>'
            f'<feMergeNode in="coloredBlur"/><feMergeNode in="SourceGraphic"/>'
            f'</feMerge>'
        )

    parts.append("</filter>")

    return "".join(parts)


def apply_fill_and_stroke(shape_svg: str, colors: dict, gradient: dict, shadow: dict, glow: dict) -> str:
    fill = colors.get("fill", "#ffffff")
    stroke = colors.get("stroke", "#000000")
    stroke_width = colors.get("stroke_width", 2)
    opacity = colors.get("fill_opacity", 1.0)

    # apply attributes
    shape_svg = shape_svg.rstrip(" />")

    # gradient?
    if gradient.get("enabled"):
        shape_svg += f' fill="url(#grad_01)"'
    else:
        shape_svg += f' fill="{fill}" fill-opacity="{opacity}"'

    # stroke
    if stroke:
        shape_svg += f' stroke="{stroke}" stroke-width="{stroke_width}"'

    # filter (shadow/glow)
    if shadow.get("enabled") or glow.get("enabled"):
        shape_svg += f' filter="url(#f_01)"'

    shape_svg += "/>"

    return shape_svg
