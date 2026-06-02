#   admin / 123    (ADM)
#   cliente1 / 123 (CLIENTE)

import auth
import fazenda
import cliente


def main():
    print("")
    print("=============================================")
    print("   SISTEMA DE GESTÃO - FAZENDA SERTÃO")
    print("=============================================")

    while True:
        print("")
        print("========== MENU PRINCIPAL ==========")
        print("1 - Login")
        print("2 - Cadastrar usuário")
        print("0 - Sair")
        opcao = input("Escolha: ")

        if opcao == "0":
            print("Saindo do sistema. Até mais!")
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
            print("Opção inválida!")


main()
