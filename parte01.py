from graphviz import Digraph

#Busca recursiva por novos estados a partir de um estado por meio de transicoes vazias 'h'
def buscar_estados_recursivo(estado_atual, instrucoes, novoestado):

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

#Cria e retorna um arquivo saida.txt com o automato finito deterministico
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
    

# Lê arquivo de entrada contendo a definição do autômato
with open("entrada.txt", "r", encoding="utf-8") as f:
    linha = f.readlines()

# Define listas de estados, estado(s) inicial(is) e estados finais a partir das 3 primeiras linhas do arquivo
estados = linha[0].split() 
eInicial = linha[1].split()   # estado inicial
eFinal = linha[2].split()     # estados finais

# Cria listas vazias para armazenar as transições e o alfabeto
instrucoes = []  # Cada transição será uma lista [origem, símbolo, destino]
alfabeto = []    # Lista de símbolos utilizados nas transições

# Percorre o restante das linhas (a partir da quarta), que contêm as transições
for lAtual in linha[3:]:
    lAtual = lAtual.split()  # Divide a linha em partes: [estado_origem, símbolo, estado_destino]
    
    # Verifica se o estado de origem é válido
    if lAtual[0] in estados:
        # Verifica se o estado de destino é válido
        if lAtual[2] in estados:
            instrucoes.append(lAtual)  # Adiciona a transição válida na lista de instruções
            
            # Caso o estado inicial tenha uma transição com símbolo 'h' (vazio),
            # o destino também é considerado como estado inicial
            if lAtual[0] in eInicial and lAtual[1] == 'h':
                eInicial.append(lAtual[2])
            
            # Adiciona o símbolo ao alfabeto, exceto se for 'h' (ε)
            if lAtual[1] not in alfabeto and lAtual[1] != 'h':
                alfabeto.append(lAtual[1])
        else:
            print(f'Estado {lAtual} inválido!')
    else:
        print(f'Estado {lAtual} inválido!')

# Ordena o alfabeto
alfabeto.sort()

# Exibe a tabela de transições do autômato original (AFND)
print_tabela_transicoes(instrucoes, alfabeto, eInicial[0])

# Gera o diagrama do autômato não determinístico (AFND) usando Graphviz
gerar_automato_graphviz(instrucoes, eInicial[0], eFinal, nome_arquivo="automatoFND")

# Inicializa a conversão para AFD (construção do autômato determinístico)
novoestados = [eInicial]  # Nova lista de estados (começa com o(s) estado(s) inicial)
novainst = []             # Nova lista de transições do AFD
novoestado = []           # Lista temporária usada durante a expansão

# Inicia o processo de construção do AFD (técnica de conjuntos de estados)
for e in novoestados:             # Para cada novo estado (conjunto de estados)
    for a in alfabeto:            # Para cada símbolo do alfabeto
        for i in instrucoes:      # Para cada transição do AFND
            # Se a origem da transição está dentro do conjunto atual e o símbolo coincide
            if i[0] in e and i[1] == a and i[2] not in novoestado:
                novoestado.append(i[2])  # Adiciona o destino à lista temporária
                buscar_estados_recursivo(i[2], instrucoes, novoestado)  # Busca recursivamente transições vazias
                novoestado.sort()  # Ordena os estados do novo conjunto
        
        # Se o novo conjunto de estados ainda não existe na lista de novos estados, adiciona
        if novoestado not in novoestados and novoestado != []:
            # Se o novo conjunto contém algum estado final, marca-o também como final
            if(eFinal[0] in novoestado):
                eFinal.append(formatar_item(novoestado))
            novoestados.append(novoestado)  # Adiciona o novo conjunto como novo estado
        
        # Registra a nova transição do AFD (origem, símbolo, destino)
        if novoestado != []:
            novainst.append([formatar_item(e), a, formatar_item(novoestado)])
        
        # Limpa a lista temporária antes da próxima iteração
        novoestado = []

# Formata o estado inicial (agora conjunto)
eInicial = formatar_item(eInicial)

# Remove o primeiro estado final antigo (que era do AFND)
eFinal.remove(eFinal[0])

# Formata todos os novos estados (para exibição mais limpa, ex: ['A','B'] → 'AB')
for i in range(len(novoestados)):
    novoestados[i] = formatar_item(novoestados[i])

# Exibe a tabela de transições do AFD resultante
print_tabela_transicoes(novainst, alfabeto, eInicial)

# Gera o diagrama do autômato determinístico (AFD)
gerar_automato_graphviz(novainst, eInicial, eFinal, nome_arquivo="automatoFD")

# Exibe/retorna as informações finais do AFD (função definida em outro trecho do código)
retornoAFD(eInicial, eFinal, novainst, novoestados)

    
