CREATE TABLE clientes (
    id_cliente INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    cpf VARCHAR(11) NOT NULL UNIQUE,
    nome VARCHAR(150) NOT NULL,
    data_nascimento DATE NOT NULL,
    endereco VARCHAR(255) NOT NULL,
    senha_hash VARCHAR(255) NOT NULL
);

CREATE TABLE contas (
    id_conta INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_cliente INTEGER NOT NULL REFERENCES clientes (id_cliente),
    agencia VARCHAR(4) NOT NULL DEFAULT '0001',
    numero INTEGER NOT NULL,
    saldo NUMERIC(14, 2) NOT NULL DEFAULT 0 CHECK (saldo >= 0),
    limite NUMERIC(14, 2) NOT NULL DEFAULT 500,
    limite_saques INTEGER NOT NULL DEFAULT 3,
    UNIQUE (agencia, numero)
);

CREATE TABLE transacoes (
    id_transacao INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_conta INTEGER NOT NULL REFERENCES contas (id_conta),
    tipo VARCHAR(30) NOT NULL CHECK (tipo IN ('Deposito', 'Saque', 'Transferencia Enviada', 'Transferencia Recebida')),
    valor NUMERIC(14, 2) NOT NULL CHECK (valor > 0),
    data_hora TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_transacoes_conta_data
    ON transacoes (id_conta, data_hora);