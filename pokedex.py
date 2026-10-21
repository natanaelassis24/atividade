# Execute no terminal: python pokedex.py
# Requer Python 3. Os dados ficam em memória durante a execução.


def obter_dados_pokemon(nome, tipo, nivel):
    """Formata os dados de um Pokémon para a listagem."""
    return f"{nome} {tipo} {nivel}"


def obter_nivel_pokemon(entrada):
    """Converte o nível ou retorna uma mensagem de validação."""
    try:
        nivel = int(entrada)
        if 1 <= nivel <= 100:
            return nivel
        return "O nível deve estar entre 1 e 100. Tente novamente."
    except (ValueError, TypeError):
        return "Erro: digite um número inteiro para o nível."


def validar_pokemon_existe(pokedex, nome):
    """Retorna True quando o nome existe, ou uma mensagem de erro."""
    if nome not in pokedex:
        return f"Erro: O Pokémon '{nome}' não foi encontrado."
    return True


def adicionar_pokemon(pokedex, nome, tipo, nivel):
    """Adiciona um Pokémon sem sobrescrever um cadastro existente."""
    if nome in pokedex:
        return "Erro: este Pokémon já está cadastrado."
    if not nome.strip() or not tipo.strip():
        return "Erro: nome e tipo não podem ficar vazios."
    nivel = obter_nivel_pokemon(nivel)
    if not isinstance(nivel, int):
        return nivel
    pokedex[nome] = {"tipo": tipo, "nivel": nivel, "capturado": 0}
    return f"{nome} adicionado com sucesso!"


def listar_pokemon(pokedex):
    """Retorna os Pokémon em ordem alfabética pelo nome."""
    if not pokedex:
        return "Não há Pokémon cadastrados."
    resultado = []
    for nome, dados in sorted(pokedex.items(), key=lambda item: item[0].casefold()):
        resultado.append(obter_dados_pokemon(nome, dados["tipo"], dados["nivel"]))
    return "\n".join(resultado)


def remover_pokemon(pokedex, nome):
    """Remove o cadastro, preservando o histórico de capturas."""
    validacao = validar_pokemon_existe(pokedex, nome)
    if validacao is not True:
        return validacao
    del pokedex[nome]
    return f"Pokémon '{nome}' removido com sucesso!"


def atualizar_nivel_pokemon(pokedex, nome, novo_nivel):
    """Valida o cadastro e o nível antes de atualizar o dicionário."""
    validacao = validar_pokemon_existe(pokedex, nome)
    if validacao is not True:
        return validacao
    novo_nivel = obter_nivel_pokemon(novo_nivel)
    if not isinstance(novo_nivel, int):
        return novo_nivel
    pokedex[nome]["nivel"] = novo_nivel
    return f"Nível de {nome} atualizado com sucesso!"


def registrar_captura(pokedex, historico, nome, capturas):
    """Soma as capturas e registra uma tupla (nome, quantidade) na lista."""
    validacao = validar_pokemon_existe(pokedex, nome)
    if validacao is not True:
        return validacao
    if not isinstance(capturas, int) or capturas <= 0:
        return "Erro: a quantidade de capturas deve ser um inteiro positivo."
    pokedex[nome]["capturado"] += capturas
    historico.append((nome, capturas))
    return f"{capturas} captura(s) registrada(s) para o Pokémon '{nome}'."


def exibir_historico_capturas(historico):
    """Retorna todas as capturas na ordem em que foram registradas."""
    if not historico:
        return "Não há histórico de capturas."
    return "\n".join([f"{nome} - quantidade: {quantidade}" for nome, quantidade in historico])


def exibir_menu():
    """Retorna as sete opções do menu."""
    return (
        "\n1 - Adicionar Pokémon\n"
        "2 - Listar Pokémon\n"
        "3 - Remover Pokémon\n"
        "4 - Atualizar nível\n"
        "5 - Registrar captura\n"
        "6 - Exibir histórico de capturas\n"
        "7 - Sair"
    )


def sair():
    """Exibe a mensagem de encerramento."""
    print("Pokédex encerrada. Até a próxima aventura!")


def menu():
    """Mantém os dados e encaminha cada opção para sua função."""
    pokedex = {}
    historico = []

    while True:
        try:
            print(exibir_menu())
            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                nome = input("Nome do Pokémon: ").strip()
                tipo = input("Tipo do Pokémon: ").strip()
                nivel = input("Nível (1 a 100): ")
                nivel_convertido = obter_nivel_pokemon(nivel)
                if isinstance(nivel_convertido, int):
                    print(adicionar_pokemon(pokedex, nome, tipo, nivel_convertido))
                else:
                    print(nivel_convertido)
            elif opcao == "2":
                print(listar_pokemon(pokedex))
            elif opcao == "3":
                nome = input("Nome do Pokémon: ").strip()
                print(remover_pokemon(pokedex, nome))
            elif opcao == "4":
                nome = input("Nome do Pokémon: ").strip()
                nivel = input("Novo nível (1 a 100): ")
                nivel_convertido = obter_nivel_pokemon(nivel)
                if isinstance(nivel_convertido, int):
                    print(atualizar_nivel_pokemon(pokedex, nome, nivel_convertido))
                else:
                    print(nivel_convertido)
            elif opcao == "5":
                nome = input("Nome do Pokémon: ").strip()
                try:
                    capturas = int(input("Quantidade capturada: "))
                    print(registrar_captura(pokedex, historico, nome, capturas))
                except ValueError:
                    print("Erro: digite um número inteiro para as capturas.")
            elif opcao == "6":
                print(exibir_historico_capturas(historico))
            elif opcao == "7":
                sair()
                break
            else:
                print("Opção inválida. Escolha um número de 1 a 7.")
        except (EOFError, KeyboardInterrupt):
            print()
            sair()
            break


if __name__ == "__main__":
    menu()
