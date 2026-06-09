from rich.console import Console
from rich.table import Table
from fpdf import FPDF

console = Console()

historico_movimentacoes = []
contador_pdfs = [0]

HOJE_DIA = 8
HOJE_MES = 6
HOJE_ANO = 2026


def registrar_movimentacao(acao, item, qtd, cliente):
    if HOJE_DIA < 10:
        dia_str = f"0{HOJE_DIA}"
    else:
        dia_str = f"{HOJE_DIA}"
    if HOJE_MES < 10:
        mes_str = f"0{HOJE_MES}"
    else:
        mes_str = f"{HOJE_MES}"
    data = f"{dia_str}/{mes_str}/{HOJE_ANO}"

    movimentacao = {
        "data": data,
        "acao": acao,
        "item": item,
        "qtd": qtd,
        "cliente": cliente
    }
    historico_movimentacoes.append(movimentacao)


def ver_historico_movimentacoes():
    console.print("\n[cyan]========== HISTÓRICO DE MOVIMENTAÇÕES ==========[/cyan]")

    if len(historico_movimentacoes) == 0:
        console.print("[yellow](nenhuma movimentação registrada)[/yellow]")
        return

    tabela = Table()
    tabela.add_column("Data", style="white")
    tabela.add_column("Ação", style="yellow")
    tabela.add_column("Item", style="green")
    tabela.add_column("Qtd", justify="right", style="cyan")
    tabela.add_column("Responsável", style="magenta")

    for m in historico_movimentacoes:
        tabela.add_row(m["data"], m["acao"], m["item"], f"{m['qtd']}", m["cliente"])

    console.print(tabela)


def dashboard_fazenda(rebanho, estoque_leite, estoque_produtos):
    console.print("\n[magenta]=================================================[/magenta]")
    console.print("[magenta]    RELATÓRIO GERAL DA FAZENDA SERTÃO[/magenta]")
    console.print("[magenta]=================================================[/magenta]")

    contagem_tipos = {}
    for a in rebanho:
        tipo = a["tipo"]
        if tipo in contagem_tipos:
            contagem_tipos[tipo] = contagem_tipos[tipo] + 1
        else:
            contagem_tipos[tipo] = 1

    if len(contagem_tipos) == 0:
        console.print("[yellow]Rebanho: vazio[/yellow]")
    else:
        tabela_animais = Table(title="ANIMAIS POR TIPO")
        tabela_animais.add_column("Tipo", style="white")
        tabela_animais.add_column("Quantidade", justify="right", style="yellow")
        for tipo in contagem_tipos:
            tabela_animais.add_row(tipo, str(contagem_tipos[tipo]))
        tabela_animais.add_row("TOTAL", str(len(rebanho)))
        console.print(tabela_animais)

    tabela_leite = Table(title="ESTOQUE DE LEITE")
    tabela_leite.add_column("Métrica", style="white")
    tabela_leite.add_column("Valor", justify="right", style="green")
    tabela_leite.add_row("Litros disponíveis", f"{estoque_leite['litros']} L")
    tabela_leite.add_row("Preço por litro", f"R$ {estoque_leite['preco_por_litro']:.2f}")
    valor_leite = estoque_leite["litros"] * estoque_leite["preco_por_litro"]
    tabela_leite.add_row("Valor total", f"R$ {valor_leite:.2f}")
    console.print(tabela_leite)

    if len(estoque_produtos) == 0:
        console.print("[yellow]Produtos fabricados: nenhum[/yellow]")
    else:
        tabela_queijos = Table(title="ESTOQUE DE QUEIJOS")
        tabela_queijos.add_column("Produto", style="white")
        tabela_queijos.add_column("Peso (kg)", justify="right")
        tabela_queijos.add_column("R$/kg", justify="right")
        tabela_queijos.add_column("Subtotal", justify="right", style="green")
        total_produtos = 0
        for p in estoque_produtos:
            subtotal = p["peso_kg"] * p["preco_kg"]
            total_produtos = total_produtos + subtotal
            tabela_queijos.add_row(p["nome"], f"{p['peso_kg']:.2f}", f"{p['preco_kg']:.2f}", f"R$ {subtotal:.2f}")
        tabela_queijos.add_row("", "", "TOTAL", f"R$ {total_produtos:.2f}")
        console.print(tabela_queijos)


def calcular_patrimonio(rebanho, estoque_leite, estoque_produtos):
    total_rebanho = 0
    for a in rebanho:
        total_rebanho = total_rebanho + a["preco"]

    valor_leite = estoque_leite["litros"] * estoque_leite["preco_por_litro"]

    valor_produtos = 0
    for p in estoque_produtos:
        valor_produtos = valor_produtos + (p["peso_kg"] * p["preco_kg"])

    total = total_rebanho + valor_leite + valor_produtos

    tabela = Table(title="PATRIMÔNIO DA FAZENDA")
    tabela.add_column("Item", style="white")
    tabela.add_column("Valor (R$)", justify="right", style="green")
    tabela.add_row("Rebanho", f"{total_rebanho:.2f}")
    tabela.add_row("Leite em estoque", f"{valor_leite:.2f}")
    tabela.add_row("Produtos em estoque", f"{valor_produtos:.2f}")
    tabela.add_row("TOTAL", f"{total:.2f}")
    console.print(tabela)


def gerar_recibo(usuario_logado, agendamento, historico_compras):
    
    console.print("\n[magenta]===============================================[/magenta]")
    console.print("[magenta]        FAZENDA SERTÃO[/magenta]")
    console.print("[magenta]        RECIBO / TICKET DE CARGA[/magenta]")
    console.print("[magenta]===============================================[/magenta]")

    console.print("[cyan]--- Dados do Cliente ---[/cyan]")
    print(f"Cliente: {usuario_logado['login']}")
    print(f"Tipo:    {usuario_logado['tipo']}")

    console.print("[cyan]--- Dados do Agendamento ---[/cyan]")
    print(f"Item para retirada: {agendamento['item']}")
    print(f"Data:               {agendamento['data']}")
    print(f"Horário:            {agendamento['horario']}")

    console.print("[cyan]--- Itens Comprados ---[/cyan]")

    total = 0
    tem_compra = 0
    for c in historico_compras:
        if c["cliente"] == usuario_logado["login"]:
            print(f"  - {c['item']:<35} R$ {c['valor']:>8.2f}")
            total = total + c["valor"]
            tem_compra = 1

    if tem_compra == 0:
        console.print("[yellow]  (nenhuma compra registrada)[/yellow]")

    console.print("[magenta]-----------------------------------------------[/magenta]")
    console.print(f"[green]  TOTAL: R$ {total:.2f}[/green]")
    console.print("[magenta]===============================================[/magenta]")


def gerar_recibo_pdf(usuario_logado, agendamento, historico_compras):
    
    contador_pdfs[0] = contador_pdfs[0] + 1

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 18)
    pdf.cell(0, 12, "FAZENDA SERTAO")
    pdf.ln(12)
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "RECIBO / TICKET DE CARGA")
    pdf.ln(15)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Dados do Cliente:")
    pdf.ln(8)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"Cliente: {usuario_logado['login']}")
    pdf.ln(7)
    pdf.cell(0, 7, f"Tipo: {usuario_logado['tipo']}")
    pdf.ln(12)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Dados do Agendamento:")
    pdf.ln(8)
    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 7, f"Item para retirada: {agendamento['item']}")
    pdf.ln(7)
    pdf.cell(0, 7, f"Data: {agendamento['data']}")
    pdf.ln(7)
    pdf.cell(0, 7, f"Horario: {agendamento['horario']}")
    pdf.ln(12)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 8, "Itens comprados:")
    pdf.ln(8)
    pdf.set_font("Arial", "", 11)

    total = 0
    tem_compra = 0
    for c in historico_compras:
        if c["cliente"] == usuario_logado["login"]:
            pdf.cell(0, 7, f"- {c['item']} ............. R$ {c['valor']:.2f}")
            pdf.ln(7)
            total = total + c["valor"]
            tem_compra = 1

    if tem_compra == 0:
        pdf.cell(0, 7, "(nenhuma compra registrada)")
        pdf.ln(7)

    pdf.ln(5)

    pdf.set_font("Arial", "B", 13)
    pdf.cell(0, 10, f"TOTAL: R$ {total:.2f}")
    pdf.ln(15)

    pdf.set_font("Arial", "I", 9)
    pdf.cell(0, 6, "Documento gerado automaticamente pelo sistema Fazenda Sertao.")

    nome_arquivo = f"recibo_{usuario_logado['login']}_{contador_pdfs[0]}.pdf"
    pdf.output(nome_arquivo)

    console.print(f"[green]Recibo PDF gerado: {nome_arquivo}[/green]")
