import relatorios
from rich.console import Console
from rich.table import Table

console = Console()

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
        console.print("[red]Tipo inválido![/red]")
        return

    brinco = input("Brinco/identificação: ")
    if len(brinco) == 0:
        console.print("[red]Brinco não pode ser vazio![/red]")
        return

    for a in rebanho:
        if a["brinco"] == brinco:
            console.print("[red]Já existe um animal com esse brinco![/red]")
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
        console.print("[red]Status inválido![/red]")
        return

    preco = float(input("Preço de venda: "))
    if preco <= 0:
        console.print("[red]Preço deve ser maior que zero![/red]")
        return

    novo_animal = {
        "tipo": tipo_animal,
        "brinco": brinco,
        "status": status,
        "preco": preco
    }
    rebanho.append(novo_animal)
    console.print("[green]Animal cadastrado![/green]")


def buscar_animal():
    brinco = input("Brinco do animal: ")
    for a in rebanho:
        if a["brinco"] == brinco:
            console.print(f"[cyan]Tipo:[/cyan] {a['tipo']}")
            console.print(f"[cyan]Brinco:[/cyan] {a['brinco']}")
            console.print(f"[cyan]Status:[/cyan] {a['status']}")
            console.print(f"[cyan]Preço:[/cyan] R$ {a['preco']:.2f}")
            return
    console.print("[red]Animal não encontrado![/red]")


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
                console.print("[red]Status inválido![/red]")
                return

            novo_preco = float(input("Novo preço: "))
            if novo_preco <= 0:
                console.print("[red]Preço deve ser maior que zero![/red]")
                return

            a["status"] = novo_status
            a["preco"] = novo_preco
            console.print("[green]Animal atualizado![/green]")
            return
    console.print("[red]Animal não encontrado![/red]")


def remover_animal():
    brinco = input("Brinco do animal: ")
    for a in rebanho:
        if a["brinco"] == brinco:
            rebanho.remove(a)
            console.print("[green]Animal removido![/green]")
            return
    console.print("[red]Animal não encontrado![/red]")


def listar_rebanho():
    if len(rebanho) == 0:
        console.print("[yellow]Rebanho vazio![/yellow]")
        return

    tabela = Table(title="REBANHO DA FAZENDA")
    tabela.add_column("Tipo", style="green")
    tabela.add_column("Brinco", style="white")
    tabela.add_column("Status", style="yellow")
    tabela.add_column("Preço (R$)", justify="right", style="cyan")

    for a in rebanho:
        tabela.add_row(a["tipo"], a["brinco"], a["status"], f"{a['preco']:.2f}")

    console.print(tabela)


def registrar_leite():
    litros = float(input("Litros ordenhados: "))
    if litros <= 0:
        console.print("[red]Litros deve ser maior que zero![/red]")
        return
    preco = float(input("Preço por litro: "))
    if preco <= 0:
        console.print("[red]Preço deve ser maior que zero![/red]")
        return

    estoque_leite["litros"] = estoque_leite["litros"] + litros
    estoque_leite["preco_por_litro"] = preco

    relatorios.registrar_movimentacao("producao", f"{litros} L de leite", litros, "ADM")

    console.print(f"[green]Estoque atual: {estoque_leite['litros']} L a R$ {estoque_leite['preco_por_litro']:.2f}/L[/green]")


def fabricar_produto():
    console.print("[cyan]===== RECEITAS DISPONÍVEIS =====[/cyan]")
    for i in range(len(receitas)):
        r = receitas[i]
        print(f"{i+1} - {r['nome']} (usa {r['litros_por_kg']} L de leite por kg)")

    escolha = int(input("Número da receita: "))
    if escolha < 1 or escolha > len(receitas):
        console.print("[red]Opção inválida![/red]")
        return

    receita = receitas[escolha - 1]
    nome_prod = receita["nome"]
    litros_por_kg = receita["litros_por_kg"]

    kg = float(input(f"Quantos kg de {nome_prod} deseja fabricar? "))
    if kg <= 0:
        console.print("[red]Quantidade inválida![/red]")
        return

    litros_necessarios = kg * litros_por_kg
    print(f"Necessário: {litros_necessarios} L de leite")
    print(f"Disponível em estoque: {estoque_leite['litros']} L")

    if litros_necessarios > estoque_leite["litros"]:
        console.print("[red]Leite insuficiente para fabricar este produto![/red]")
        return

    preco = float(input("Preço de venda por kg: "))
    if preco <= 0:
        console.print("[red]Preço deve ser maior que zero![/red]")
        return

    estoque_leite["litros"] = estoque_leite["litros"] - litros_necessarios

    novo_produto = {"nome": nome_prod, "peso_kg": kg, "preco_kg": preco}
    estoque_produtos.append(novo_produto)

    relatorios.registrar_movimentacao("producao", f"{kg}kg de {nome_prod}", kg, "ADM")

    console.print(f"[green]Fabricado {kg}kg de {nome_prod}![/green]")
    console.print(f"[yellow]Leite restante no estoque: {estoque_leite['litros']} L[/yellow]")


def ver_estoque():
    console.print("\n[cyan]===== ESTOQUE COMPLETO =====[/cyan]")
    console.print(f"[green]Leite:[/green] {estoque_leite['litros']} L - R$ {estoque_leite['preco_por_litro']:.2f}/L")

    if len(estoque_produtos) == 0:
        console.print("[yellow]Produtos fabricados: (nenhum)[/yellow]")
    else:
        tabela = Table(title="Produtos Fabricados")
        tabela.add_column("Produto", style="white")
        tabela.add_column("Peso (kg)", justify="right")
        tabela.add_column("R$/kg", justify="right", style="cyan")
        for p in estoque_produtos:
            tabela.add_row(p["nome"], f"{p['peso_kg']:.2f}", f"{p['preco_kg']:.2f}")
        console.print(tabela)

    disponiveis = []
    for a in rebanho:
        if a["status"] == "Disponivel para venda":
            disponiveis.append(a)

    if len(disponiveis) == 0:
        console.print("[yellow]Animais à venda: (nenhum)[/yellow]")
    else:
        tabela = Table(title="Animais à Venda")
        tabela.add_column("Tipo", style="green")
        tabela.add_column("Brinco")
        tabela.add_column("Preço (R$)", justify="right", style="cyan")
        for a in disponiveis:
            tabela.add_row(a["tipo"], a["brinco"], f"{a['preco']:.2f}")
        console.print(tabela)


def menu_adm():
    while True:
        print("")
        console.print("[cyan]========== MENU ADM ==========[/cyan]")
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
            console.print("[yellow]Logout realizado![/yellow]")
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
            console.print("[red]Opção inválida![/red]")
