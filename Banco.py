from abc import ABC, abstractmethod
from datetime import datetime

usuarios = []
contas = []
numero_conta_sequencial = 1

class Usuario:
    def __init__(self, nome, cpf, data_nascimento, endereco):
        self.nome = nome
        self.cpf = cpf.replace(".", "").replace("-", "").replace(" ", "")
        self.data_nascimento = data_nascimento
        self.endereco = endereco
        self.contas = []

    def adicionar_conta(self, conta):
        self.contas.append(conta)

def cadastrar_usuario(nome, cpf, data_nascimento, endereco):
    for usuario in usuarios:
        if usuario.cpf == cpf:
            print("Erro: Já existe um usuário com este CPF.")
            return
    novo_usuario = Usuario(nome, cpf, data_nascimento, endereco)
    usuarios.append(novo_usuario)
    print(f"Usuário {nome} cadastrado com sucesso!")

class Conta:
    def __init__(self, numero, usuario):
        self._saldo = 0
        self.numero = numero
        self.agencia = "0001"
        self.usuario = usuario
        self.historico = Historico()
    
    @classmethod
    def nova_conta(cls, usuario, numero):
        return cls(numero, usuario)

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso!")
            self.historico.adicionar_transacao(Deposito(valor))
        else:
            print("\nErro: Valor inválido.")
            return False
        return True

    def sacar(self, valor):
        if valor > self._saldo:
            print("\nErro: Saldo insuficiente.")
        elif valor > 0:
            self._saldo -= valor
            print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!")
            self.historico.adicionar_transacao(Saque(valor))
            return True
        else:
            print("\nErro: Valor inválido.")
        return False

    @property
    def saldo(self):
        return self._saldo

    def exibir_extrato(self):
        print("\n========== EXTRATO ==========")
        if not self.historico.transacoes:
            print("Nenhuma movimentação registrada.")
        else:
            for transacao in self.historico.transacoes:
                print(transacao)
        print(f"Saldo atual: R$ {self.saldo:.2f}")
        print("==============================")

class ContaCorrente(Conta):
    def __init__(self, numero, usuario, limite=500, limite_saques=3):
        super().__init__(numero, usuario)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len([t for t in self.historico.transacoes if isinstance(t, Saque)])
        if valor > self.limite:
            print("\nErro: O valor excede o limite de saque.")
        elif numero_saques >= self.limite_saques:
            print("\nErro: Limite de saques diários atingido.")
        else:
            return super().sacar(valor)
        return False

class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        self._transacoes.append(f"{timestamp} - {transacao}")

class Transacao(ABC):
    @abstractmethod
    def __str__(self):
        pass

class Saque(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return f"Saque de R$ {self.valor:.2f}"

class Deposito(Transacao):
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return f"Depósito de R$ {self.valor:.2f}"

def criar_conta_corrente(cpf):
    global numero_conta_sequencial
    usuario = next((u for u in usuarios if u.cpf == cpf), None)
    
    if not usuario:
        print("Erro: Usuário não encontrado.")
        return

    nova_conta = ContaCorrente(numero_conta_sequencial, usuario)
    usuario.adicionar_conta(nova_conta)
    contas.append(nova_conta)
    numero_conta_sequencial += 1
    print(f"Conta {nova_conta.numero} criada com sucesso para o usuário {usuario.nome}!")

def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for conta in contas:
        print(f"Agência: {conta.agencia}, Número da Conta: {conta.numero}, Usuário: {conta.usuario.nome}")

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
        conta = contas[0]
        conta.depositar(valor)

    elif escolha == "4":
        if len(contas) == 0:
            print("Nenhuma conta criada.")
            continue
        valor = float(input("Digite o valor do saque: "))
        conta = contas[0]
        conta.sacar(valor)

    elif escolha == "5":
        if len(contas) == 0:
            print("Nenhuma conta criada.")
            continue
        conta = contas[0]
        conta.exibir_extrato()

    elif escolha == "6":
        listar_contas()

    elif escolha == "7":
        print("Saindo do sistema bancário. Obrigado!")
        break

    else:
        print("Opção inválida. Tente novamente.")
