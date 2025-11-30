import os
import sys
import textwrap
from urllib.request import urlopen
from PIL import Image, ImageDraw, ImageFont

def main():
    url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000/metrics"
    data = urlopen(url).read().decode("utf-8")
    lines = data.splitlines()[:60]
    text = "\n".join(lines)
    wrapped = []
    for line in lines:
        wrapped.extend(textwrap.wrap(line, width=120) or [""])
    w = 1400
    h = 20 + 18 * (len(wrapped) + 2)
    img = Image.new("RGB", (w, h), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    draw.text((10, 10), "GET /metrics", fill=(200, 200, 200), font=font)
    y = 30
    for ln in wrapped:
        draw.text((10, y), ln, fill=(160, 220, 160), font=font)
        y += 18
    os.makedirs("screenshots", exist_ok=True)
    out = os.path.join("screenshots", "metrics.png")
    img.save(out)
    print(out)

if __name__ == "__main__":
    main()