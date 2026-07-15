# -*- coding: utf-8 -*-
"""Render dos temas REAIS do Ensino com o mapa estendido."""
import json, urllib.request, time
BASE = "http://127.0.0.1:5001/render-post"
TS = int(time.time())
CASES = [
    ("rag",   "A IA que aprende com seus arquivos", "RAG faz a IA consultar seus documentos antes de responder. Nada de invencao."),
    ("aluc",  "Por que a IA inventa coisas?",       "A alucinacao acontece quando a IA responde com seguranca uma informacao falsa."),
    ("token", "Token: a moeda da IA",               "A IA quebra o texto em tokens. Quando passa da janela de contexto, ela esquece o comeco."),
    ("hist",  "De 1956 ate hoje",                   "A linha do tempo da IA: 1956 nasceu o termo, 1997 Deep Blue, 2012 redes neurais, 2022 ChatGPT."),
    ("reun",  "Nunca mais perca uma reuniao",       "Ferramentas de IA transcrevem a reuniao e resumem o que foi dito automaticamente."),
    ("tools", "A ferramenta certa pra cada tarefa", "Existem as melhores ferramentas de IA para escrever, criar imagens e planilhas."),
]
for k, tit, body in CASES:
    b = dict(layout="illustration", slide_index=2, total=4, tag="ESCOLA DE IA",
             filename_base="cdc_ill_%s_%d" % (k, TS), categoria="Escola de IA",
             titulo=tit, body=body, site="clubedoscisnes.com", bg_prompt="x")
    req = urllib.request.Request(BASE, data=json.dumps(b).encode(), headers={"Content-Type": "application/json"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=120).read())
        print("%s ok url=%s" % (k, r.get("url")), flush=True)
    except Exception as e:
        print("%s FAIL %s" % (k, str(e)[:120]), flush=True)
