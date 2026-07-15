# -*- coding: utf-8 -*-
import requests
BASE = 'http://localhost:5001/render-post'

def go(name, payload):
    try:
        r = requests.post(BASE, json=payload, timeout=200)
        try:
            j = r.json()
        except Exception:
            j = {'raw': r.text[:200]}
        print('%s STATUS=%s url=%s ok=%s bg=%s' % (
            name, r.status_code, j.get('url'), j.get('ok'), j.get('bg_ai')))
    except Exception as e:
        print('%s ERR %r' % (name, e))

go('VEND_S1', {"layout": "illustration", "slide_index": 1, "total": 4, "categoria": "",
    "titulo": "Sua clinica perde paciente as 23h?", "body": "", "site": "clubedoscisnes.com",
    "tag": "VENDAS", "filename_base": "cdc_t2_vend_s1", "bg_prompt": "soft abstract shapes"})
go('VEND_S2', {"layout": "illustration", "slide_index": 2, "total": 4, "categoria": "O problema",
    "titulo": "Fora do horario, ele nao espera.", "body": "O paciente acha o concorrente e agenda em minutos.",
    "site": "clubedoscisnes.com", "filename_base": "cdc_t2_vend_s2", "bg_prompt": "x"})
go('ENS_S1', {"layout": "tweet", "slide_index": 1, "total": 4, "titulo": "",
    "body": "Voce usa o ChatGPT todo dia, mas sabe o que roda por baixo?", "site": "clubedoscisnes.com",
    "filename_base": "cdc_t2_ens_s1", "bg_prompt": "abstract glowing blue neural network on dark background, no text"})
go('ENS_S2', {"layout": "tweet", "slide_index": 2, "total": 4,
    "body": "LLM e um modelo de linguagem treinado com bilhoes de textos.", "site": "clubedoscisnes.com",
    "filename_base": "cdc_t2_ens_s2", "bg_prompt": ""})
print('DONE_TEST')
