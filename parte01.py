from graphviz import Digraph

def buscar_estados_recursivo(estado_atual, instrucoes, novoestado):
    """
    Busca recursiva de novos estados a partir de um estado atual,
    incluindo transições com símbolo 'h'.
    """
    for i in instrucoes:
        # Verifica se a transição parte do estado atual
        if i[0] == estado_atual:
            # Se for uma transição válida (inclusive 'h')
            if i[2] not in novoestado and i[1] == 'h':
                novoestado.append(i[2])
                # Chamada recursiva para expandir o novo estado
                buscar_estados_recursivo(i[2], instrucoes, novoestado)

def print_tabela_transicoes(instrucoes, alfabeto, eInicial):
    # Largura padrão de cada coluna
    largura_coluna = 15  

    print("\n📋  Tabela de Transições")
    print("=" * (largura_coluna * (len(alfabeto) + 1) + len(alfabeto) * 3))

    # Cabeçalho da tabela
    cabecalho = ["Estado"] + alfabeto
    print(" | ".join(f"{c:^{largura_coluna}}" for c in cabecalho))
    print("-" * (largura_coluna * (len(alfabeto) + 1) + len(alfabeto) * 3))

    # Coleta e formata os estados únicos
    estados = set()
    for i in instrucoes:
        e = i[0]
        if isinstance(e, list):
            e = "{" + ",".join(e) + "}"
        estados.add(e)
    estados = sorted(estados)

    # Cria uma linha para cada estado
    for estado in estados:
        linha = []

        # Marca o estado inicial
        if estado in eInicial or estado.strip("{}") in eInicial:
            nome_estado = f"→ {estado}"
        else:
            nome_estado = f"  {estado}"
        linha.append(f"{nome_estado:<{largura_coluna}}")

        # Preenche cada coluna do alfabeto
        for a in alfabeto:
            destinos = []
            for i in instrucoes:
                e_origem = i[0]
                if isinstance(e_origem, list):
                    e_origem = "{" + ",".join(e_origem) + "}"
                if e_origem == estado and i[1] == a:
                    d = i[2]
                    if isinstance(d, list):
                        d = "{" + ",".join(d) + "}"
                    destinos.append(d)
            if destinos:
                linha.append(",".join(destinos))
            else:
                linha.append("-")

        # Imprime a linha completa
        print(" | ".join(f"{x:^{largura_coluna}}" for x in linha))

    print("=" * (largura_coluna * (len(alfabeto) + 1) + len(alfabeto) * 3))

def gerar_automato_graphviz(transicoes, eInicial, eFinal, nome_arquivo="automato"):
    dot = Digraph(comment='AFD Gerado', format='png')
    dot.attr(rankdir='LR', size='8,5')

    # Função auxiliar para converter listas/sets em strings
    def nome_estado(e):
        if isinstance(e, (list, set, tuple)):
            return "{" + ",".join(sorted(str(x) for x in e)) + "}"
        return str(e)

    # Estado inicial tratado como um conjunto único
    estado_inicial_nome = nome_estado(eInicial)

    # Adiciona nó inicial
    dot.node(estado_inicial_nome, shape='doublecircle' if estado_inicial_nome in map(nome_estado, eFinal) else 'circle')

    # Adiciona nós finais
    for e in eFinal:
        dot.node(nome_estado(e), shape='doublecircle')

    # Adiciona transições
    for origem, simbolo, destino in transicoes:
        dot.edge(nome_estado(origem), nome_estado(destino), label=str(simbolo))

    # Adiciona seta de início (do vazio -> inicial)
    dot.node('', shape='none', width='0')
    dot.edge('', estado_inicial_nome)

    # Renderiza o arquivo
    saida = dot.render(filename=nome_arquivo, cleanup=True)
    
def formatar_item(item):
    if isinstance(item, list):
        # se for lista, junta todos os elementos recursivamente
        return ''.join(formatar_item(x) for x in item)
    return str(item)   

def retornoAFD(eInicial, eFinal, instrucoes, estados):
    linhas = []

    estados = " ".join(estados)
    estados = estados + "\n"
    linhas.append(estados)

    eInicial = eInicial + "\n"
    linhas.append(eInicial)
    
    eFinal = " ".join(eFinal)
    eFinal = eFinal + "\n"
    linhas.append(eFinal)

    for i in instrucoes:
        x = i[0] + " " + i[1] + " " + i[2] + "\n"
        linhas.append(x)

    with open("saida.txt", "w") as arquivo:
        arquivo.writelines(linhas)
    


with open("entrada.txt", "r", encoding="utf-8") as f:
    linha = f.readlines()
    
estados = linha[0].split()
eInicial = linha[1].split()
eFinal = linha[2].split()

instrucoes = []
alfabeto = []

for lAtual in linha[3:]:
    lAtual = lAtual.split()
    if lAtual[0] in estados:
        if(lAtual[2] in estados):
            instrucoes.append(lAtual)
            if lAtual[0] in eInicial and lAtual[1] == 'h':
                eInicial.append(lAtual[2])
            if lAtual[1] not in alfabeto and lAtual[1] != 'h':
                alfabeto.append(lAtual[1])
        else:
            print(f'Estado {lAtual} inválido!')
    else:
        print(f'Estado {lAtual} inválido!')

alfabeto.sort()

print_tabela_transicoes(instrucoes, alfabeto, eInicial[0])
gerar_automato_graphviz(instrucoes, eInicial[0], eFinal, nome_arquivo="automatoFND")

novoestados = [eInicial]
novainst = []
novoestado = []

for e in novoestados:
    for a in alfabeto:
        for i in instrucoes:
            if i[0] in e and i[1] == a and i[1] != 'h' and i[2] not in novoestado:
                novoestado.append(i[2])
                buscar_estados_recursivo(i[2], instrucoes, novoestado)
                novoestado.sort()
        if novoestado not in novoestados and novoestado != []:
            if(eFinal[0] in novoestado):
                eFinal.append(formatar_item(novoestado))
            novoestados.append(novoestado)
        if novoestado != []:
            novainst.append([formatar_item(e), a, formatar_item(novoestado)])
        novoestado = []


eInicial = formatar_item(eInicial)
eFinal.remove(eFinal[0])

for i in range(len(novoestados)):
    novoestados[i] = formatar_item(novoestados[i])


print_tabela_transicoes(novainst, alfabeto, eInicial)
gerar_automato_graphviz(novainst, eInicial, eFinal, nome_arquivo="automatoFD")
retornoAFD(eInicial, eFinal, novainst, novoestados)
    
