# -*- coding: utf-8 -*-
import json, urllib.request, time
BASE = "http://127.0.0.1:5001/render-post"
TS = int(time.time())
CASES = [
    dict(t="EMOJI_ILLUS", b=dict(layout="illustration", slide_index=2, total=4, tag="ESCOLA DE IA",
         filename_base="cdc_emoji_illus_%d" % TS, categoria="Escola de IA",
         titulo="Ferramenta certa pra cada tarefa",
         body="✍️ Escrever: ChatGPT • \U0001f5bc️ Imagens: Midjourney • \U0001f4ca Planilhas: Julius • \U0001f3a5 Vídeos: Runway \U0001f680",
         site="clubedoscisnes.com", bg_prompt="x")),
    dict(t="EMOJI_TWEET", b=dict(layout="tweet", slide_index=2, total=4,
         filename_base="cdc_emoji_tweet_%d" % TS, categoria="", titulo="",
         body="Você usa o ChatGPT todo dia \U0001f9e0 mas sabe o que roda por baixo? \U0001f447 A gente explica ✨",
         site="clubedoscisnes.com", bg_prompt="x")),
]
for c in CASES:
    req = urllib.request.Request(BASE, data=json.dumps(c["b"]).encode(), headers={"Content-Type": "application/json"})
    try:
        r = json.loads(urllib.request.urlopen(req, timeout=200).read())
        print("%s ok url=%s" % (c["t"], r.get("url")), flush=True)
    except Exception as e:
        print("%s FAIL %s" % (c["t"], str(e)[:140]), flush=True)
