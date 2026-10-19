"""One-off: pull the YouTube, Instagram and TikTok logos out of the Font Awesome 6 Brands font (CC BY 4.0,
already credited on the page) and store their outlines in store_icons.json, in the same form as the store logos."""
import json
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.boundsPen import BoundsPen

HERE = Path(__file__).parent
FONT = Path("E:/AD Personal/Ideas/IronLog/app/node_modules/@expo/vector-icons/build/vendor/react-native-vector-icons/Fonts/FontAwesome6_Brands.ttf")
CODEPOINTS = {"youtube": 0xF167, "instagram": 0xF16D, "tiktok": 0xE07B}

font = TTFont(FONT)
cmap = font.getBestCmap()
gs = font.getGlyphSet()
icons = json.load(open(HERE / "store_icons.json", encoding="utf-8"))
for name, cp in CODEPOINTS.items():
    glyph_name = cmap[cp]
    pen = SVGPathPen(gs)
    gs[glyph_name].draw(pen)
    bp = BoundsPen(gs)
    gs[glyph_name].draw(bp)
    icons[name] = {"d": pen.getCommands(), "bounds": list(bp.bounds)}
    print(name, glyph_name, bp.bounds)
json.dump(icons, open(HERE / "store_icons.json", "w", encoding="utf-8"))
