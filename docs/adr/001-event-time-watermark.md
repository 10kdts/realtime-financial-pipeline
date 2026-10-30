# ADR 001 — tempo do evento e watermark

## Status

Aceito.

## Contexto

Usar apenas a ordem de chegada distorce janelas quando a rede ou a origem atrasa uma mensagem.

## Decisão

As regras usam `occurred_at`. O maior tempo de evento observado, menos 90 segundos, define o watermark. Eventos mais antigos são registrados em quarentena para análise e replay.

## Consequências

A janela representa melhor o comportamento real e o atraso fica visível. Em contrapartida, o limite precisa ser acompanhado: curto demais aumenta a quarentena; longo demais aumenta estado e latência.

