# -*- coding: utf-8 -*-
"""
patch_render_layout_app.py — adiciona `layout` (tweet/illustration) a render_post() INLINE no app.py.
Escopado APENAS a def render_post() (nao toca render-carousel/story/insights). Idempotente. Valida sintaxe.
"""
import re, sys, py_compile

P = '/opt/cdc/app.py'
src = open(P, encoding='utf-8').read()

if 'render_slide_html' in src:
    print('ALREADY_PATCHED')
    sys.exit(0)

key = '\ndef render_post():'
if key not in src:
    print('ERR_NO_RENDER_POST')
    sys.exit(2)

start = src.index(key) + 1  # posiciona no 'def render_post():'
head_len = len('def render_post():')
after = src[start + head_len:]
m = re.search(r'\n(def |@app\.route)', after)   # proxima def/rota de nivel de modulo
end = start + head_len + (m.start() if m else len(after))
block = src[start:end]
ob = block

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

anchor = '    with sync_playwright() as pw:'
if anchor not in block:
    print('ERR_NO_ANCHOR')
    sys.exit(3)
block = block.replace(anchor, BRANCH + anchor, 1)

b2 = re.sub(r'viewport\s*=\s*\{[^}]*1350[^}]*\}', 'viewport=_vp', block, count=1)
if b2 == block:
    print('ERR_NO_VIEWPORT')
    sys.exit(4)
block = b2

b3 = re.sub(r'_cdc_post_html\(\s*categoria\s*,\s*titulo\s*,\s*body\s*,\s*site\s*,\s*bg_uri\s*\)',
            '_html', block, count=1)
if b3 == block:
    print('ERR_NO_SETCONTENT')
    sys.exit(5)
block = b3

newsrc = src[:start] + block + src[end:]
open(P + '.bak_layout', 'w', encoding='utf-8').write(src)
open(P, 'w', encoding='utf-8').write(newsrc)
try:
    py_compile.compile(P, doraise=True)
except Exception as e:
    open(P, 'w', encoding='utf-8').write(src)
    print('SYNTAX_ERROR_ROLLED_BACK:', e)
    sys.exit(6)

print('APPPATCH_OK bytes=%d bak=%s' % (len(newsrc), P + '.bak_layout'))
