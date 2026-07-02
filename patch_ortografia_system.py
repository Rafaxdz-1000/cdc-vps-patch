import sys
P = '/opt/cdc/claude-svc/app.py'
s = open(P, encoding='utf-8').read()
if 'ORTOGRAFIA' in s:
    print('JA_APLICADO')
    sys.exit(0)
if 'def run_claude' not in s:
    print('ERRO_MARKER_NAO_ENCONTRADO')
    sys.exit(1)
LINE = 'SYSTEM = SYSTEM + " ORTOGRAFIA OBRIGATÓRIA (regra inviolável): escreva SEMPRE em português do Brasil com acentuação e pontuação completas e corretas — todos os acentos (á é í ó ú, â ê ô), o til (ã, õ), a crase (à) e a cedilha (ç). Linguagem simples e acessível NÃO significa escrever sem acento, e NUNCA é para escrever no estilo WhatsApp. Mesmo que o título, as fontes ou o conteúdo-base venham SEM acento, o SEU texto DEVE ter acentuação impecável (ex.: não, você, é, inteligência, ação, informação, robô, década, história, matemática, cérebro, também, além, análise, português, saúde). Texto com acentos faltando é ERRO GRAVE e reprova o resultado."'
s = s.replace('def run_claude', LINE + chr(10) + chr(10) + 'def run_claude', 1)
open(P, 'w', encoding='utf-8').write(s)
print('APLICADO ok=' + str('ORTOGRAFIA' in open(P, encoding='utf-8').read()))
