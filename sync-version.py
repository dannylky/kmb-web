#!/usr/bin/env python3
import re, sys
from pathlib import Path

repo = Path(__file__).resolve().parent
html = repo / 'index.html'
ver = (repo / 'VERSION').read_text(encoding='utf-8').splitlines()[0]
content = html.read_text(encoding='utf-8')
content = re.sub(r'<span class="version">v[\d.]+</span>', f'<span class="version">{ver}</span>', content)
html.write_text(content, encoding='utf-8')
print(f'Version synced to {ver}')
