# -*- coding: utf-8 -*-
"""
patch_render_layout.py — adiciona suporte a `layout` (tweet/illustration) ao /render-post do cdc-slides.
Cirurgico: NAO altera _cdc_post_html nem o fluxo Gemini. Quando data['layout'] e tweet/illustration,
monta o HTML via cdc_ig_layouts.render_slide_html em viewport 1080x1080; senao, comportamento identico.
Idempotente (checa marcador). Valida sintaxe antes de gravar.
"""
import re, sys, py_compile

P = '/opt/cdc/_render_post_route.py'
src = open(P, encoding='utf-8').read()

if 'render_slide_html' in src:
    print('ALREADY_PATCHED')
    sys.exit(0)

orig = src

BRANCH = (
    "    # --- CDC IG layouts (tweet=Ensino / illustration=Vendas) ---\n"
    "    import sys as _sys\n"
    "    if '/opt/cdc' not in _sys.path:\n"
    "        _sys.path.insert(0, '/opt/cdc')\n"
    "    _layout = (data.get('layout') or '').lower()\n"
    "    _sidx = int(data.get('slide_index') or 1)\n"
    "    _total = int(data.get('total') or 4)\n"
    "    _tag = data.get('tag') or 'VENDAS'\n"
    "    try:\n"
    "        _bg = bg_uri\n"
    "    except Exception:\n"
    "        _bg = None\n"
    "    if _layout in ('tweet', 'illustration'):\n"
    "        from cdc_ig_layouts import render_slide_html as _rsh\n"
    "        _img = _bg if (_layout == 'tweet' and _sidx == 1) else None\n"
    "        _html = _rsh(_layout, _sidx, _total, categoria, titulo, body,\n"
    "                     image_data_uri=_img, site=site, tag=_tag, seed=titulo)\n"
    "        _vp = {\"width\": 1080, \"height\": 1080}\n"
    "    else:\n"
    "        _html = _cdc_post_html(categoria, titulo, body, site, _bg)\n"
    "        _vp = {\"width\": 1080, \"height\": 1350}\n"
)

# 1) injeta o branch antes do bloco Playwright
anchor = '    with sync_playwright() as pw:'
if anchor not in src:
    print('ERR_NO_PLAYWRIGHT_ANCHOR')
    sys.exit(2)
src = src.replace(anchor, BRANCH + anchor, 1)

# 2) viewport 1080x1350 fixo -> _vp (so o do new_page, que contem 1350)
src2 = re.sub(r'viewport\s*=\s*\{[^}]*1350[^}]*\}', 'viewport=_vp', src, count=1)
if src2 == src:
    print('ERR_NO_VIEWPORT')
    sys.exit(3)
src = src2

# 3) set_content usa _html (substitui a chamada original que passa bg_uri)
src3 = re.sub(r'_cdc_post_html\(\s*categoria\s*,\s*titulo\s*,\s*body\s*,\s*site\s*,\s*bg_uri\s*\)',
              '_html', src, count=1)
if src3 == src:
    print('ERR_NO_SETCONTENT_CALL')
    sys.exit(4)
src = src3

if not ('_html' in src and 'viewport=_vp' in src and 'render_slide_html' in src):
    print('ERR_SANITY')
    sys.exit(5)

# backup + grava + valida sintaxe
open(P + '.bak_layout', 'w', encoding='utf-8').write(orig)
open(P, 'w', encoding='utf-8').write(src)
try:
    py_compile.compile(P, doraise=True)
except Exception as e:
    # rollback em caso de erro de sintaxe
    open(P, 'w', encoding='utf-8').write(orig)
    print('SYNTAX_ERROR_ROLLED_BACK:', e)
    sys.exit(6)

print('PATCH_OK bytes=%d bak=%s' % (len(src), P + '.bak_layout'))
