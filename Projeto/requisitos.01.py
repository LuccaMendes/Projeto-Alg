# Título do Projeto: Sistema de Gestão Agropecuária (Fazenda Sertão)
# Nosso sistema deve possuir 2 perfis/tipos de usuários:

# Administrador (Produtor Rural / Gestor da Fazenda): Responsável por gerenciar o rebanho, a produção de leite, a fabricação de queijos e a venda de animais.

# Cliente (Comerciante / Laticínio / Atravessador): Acessa o sistema para comprar os produtos derivados, lotes de leite ou adquirir animais (como leitões e bodes).

# Primeira Etapa (Estruturas de Repetição e Listas)
# Nesta etapa, os alunos devem usar listas para armazenar os dados em memória enquanto o programa roda.

# R1 - Login: Efetuar login com usuário e senha para acessar o menu de gestão da fazenda. Tanto ADM ou CLIENTE pode fazer login.

# -----------Requisitos Funcionais (ADM):

# R2 - Gerenciar Rebanho: Cadastrar, buscar, atualizar e remover animais. O cadastro deve incluir o tipo do animal (Bovino de Leite, Caprino, Ovino, Suíno/Leitão), identificação (brinco/número) e status (ex: em lactação, para engorda, disponível para venda).

# R3 - Gerenciar Produção e Derivados: Cadastrar a produção diária. O ADM deve poder registrar litros de leite ordenhados e adicionar ao estoque produtos fabricados (ex. Queijo Coalho, Queijo Manteiga), informando o peso (kg) e o valor de venda.

# R4 - Tema Livre (ADM): Criar uma funcionalidade útil para o produtor rural.

# ------------Requisitos Funcionais (CLIENTE):

# R5 - Efetuar Compra: O cliente logado pode visualizar o estoque e comprar produtos (ex: 10kg de Queijo Coalho ou 5 Leitões). A compra deve diminuir a quantidade disponível nas listas de estoque do administrador. Usuário ADM não pode fazer compras.

# R6 - Agendar Retirada/Transporte: O cliente deve agendar uma data e horário para o caminhão buscar o leite, os queijos ou os animais comprados na fazenda.

# R7 - Tema Livre (CLIENTE): Criar uma funcionalidade útil para o comprador.

# -----------Requisitos Gerais:

# R8 - Cadastro de Usuários: Cadastrar logins definindo quem é ADM e quem é CLIENTE.

# R9 - Navegabilidade: O sistema deve rodar no terminal, preso em um laço while principal (Menu Principal), permitindo que o usuário navegue entre as opções sem que o programa encerre inesperadamente.