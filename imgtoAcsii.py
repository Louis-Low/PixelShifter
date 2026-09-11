from PIL import Image
from pathlib import Path
import html

ASCII_CHARS = "@%#*+=-:. "
DEFAULT_WIDTH = 100


def image_to_colored_ascii(image_path, width=DEFAULT_WIDTH):
    image = Image.open(image_path).convert("RGB")

    aspect_ratio = image.height / image.width
    height = max(1, int(width * aspect_ratio * 0.5))
    image = image.resize((width, height))

    lines = []

    for y in range(height):
        line = []

        for x in range(width):
            r, g, b = image.getpixel((x, y))

            # Convert RGB to brightness
            brightness = (0.299 * r + 0.587 * g + 0.114 * b)
            index = int(brightness / 255 * (len(ASCII_CHARS) - 1))
            char = ASCII_CHARS[index]

            # Preserve the original pixel color
            line.append(
                f'<span style="color:rgb({r},{g},{b})">{html.escape(char)}</span>'
            )

        lines.append("".join(line))

    return "<br>".join(lines)


def create_html(ascii_art, output_path="ascii_output.html"):
    document = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Colored ASCII Art</title>

<style>
    * {{
        box-sizing: border-box;
    }}

    body {{
        margin: 0;
        min-height: 100vh;
        background: #050505;
        color: white;
        display: flex;
        justify-content: center;
        align-items: center;
        overflow: auto;
        font-family: monospace;
    }}

    .wrapper {{
        width: 100%;
        padding: 30px;
        text-align: center;
    }}

    h1 {{
        margin-bottom: 25px;
        font-size: 24px;
        letter-spacing: 2px;
    }}

    .ascii {{
        display: inline-block;
        text-align: left;
        white-space: nowrap;
        line-height: 0.55;
        font-size: 8px;
        letter-spacing: 0;
        user-select: none;
        animation: float 4s ease-in-out infinite;
    }}

    .ascii span {{
        display: inline;
    }}

    @keyframes float {{
        0%, 100% {{ transform: translateY(0); }}
        50% {{ transform: translateY(-8px); }}
    }}

    .hint {{
        margin-top: 25px;
        color: #888;
        font-size: 12px;
    }}
</style>
</head>

<body>
<div class="wrapper">
    <h1>COLORED ASCII ART</h1>

    <div class="ascii">
        {ascii_art}
    </div>

    <div class="hint">
        Generated with Python + Pillow
    </div>
</div>
</body>
</html>
"""

    Path(output_path).write_text(document, encoding="utf-8")


def main():
    image_path = input("Enter image path: ").strip()

    if not Path(image_path).exists():
        print("Error: Image not found.")
        return

    try:
        width = int(input("ASCII width (default 100): ").strip() or DEFAULT_WIDTH)
    except ValueError:
        width = DEFAULT_WIDTH

    print("Converting image...")

    ascii_art = image_to_colored_ascii(image_path, width)
    create_html(ascii_art)

    print("Done!")
    print("Output: ascii_output.html")


if __name__ == "__main__":
    main()
