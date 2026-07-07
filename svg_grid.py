def grid_to_svg(
    width: int,
    height: int,
    paths: list[list[tuple[int, int]]],
    filename: str,
    *,
    cell_size: float = 20,
    dot_radius: float = 2,
    dot_color: str = "#888",
    line_color: str = "#000",
    line_width: float = 2,
) -> str:
    """Render an SVG grid with dots at every integer coordinate and broken lines for each path.

    Coordinates are (x, y) with x in [0, width) and y in [0, height).
    Each inner list in ``paths`` is drawn as a separate polyline.
    The SVG is written to ``{filename}.svg``.
    """
    svg_width = width * cell_size
    svg_height = height * cell_size

    parts: list[str] = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{svg_width}" height="{svg_height}" viewBox="0 0 {svg_width} {svg_height}">',
    ]

    for y in range(height):
        for x in range(width):
            cx = x * cell_size + cell_size / 2
            cy = y * cell_size + cell_size / 2
            parts.append(
                f'<circle cx="{cx}" cy="{cy}" r="{dot_radius}" fill="{dot_color}" />'
            )

    for path in paths:
        if len(path) < 2:
            continue
        points = " ".join(
            f"{x * cell_size + cell_size / 2},{y * cell_size + cell_size / 2}"
            for x, y in path
        )
        parts.append(
            f'<polyline points="{points}" fill="none" stroke="{line_color}" '
            f'stroke-width="{line_width}" stroke-linejoin="round" stroke-linecap="round" />'
        )

    parts.append("</svg>")
    svg = "\n".join(parts)
    with open(f"svg/{filename}.svg", "w", encoding="utf-8") as f:
        f.write(svg)
    return svg
