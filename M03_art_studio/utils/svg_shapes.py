"""
Shape Builder
-------------
Tüm vektörel şekillerin SVG <path> çıktısını burada üretiyoruz.
"""

def build_shape(shape: dict) -> str:
    stype = shape.get("type", "circle")
    size = shape.get("size", 256)
    width = shape.get("width", size)
    height = shape.get("height", size)
    radius = shape.get("radius", 0)

    # === CIRCLE ===
    if stype == "circle":
        r = size / 2
        return f'<circle cx="{r}" cy="{r}" r="{r}" '

    # === SQUARE ===
    if stype == "square":
        return f'<rect width="{size}" height="{size}" '

    # === ROUNDED SQUARE ===
    if stype == "rounded_square":
        return f'<rect width="{size}" height="{size}" rx="{radius}" ry="{radius}" '

    # === DIAMOND ===
    if stype == "diamond":
        half = size / 2
        return f'<polygon points="{half},0 {size},{half} {half},{size} 0,{half}" '

    # === HEXAGON (regular) ===
    if stype == "hexagon":
        h = size
        w = size
        return f'<polygon points="{w*0.25},0 {w*0.75},0 {w}, {h*0.5} {w*0.75},{h} {w*0.25},{h} 0,{h*0.5}" '

    # === CUSTOM PATH ===
    if stype == "path":
        pathd = shape.get("path", "")
        return f'<path d="{pathd}" '

    # fallback
    return f'<rect width="{size}" height="{size}" '
