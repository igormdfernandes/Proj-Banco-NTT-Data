fundos = 0
limite_diario = 500
historico = ""
saques_realizados = 0
limite_saques = 3

while True:

    print('[1] Depósito')
    print('[2] Saque')
    print('[3] Extrato')
    print('[4] Encerrar')
    escolha = input()

    if escolha == "1":
        quantia = float(input("Digite o valor para adicionar: "))

        if quantia > 0:
            fundos += quantia
            historico += f"Adição: R$ {quantia:.2f}\n"
        else:
            print("Operação falhou: valor inválido.")

    elif escolha == "2":
        quantia = float(input("Digite o valor para retirar: "))

        saldo_insuficiente = quantia > fundos
        acima_limite = quantia > limite_diario
        limite_saques_atingido = saques_realizados >= limite_saques

        if saldo_insuficiente:
            print("Erro: Saldo insuficiente para essa operação.")

        elif acima_limite:
            print("Erro: O valor excede o limite diário de retirada.")

        elif limite_saques_atingido:
            print("Erro: Você já atingiu o limite de retiradas diárias.")

        elif quantia > 0:
            fundos -= quantia
            historico += f"Retirada: R$ {quantia:.2f}\n"
            saques_realizados += 1
        else:
            print("Operação falhou: valor inválido.")

    elif escolha == "3":
        print("\n========== DETALHES DA CONTA ==========")
        print("Nenhuma movimentação registrada." if not historico else historico)
        print(f"Saldo atual: R$ {fundos:.2f}")
        print("=======================================")

    elif escolha == "4":
        print("Saindo do sistema bancário. Obrigado!")
        break

    else:
       print("Opção inválida. Tente novamente.")
