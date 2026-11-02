#!/usr/bin/env python3
"""Gera casa.html autossuficiente a partir de src/house-template.html."""
from pathlib import Path
import base64

ROOT = Path(__file__).resolve().parent
tpl = (ROOT / "src" / "house-template.html").read_text(encoding="utf-8")
three = (ROOT / "vendor" / "three.min.js").read_text(encoding="utf-8")
font = base64.b64encode((ROOT / "assets" / "press-start-2p-latin.woff2").read_bytes()).decode()
if "</script" in three.lower():
    raise RuntimeError("fechamento de script inesperado no Three.js")
out = (ROOT / "casa.html")
out.write_text(tpl.replace("__FONT_B64__", font).replace("/*__THREE_JS__*/", three), encoding="utf-8")
print(f"✓ {out.name} gerado ({out.stat().st_size/1024:.0f} KB, 100% offline)")
