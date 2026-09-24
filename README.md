# Sistema Bancário em Python (POO)

Sistema bancário de linha de comando desenvolvido em Python com **Programação Orientada a Objetos**. Permite cadastrar clientes, criar contas correntes e realizar depósitos, saques e consulta de extrato, tudo por um menu no terminal.

Projeto criado com foco em estudo, para praticar os pilares da POO em um cenário do mundo real.

## Funcionalidades

- **Novo usuário:** cadastro de cliente (pessoa física) com CPF, nome, data de nascimento e endereço, sem permitir CPF duplicado
- **Nova conta:** criação de conta corrente vinculada a um cliente, com agência `0001` e numeração sequencial
- **Listar contas:** exibe agência, número da conta e titular
- **Depositar:** aceita apenas valores positivos
- **Sacar:** valida saldo, limite de R$ 500,00 por saque e limite de 3 saques por conta
- **Extrato:** lista as movimentações e mostra o saldo atual

## Modelagem

| Classe | Papel |
|---|---|
| `Cliente` / `PessoaFisica` | Dados do cliente e suas contas (herança) |
| `Conta` / `ContaCorrente` | Regras de saldo, depósito e saque; a conta corrente adiciona limites (herança) |
| `Historico` | Guarda as transações de cada conta, com tipo, valor e data/hora |
| `Transacao` (abstrata) | Contrato que `Saque` e `Deposito` precisam cumprir |
| `Saque` / `Deposito` | Transações concretas que se registram na conta (polimorfismo) |

Conceitos praticados: herança, abstração (`ABC` e `@abstractmethod`), encapsulamento (atributos protegidos e `@property`) e polimorfismo.

## Como executar

Requisito: Python 3.8 ou superior. Não há dependências externas.

```bash
git clone https://github.com/romulothe/sistema_bancario.git
cd sistema_bancario
python desafio_sistema_bancario.py
```

Menu do sistema:

```
================ MENU ================
[d]   Depositar
[s]   Sacar
[e]   Extrato
[nc]  Nova conta
[lc]  Listar contas
[nu]  Novo usuário
[q]   Sair
```

Para começar, crie um usuário (`nu`), depois uma conta (`nc`) e então faça depósitos e saques.

## Limitações conhecidas

- Os dados ficam apenas em memória e são perdidos ao fechar o programa
- O limite de 3 saques considera todos os saques da conta, e não apenas os do dia
- Não há validação de formato para CPF e data de nascimento

Pontos que pretendo melhorar em próximas versões.

## Autor

**Rômulo Leite Brito**
[LinkedIn](https://www.linkedin.com/in/romulolebri) · [GitHub](https://github.com/romulothe)
