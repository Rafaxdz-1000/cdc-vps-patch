# -*- coding: utf-8 -*-
"""
patch_gate_gemini.py — gateia a chamada Gemini no /render-post: só gera bg quando é necessário
(default sem layout, ou tweet slide 1). Para illustration e tweet slides 2-4, pula o loop Gemini
(economiza custo/latencia). Mudança minima: define _need_bg + troca range(3) -> range(0) quando nao precisa.
Requer o patch de layout ja aplicado. Idempotente. Valida sintaxe.
"""
import re, sys, py_compile

P = '/opt/cdc/app.py'
orig = open(P, encoding='utf-8').read()

if '_need_bg' in orig:
    print('ALREADY_PATCHED')
    sys.exit(0)
if 'render_slide_html' not in orig:
    print('ERR_LAYOUT_PATCH_MISSING')
    sys.exit(2)

src = orig

# 1) injeta _need_bg logo apos a init de bg_uri (quote-agnostico), dentro de render_post
INJ = ("\\g<0>"
       "    _lay0 = (data.get('layout') or '').lower()\n"
       "    _need_bg = (_lay0 not in ('tweet', 'illustration')) or (_lay0 == 'tweet' and int(data.get('slide_index') or 1) == 1)\n")
src2, n1 = re.subn(r'(?m)^    bg_uri = [\'"]{2}\n', INJ, src, count=1)
if n1 != 1:
    print('ERR_NO_BGURI_INIT n=%d' % n1)
    sys.exit(3)
src = src2

# 2) gateia o loop de tentativas do Gemini
src3, n2 = re.subn(r'(?m)^    for _att in range\(3\):$',
                   '    for _att in (range(3) if _need_bg else range(0)):', src, count=1)
if n2 != 1:
    print('ERR_NO_LOOP n=%d' % n2)
    sys.exit(4)
src = src3

if '_need_bg' not in src or 'if _need_bg else range(0)' not in src:
    print('ERR_SANITY')
    sys.exit(5)

open(P + '.bak_gemini', 'w', encoding='utf-8').write(orig)
open(P, 'w', encoding='utf-8').write(src)
try:
    py_compile.compile(P, doraise=True)
except Exception as e:
    open(P, 'w', encoding='utf-8').write(orig)
    print('SYNTAX_ERROR_ROLLED_BACK:', e)
    sys.exit(6)

print('GATE_OK bytes=%d bak=%s' % (len(src), P + '.bak_gemini'))
