# Arquitetura

```text
produtor -> tópico transactions -> processador -> estado/deduplicação
                                    |       |
                                    |       +-> alertas
                                    +----------> quarentena -> replay
```

O exemplo executável lê JSONL para não exigir infraestrutura. A fronteira de entrada é deliberadamente simples: cada linha representa a mesma mensagem que seria consumida de um tópico Kafka/Redpanda.

## Fluxo

1. A mensagem é validada pelo contrato e consultada pelo `event_id`.
2. Um evento já registrado termina como duplicidade.
3. O maior `occurred_at` conhecido define o watermark, descontando 90 segundos.
4. Eventos anteriores ao watermark seguem para quarentena.
5. Eventos válidos atualizam a janela da conta, persistem o estado e geram zero ou mais alertas.
6. O replay lê a quarentena e grava somente o que ainda não existe no estado final.

## Garantias e limites

O projeto entrega processamento efetivamente único no armazenamento final por meio de chaves primárias e idempotência. Não promete *exactly once* entre sistemas distribuídos. Em produção, eu usaria partição por conta, *consumer groups*, observabilidade e uma estratégia transacional ou *outbox* para a publicação de alertas.

