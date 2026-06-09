# Usuários pré-cadastrados:
#   admin / 123    (ADM)
#   cliente1 / 123 (CLIENTE)

import auth
import fazenda
import cliente
from rich.console import Console

console = Console()


def main():
    print("")
    console.print("[green]=============================================[/green]")
    console.print("[green]   SISTEMA DE GESTÃO - FAZENDA SERTÃO[/green]")
    console.print("[green]=============================================[/green]")

    while True:
        print("")
        console.print("[cyan]========== MENU PRINCIPAL ==========[/cyan]")
        print("1 - Login")
        print("2 - Cadastrar usuário")
        print("0 - Sair")
        opcao = input("Escolha: ")

        if opcao == "0":
            console.print("[yellow]Saindo do sistema. Até mais![/yellow]")
            break

        elif opcao == "1":
            usuario_logado = auth.fazer_login()
            if usuario_logado is None:
                continue

            if usuario_logado["tipo"] == "ADM":
                fazenda.menu_adm()
            else:
                cliente.menu_cliente(usuario_logado)

        elif opcao == "2":
            auth.cadastrar_usuario()

        else:
            console.print("[red]Opção inválida![/red]")


main()
