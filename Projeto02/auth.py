from rich.console import Console

console = Console()

usuarios = [
    {"login": "admin", "senha": "123", "tipo": "ADM"},
    {"login": "cliente1", "senha": "123", "tipo": "CLIENTE"}
]


def cadastrar_usuario():
    novo_login = input("Login: ")
    if len(novo_login) == 0:
        console.print("[red]Login não pode ser vazio![/red]")
        return False

    for u in usuarios:
        if u["login"] == novo_login:
            console.print("[red]Login já existe![/red]")
            return False

    nova_senha = input("Senha: ")
    if len(nova_senha) == 0:
        console.print("[red]Senha não pode ser vazia![/red]")
        return False

    i

    tipo = input("Tipo (ADM/CLIENTE): ")
    tipo = tipo.upper()
    if tipo != "ADM" and tipo != "CLIENTE":
        console.print("[red]Tipo inválido![/red]")
        return False

    novo_usuario = {"login": novo_login, "senha": nova_senha, "tipo": tipo}
    usuarios.append(novo_usuario)
    console.print("[green]Usuário cadastrado![/green]")
    return True


def fazer_login():
    login = input("Login: ")
    senha = input("Senha: ")

    for u in usuarios:
        if u["login"] == login and u["senha"] == senha:
            console.print(f"[green]Bem-vindo(a), {u['login']}![/green]")
            return u

    console.print("[red]Login ou senha incorretos![/red]")
    return None
