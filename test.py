import urllib.request, json, urllib.error

PROMPT = (
    "Voce e designer de conteudo do Clube dos Cisnes. "
    "Gere um carrossel de Instagram de 3 slides sobre 'IA no trabalho'. "
    "Responda SOMENTE com JSON puro no formato "
    '{"slides":[{"titulo":"...","texto":"..."}],"legenda":"...","hashtags":["..."]}.'
)
body = json.dumps({
    "contents": [{"parts": [{"text": PROMPT}]}],
    "required_fields": [],
}).encode()
req = urllib.request.Request(
    "http://localhost:5002/generate-article", body,
    {"content-type": "application/json"},
)
try:
    r = urllib.request.urlopen(req, timeout=600)
    print("STATUS", r.status)
    print(r.read().decode()[:700])
except urllib.error.HTTPError as e:
    print("HTTPERROR", e.code)
    print(e.read().decode()[:700])
