from autenticacao import gerar_hash_senha
from repositorio import atualizar_senha

cpf = input("Informe o CPF do cliente: ")
senha = input("Informe a nova senha: ")

senha_hash = gerar_hash_senha(senha)
atualizar_senha(cpf, senha_hash)

print("\nSenha atualizada com sucesso!")