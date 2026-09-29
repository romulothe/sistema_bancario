import hashlib
import secrets


def gerar_hash_senha(senha):
    salt = secrets.token_hex(16)
    hash_senha = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt.encode(), 100_000)
    return f"{salt}${hash_senha.hex()}"


def verificar_senha(senha, hash_armazenado):
    salt, hash_hex = hash_armazenado.split("$")
    hash_senha = hashlib.pbkdf2_hmac("sha256", senha.encode(), salt.encode(), 100_000)
    return hash_senha.hex() == hash_hex