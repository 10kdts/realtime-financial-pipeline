# Contrato do evento financeiro

| Campo | Tipo | Regra |
|---|---|---|
| `event_id` | string | obrigatório e único na origem |
| `account_id` | string | obrigatório; chave natural de partição |
| `occurred_at` | datetime UTC | instante da operação, em ISO 8601 |
| `received_at` | datetime UTC | instante de chegada, em ISO 8601 |
| `amount` | número | maior ou igual a zero |
| `type` | enum | `pix`, `card` ou `transfer` |
| `country` | string | `BR` ou `INT` no conjunto de demonstração |

## Compatibilidade

Novos campos opcionais podem ser adicionados sem quebrar consumidores. Renomear, remover ou alterar o tipo de um campo exige uma nova versão do contrato e período de convivência entre produtores e consumidores.

## Qualidade

Mensagens sem identificador, conta ou data válida devem seguir para uma fila de erro. Duplicidade é uma condição esperada e não um erro operacional. Atraso acima do limite deve ser mensurado e investigado antes de qualquer descarte.

