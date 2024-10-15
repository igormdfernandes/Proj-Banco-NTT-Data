import datetime

usuarios = []
contas = []
numero_conta_sequencial = 1

def cadastrar_usuario(nome, cpf, data_nascimento, endereco):
    cpf = cpf.replace(".", "").replace("-", "").replace(" ", "")
    
    # Verifica se o CPF já está cadastrado
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            print("Erro: Já existe um usuário com este CPF.")
            return
    
    usuario = {
        "nome": nome,
        "cpf": cpf,
        "data_nascimento": data_nascimento,
        "endereco": endereco
    }
    usuarios.append(usuario)
    print(f"Usuário {nome} cadastrado com sucesso!")

def criar_conta_corrente(cpf):
    global numero_conta_sequencial
    usuario = None
    
    for u in usuarios:
        if u["cpf"] == cpf:
            usuario = u
            break

    if not usuario:
        print("Erro: Usuário não encontrado.")
        return

    conta = {
        "agencia": "0001",
        "numero_conta": numero_conta_sequencial,
        "usuario": usuario
    }
    contas.append(conta)
    numero_conta_sequencial += 1
    print(f"Conta {conta['numero_conta']} criada com sucesso para o usuário {usuario['nome']}!")

def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    
    for conta in contas:
        usuario = conta['usuario']
        print(f"Agência: {conta['agencia']}, Número da Conta: {conta['numero_conta']}, Usuário: {usuario['nome']}")

def saque(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if valor > saldo:
        print("Erro: Saldo insuficiente.")
    elif valor > limite:
        print("Erro: O valor excede o limite diário de retirada.")
    elif numero_saques >= limite_saques:
        print("Erro: Você já atingiu o limite de saques diários.")
    elif valor > 0:
        saldo -= valor
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        extrato += f"[{timestamp}] Retirada: R$ {valor:.2f}\n"
        numero_saques += 1
        print(f"Saque de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Erro: Valor inválido.")

    return saldo, extrato

def deposito(saldo, valor, extrato):
    if valor > 0:
        saldo += valor
        timestamp = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        extrato += f"[{timestamp}] Depósito: R$ {valor:.2f}\n"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso!")
    else:
        print("Erro: Valor inválido.")
    
    return saldo, extrato

def extrato_conta(saldo, *, extrato):
    print("\n========== EXTRATO ==========")
    print("Nenhuma movimentação registrada." if not extrato else extrato)
    print(f"Saldo atual: R$ {saldo:.2f}")
    print("==============================")

# Exemplo de uso
fundos = 0
historico = ""
saques_realizados = 0
limite_diario = 500
limite_saques = 3

while True:
    print("\n[1] Cadastrar Usuário")
    print("[2] Criar Conta Corrente")
    print("[3] Depósito")
    print("[4] Saque")
    print("[5] Extrato")
    print("[6] Listar Contas")
    print("[7] Encerrar")
    
    escolha = input()

    if escolha == "1":
        nome = input("Nome: ")
        cpf = input("CPF: ")
        data_nascimento = input("Data de Nascimento (dd/mm/yyyy): ")
        endereco = input("Endereço (logradouro, número, bairro, cidade/UF): ")
        cadastrar_usuario(nome, cpf, data_nascimento, endereco)
    
    elif escolha == "2":
        cpf = input("CPF do usuário: ")
        criar_conta_corrente(cpf)

    elif escolha == "3":
        if len(contas) == 0:
            print("Nenhuma conta criada.")
            continue
        valor = float(input("Digite o valor do depósito: "))
        fundos, historico = deposito(fundos, valor, historico)

    elif escolha == "4":
        if len(contas) == 0:
            print("Nenhuma conta criada.")
            continue
        valor = float(input("Digite o valor do saque: "))
        fundos, historico = saque(saldo=fundos, valor=valor, extrato=historico, limite=limite_diario, numero_saques=saques_realizados, limite_saques=limite_saques)
        saques_realizados += 1

    elif escolha == "5":
        extrato_conta(fundos, extrato=historico)

    elif escolha == "6":
        listar_contas()

    elif escolha == "7":
        print("Saindo do sistema bancário. Obrigado!")
        break

    else:
        print("Opção inválida. Tente novamente.")
