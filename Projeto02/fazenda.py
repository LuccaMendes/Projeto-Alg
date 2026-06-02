import relatorios

rebanho = []
estoque_leite = {"litros": 0, "preco_por_litro": 0.0}
estoque_produtos = []

receitas = [
    {"nome": "Queijo Coalho", "litros_por_kg": 8},
    {"nome": "Queijo Manteiga", "litros_por_kg": 10},
    {"nome": "Manteiga", "litros_por_kg": 15}
]


def cadastrar_animal():
    print("Tipos: 1-Bovino, 2-Caprino, 3-Ovino, 4-Suíno")
    t = input("Tipo: ")
    if t == "1":
        tipo_animal = "Bovino"
    elif t == "2":
        tipo_animal = "Caprino"
    elif t == "3":
        tipo_animal = "Ovino"
    elif t == "4":
        tipo_animal = "Suíno"
    else:
        print("Tipo inválido!")
        return

    brinco = input("Brinco/identificação: ")
    if len(brinco) == 0:
        print("Brinco não pode ser vazio!")
        return

    for a in rebanho:
        if a["brinco"] == brinco:
            print("Já existe um animal com esse brinco!")
            return

    print("Status: 1-Em lactacao, 2-Para engorda, 3-Disponivel para venda")
    s = input("Status: ")
    if s == "1":
        status = "Em lactacao"
    elif s == "2":
        status = "Para engorda"
    elif s == "3":
        status = "Disponivel para venda"
    else:
        print("Status inválido!")
        return

    preco = float(input("Preço de venda: "))
    if preco <= 0:
        print("Preço deve ser maior que zero!")
        return

    novo_animal = {
        "tipo": tipo_animal,
        "brinco": brinco,
        "status": status,
        "preco": preco
    }
    rebanho.append(novo_animal)
    print("Animal cadastrado!")


def buscar_animal():
    brinco = input("Brinco do animal: ")
    for a in rebanho:
        if a["brinco"] == brinco:
            print(f"Tipo: {a['tipo']}")
            print(f"Brinco: {a['brinco']}")
            print(f"Status: {a['status']}")
            print(f"Preço: R$ {a['preco']:.2f}")
            return
    print("Animal não encontrado!")


def atualizar_animal():
    brinco = input("Brinco do animal: ")
    for a in rebanho:
        if a["brinco"] == brinco:
            print("Novo status: 1-Em lactacao, 2-Para engorda, 3-Disponivel para venda")
            s = input("Status: ")
            if s == "1":
                novo_status = "Em lactacao"
            elif s == "2":
                novo_status = "Para engorda"
            elif s == "3":
                novo_status = "Disponivel para venda"
            else:
                print("Status inválido!")
                return

            novo_preco = float(input("Novo preço: "))
            if novo_preco <= 0:
                print("Preço deve ser maior que zero!")
                return

            a["status"] = novo_status
            a["preco"] = novo_preco
            print("Animal atualizado!")
            return
    print("Animal não encontrado!")


def remover_animal():
    brinco = input("Brinco do animal: ")
    for a in rebanho:
        if a["brinco"] == brinco:
            rebanho.remove(a)
            print("Animal removido!")
            return
    print("Animal não encontrado!")


def listar_rebanho():
    if len(rebanho) == 0:
        print("Rebanho vazio!")
        return

    print("")
    print("+----------------+----------+----------------------------+------------+")
    print("| Tipo           | Brinco   | Status                     | Preço (R$) |")
    print("+----------------+----------+----------------------------+------------+")
    for a in rebanho:
        print(f"| {a['tipo']:<14} | {a['brinco']:<8} | {a['status']:<26} | {a['preco']:>10.2f} |")
    print("+----------------+----------+----------------------------+------------+")


def registrar_leite():
    litros = float(input("Litros ordenhados: "))
    if litros <= 0:
        print("Litros deve ser maior que zero!")
        return
    preco = float(input("Preço por litro: "))
    if preco <= 0:
        print("Preço deve ser maior que zero!")
        return

    estoque_leite["litros"] = estoque_leite["litros"] + litros
    estoque_leite["preco_por_litro"] = preco

    relatorios.registrar_movimentacao("producao", f"{litros} L de leite", litros, "ADM")

    print(f"Estoque atual: {estoque_leite['litros']} L a R$ {estoque_leite['preco_por_litro']}/L")


def fabricar_produto():
    print("===== RECEITAS DISPONÍVEIS =====")
    for i in range(len(receitas)):
        r = receitas[i]
        print(f"{i+1} - {r['nome']} (usa {r['litros_por_kg']} L de leite por kg)")

    escolha = int(input("Número da receita: "))
    if escolha < 1 or escolha > len(receitas):
        print("Opção inválida!")
        return

    receita = receitas[escolha - 1]
    nome_prod = receita["nome"]
    litros_por_kg = receita["litros_por_kg"]

    kg = float(input(f"Quantos kg de {nome_prod} deseja fabricar? "))
    if kg <= 0:
        print("Quantidade inválida!")
        return

    litros_necessarios = kg * litros_por_kg
    print(f"Necessário: {litros_necessarios} L de leite")
    print(f"Disponível em estoque: {estoque_leite['litros']} L")

    if litros_necessarios > estoque_leite["litros"]:
        print("Leite insuficiente para fabricar este produto!")
        return

    preco = float(input("Preço de venda por kg: "))
    if preco <= 0:
        print("Preço deve ser maior que zero!")
        return

    estoque_leite["litros"] = estoque_leite["litros"] - litros_necessarios

    novo_produto = {"nome": nome_prod, "peso_kg": kg, "preco_kg": preco}
    estoque_produtos.append(novo_produto)

    relatorios.registrar_movimentacao("producao", f"{kg}kg de {nome_prod}", kg, "ADM")

    print(f"Fabricado {kg}kg de {nome_prod}!")
    print(f"Leite restante no estoque: {estoque_leite['litros']} L")


def ver_estoque():
    print("")
    print("========== ESTOQUE COMPLETO ==========")
    print(f"Leite: {estoque_leite['litros']} L - R$ {estoque_leite['preco_por_litro']:.2f}/L")
    print("")
    print("--- Produtos Fabricados ---")
    if len(estoque_produtos) == 0:
        print("(nenhum)")
    else:
        for p in estoque_produtos:
            print(f"  {p['nome']} - {p['peso_kg']:.2f} kg - R$ {p['preco_kg']:.2f}/kg")

    print("")
    print("--- Animais à Venda ---")
    disponiveis = []
    for a in rebanho:
        if a["status"] == "Disponivel para venda":
            disponiveis.append(a)
    if len(disponiveis) == 0:
        print("(nenhum)")
    else:
        for a in disponiveis:
            print(f"  {a['tipo']} - Brinco {a['brinco']} - R$ {a['preco']:.2f}")


def menu_adm():
    while True:
        print("")
        print("========== MENU ADM ==========")
        print("1 - Cadastrar animal")
        print("2 - Buscar animal")
        print("3 - Atualizar animal")
        print("4 - Remover animal")
        print("5 - Listar rebanho")
        print("6 - Registrar leite ordenhado")
        print("7 - Fabricar produto")
        print("8 - Ver estoque completo")
        print("9 - Calcular patrimônio")
        print("10 - Relatório Geral")
        print("11 - Histórico de movimentações")
        print("0 - Logout")
        op = input("Escolha: ")

        if op == "0":
            print("Logout realizado!")
            break
        elif op == "1":
            cadastrar_animal()
        elif op == "2":
            buscar_animal()
        elif op == "3":
            atualizar_animal()
        elif op == "4":
            remover_animal()
        elif op == "5":
            listar_rebanho()
        elif op == "6":
            registrar_leite()
        elif op == "7":
            fabricar_produto()
        elif op == "8":
            ver_estoque()
        elif op == "9":
            relatorios.calcular_patrimonio(rebanho, estoque_leite, estoque_produtos)
        elif op == "10":
            relatorios.dashboard_fazenda(rebanho, estoque_leite, estoque_produtos)
        elif op == "11":
            relatorios.ver_historico_movimentacoes()
        else:
            print("Opção inválida!")
