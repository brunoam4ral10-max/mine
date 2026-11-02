#!/usr/bin/env python3
"""
Gera o index.html autossuficiente do viewer 3D.

- Lê as texturas vanilla 16x16 (assets/textures) e as codifica como matrizes
  de índices de paleta, para serem redesenhadas em <canvas> em tempo de execução.
- Incorpora o Three.js (vendor/three.min.js) e a fonte pixelada (woff2)
  diretamente no HTML, para que o arquivo funcione 100% offline.
"""
from __future__ import annotations

import base64
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
CHARS = "0123456789abcdefghijklmnopqrstuvwxyz"

# Dados fiéis ao Java Edition 1.20.x
META = [
    dict(
        file="wooden_sword", id="wood", name="Madeira", tier="Madeira",
        accent="#c8914f", glow="#e6b26a",
        flavor="O primeiro fio. Simples, leve e honesto.",
        damage="4", speed="1,6", durability="59", durability_num=59, enchant="15",
    ),
    dict(
        file="stone_sword", id="stone", name="Pedra", tier="Pedra",
        accent="#a9adb2", glow="#d5dce2",
        flavor="Talhada na rocha, mais firme que a madeira.",
        damage="5", speed="1,6", durability="131", durability_num=131, enchant="5",
    ),
    dict(
        file="iron_sword", id="iron", name="Ferro", tier="Ferro",
        accent="#d8e2ea", glow="#ffffff",
        flavor="O equilíbrio exato entre peso e corte.",
        damage="6", speed="1,6", durability="250", durability_num=250, enchant="14",
    ),
    dict(
        file="golden_sword", id="gold", name="Ouro", tier="Ouro",
        accent="#ffd257", glow="#ffe98a",
        flavor="Frágil e veloz, mas faminta por encantamentos.",
        damage="4", speed="1,6", durability="32", durability_num=32, enchant="22",
    ),
    dict(
        file="diamond_sword", id="diamond", name="Diamante", tier="Diamante",
        accent="#43e3cc", glow="#a4fdf0",
        flavor="Azul profundo. O clássico absoluto do Overworld.",
        damage="7", speed="1,6", durability="1561", durability_num=1561, enchant="10",
    ),
    dict(
        file="netherite_sword", id="netherite", name="Netherita", tier="Netherita",
        accent="#b493b4", glow="#e0a9a0",
        flavor="Forjada no fogo do Nether. O fogo não a consome.",
        damage="8", speed="1,6", durability="2031", durability_num=2031, enchant="15",
    ),
]


def encode_png(path: Path) -> dict:
    im = Image.open(path).convert("RGBA")
    if im.size != (16, 16):
        raise ValueError(f"{path} não é 16x16")
    px = list(im.get_flattened_data())
    palette: list[str] = []
    lut: dict[str, int] = {}
    rows: list[str] = []
    for p in px:
        if p[3] < 128:
            rows.append(".")
            continue
        key = "#%02x%02x%02x" % (p[0], p[1], p[2])
        if key not in lut:
            lut[key] = len(palette)
            palette.append(key)
        rows.append(CHARS[lut[key]])
    return {"palette": palette, "pixels": "".join(rows)}


def main() -> None:
    materials = []
    for m in META:
        enc = encode_png(ROOT / "assets" / "textures" / f"{m['file']}.png")
        item = {k: v for k, v in m.items() if k != "file"}
        item.update(enc)
        materials.append(item)

    template = (ROOT / "src" / "template.html").read_text(encoding="utf-8")
    three_js = (ROOT / "vendor" / "three.min.js").read_text(encoding="utf-8")
    font_b64 = base64.b64encode(
        (ROOT / "assets" / "press-start-2p-latin.woff2").read_bytes()
    ).decode("ascii")
    texture_js = (
        "/* Texturas vanilla 16x16 do Minecraft (Java 1.20.4), codificadas por paleta. */\n"
        "const TEXTURE_DATA = " + json.dumps(materials, ensure_ascii=False, separators=(",", ":")) + ";\n"
    )

    if "</script" in three_js.lower():
        raise RuntimeError("Three.js contém um fechamento de <script> inesperado")

    html = (
        template
        .replace("__FONT_B64__", font_b64)
        .replace("/*__THREE_JS__*/", three_js)
        .replace("/*__TEXTURE_DATA__*/", texture_js)
    )
    out = ROOT / "index.html"
    out.write_text(html, encoding="utf-8")
    print(f"✓ {out.name} gerado ({out.stat().st_size / 1024:.0f} KB, {len(materials)} materiais, 84 voxels)")


if __name__ == "__main__":
    main()
