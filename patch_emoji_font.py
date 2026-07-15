# -*- coding: utf-8 -*-
"""
patch_emoji_font.py — adiciona fonte de emoji ao container cdc-slides.
Sem a fonte, emojis na copy renderizam como quadradinhos (tofu) nos slides do IG.
Insere a camada DEPOIS do playwright install para reaproveitar o cache das camadas pesadas.
Idempotente. Backup em Dockerfile.bak_emoji.
"""
import sys

P = '/opt/cdc/Dockerfile'
src = open(P, encoding='utf-8').read()

if 'fonts-noto-color-emoji' in src:
    print('ALREADY_PATCHED')
    sys.exit(0)

ANCHOR = 'RUN python3 -m playwright install chromium\n'
if ANCHOR not in src:
    print('ERR_NO_ANCHOR')
    sys.exit(2)

ADD = (ANCHOR +
       '\n# fonte de emoji: sem isso, emoji na copy vira quadradinho (tofu) no screenshot\n'
       'RUN apt-get update && apt-get install -y --no-install-recommends '
       'fonts-noto-color-emoji fontconfig && rm -rf /var/lib/apt/lists/* && fc-cache -f\n')

out = src.replace(ANCHOR, ADD, 1)
if out == src:
    print('ERR_REPLACE')
    sys.exit(3)

open(P + '.bak_emoji', 'w', encoding='utf-8').write(src)
open(P, 'w', encoding='utf-8').write(out)
print('OK_EMOJI_LAYER_ADDED bak=%s.bak_emoji' % P)
