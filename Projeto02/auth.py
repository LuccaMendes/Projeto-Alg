usuarios = [
    {"login": "admin", "senha": "123", "tipo": "ADM"},
    {"login": "cliente1", "senha": "123", "tipo": "CLIENTE"}
]

def cadastrar_usuario():

    novo_login = input("Login: ")
    if len(novo_login) == 0:
        print("Login não pode ser vazio!")
        return False

    for u in usuarios:
        if u["login"] == novo_login:
            print("Login já existe!")
            return False

    nova_senha = input("Senha: ")
    if len(nova_senha) == 0:
        print("Senha não pode ser vazia!")
        return False

    tipo = input("Tipo (ADM/CLIENTE): ")
    tipo = tipo.upper()
    if tipo != "ADM" and tipo != "CLIENTE":
        print("Tipo inválido!")
        return False

    novo_usuario = {"login": novo_login, "senha": nova_senha, "tipo": tipo}
    usuarios.append(novo_usuario)
    print("Usuário cadastrado!")
    return True


def fazer_login():
    login = input("Login: ")
    senha = input("Senha: ")

    for u in usuarios:
        if u["login"] == login and u["senha"] == senha:
            print(f"Bem-vindo(a), {u['login']}!")
            return u

    print("Login ou senha incorretos!")
    return None
