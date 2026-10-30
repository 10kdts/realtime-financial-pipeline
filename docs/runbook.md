# Runbook — atraso ou acúmulo no pipeline financeiro

## Objetivo

Restabelecer o processamento e preservar eventos quando a latência ou a quarentena ultrapassar o comportamento esperado.

## Sintomas

- aumento contínuo de eventos atrasados;
- diferença crescente entre mensagens recebidas e processadas;
- alertas deixam de ser produzidos;
- reinícios repetidos do consumidor.

## Impacto

Alertas financeiros podem chegar tarde. As transações permanecem disponíveis para replay, mas o tempo de resposta operacional piora.

## Diagnóstico

1. Confirmar saúde do broker e do consumidor.
2. Comparar horário da origem, `occurred_at` e `received_at`.
3. Consultar volume, atraso máximo e motivos de alerta com `sql/monitoring.sql`.
4. Verificar erros de schema, armazenamento e reinícios.
5. Validar se o aumento é real ou causado por relógio incorreto na origem.

## Mitigação

1. Pausar o replay se ele estiver disputando recursos com o fluxo principal.
2. Escalar consumidores mantendo a mesma chave de partição.
3. Corrigir a origem ou a capacidade antes de ampliar o watermark.
4. Executar o replay em lotes e acompanhar duplicidades e latência.

## Validação

- o atraso deixa de crescer por pelo menos 15 minutos;
- novas mensagens são processadas dentro do objetivo de serviço;
- o replay não cria duplicidades;
- a quarentena retorna ao patamar normal.

## Rollback

Se uma mudança piorar o processamento, restaurar a versão anterior do consumidor, manter a quarentena intacta e interromper o replay até nova análise.

## Escalonamento

Acionar engenharia de dados quando o acúmulo persistir após escala. Acionar a equipe de origem quando timestamps ou schema estiverem inválidos. Envolver risco/fraude se os alertas críticos estiverem atrasados.

