# Pipeline financeiro em tempo quase real

Eu construí este projeto para explorar um problema que aparece muito em pagamentos: o evento chega duplicado, atrasado ou fora de ordem, mas o processamento ainda precisa ser confiável. Em vez de esconder esses casos, gerei uma massa determinística que força cada um deles a acontecer.

O pipeline processa transações por tempo do evento, mantém um *watermark* de 90 segundos, elimina duplicidades e cria alertas por valor alto, velocidade e operação internacional. Eventos atrasados ficam em quarentena e podem ser reprocessados sem duplicar o resultado.

## O que este projeto mostra

- processamento idempotente com estado persistido;
- janelas móveis de cinco minutos por conta;
- tratamento explícito de eventos atrasados e fora de ordem;
- replay controlado e trilha operacional em SQLite;
- contrato de dados, consultas de monitoramento, testes e CI;
- arquitetura local simples, com Redpanda disponível para evoluir o fluxo para streaming real.

## Teste rápido

```bash
python -m realtime_finance.generate --rows 1200 --output data/sample/events.jsonl
python -m realtime_finance.processor --input data/sample/events.jsonl --db data/pipeline.db --replay
python -m unittest discover -s tests -v
```

Antes dos comandos, instale o pacote localmente com `python -m pip install -e .`.

Uma execução de referência com 1.204 mensagens resultou em 1.201 eventos únicos processados, três duplicidades identificadas, um evento atrasado e 53 alertas. O evento atrasado foi recuperado pelo replay.

## Decisões que tomei

Escolhi SQLite para deixar a demonstração reproduzível e sem dependências externas. O estado e as regras foram separados o suficiente para trocar esse armazenamento por PostgreSQL e alimentar o processador por Kafka/Redpanda. Também optei por não descartar silenciosamente eventos atrasados: eles ficam registrados para investigação e replay.

A visão completa está em [docs/architecture.md](docs/architecture.md), o formato das mensagens em [docs/data_contract.md](docs/data_contract.md) e o procedimento operacional em [docs/runbook.md](docs/runbook.md).

## Próximos passos

- consumir e publicar diretamente em tópicos Redpanda;
- adicionar métricas Prometheus e painel Grafana;
- particionar por `account_id` e testar concorrência;
- trocar regras fixas por um serviço de decisão versionado.

## Autor

Kaio Paiva

