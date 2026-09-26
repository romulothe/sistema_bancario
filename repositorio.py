from conexao import conectar


def inserir_cliente(cpf, nome, data_nascimento, endereco):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO clientes (
                    cpf,
                    nome,
                    data_nascimento,
                    endereco
                )
                VALUES (%s, %s, %s, %s)
                """,
                (cpf, nome, data_nascimento, endereco),
            )
        conn.commit()


def buscar_cliente_por_cpf(cpf):
    with conectar() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    id_cliente,

                    cpf,

                    nome,

                    data_nascimento,

                    endereco

                FROM clientes

                WHERE cpf = %s
                """,
                (cpf,),
            )
            return cur.fetchone()