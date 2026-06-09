import fazenda
import relatorios
from rich.console import Console
from rich.table import Table

console = Console()

historico_compras = []

HOJE_DIA = 8
HOJE_MES = 6
HOJE_ANO = 2026


def ver_estoque_disponivel():
    console.print("\n[cyan]========== DISPONÍVEL PARA COMPRA ==========[/cyan]")
    console.print(f"[green]Leite:[/green] {fazenda.estoque_leite['litros']} L - R$ {fazenda.estoque_leite['preco_por_litro']:.2f}/L")

    if len(fazenda.estoque_produtos) == 0:
        console.print("[yellow]Produtos: (nenhum)[/yellow]")
    else:
        tabela = Table(title="Produtos Disponíveis")
        tabela.add_column("Produto", style="white")
        tabela.add_column("Disponível (kg)", justify="right")
        tabela.add_column("R$/kg", justify="right", style="cyan")
        for p in fazenda.estoque_produtos:
            tabela.add_row(p["nome"], f"{p['peso_kg']:.2f}", f"{p['preco_kg']:.2f}")
        console.print(tabela)

    disponiveis = []
    for a in fazenda.rebanho:
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


def comprar_leite(usuario_logado):
    if fazenda.estoque_leite["litros"] == 0:
        console.print("[red]Sem leite em estoque![/red]")
        return

    print(f"Disponível: {fazenda.estoque_leite['litros']} L a R$ {fazenda.estoque_leite['preco_por_litro']:.2f}/L")
    qtd = float(input("Quantos litros deseja comprar? "))
    if qtd <= 0:
        console.print("[red]Quantidade inválida![/red]")
        return
    if qtd > fazenda.estoque_leite["litros"]:
        console.print("[red]Estoque insuficiente![/red]")
        return

    valor = qtd * fazenda.estoque_leite["preco_por_litro"]
    fazenda.estoque_leite["litros"] = fazenda.estoque_leite["litros"] - qtd

    compra = {
        "cliente": usuario_logado["login"],
        "item": f"{qtd} L de leite",
        "valor": valor
    }
    historico_compras.append(compra)

    relatorios.registrar_movimentacao("venda", f"{qtd} L de leite", qtd, usuario_logado["login"])

    console.print(f"[green]Compra realizada! Total: R$ {valor:.2f}[/green]")


def comprar_produto(usuario_logado):
    if len(fazenda.estoque_produtos) == 0:
        console.print("[red]Sem produtos em estoque![/red]")
        return

    console.print("[cyan]===== PRODUTOS DISPONÍVEIS =====[/cyan]")
    for i in range(len(fazenda.estoque_produtos)):
        p = fazenda.estoque_produtos[i]
        print(f"{i+1} - {p['nome']} - {p['peso_kg']:.2f} kg - R$ {p['preco_kg']:.2f}/kg")

    escolha = int(input("Número do produto: "))
    if escolha < 1 or escolha > len(fazenda.estoque_produtos):
        console.print("[red]Inválido![/red]")
        return

    idx = escolha - 1
    produto = fazenda.estoque_produtos[idx]
    peso_quer = float(input("Quantos kg deseja comprar? "))
    if peso_quer <= 0:
        console.print("[red]Quantidade inválida![/red]")
        return
    if peso_quer > produto["peso_kg"]:
        console.print("[red]Peso indisponível em estoque![/red]")
        return

    valor = peso_quer * produto["preco_kg"]
    nome_prod = produto["nome"]
    produto["peso_kg"] = produto["peso_kg"] - peso_quer

    compra = {
        "cliente": usuario_logado["login"],
        "item": f"{peso_quer}kg de {nome_prod}",
        "valor": valor
    }
    historico_compras.append(compra)

    relatorios.registrar_movimentacao("venda", f"{peso_quer}kg de {nome_prod}", peso_quer, usuario_logado["login"])

    console.print(f"[green]Compra realizada! Total: R$ {valor:.2f}[/green]")

    if produto["peso_kg"] == 0:
        fazenda.estoque_produtos.pop(idx)


def comprar_animal(usuario_logado):
    disponiveis = []
    for a in fazenda.rebanho:
        if a["status"] == "Disponivel para venda":
            disponiveis.append(a)

    if len(disponiveis) == 0:
        console.print("[red]Nenhum animal à venda![/red]")
        return

    console.print("[cyan]===== ANIMAIS À VENDA =====[/cyan]")
    for i in range(len(disponiveis)):
        a = disponiveis[i]
        print(f"{i+1} - {a['tipo']} - Brinco {a['brinco']} - R$ {a['preco']:.2f}")

    escolha = int(input("Número do animal: "))
    if escolha < 1 or escolha > len(disponiveis):
        console.print("[red]Inválido![/red]")
        return

    animal = disponiveis[escolha - 1]

    compra = {
        "cliente": usuario_logado["login"],
        "item": f"{animal['tipo']} (brinco {animal['brinco']})",
        "valor": animal["preco"]
    }
    historico_compras.append(compra)

    relatorios.registrar_movimentacao("venda", f"{animal['tipo']} brinco {animal['brinco']}", 1, usuario_logado["login"])

    fazenda.rebanho.remove(animal)
    console.print(f"[green]Animal comprado por R$ {animal['preco']:.2f}![/green]")


def agendar_retirada(usuario_logado):
    item = input("O que vai retirar? (ex: 10kg Queijo Coalho): ")

    print("--- Data da retirada ---")
    dia = int(input("Dia (1-31): "))
    mes = int(input("Mês (1-12): "))
    ano = int(input("Ano: "))

    if mes < 1 or mes > 12:
        console.print("[red]Mês inválido![/red]")
        return

    dias_max = 31
    if mes == 4 or mes == 6 or mes == 9 or mes == 11:
        dias_max = 30
    if mes == 2:
        if (ano % 4 == 0 and ano % 100 != 0) or ano % 400 == 0:
            dias_max = 29
        else:
            dias_max = 28

    if dia < 1 or dia > dias_max:
        console.print(f"[red]Dia inválido! O mês {mes} tem {dias_max} dias.[/red]")
        return

    if ano < HOJE_ANO:
        console.print("[red]Ano inválido! Não é possível agendar para o passado.[/red]")
        return
    if ano == HOJE_ANO and mes < HOJE_MES:
        console.print("[red]Mês inválido! Esse mês já passou.[/red]")
        return
    if ano == HOJE_ANO and mes == HOJE_MES and dia < HOJE_DIA:
        console.print("[red]Dia inválido! Esse dia já passou.[/red]")
        return

    print("--- Horário da retirada ---")
    hora = int(input("Hora (6-17): "))
    minuto = int(input("Minuto (0-59): "))

    if hora < 6 or hora > 17:
        console.print("[red]Horário inválido! A fazenda atende das 6h às 18h.[/red]")
        return
    if minuto < 0 or minuto > 59:
        console.print("[red]Minuto inválido![/red]")
        return

    if dia < 10:
        dia_str = f"0{dia}"
    else:
        dia_str = f"{dia}"
    if mes < 10:
        mes_str = f"0{mes}"
    else:
        mes_str = f"{mes}"
    if hora < 10:
        hora_str = f"0{hora}"
    else:
        hora_str = f"{hora}"
    if minuto < 10:
        minuto_str = f"0{minuto}"
    else:
        minuto_str = f"{minuto}"

    data = f"{dia_str}/{mes_str}/{ano}"
    horario = f"{hora_str}:{minuto_str}"

    agendamento = {
        "cliente": usuario_logado["login"],
        "item": item,
        "data": data,
        "horario": horario
    }

    console.print(f"[green]Retirada agendada para {data} às {horario}![/green]")

    relatorios.gerar_recibo(usuario_logado, agendamento, historico_compras)
    relatorios.gerar_recibo_pdf(usuario_logado, agendamento, historico_compras)


def minhas_compras(usuario_logado):
    console.print("\n[cyan]========== MINHAS COMPRAS ==========[/cyan]")

    minhas = []
    for c in historico_compras:
        if c["cliente"] == usuario_logado["login"]:
            minhas.append(c)

    if len(minhas) == 0:
        console.print("[yellow](nenhuma compra)[/yellow]")
        return

    tabela = Table()
    tabela.add_column("Item", style="white")
    tabela.add_column("Valor (R$)", justify="right", style="green")

    total = 0
    for c in minhas:
        tabela.add_row(c["item"], f"{c['valor']:.2f}")
        total = total + c["valor"]

    console.print(tabela)
    console.print(f"[yellow]TOTAL GASTO: R$ {total:.2f}[/yellow]")


def menu_cliente(usuario_logado):
    while True:
        print("")
        console.print("[cyan]========== MENU CLIENTE ==========[/cyan]")
        print("1 - Ver estoque disponível")
        print("2 - Comprar leite")
        print("3 - Comprar produto fabricado")
        print("4 - Comprar animal")
        print("5 - Agendar retirada (gera recibo + PDF)")
        print("6 - Minhas compras")
        print("0 - Logout")
        op = input("Escolha: ")

        if op == "0":
            console.print("[yellow]Logout realizado![/yellow]")
            break
        elif op == "1":
            ver_estoque_disponivel()
        elif op == "2":
            comprar_leite(usuario_logado)
        elif op == "3":
            comprar_produto(usuario_logado)
        elif op == "4":
            comprar_animal(usuario_logado)
        elif op == "5":
            agendar_retirada(usuario_logado)
        elif op == "6":
            minhas_compras(usuario_logado)
        else:
            console.print("[red]Opção inválida![/red]")
