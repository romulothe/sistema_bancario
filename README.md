# Sistema Bancário em Python (POO + PostgreSQL)

Sistema bancário de linha de comando desenvolvido em Python com **Programação Orientada a Objetos**, com persistência de dados em **PostgreSQL**. Permite cadastrar clientes, criar contas correntes e realizar depósitos, saques e consulta de extrato, tudo por um menu no terminal.

Projeto criado com foco em estudo e portfólio, evoluindo de um sistema puramente em memória para uma aplicação com banco de dados real.

## Funcionalidades

- **Novo usuário:** cadastro de cliente (pessoa física) com CPF, nome, data de nascimento e endereço, sem permitir CPF duplicado
- **Nova conta:** criação de conta corrente vinculada a um cliente, com agência `0001` e numeração sequencial (sem duplicidade)
- **Listar contas:** exibe agência, número da conta e titular, consultando o banco de dados
- **Depositar:** aceita apenas valores positivos
- **Sacar:** valida saldo, limite de R$ 500,00 por saque e limite de 3 saques **por dia** (não por conta)
- **Extrato:** lista as movimentações com data/hora de cada transação e mostra o saldo atual

## Arquitetura

| Arquivo | Papel |
|---|---|
| `desafio_sistema_bancario.py` | Menu, fluxo do programa e regras de negócio |
| `repositorio.py` | Funções de acesso ao banco de dados (inserir/buscar clientes, contas e transações) |
| `conexao.py` | Abre a conexão com o PostgreSQL usando as credenciais do `.env` |
| `001_create_tables.sql` | Script SQL de criação das tabelas `clientes`, `contas` e `transacoes` |

Todos os dados (clientes, contas e transações) são persistidos em um banco **PostgreSQL**, substituindo a versão anterior que guardava tudo apenas em listas na memória.

## Como executar

Requisitos: Python 3.8+ e um PostgreSQL rodando localmente (ou acessível pela rede).

1. Clone o repositório:
```bash
   git clone https://github.com/romulothe/sistema_bancario.git
   cd sistema_bancario
```

2. Instale as dependências:
```bash
   pip install -r requirements.txt
```

3. Crie o banco de dados e as tabelas:
```bash
   psql -U postgres -c "CREATE DATABASE sistema_bancario;"
   psql -U postgres -d sistema_bancario -f 001_create_tables.sql
```

4. Copie o `.env.example` para `.env` e preencha com suas credenciais reais:
```bash
   cp .env.example .env
```

5. Execute o programa:
```bash
   python desafio_sistema_bancario.py
```

Menu do sistema:

```
================ MENU ================
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuário
[q] Sair
```


Para começar, crie um usuário (`nu`), depois uma conta (`nc`) e então faça depósitos e saques.

## Limitações conhecidas

- Não há validação de formato para CPF
- O programa ainda contém, no arquivo principal, as classes originais em memória (mantidas por ora como referência do design orientado a objetos, sem uso pelo fluxo atual)

Pontos que pretendo melhorar em próximas versões.

## Autor

**Rômulo Leite Brito**
[LinkedIn](https://www.linkedin.com/in/romulolebri) · [GitHub](https://github.com/romulothe)