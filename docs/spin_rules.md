# Regras Oficiais do Spin

## 1. Conceito do Spin
- Spin e o ato transacional de sortear um premio para um usuario em uma campanha ativa.
- Pode ser executado apenas quando o usuario esta autenticado, a campanha esta ativa e os requisitos de saldo/limites sao atendidos.
- Objetivo: debitar o custo do spin, executar o sorteio e retornar um premio (inclusive premio zero) de forma atomica e auditavel.

## 2. Custo do Spin
- Cada campanha define um custo fixo `spin_price` para cada execucao.
- O custo e debitado do saldo do usuario **antes** do sorteio ser realizado. Sem debito bem-sucedido nao existe spin.
- O debito gera uma transacao de tipo `DEBIT_SPIN` vinculada ao usuario/conta e ao spin.

## 3. Premios
- Estrutura de um premio: `id` (identificador unico), `name` (nome curto), `description` (texto opcional), `value` (numero monetario >= 0) e `probability` (percentual da distribuicao).
- Premios com `value = 0` sao validos para representar giro sem ganho financeiro.
- Exemplo de tabela de premios de uma campanha:
  - `id`: 1, `name`: "Nada", `value`: 0
  - `id`: 2, `name`: "Bonus Bronze", `value`: 5
  - `id`: 3, `name`: "Bonus Prata", `value`: 20
  - `id`: 4, `name`: "Bonus Ouro", `value`: 100

## 4. Probabilidades
- Cada premio possui uma probabilidade explicita, e a soma de todas deve ser **100%** para a campanha.
- A selecao do premio deve respeitar essas probabilidades e ser feita com aleatoriedade estatisticamente justa.
- Exemplo de distribuicao:
  - Nada: 55%
  - Bonus Bronze: 30%
  - Bonus Prata: 13%
  - Bonus Ouro: 2%

## 5. Saldo / Credito
- Saldo do usuario representa o credito disponivel para pagar o custo do spin.
- O saldo e debitado imediatamente ao iniciar o spin. Em caso de erro, o debito deve ser revertido.
- O premio sorteado e creditado na mesma conta do usuario apos o sorteio, junto com a gravacao do spin e das transacoes de debito/credito correspondentes.

## 6. Limites (conceitual)
- Limite diario de spins por usuario/campanha (ex.: `max_spins_per_day`).
- Limite diario de premio pago por usuario/campanha (ex.: `max_payout_per_day`).
- Implementacao e enforcement desses limites ficam para a Fase 2, mas ja devem ser considerados no contrato de erros e idempotencia.

## 7. Estados invalidos
- Saldo insuficiente: nao iniciar o spin e retornar erro adequado.
- Spin duplicado: detectar via `Idempotency-Key` e retornar 409 sem reexecutar o sorteio.
- Sistema indisponivel (banco, servico de randomizacao ou cache de limites): nao consumir saldo e retornar erro 503/500 com detalhe rastreavel.
