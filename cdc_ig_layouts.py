# -*- coding: utf-8 -*-
"""
cdc_ig_layouts.py — construtores de slide (1080x1080) para os carrosseis de IG do CDC.
Dois layouts, escolhidos pelo campo `layout` do /render-post:
  - "tweet"        -> vertente ENSINO IA (card estilo X/Twitter, claro). Slide 1 com imagem de contexto (data URI).
  - "illustration" -> vertente VENDAS (ilustracao flat/ludica, fundo escuro da marca; biblioteca SVG on-brand).

Cada funcao retorna UMA pagina HTML completa de 1080x1080 (sem escala), pronta pro Playwright screenshotar.
Fonte da verdade do visual: previews aprovados pelo usuario em 2026-07-15 (logo oficial cisne tangram).

Uso no servico (wrapper que ja existe faz o screenshot):
    from cdc_ig_layouts import render_slide_html
    html = render_slide_html(layout="tweet", slide_index=1, total=4,
                             categoria="", titulo="...", body="...",
                             image_data_uri="data:image/png;base64,....",  # so slide 1 do tweet
                             site="clubedoscisnes.com")
"""

import html as _html

# ---------------------------------------------------------------- assets
# Logo oficial (brandkit/clubedoscisnes-logo.svg) — cisne tangram teal/azul/navy.
LOGO = ('<svg viewBox="6 6 138 138">'
        '<polygon points="46,13 21,40 46,40" fill="#00C0C0"/>'
        '<polygon points="46,13 63,32 63,66 48,50 47,40" fill="#3070E0"/>'
        '<polygon points="45,53 49,53 63,66 54,80 27,107 27,71" fill="#0040A0"/>'
        '<polygon points="54,80 123,80 93,116" fill="#0040A0"/>'
        '<polygon points="54,80 54,135 30,107" fill="#00C0C0"/>'
        '<polygon points="54,80 111,135 54,135" fill="#3070E0"/></svg>')

_XBIRD = ('<svg class="xbird" viewBox="0 0 24 24" fill="#0F1419"><path d="M18.244 2.25h3.308'
          'l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08'
          'l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>')

_CHECK = ('<svg class="ck" viewBox="0 0 22 22"><path fill="#2563EB" d="M20.396 11c-.018-.646'
          '-.215-1.275-.57-1.816-.354-.54-.852-.972-1.438-1.246.223-.607.27-1.264.14-1.897'
          '-.131-.634-.437-1.218-.882-1.687-.47-.445-1.053-.75-1.687-.882-.633-.13-1.29-.083'
          '-1.897.14-.273-.587-.704-1.086-1.245-1.44S11.647 1.62 11 1.604c-.646.018-1.273.215'
          '-1.813.57-.54.354-.972.85-1.245 1.44-.608-.223-1.264-.27-1.898-.14-.633.13-1.216.437'
          '-1.686.882-.445.47-.75 1.053-.882 1.687-.13.633-.083 1.29.14 1.897-.587.274-1.087.705'
          '-1.44 1.246-.354.54-.551 1.17-.569 1.816.018.646.215 1.275.57 1.816.353.54.851.972'
          ' 1.438 1.246-.223.607-.27 1.264-.14 1.897.131.634.437 1.218.882 1.687.47.445 1.053.75'
          ' 1.687.882.633.13 1.29.083 1.897-.14.274.587.705 1.086 1.246 1.44.54.354 1.17.551'
          ' 1.816.569.646-.018 1.273-.215 1.813-.57.54-.354.972-.85 1.245-1.44.577.204 1.194.293'
          ' 1.812.259.618-.033 1.222-.19 1.771-.46.549-.27 1.033-.653 1.42-1.121.386-.469.667'
          '-1.012.825-1.594.157-.582.187-1.19.088-1.784.575-.291 1.05-.735 1.375-1.283.325-.548'
          '.485-1.18.462-1.816zm-8.567 4.638l-3.87-3.87 1.415-1.414 2.404 2.404 4.72-5.24 1.474'
          ' 1.33z"/></svg>')

_ICON_REPLY = '<svg viewBox="0 0 24 24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>'
_ICON_RT = '<svg viewBox="0 0 24 24"><path d="M17 1l4 4-4 4M3 11V9a4 4 0 014-4h14M7 23l-4-4 4-4M21 13v2a4 4 0 01-4 4H3"/></svg>'
_ICON_LIKE = '<svg viewBox="0 0 24 24"><path d="M12 21s-8-5.5-8-11a4 4 0 018-1 4 4 0 018 1c0 5.5-8 11-8 11z"/></svg>'

_FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com">'
          '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
          '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800;900'
          '&family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">')


def esc(s):
    return _html.escape(str(s or ""), quote=True)


def _nl2br(s):
    return esc(s).replace("\n", "<br>")


def _fs(text, sizes):
    """Dimensiona fonte pela quantidade de caracteres. sizes = [(maxlen, px), ...] crescente."""
    n = len(str(text or ""))
    for mx, px in sizes:
        if n <= mx:
            return px
    return sizes[-1][1]


# ---------------------------------------------------------------- TWEET (Ensino)
_TWEET_CSS = """
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1080px;overflow:hidden}
.slide{width:1080px;height:1080px;background:#fff;color:#0F1419;
 display:flex;flex-direction:column;padding:70px 68px 58px;position:relative;font-family:'Inter',sans-serif}
.xbird{position:absolute;top:64px;right:68px;width:60px;height:60px;opacity:.9}
.hd{display:flex;align-items:center;gap:22px;margin-bottom:14px}
.av{width:112px;height:112px;border-radius:50%;background:#fff;border:1px solid #E1E8ED;flex-shrink:0;
 display:flex;align-items:center;justify-content:center;box-shadow:0 2px 10px rgba(0,0,0,.06)}
.av svg{width:80px;height:80px}
.who{display:flex;flex-direction:column;gap:3px}
.nm{display:flex;align-items:center;gap:9px;font-size:36px;font-weight:800;color:#0F1419;line-height:1}
.ck{width:32px;height:32px}.hn{font-size:30px;color:#536471;font-weight:400;line-height:1}
.tw{font-size:52px;line-height:1.32;font-weight:500;color:#0F1419;letter-spacing:-.5px;margin-top:20px}
.tw .em{color:#2563EB;font-weight:600}
/* slides sem imagem (2..N): bloco de texto centralizado verticalmente entre header e footer */
.mid{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:flex-start}
.mid .tw{margin-top:0}
.img{margin-top:34px;border-radius:26px;overflow:hidden;border:1px solid #E1E8ED;height:430px;position:relative;background:#0B1629}
.img img{width:100%;height:100%;object-fit:cover}
.thread{display:inline-flex;align-items:center;gap:9px;align-self:flex-start;margin-top:26px;
 background:#EFF5FF;color:#2563EB;font-size:22px;font-weight:700;padding:9px 20px;border-radius:100px}
.thread .dot{width:9px;height:9px;border-radius:50%;background:#2563EB}
.ft{margin-top:auto;padding-top:30px;border-top:1px solid #EFF3F4}
.time{font-size:24px;color:#536471;font-weight:400;margin-bottom:26px}.time b{color:#0F1419;font-weight:600}
.eng{display:flex;align-items:center;gap:70px}
.eng .it{display:flex;align-items:center;gap:14px;color:#536471;font-size:26px;font-weight:500}
.eng .it svg{width:34px;height:34px;stroke:#536471;fill:none;stroke-width:2.1}
.eng .it.like svg{fill:#F91880;stroke:#F91880}.eng .it.like{color:#F91880}
.cnt{position:absolute;bottom:58px;right:68px;font-size:24px;font-weight:800;color:#AAB8C2;letter-spacing:1px}
.big-cta{margin-top:30px;align-self:flex-start;display:inline-flex;align-items:center;gap:14px;
 background:#2563EB;color:#fff;font-size:30px;font-weight:800;padding:22px 44px;border-radius:100px;
 box-shadow:0 12px 34px rgba(37,99,235,.34);letter-spacing:.3px}
"""


def _tweet_header(handle):
    return ('<div class="hd"><div class="av">%s</div><div class="who">'
            '<div class="nm">Clube dos Cisnes%s</div>'
            '<div class="hn">%s</div></div></div>') % (LOGO, _CHECK, esc(handle))


def _eng(reply, rt, like, show_rt=True):
    rtblock = ('<div class="it">%s%s</div>' % (_ICON_RT, esc(rt))) if show_rt else ''
    return ('<div class="eng"><div class="it">%s%s</div>%s'
            '<div class="it like">%s%s</div></div>') % (_ICON_REPLY, esc(reply), rtblock, _ICON_LIKE, esc(like))


def slide_tweet(slide_index, total, titulo, body, image_data_uri=None,
                handle="@clubedoscisnes_", when="", site="clubedoscisnes.com", cta_url=None):
    """Um slide do carrossel Ensino no estilo tweet/thread. slide_index 1..total."""
    is_cover = (slide_index == 1)
    is_cta = (slide_index == total)
    text = _nl2br(body if body else titulo)
    parts = ['<div class="slide">', _XBIRD, _tweet_header(handle)]

    mid = []
    if not is_cover:
        mid.append('<div class="thread"><span class="dot"></span>Thread &middot; %d de %d</div>'
                   % (slide_index, total))
    raw = body if body else titulo
    twfs = _fs(raw, [(90, 52), (150, 46), (230, 40), (999, 34)])
    mid.append('<div class="tw" style="font-size:%dpx">%s</div>' % (twfs, text))

    if is_cover and image_data_uri:
        mid.append('<div class="img"><img src="%s" alt=""></div>' % esc(image_data_uri))

    if is_cta:
        mid.append('<a class="big-cta">%s &rarr;</a>' % esc(site))

    if is_cover:
        # capa: texto no topo + imagem de contexto logo abaixo (fluxo normal)
        parts.extend(mid)
    else:
        # demais slides: bloco de texto centralizado verticalmente entre header e footer
        parts.append('<div class="mid">%s</div>' % "".join(mid))

    # footer
    footer_time = ('<b>Clube dos Cisnes</b> &middot; IA e tecnologia para o seu neg&oacute;cio'
                   if is_cta else ('%s &middot; Instagram' % (esc(when) if when else 'agora')))
    eng = _eng("128", "340", "2,1 mil", show_rt=not is_cta)
    parts.append('<div class="ft"><div class="time">%s</div>%s</div>' % (footer_time, eng))
    parts.append('<div class="cnt">%d / %d</div>' % (slide_index, total))
    parts.append('</div>')

    return ("<!DOCTYPE html><html lang='pt-BR'><head><meta charset='UTF-8'>%s"
            "<style>%s</style></head><body>%s</body></html>") % (_FONTS, _TWEET_CSS, "".join(parts))


# ---------------------------------------------------------------- ILLUSTRATION (Vendas)
# Biblioteca de ilustracoes flat on-brand (fundo escuro). Escolhida por indice/tema.
ILLUS = {
    "phone_night": ('<svg width="620" height="440" viewBox="0 0 620 440">'
        '<circle cx="150" cy="120" r="70" fill="#FBBF24"/><circle cx="126" cy="106" r="60" fill="#0B1629"/>'
        '<circle cx="500" cy="80" r="7" fill="#38BDF8"/><circle cx="540" cy="130" r="5" fill="#00C0C0"/><circle cx="470" cy="150" r="4" fill="#FBBF24"/>'
        '<rect x="220" y="70" width="230" height="330" rx="34" fill="#fff"/><rect x="238" y="92" width="194" height="286" rx="20" fill="#EAF3FF"/>'
        '<rect x="238" y="92" width="194" height="58" rx="20" fill="#22C55E"/><rect x="238" y="130" width="194" height="20" fill="#22C55E"/>'
        '<circle cx="270" cy="121" r="15" fill="#fff"/><rect x="296" y="112" width="90" height="9" rx="4" fill="rgba(255,255,255,.85)"/>'
        '<rect x="296" y="128" width="60" height="7" rx="3" fill="rgba(255,255,255,.6)"/>'
        '<rect x="256" y="178" width="120" height="40" rx="14" fill="#fff"/><rect x="270" y="192" width="80" height="10" rx="5" fill="#9db4d6"/>'
        '<rect x="300" y="234" width="118" height="40" rx="14" fill="#2563EB"/><rect x="316" y="248" width="80" height="10" rx="5" fill="rgba(255,255,255,.85)"/>'
        '<circle cx="288" cy="316" r="8" fill="#38BDF8"/><circle cx="312" cy="316" r="8" fill="#38BDF8"/><circle cx="336" cy="316" r="8" fill="#38BDF8"/></svg>'),
    "clock_lost": ('<svg width="560" height="300" viewBox="0 0 560 300">'
        '<circle cx="120" cy="150" r="92" fill="rgba(251,113,133,.16)"/><circle cx="120" cy="150" r="66" fill="#0f2038" stroke="#FB7185" stroke-width="8"/>'
        '<line x1="120" y1="150" x2="120" y2="104" stroke="#fff" stroke-width="8" stroke-linecap="round"/>'
        '<line x1="120" y1="150" x2="156" y2="166" stroke="#FB7185" stroke-width="8" stroke-linecap="round"/>'
        '<path d="M300 150 L430 150" stroke="#33456b" stroke-width="8" stroke-dasharray="4 18" stroke-linecap="round"/>'
        '<polygon points="430,132 466,150 430,168" fill="#5b6f97"/><rect x="470" y="96" width="66" height="120" rx="16" fill="#38BDF8"/>'
        '<rect x="482" y="110" width="42" height="70" rx="8" fill="#0B1629"/><circle cx="503" cy="196" r="7" fill="#0B1629"/>'
        '<text x="503" y="66" font-family="Montserrat" font-size="34" font-weight="900" fill="#22C55E" text-anchor="middle">&#10003;</text></svg>'),
    "robot_24h": ('<svg width="560" height="300" viewBox="0 0 560 300">'
        '<rect x="180" y="70" width="200" height="170" rx="34" fill="#2563EB"/><rect x="206" y="102" width="148" height="80" rx="18" fill="#0B1629"/>'
        '<circle cx="245" cy="142" r="17" fill="#38BDF8"/><circle cx="315" cy="142" r="17" fill="#38BDF8"/><rect x="268" y="136" width="24" height="12" rx="6" fill="#0B1629"/>'
        '<line x1="280" y1="70" x2="280" y2="46" stroke="#fff" stroke-width="8"/><circle cx="280" cy="42" r="12" fill="#FBBF24"/>'
        '<rect x="238" y="200" width="84" height="20" rx="10" fill="rgba(255,255,255,.5)"/>'
        '<rect x="382" y="96" width="150" height="60" rx="18" fill="#12325f"/><circle cx="410" cy="126" r="7" fill="#38BDF8"/><circle cx="434" cy="126" r="7" fill="#38BDF8"/><circle cx="458" cy="126" r="7" fill="#38BDF8"/>'
        '<rect x="30" y="170" width="150" height="60" rx="18" fill="#0f3324"/><path d="M64 200 l14 14 26 -30" stroke="#22C55E" stroke-width="9" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="470" cy="215" r="42" fill="#FBBF24"/><text x="470" y="228" font-family="Montserrat" font-size="30" font-weight="900" fill="#0B1629" text-anchor="middle">24h</text></svg>'),
    "growth": ('<svg width="560" height="300" viewBox="0 0 560 300">'
        '<rect x="70" y="60" width="420" height="200" rx="24" fill="#0f2038"/>'
        '<polyline points="110,220 200,180 270,205 350,120 450,90" fill="none" stroke="#38BDF8" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>'
        '<circle cx="450" cy="90" r="16" fill="#00C0C0"/><polygon points="430,110 450,70 470,110" fill="#22C55E"/>'
        '<rect x="110" y="235" width="340" height="6" rx="3" fill="rgba(255,255,255,.15)"/></svg>'),
    "gears": ('<svg width="560" height="300" viewBox="0 0 560 300">'
        '<g fill="#2563EB"><circle cx="230" cy="150" r="80"/></g><circle cx="230" cy="150" r="34" fill="#0B1629"/>'
        '<g fill="#38BDF8"><circle cx="360" cy="200" r="52"/></g><circle cx="360" cy="200" r="22" fill="#0B1629"/>'
        '<circle cx="470" cy="120" r="34" fill="#00C0C0"/><circle cx="470" cy="120" r="14" fill="#0B1629"/>'
        '<text x="230" y="164" font-family="Montserrat" font-size="44" font-weight="900" fill="#fff" text-anchor="middle">IA</text></svg>'),
    "chat": ('<svg width="560" height="300" viewBox="0 0 560 300">'
        '<rect x="110" y="60" width="230" height="140" rx="28" fill="#2563EB"/><polygon points="160,196 160,240 208,196" fill="#2563EB"/>'
        '<circle cx="180" cy="130" r="13" fill="#fff"/><circle cx="230" cy="130" r="13" fill="#fff"/><circle cx="280" cy="130" r="13" fill="#fff"/>'
        '<rect x="300" y="112" width="150" height="92" rx="24" fill="#12325f"/><polygon points="398,200 398,236 356,200" fill="#12325f"/>'
        '<rect x="322" y="142" width="88" height="11" rx="5" fill="#38BDF8"/><rect x="322" y="164" width="58" height="11" rx="5" fill="#7f9fd0"/>'
        '<circle cx="440" cy="92" r="30" fill="#22C55E"/><path d="M427 92 l9 9 16 -19" stroke="#fff" stroke-width="7" fill="none" stroke-linecap="round" stroke-linejoin="round"/></svg>'),
    "target": ('<svg width="560" height="300" viewBox="0 0 560 300">'
        '<circle cx="250" cy="155" r="100" fill="none" stroke="#1e3a6b" stroke-width="18"/>'
        '<circle cx="250" cy="155" r="64" fill="none" stroke="#2563EB" stroke-width="18"/><circle cx="250" cy="155" r="28" fill="#38BDF8"/>'
        '<line x1="380" y1="55" x2="258" y2="150" stroke="#FBBF24" stroke-width="11" stroke-linecap="round"/>'
        '<polygon points="258,150 292,132 286,168" fill="#FBBF24"/><polygon points="380,55 352,60 372,82" fill="#FBBF24"/></svg>'),
    "maps": ('<svg width="560" height="300" viewBox="0 0 560 300">'
        '<ellipse cx="280" cy="250" rx="70" ry="18" fill="rgba(56,189,248,.18)"/>'
        '<path d="M280 60 C214 60 170 108 170 168 C170 232 280 268 280 268 C280 268 390 232 390 168 C390 108 346 60 280 60 Z" fill="#2563EB"/>'
        '<circle cx="280" cy="162" r="42" fill="#0B1629"/><circle cx="280" cy="162" r="20" fill="#38BDF8"/></svg>'),
    "store": ('<svg width="560" height="300" viewBox="0 0 560 300">'
        '<rect x="150" y="130" width="260" height="130" rx="10" fill="#12325f"/>'
        '<path d="M140 90 L420 90 L400 135 L160 135 Z" fill="#2563EB"/>'
        '<rect x="150" y="130" width="45" height="14" fill="#38BDF8"/><rect x="230" y="130" width="45" height="14" fill="#00C0C0"/><rect x="310" y="130" width="45" height="14" fill="#38BDF8"/>'
        '<rect x="250" y="180" width="60" height="80" rx="6" fill="#0B1629"/><circle cx="300" cy="222" r="4" fill="#FBBF24"/></svg>'),
}
_ILLUS_KEYS = list(ILLUS.keys())

import re as _re
# match de palavra-chave (pt-BR, minusculo) -> ilustracao mais relevante ao tema do slide
KEYWORD_MAP = [
    (r'whats|chatbot|chat|atend|mensag|convers|direct|duvida|d[uú]vida|responder|sac', 'chat'),
    (r'lead|tr[aá]fego|an[uú]ncio|\bads\b|convers|roi|campanha|google ads|meta ads|impuls', 'target'),
    (r'google meu neg|maps|mapa|local|no google|perto|bairro|encontr|busca local|seo local', 'maps'),
    (r'loja|varejo|roupa|moda|vitrine|produto|estoque|e-?commerce', 'store'),
    (r'agenda|reserva|marca[cç]|hor[aá]rio|24 ?h|24 ?hora|noite|dorme|sozinho|autom[aá]tico', 'robot_24h'),
    (r'autom|tarefa|processo|sistema|repetit|integra|fluxo|workflow', 'gears'),
    (r'cresc|resultado|aumentar|vend|receita|ranking|topo|escala|fatur', 'growth'),
    (r'atras|perde|perda|rel[oó]gio|tempo|espera|demora', 'clock_lost'),
    (r'agente|assistente|rob[oô]|\bia\b|intelig', 'robot_24h'),
]


def _pick_by_text(text, offset=0):
    """Escolhe a ilustracao pelo tema (keyword). Se nada casar, cai no hash (variado)."""
    t = str(text or "").lower()
    for pat, key in KEYWORD_MAP:
        if _re.search(pat, t):
            return ILLUS.get(key) or _pick_illus(text, offset)
    return _pick_illus(text, offset)

_ILL_CSS = """
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1080px;overflow:hidden}
.slide{width:1080px;height:1080px;position:relative;overflow:hidden;font-family:'Inter',sans-serif;display:flex;flex-direction:column;color:#fff}
.blob{position:absolute;border-radius:50%;z-index:0}
.brand{display:flex;align-items:center;gap:16px;z-index:5}
.brand .lg{width:70px;height:70px;border-radius:18px;background:#fff;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(0,0,0,.35)}
.brand .lg svg{width:48px;height:48px}
.brand .bn{font-family:'Montserrat';font-size:27px;font-weight:800;color:#fff;letter-spacing:-.3px;line-height:1}
.brand .bt{font-size:15px;color:#7f92b3;font-weight:600;letter-spacing:2px;text-transform:uppercase;margin-top:4px}
.tagpill{margin-left:auto;background:#00C0C0;color:#04202a;font-family:'Montserrat';font-weight:800;font-size:19px;letter-spacing:2px;padding:11px 26px;border-radius:100px}
.eyebrow{display:inline-flex;align-items:center;gap:12px;font-family:'Montserrat';font-weight:800;font-size:24px;letter-spacing:3px;text-transform:uppercase;color:#38BDF8}
.eyebrow .b{width:16px;height:16px;border-radius:50%;background:#38BDF8}
.s1{background:radial-gradient(120% 90% at 80% 0%,#12325f 0%,#0B1629 55%,#080f1d 100%);padding:70px 72px}
.s1 .top{display:flex;align-items:center;width:100%}
.s1 .illu{flex:1 1 auto;min-height:0;max-height:400px;display:flex;align-items:center;justify-content:center;z-index:3;margin:8px 0;overflow:hidden}
.s1 .illu svg{max-height:100%;max-width:100%;height:auto;width:auto}
.s1 h1{font-family:'Montserrat';font-weight:900;font-size:82px;line-height:1.02;color:#fff;letter-spacing:-2px;z-index:3;text-transform:uppercase}
.s1 h1 .hl{color:#38BDF8}
.s1 .swipe{display:flex;align-items:center;gap:14px;margin-top:26px;z-index:3;font-size:24px;font-weight:600;color:#8ea3c4}
.s1 .swipe .arw{width:52px;height:52px;border-radius:50%;background:#2563EB;color:#fff;display:flex;align-items:center;justify-content:center;font-size:26px;box-shadow:0 8px 22px rgba(37,99,235,.5)}
.sc{background:#0B1629;padding:74px 72px}
.sc .illu{margin:16px 0 6px;display:flex;align-items:center;justify-content:center;z-index:3}
.sc h2{font-family:'Montserrat';font-weight:900;font-size:60px;line-height:1.08;color:#fff;letter-spacing:-1.2px;margin-top:26px;z-index:3}
.sc p{font-size:34px;line-height:1.5;color:#aebdd6;font-weight:500;margin-top:24px;z-index:3;max-width:900px}
.sc p b{color:#38BDF8;font-weight:800}
.foot{margin-top:auto;display:flex;align-items:center;gap:14px;z-index:5;padding-top:30px;border-top:1px solid rgba(255,255,255,.08)}
.foot .lg{width:48px;height:48px;border-radius:13px;background:#fff;display:flex;align-items:center;justify-content:center}
.foot .lg svg{width:34px;height:34px}
.foot span{font-family:'Montserrat';font-weight:800;font-size:22px;color:#fff}
.foot .site{margin-left:auto;font-size:22px;color:#6f82a3;font-weight:600}
.num{position:absolute;top:74px;right:72px;font-family:'Montserrat';font-weight:900;font-size:30px;color:rgba(255,255,255,.14);z-index:5}
.s4{background:linear-gradient(150deg,#2563EB 0%,#1D4ED8 55%,#0B1629 100%);padding:80px 72px;align-items:flex-start;justify-content:center}
.s4 .lgbig{width:120px;height:120px;border-radius:30px;background:#fff;display:flex;align-items:center;justify-content:center;z-index:3;margin-bottom:38px;box-shadow:0 14px 40px rgba(0,0,0,.4)}
.s4 .lgbig svg{width:82px;height:82px}
.s4 .eye{font-family:'Montserrat';font-weight:800;font-size:24px;letter-spacing:4px;text-transform:uppercase;color:#bfe0ff;z-index:3}
.s4 h1{font-family:'Montserrat';font-weight:900;font-size:78px;line-height:1.04;letter-spacing:-2px;color:#fff;text-transform:uppercase;margin-top:20px;z-index:3;max-width:920px}
.s4 .btn{margin-top:44px;display:inline-flex;align-items:center;gap:16px;background:#fff;color:#1D4ED8;font-family:'Montserrat';font-weight:900;font-size:34px;padding:26px 54px;border-radius:100px;z-index:3;box-shadow:0 20px 50px rgba(0,0,0,.35)}
.s4 .sub{margin-top:26px;font-size:26px;color:rgba(255,255,255,.8);font-weight:500;z-index:3}
"""


def _pick_illus(seed, offset=0):
    h = 0
    for ch in str(seed):
        h = (h * 31 + ord(ch)) & 0xffffffff
    return ILLUS[_ILLUS_KEYS[(h + offset) % len(_ILLUS_KEYS)]]


def slide_illustration(slide_index, total, categoria, titulo, body,
                       site="clubedoscisnes.com", tag="VENDAS", seed=""):
    """Um slide do carrossel Vendas, ilustracao flat, fundo escuro. slide_index 1..total."""
    logo = LOGO
    is_cover = (slide_index == 1)
    is_cta = (slide_index == total)
    seed = seed or titulo

    if is_cover:
        illus = _pick_by_text(titulo, 0)
        h1 = esc(titulo).upper()
        fs = _fs(titulo, [(24, 82), (38, 68), (56, 56), (999, 48)])
        return ("<!DOCTYPE html><html lang='pt-BR'><head><meta charset='UTF-8'>%s<style>%s</style></head><body>"
                "<div class='slide s1'>"
                "<div class='blob' style='width:340px;height:340px;background:rgba(0,192,192,.16);top:-90px;right:-70px'></div>"
                "<div class='blob' style='width:200px;height:200px;background:rgba(251,191,36,.14);bottom:120px;left:-60px'></div>"
                "<div class='blob' style='width:70px;height:70px;background:rgba(52,211,153,.5);top:360px;right:120px'></div>"
                "<div class='top'><div class='brand'><div class='lg'>%s</div><div>"
                "<div class='bn'>Clube dos Cisnes</div><div class='bt'>Solu&ccedil;&otilde;es em IA</div></div></div>"
                "<div class='tagpill'>%s</div></div>"
                "<div class='illu'>%s</div>"
                "<h1 style='font-size:%dpx'>%s</h1>"
                "<div class='swipe'><span class='arw'>&rarr;</span> arraste e descubra a solu&ccedil;&atilde;o</div>"
                "</div></body></html>") % (_FONTS, _ILL_CSS, logo, esc(tag), illus, fs, h1)

    if is_cta:
        fs = _fs(titulo, [(26, 78), (42, 64), (70, 52), (999, 44)])
        return ("<!DOCTYPE html><html lang='pt-BR'><head><meta charset='UTF-8'>%s<style>%s</style></head><body>"
                "<div class='slide s4'>"
                "<div class='blob' style='width:380px;height:380px;background:rgba(56,189,248,.2);top:-110px;right:-100px'></div>"
                "<div class='blob' style='width:160px;height:160px;background:rgba(0,192,192,.3);bottom:90px;left:-50px'></div>"
                "<div class='lgbig'>%s</div>"
                "<div class='eye'>Clube dos Cisnes</div>"
                "<h1 style='font-size:%dpx'>%s</h1>"
                "<a class='btn'>%s &rarr;</a>"
                "<div class='sub'>%s</div>"
                "</div></body></html>") % (_FONTS, _ILL_CSS, logo, fs, esc(titulo).upper(), esc(site),
                                           _nl2br(body) if body else "Fale com a gente e monte seu atendimento com IA.")

    # content slide (2..total-1)
    illus = _pick_by_text((categoria or "") + " " + (titulo or "") + " " + (body or ""), slide_index)
    eyeb = esc(categoria) if categoria else ("Ponto %d" % slide_index)
    h2fs = _fs(titulo, [(28, 60), (46, 50), (70, 42), (999, 36)])
    pfs = _fs(body, [(110, 34), (180, 30), (999, 26)])
    return ("<!DOCTYPE html><html lang='pt-BR'><head><meta charset='UTF-8'>%s<style>%s</style></head><body>"
            "<div class='slide sc'>"
            "<div class='blob' style='width:300px;height:300px;background:rgba(56,189,248,.12);bottom:-100px;left:-70px'></div>"
            "<div class='num'>%02d</div>"
            "<div class='eyebrow'><span class='b'></span>%s</div>"
            "<div class='illu'>%s</div>"
            "<h2 style='font-size:%dpx'>%s</h2>"
            "<p style='font-size:%dpx'>%s</p>"
            "<div class='foot'><div class='lg'>%s</div><span>Clube dos Cisnes</span><span class='site'>%s</span></div>"
            "</div></body></html>") % (_FONTS, _ILL_CSS, slide_index, eyeb.upper(), illus,
                                       h2fs, esc(titulo), pfs, _nl2br(body), logo, esc(site))


# ---------------------------------------------------------------- dispatcher
def render_slide_html(layout, slide_index, total=4, categoria="", titulo="", body="",
                      image_data_uri=None, site="clubedoscisnes.com", when="", tag="VENDAS", seed=""):
    layout = (layout or "").lower()
    if layout == "tweet":
        return slide_tweet(slide_index, total, titulo, body, image_data_uri=image_data_uri,
                           when=when, site=site)
    if layout == "illustration":
        return slide_illustration(slide_index, total, categoria, titulo, body, site=site, tag=tag, seed=seed)
    raise ValueError("layout desconhecido: %r (use 'tweet' ou 'illustration')" % layout)
