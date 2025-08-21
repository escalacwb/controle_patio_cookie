# generate_hash_direto.py
import bcrypt
import sys

# Pede a senha
password = input("Digite a senha para gerar o hash: ")

try:
    # Codifica a senha para bytes
    password_bytes = password.encode('utf-8')

    # Gera o hash
    hashed_bytes = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    # Decodifica o hash de volta para uma string para salvar no banco
    hashed_string = hashed_bytes.decode('utf-8')

    print("\n--- HASH GERADO COM SUCESSO ---")
    print("Copie este valor e cole no campo 'password_hash' do seu banco de dados:")
    print(hashed_string)

except Exception as e:
    print(f"\nOcorreu um erro: {e}")
    print("Pode ser necessário instalar o bcrypt diretamente.")
    print("Execute: py -3.13 -m pip install bcrypt")
    sys.exit(1)