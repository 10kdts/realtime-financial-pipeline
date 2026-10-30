# Plano do projeto

## Objetivo

Criar uma demonstração reproduzível de processamento financeiro orientado a eventos, com foco em confiabilidade e operação.

## Entregas

- [x] gerador determinístico de transações;
- [x] deduplicação e estado persistido;
- [x] watermark e quarentena de atraso;
- [x] regras de alerta em janela móvel;
- [x] replay idempotente;
- [x] testes automatizados;
- [x] documentação técnica e operacional;
- [x] infraestrutura local de streaming;
- [x] workflow de integração contínua.

## Critérios de aceite

Uma execução repetida não pode duplicar eventos ou alertas. O cenário de teste deve conter duplicidade e atraso, e o replay precisa recuperar o evento em quarentena.

