# -*- coding: utf-8 -*-
"""Testa a INVERSAO: Ensino=illustration (tag ESCOLA DE IA) / Vendas=tweet (centralizado)."""
import json, urllib.request, time

BASE = "http://127.0.0.1:5001/render-post"

CASES = [
    # Ensino agora = ILUSTRACAO
    dict(tag="ENS_CAPA", body=dict(layout="illustration", slide_index=1, total=4, tag="ESCOLA DE IA",
         filename_base="cdc_swap_ens_s1_%d" % int(time.time()),
         categoria="", titulo="O que e um LLM afinal?", body="",
         site="clubedoscisnes.com", bg_prompt="ai neural network")),
    dict(tag="ENS_CONT", body=dict(layout="illustration", slide_index=2, total=4, tag="ESCOLA DE IA",
         filename_base="cdc_swap_ens_s2_%d" % int(time.time()),
         categoria="Escola de IA", titulo="Uma esponja que leu a internet",
         body="O LLM e treinado com bilhoes de textos e aprende a prever a proxima palavra.",
         site="clubedoscisnes.com", bg_prompt="ai brain")),
    # Vendas agora = TWEET
    dict(tag="VEN_CAPA", body=dict(layout="tweet", slide_index=1, total=4,
         filename_base="cdc_swap_ven_s1_%d" % int(time.time()),
         categoria="", titulo="", body="Sua clinica perde paciente as 23h porque nao tem quem responda o WhatsApp.",
         site="clubedoscisnes.com", bg_prompt="empty medical clinic reception at night, realistic photo")),
    dict(tag="VEN_MID", body=dict(layout="tweet", slide_index=2, total=4,
         filename_base="cdc_swap_ven_s2_%d" % int(time.time()),
         categoria="", titulo="", body="Um chatbot de WhatsApp com IA agenda, tira duvidas e qualifica pacientes. Sozinho, 24h por dia.",
         site="clubedoscisnes.com", bg_prompt="chatbot")),
]

for c in CASES:
    t0 = time.time()
    req = urllib.request.Request(BASE, data=json.dumps(c["body"]).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=200).read())
        print("%s ok url=%s secs=%d" % (c["tag"], r.get("url"), time.time() - t0), flush=True)
    except Exception as e:
        print("%s FAIL %s" % (c["tag"], str(e)[:160]), flush=True)
