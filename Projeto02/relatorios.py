historico_movimentacoes = []

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
    print("")
    print("========== HISTÓRICO DE MOVIMENTAÇÕES ==========")

    if len(historico_movimentacoes) == 0:
        print("(nenhuma movimentação registrada)")
        return

    print("+------------+----------+------------------------------+--------+-------------+")
    print("| Data       | Ação     | Item                         | Qtd    | Responsável |")
    print("+------------+----------+------------------------------+--------+-------------+")
    for m in historico_movimentacoes:
        print(f"| {m['data']:<10} | {m['acao']:<8} | {m['item']:<28} | {m['qtd']:<6} | {m['cliente']:<11} |")
    print("+------------+----------+------------------------------+--------+-------------+")


def dashboard_fazenda(rebanho, estoque_leite, estoque_produtos):
    print("")
    print("=================================================")
    print("    RELATÓRIO GERAL DA FAZENDA SERTÃO")
    print("=================================================")

    contagem_tipos = {}
    for a in rebanho:
        tipo = a["tipo"]
        if tipo in contagem_tipos:
            contagem_tipos[tipo] = contagem_tipos[tipo] + 1
        else:
            contagem_tipos[tipo] = 1

    print("")
    print("--- ANIMAIS POR TIPO ---")
    if len(contagem_tipos) == 0:
        print("Rebanho: vazio")
    else:
        print("+------------------+------------+")
        print("| Tipo             | Quantidade |")
        print("+------------------+------------+")
        for tipo in contagem_tipos:
            print(f"| {tipo:<16} | {contagem_tipos[tipo]:>10} |")
        print("+------------------+------------+")
        print(f"| TOTAL            | {len(rebanho):>10} |")
        print("+------------------+------------+")

    print("")
    print("--- ESTOQUE DE LEITE ---")
    print("+--------------------------+--------------+")
    print("| Métrica                  | Valor        |")
    print("+--------------------------+--------------+")
    print(f"| Litros disponíveis       | {estoque_leite['litros']:>10} L |")
    print(f"| Preço por litro          | R$ {estoque_leite['preco_por_litro']:>8.2f}  |")
    valor_leite = estoque_leite["litros"] * estoque_leite["preco_por_litro"]
    print(f"| Valor total              | R$ {valor_leite:>8.2f}  |")
    print("+--------------------------+--------------+")

    print("")
    print("--- ESTOQUE DE QUEIJOS ---")
    if len(estoque_produtos) == 0:
        print("Produtos fabricados: nenhum")
    else:
        print("+----------------------+----------+--------+--------------+")
        print("| Produto              | Peso(kg) | R$/kg  | Subtotal     |")
        print("+----------------------+----------+--------+--------------+")
        total_produtos = 0
        for p in estoque_produtos:
            subtotal = p["peso_kg"] * p["preco_kg"]
            total_produtos = total_produtos + subtotal
            print(f"| {p['nome']:<20} | {p['peso_kg']:>8.2f} | {p['preco_kg']:>6.2f} | R$ {subtotal:>8.2f}  |")
        print("+----------------------+----------+--------+--------------+")
        print(f"| TOTAL                                            | R$ {total_produtos:>8.2f}  |")
        print("+----------------------+----------+--------+--------------+")


def calcular_patrimonio(rebanho, estoque_leite, estoque_produtos):
    total_rebanho = 0
    for a in rebanho:
        total_rebanho = total_rebanho + a["preco"]

    valor_leite = estoque_leite["litros"] * estoque_leite["preco_por_litro"]

    valor_produtos = 0
    for p in estoque_produtos:
        valor_produtos = valor_produtos + (p["peso_kg"] * p["preco_kg"])

    total = total_rebanho + valor_leite + valor_produtos

    print("")
    print("========== PATRIMÔNIO DA FAZENDA ==========")
    print("+----------------------+----------------+")
    print("| Item                 | Valor (R$)     |")
    print("+----------------------+----------------+")
    print(f"| Rebanho              | {total_rebanho:>14.2f} |")
    print(f"| Leite em estoque     | {valor_leite:>14.2f} |")
    print(f"| Produtos em estoque  | {valor_produtos:>14.2f} |")
    print("+----------------------+----------------+")
    print(f"| TOTAL                | {total:>14.2f} |")
    print("+----------------------+----------------+")


def gerar_recibo(usuario_logado, agendamento, historico_compras):
    print("")
    print("===============================================")
    print("        FAZENDA SERTÃO")
    print("        RECIBO / TICKET DE CARGA")
    print("===============================================")
    print("")
    print("--- Dados do Cliente ---")
    print(f"Cliente: {usuario_logado['login']}")
    print(f"Tipo:    {usuario_logado['tipo']}")
    print("")
    print("--- Dados do Agendamento ---")
    print(f"Item para retirada: {agendamento['item']}")
    print(f"Data:               {agendamento['data']}")
    print(f"Horário:            {agendamento['horario']}")
    print("")
    print("--- Itens Comprados ---")

    total = 0
    tem_compra = 0
    for c in historico_compras:
        if c["cliente"] == usuario_logado["login"]:
            print(f"  - {c['item']:<35} R$ {c['valor']:>8.2f}")
            total = total + c["valor"]
            tem_compra = 1

    if tem_compra == 0:
        print("  (nenhuma compra registrada)")

    print("")
    print("-----------------------------------------------")
    print(f"  TOTAL: R$ {total:.2f}")
    print("===============================================")
    print("  Documento gerado pelo sistema Fazenda Sertão")
    print("===============================================")
