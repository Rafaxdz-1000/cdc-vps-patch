# -*- coding: utf-8 -*-
"""Verificacao final: Ensino=illustration (sem emoji) / Vendas=tweet (com emoji)."""
import json, urllib.request, time
BASE = "http://127.0.0.1:5001/render-post"
TS = int(time.time())
CASES = [
    dict(t="ENS_S1", b=dict(layout="illustration", slide_index=1, total=4, tag="ESCOLA DE IA",
         filename_base="cdc_fin_ens1_%d" % TS, categoria="", titulo="O que e um agente de IA?",
         body="", site="clubedoscisnes.com", bg_prompt="x")),
    dict(t="ENS_S2", b=dict(layout="illustration", slide_index=2, total=4, tag="ESCOLA DE IA",
         filename_base="cdc_fin_ens2_%d" % TS, categoria="Escola de IA",
         titulo="Ele age, nao so responde",
         body="Um chatbot responde. Um agente pesquisa, decide e executa a tarefa inteira sozinho.",
         site="clubedoscisnes.com", bg_prompt="x")),
    dict(t="VEN_S1", b=dict(layout="tweet", slide_index=1, total=4,
         filename_base="cdc_fin_ven1_%d" % TS, categoria="", titulo="",
         body="Sua clinica perde paciente as 23h porque nao tem quem responda o WhatsApp. \U0001f634",
         site="clubedoscisnes.com", bg_prompt="empty medical clinic reception at night, realistic photo")),
    dict(t="VEN_S2", b=dict(layout="tweet", slide_index=2, total=4,
         filename_base="cdc_fin_ven2_%d" % TS, categoria="", titulo="",
         body="Um chatbot de WhatsApp com IA agenda, tira duvidas e qualifica pacientes. Sozinho, 24h por dia. \U0001f916",
         site="clubedoscisnes.com", bg_prompt="x")),
]
for c in CASES:
    t0 = time.time()
    req = urllib.request.Request(BASE, data=json.dumps(c["b"]).encode(), headers={"Content-Type": "application/json"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=200).read())
        print("%s ok %ds url=%s" % (c["t"], time.time() - t0, r.get("url")), flush=True)
    except Exception as e:
        print("%s FAIL %s" % (c["t"], str(e)[:140]), flush=True)
