# -----------------------------------------------
# SISTEMA DE GESTÃO AGROPECUÁRIA - FAZENDA SERTÃO
# -----------------------------------------------

# Usuários pré-cadastrados: 
usuarios = [["admin", "123", "ADM"], ["cliente1", "123", "CLIENTE"]]

# Listas de dados
rebanho = []                # [tipo, brinco, status, preco]
estoque_leite = [0, 0.0]    # [litros, preco_por_litro]
estoque_produtos = []       # [nome, peso_kg, preco_por_kg]
agendamentos = []           # [cliente, item, data, horario]
historico_compras = []      # [cliente, item, valor]

# Receitas dos produtos: 
receitas = [
    ["Queijo Coalho", 8],
    ["Queijo Manteiga", 10],
    ["Manteiga", 15]
]

# Data atual do sistema 
HOJE_DIA = 18
HOJE_MES = 5
HOJE_ANO = 2026


# ----------- MENU PRINCIPAL -----------
while True:
    print("")
    print("===== FAZENDA SERTÃO =====")
    print("1 - Login")
    print("2 - Cadastrar usuário")
    print("0 - Sair")
    opcao = input("Escolha: ")

    if opcao == "0":
        print("Saindo do sistema. Até mais!")
        break

    # ---------- CADASTRO DE USUÁRIO ----------
    elif opcao == "2":
        novo_login = input("Login: ")
        if len(novo_login) == 0:
            print("Login não pode ser vazio!")
            continue
        existe = 0
        for u in usuarios:
            if u[0] == novo_login:
                existe = 1
                break
        if existe == 1:
            print("Login já existe!")
        else:
            nova_senha = input("Senha: ")
            if len(nova_senha) == 0:
                print("Senha não pode ser vazia!")
                continue
            tipo = input("Tipo (ADM/CLIENTE): ")
            tipo = tipo.upper()
            if tipo == "ADM" or tipo == "CLIENTE":
                usuarios.append([novo_login, nova_senha, tipo])
                print("Usuário cadastrado!")
            else:
                print("Tipo inválido!")

    # ---------- LOGIN ----------
    elif opcao == "1":
        login = input("Login: ")
        senha = input("Senha: ")
        autenticado = 0
        tipo_usuario = ""
        usuario_logado = ""
        for u in usuarios:
            if u[0] == login and u[1] == senha:
                autenticado = 1
                tipo_usuario = u[2]
                usuario_logado = u[0]
                break

        if autenticado == 0:
            print("Login ou senha incorretos!")
            continue

        print(f"Bem-vindo(a), {usuario_logado}!")

        # ---------- MENU DO ADMINISTRADOR ------------
        if tipo_usuario == "ADM":
            while True:
                print("")
                print("===== MENU ADM =====")
                print("1 - Cadastrar animal")
                print("2 - Buscar animal")
                print("3 - Atualizar animal")
                print("4 - Remover animal")
                print("5 - Listar rebanho")
                print("6 - Registrar leite ordenhado")
                print("7 - Fabricar produto")
                print("8 - Ver estoque completo")
                print("9 - Calcular patrimônio")
                print("0 - Logout")
                op = input("Escolha: ")

                if op == "0":
                    print("Logout realizado!")
                    break

                # ----- Cadastrar animal -----
                elif op == "1":
                    print("Tipos: 1-Bovino, 2-Caprino, 3-Ovino, 4-Suíno")
                    t = input("Tipo: ")
                    tipo_animal = ""
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
                        continue
                    brinco = input("Brinco/identificação: ")
                    if len(brinco) == 0:
                        print("Brinco não pode ser vazio!")
                        continue
                    
                    brinco_existe = 0
                    for a in rebanho:
                        if a[1] == brinco:
                            brinco_existe = 1
                            break
                    if brinco_existe == 1:
                        print("Já existe um animal com esse brinco!")
                        continue
                    
                    print("Status: 1-Em lactacao, 2-Para engorda, 3-Disponivel para venda")
                    s = input("Status: ")
                    status = ""
                    if s == "1":
                        status = "Em lactacao"
                    elif s == "2":
                        status = "Para engorda"
                    elif s == "3":
                        status = "Disponivel para venda"
                    else:
                        print("Status inválido!")
                        continue
                    preco = float(input("Preço de venda: "))
                    if preco <= 0:
                        print("Preço deve ser maior que zero!")
                        continue
                    rebanho.append([tipo_animal, brinco, status, preco])
                    print("Animal cadastrado!")

                # ----- Buscar animal -----
                elif op == "2":
                    brinco = input("Brinco do animal: ")
                    achou = 0
                    for a in rebanho:
                        if a[1] == brinco:
                            print(f"Tipo: {a[0]}")
                            print(f"Brinco: {a[1]}")
                            print(f"Status: {a[2]}")
                            print(f"Preço: R$ {a[3]}")
                            achou = 1
                            break
                    if achou == 0:
                        print("Animal não encontrado!")

                # ----- Atualizar animal -----
                elif op == "3":
                    brinco = input("Brinco do animal: ")
                    achou = 0
                    for a in rebanho:
                        if a[1] == brinco:
                            print("Novo status: 1-Em lactacao, 2-Para engorda, 3-Disponivel para venda")
                            s = input("Status: ")
                            novo_status = ""
                            if s == "1":
                                novo_status = "Em lactacao"
                            elif s == "2":
                                novo_status = "Para engorda"
                            elif s == "3":
                                novo_status = "Disponivel para venda"
                            else:
                                print("Status inválido!")
                                achou = 1
                                break
                            novo_preco = float(input("Novo preço: "))
                            if novo_preco <= 0:
                                print("Preço deve ser maior que zero!")
                                achou = 1
                                break
                            a[2] = novo_status
                            a[3] = novo_preco
                            print("Animal atualizado!")
                            achou = 1
                            break
                    if achou == 0:
                        print("Animal não encontrado!")

                # ----- Remover animal -----
                elif op == "4":
                    brinco = input("Brinco do animal: ")
                    achou = 0
                    for a in rebanho:
                        if a[1] == brinco:
                            rebanho.remove(a)
                            print("Animal removido!")
                            achou = 1
                            break
                    if achou == 0:
                        print("Animal não encontrado!")

                # ----- Listar rebanho -----
                elif op == "5":
                    if len(rebanho) == 0:
                        print("Rebanho vazio!")
                    else:
                        print("===== REBANHO =====")
                        for a in rebanho:
                            print(f"{a[0]} | Brinco: {a[1]} | Status: {a[2]} | R$ {a[3]}")

                # ----- Registrar leite ordenhado -----
                elif op == "6":
                    litros = float(input("Litros ordenhados: "))
                    if litros <= 0:
                        print("Litros deve ser maior que zero!")
                        continue
                    preco = float(input("Preço por litro: "))
                    if preco <= 0:
                        print("Preço deve ser maior que zero!")
                        continue
                    estoque_leite[0] = estoque_leite[0] + litros
                    estoque_leite[1] = preco
                    print(f"Estoque atual: {estoque_leite[0]} L a R$ {estoque_leite[1]}/L")

                # ----- Fabricar produto -----
                elif op == "7":
                    print("===== RECEITAS DISPONÍVEIS =====")
                    for i in range(len(receitas)):
                        r = receitas[i]
                        print(f"{i+1} - {r[0]} (usa {r[1]} L de leite por kg)")
                    escolha = int(input("Número da receita: "))
                    if escolha < 1 or escolha > len(receitas):
                        print("Opção inválida!")
                        continue
                    receita = receitas[escolha - 1]
                    nome_prod = receita[0]
                    litros_por_kg = receita[1]

                    kg = float(input(f"Quantos kg de {nome_prod} deseja fabricar? "))
                    if kg <= 0:
                        print("Quantidade inválida!")
                        continue

                    litros_necessarios = kg * litros_por_kg
                    print(f"Necessário: {litros_necessarios} L de leite")
                    print(f"Disponível em estoque: {estoque_leite[0]} L")

                    if litros_necessarios > estoque_leite[0]:
                        print("Leite insuficiente para fabricar este produto!")
                        continue

                    preco = float(input("Preço de venda por kg: "))
                    if preco <= 0:
                        print("Preço deve ser maior que zero!")
                        continue
                    estoque_leite[0] = estoque_leite[0] - litros_necessarios
                    estoque_produtos.append([nome_prod, kg, preco])
                    print(f"Fabricado {kg} kg de {nome_prod}!")
                    print(f"Leite restante no estoque: {estoque_leite[0]} L")

                # ----- Ver estoque completo -----
                elif op == "8":
                    print("===== ESTOQUE =====")
                    print(f"Leite: {estoque_leite[0]} L - R$ {estoque_leite[1]}/L")
                    print("Produtos fabricados:")
                    if len(estoque_produtos) == 0:
                        print("  (nenhum)")
                    else:
                        for p in estoque_produtos:
                            print(f"  {p[0]} - {p[1]} kg - R$ {p[2]}/kg")
                    print("Animais à venda:")
                    tem_animal = 0
                    for a in rebanho:
                        if a[2] == "Disponivel para venda":
                            print(f"  {a[0]} - Brinco {a[1]} - R$ {a[3]}")
                            tem_animal = 1
                    if tem_animal == 0:
                        print("  (nenhum)")

                # -----  Calcular Patrimônio -----
                elif op == "9":
                    total_rebanho = 0
                    for a in rebanho:
                        total_rebanho = total_rebanho + a[3]
                    valor_leite = estoque_leite[0] * estoque_leite[1]
                    valor_produtos = 0
                    for p in estoque_produtos:
                        valor_produtos = valor_produtos + (p[1] * p[2])
                    print("===== PATRIMÔNIO =====")
                    print(f"Rebanho: R$ {total_rebanho}")
                    print(f"Leite em estoque: R$ {valor_leite}")
                    print(f"Produtos em estoque: R$ {valor_produtos}")
                    print(f"TOTAL: R$ {total_rebanho + valor_leite + valor_produtos}")

                else:
                    print("Opção inválida!")

        # ----------- MENU DO CLIENTE ---------
        else:
            while True:
                print("")
                print("===== MENU CLIENTE =====")
                print("1 - Ver estoque disponível")
                print("2 - Comprar leite")
                print("3 - Comprar produto fabricado")
                print("4 - Comprar animal")
                print("5 - Agendar retirada/transporte")
                print("6 - Minhas compras")
                print("0 - Logout")
                op = input("Escolha: ")

                if op == "0":
                    print("Logout realizado!")
                    break

                # ----- Ver estoque -----
                elif op == "1":
                    print("===== DISPONÍVEL PARA COMPRA =====")
                    print(f"Leite: {estoque_leite[0]} L - R$ {estoque_leite[1]}/L")
                    print("Produtos:")
                    if len(estoque_produtos) == 0:
                        print("  (nenhum)")
                    else:
                        for p in estoque_produtos:
                            print(f"  {p[0]} - {p[1]} kg disponíveis - R$ {p[2]}/kg")
                    print("Animais:")
                    tem_animal = 0
                    for a in rebanho:
                        if a[2] == "Disponivel para venda":
                            print(f"  {a[0]} - Brinco {a[1]} - R$ {a[3]}")
                            tem_animal = 1
                    if tem_animal == 0:
                        print("  (nenhum)")

                # ----- Comprar leite -----
                elif op == "2":
                    if estoque_leite[0] == 0:
                        print("Sem leite em estoque!")
                        continue
                    print(f"Disponível: {estoque_leite[0]} L a R$ {estoque_leite[1]}/L")
                    qtd = float(input("Quantos litros? "))
                    if qtd <= 0:
                        print("Quantidade inválida!")
                    elif qtd > estoque_leite[0]:
                        print("Estoque insuficiente!")
                    else:
                        valor = qtd * estoque_leite[1]
                        estoque_leite[0] = estoque_leite[0] - qtd
                        historico_compras.append([usuario_logado, f"{qtd} L de leite", valor])
                        print(f"Compra realizada! Total: R$ {valor}")

                # ----- Comprar produto -----
                elif op == "3":
                    if len(estoque_produtos) == 0:
                        print("Sem produtos em estoque!")
                        continue
                    print("===== PRODUTOS =====")
                    for i in range(len(estoque_produtos)):
                        p = estoque_produtos[i]
                        print(f"{i+1} - {p[0]} - {p[1]} kg - R$ {p[2]}/kg")
                    escolha = int(input("Número do produto: "))
                    if escolha < 1 or escolha > len(estoque_produtos):
                        print("Inválido!")
                        continue
                    idx = escolha - 1
                    peso_quer = float(input("Quantos kg? "))
                    if peso_quer <= 0:
                        print("Quantidade inválida!")
                    elif peso_quer > estoque_produtos[idx][1]:
                        print("Peso indisponível!")
                    else:
                        valor = peso_quer * estoque_produtos[idx][2]
                        nome_prod = estoque_produtos[idx][0]
                        estoque_produtos[idx][1] = estoque_produtos[idx][1] - peso_quer
                        historico_compras.append([usuario_logado, f"{peso_quer}kg de {nome_prod}", valor])
                        print(f"Compra realizada! Total: R$ {valor}")
                        if estoque_produtos[idx][1] == 0:
                            estoque_produtos.pop(idx)

                # ----- Comprar animal -----
                elif op == "4":
                    disponiveis = []
                    for a in rebanho:
                        if a[2] == "Disponivel para venda":
                            disponiveis.append(a)
                    if len(disponiveis) == 0:
                        print("Nenhum animal à venda!")
                        continue
                    print("===== ANIMAIS À VENDA =====")
                    for i in range(len(disponiveis)):
                        a = disponiveis[i]
                        print(f"{i+1} - {a[0]} - Brinco {a[1]} - R$ {a[3]}")
                    escolha = int(input("Número do animal: "))
                    if escolha < 1 or escolha > len(disponiveis):
                        print("Inválido!")
                        continue
                    animal = disponiveis[escolha - 1]
                    historico_compras.append([usuario_logado, f"{animal[0]} (brinco {animal[1]})", animal[3]])
                    rebanho.remove(animal)
                    print(f"Animal comprado por R$ {animal[3]}!")

                # ----- Agendar retirada -----
                elif op == "5":
                    item = input("O que vai retirar? (ex: 10kg Queijo Coalho): ")
                    
                    print("--- Data da retirada ---")
                    dia = int(input("Dia (1-31): "))
                    mes = int(input("Mês (1-12): "))
                    ano = int(input("Ano: "))
                    
                    if mes < 1 or mes > 12:
                        print("Mês inválido! Deve ser entre 1 e 12.")
                        continue
                    
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
                        continue
                    
                    if ano < HOJE_ANO:
                        print("Ano inválido! Não é possível agendar para o passado.")
                        continue
                    
                    if ano == HOJE_ANO and mes < HOJE_MES:
                        print("Mês inválido! Esse mês já passou.")
                        continue
                    if ano == HOJE_ANO and mes == HOJE_MES and dia < HOJE_DIA:
                        print("Dia inválido! Esse dia já passou.")
                        continue
                    
                    print("--- Horário da retirada ---")
                    hora = int(input("Hora (6-17): "))
                    minuto = int(input("Minuto (0-59): "))
                    
                    if hora < 6 or hora > 17:
                        print("Horário inválido! A fazenda atende das 6h às 18h.")
                        continue
                    
                    if minuto < 0 or minuto > 59:
                        print("Minuto inválido! Deve ser entre 0 e 59.")
                        continue

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

                    agendamentos.append([usuario_logado, item, data, horario])
                    print(f"Retirada agendada para {data} às {horario}!")

                # ----- Minhas Compras -----
                elif op == "6":
                    print("===== MINHAS COMPRAS =====")
                    achou = 0
                    total = 0
                    for c in historico_compras:
                        if c[0] == usuario_logado:
                            print(f"- {c[1]} - R$ {c[2]}")
                            total = total + c[2]
                            achou = 1
                    if achou == 0:
                        print("(nenhuma compra)")
                    else:
                        print(f"TOTAL GASTO: R$ {total}")

                else:
                    print("Opção inválida!")

    else:
        print("Opção inválida!")