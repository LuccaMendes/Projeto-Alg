import fazenda
import relatorios

historico_compras = []

HOJE_DIA = 8
HOJE_MES = 6
HOJE_ANO = 2026


def ver_estoque_disponivel():
    print("")
    print("========== DISPONÍVEL PARA COMPRA ==========")
    print(f"Leite: {fazenda.estoque_leite['litros']} L - R$ {fazenda.estoque_leite['preco_por_litro']:.2f}/L")
    print("")
    print("--- Produtos ---")
    if len(fazenda.estoque_produtos) == 0:
        print("(nenhum)")
    else:
        for p in fazenda.estoque_produtos:
            print(f"  {p['nome']} - {p['peso_kg']:.2f} kg disponíveis - R$ {p['preco_kg']:.2f}/kg")

    print("")
    print("--- Animais ---")
    disponiveis = []
    for a in fazenda.rebanho:
        if a["status"] == "Disponivel para venda":
            disponiveis.append(a)
    if len(disponiveis) == 0:
        print("(nenhum)")
    else:
        for a in disponiveis:
            print(f"  {a['tipo']} - Brinco {a['brinco']} - R$ {a['preco']:.2f}")


def comprar_leite(usuario_logado):
    if fazenda.estoque_leite["litros"] == 0:
        print("Sem leite em estoque!")
        return

    print(f"Disponível: {fazenda.estoque_leite['litros']} L a R$ {fazenda.estoque_leite['preco_por_litro']:.2f}/L")
    qtd = float(input("Quantos litros deseja comprar? "))
    if qtd <= 0:
        print("Quantidade inválida!")
        return
    if qtd > fazenda.estoque_leite["litros"]:
        print("Estoque insuficiente!")
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

    print(f"Compra realizada! Total: R$ {valor:.2f}")


def comprar_produto(usuario_logado):
    if len(fazenda.estoque_produtos) == 0:
        print("Sem produtos em estoque!")
        return

    print("===== PRODUTOS DISPONÍVEIS =====")
    for i in range(len(fazenda.estoque_produtos)):
        p = fazenda.estoque_produtos[i]
        print(f"{i+1} - {p['nome']} - {p['peso_kg']:.2f} kg - R$ {p['preco_kg']:.2f}/kg")

    escolha = int(input("Número do produto: "))
    if escolha < 1 or escolha > len(fazenda.estoque_produtos):
        print("Inválido!")
        return

    idx = escolha - 1
    produto = fazenda.estoque_produtos[idx]
    peso_quer = float(input("Quantos kg deseja comprar? "))
    if peso_quer <= 0:
        print("Quantidade inválida!")
        return
    if peso_quer > produto["peso_kg"]:
        print("Peso indisponível em estoque!")
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

    print(f"Compra realizada! Total: R$ {valor:.2f}")

    if produto["peso_kg"] == 0:
        fazenda.estoque_produtos.pop(idx)


def comprar_animal(usuario_logado):
    disponiveis = []
    for a in fazenda.rebanho:
        if a["status"] == "Disponivel para venda":
            disponiveis.append(a)

    if len(disponiveis) == 0:
        print("Nenhum animal à venda!")
        return

    print("===== ANIMAIS À VENDA =====")
    for i in range(len(disponiveis)):
        a = disponiveis[i]
        print(f"{i+1} - {a['tipo']} - Brinco {a['brinco']} - R$ {a['preco']:.2f}")

    escolha = int(input("Número do animal: "))
    if escolha < 1 or escolha > len(disponiveis):
        print("Inválido!")
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
    print(f"Animal comprado por R$ {animal['preco']:.2f}!")


def agendar_retirada(usuario_logado):
    item = input("O que vai retirar? (ex: 10kg Queijo Coalho): ")

    print("--- Data da retirada ---")
    dia = int(input("Dia (1-31): "))
    mes = int(input("Mês (1-12): "))
    ano = int(input("Ano: "))

    if mes < 1 or mes > 12:
        print("Mês inválido!")
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
        print(f"Dia inválido! O mês {mes} tem {dias_max} dias.")
        return

    if ano < HOJE_ANO:
        print("Ano inválido! Não é possível agendar para o passado.")
        return
    if ano == HOJE_ANO and mes < HOJE_MES:
        print("Mês inválido! Esse mês já passou.")
        return
    if ano == HOJE_ANO and mes == HOJE_MES and dia < HOJE_DIA:
        print("Dia inválido! Esse dia já passou.")
        return

    print("--- Horário da retirada ---")
    hora = int(input("Hora (6-17): "))
    minuto = int(input("Minuto (0-59): "))

    if hora < 6 or hora > 17:
        print("Horário inválido! A fazenda atende das 6h às 18h.")
        return
    if minuto < 0 or minuto > 59:
        print("Minuto inválido!")
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

    print(f"Retirada agendada para {data} às {horario}!")

    relatorios.gerar_recibo(usuario_logado, agendamento, historico_compras)


def minhas_compras(usuario_logado):
    print("")
    print("========== MINHAS COMPRAS ==========")

    minhas = []
    for c in historico_compras:
        if c["cliente"] == usuario_logado["login"]:
            minhas.append(c)

    if len(minhas) == 0:
        print("(nenhuma compra)")
        return

    print("+----------------------------------+--------------+")
    print("| Item                             | Valor (R$)   |")
    print("+----------------------------------+--------------+")
    total = 0
    for c in minhas:
        print(f"| {c['item']:<32} | {c['valor']:>12.2f} |")
        total = total + c["valor"]
    print("+----------------------------------+--------------+")
    print(f"TOTAL GASTO: R$ {total:.2f}")


def menu_cliente(usuario_logado):
    while True:
        print("")
        print("========== MENU CLIENTE ==========")
        print("1 - Ver estoque disponível")
        print("2 - Comprar leite")
        print("3 - Comprar produto fabricado")
        print("4 - Comprar animal")
        print("5 - Agendar retirada (gera recibo)")
        print("6 - Minhas compras")
        print("0 - Logout")
        op = input("Escolha: ")

        if op == "0":
            print("Logout realizado!")
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
            print("Opção inválida!")
