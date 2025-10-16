# Lê o arquivo de saída
with open("saida.txt", "r", encoding="utf-8") as f:
    linhas = f.readlines()  # Lê todas as linhas do arquivo em uma lista

estados = linhas[0].strip().split()
eInicial = linhas[1].strip()
eFinal = linhas[2].strip().split()
instrucoes = []
alfabeto = []

# Percorre as linhas restantes do arquivo (definições das transições)
for lAtual in linhas[3:]:
    lAtual = lAtual.strip().split()  # Divide a linha por espaços: [origem, símbolo, destino]
    
    # Verifica se a linha tem exatamente 3 elementos
    if len(lAtual) != 3:
        print(f'Linha inválida: {lAtual}')  # Caso não tenha o formato esperado
        continue  # Pula para a próxima linha
    
    # Verifica se o estado de origem é válido
    if lAtual[0] in estados:
        # Verifica se o estado de destino é válido
        if lAtual[2] in estados:
            instrucoes.append(lAtual)  # Adiciona a transição à lista de instruções
        else:
            print(f'Estado destino inválido: {lAtual[2]}')
    else:
        print(f'Estado origem inválido: {lAtual[0]}')

# Agora, lê o arquivo com as palavras que serão testadas no autômato
with open("palavras.txt", "r", encoding="utf-8") as f:
    palavras = f.readlines()  # Cada linha contém uma palavra a ser testada

# Cria (ou substitui) o arquivo de saída que armazenará os resultados
with open("resultado.txt", "w", encoding="utf-8") as saida:
    
    # Para cada palavra na lista de entrada
    for lAtual in palavras:
        atual = eInicial     # Começa sempre no estado inicial
        linhaValida = True   # Marca se a palavra é reconhecida ou não
        lAtual = lAtual.strip()
        
        # Percorre cada símbolo (caractere) da palavra
        for c in lAtual:
            encontrou = False  # Marca se foi encontrada uma transição válida para o símbolo atual
            
            # Procura uma transição que parta do estado atual com o símbolo lido
            for i in instrucoes:
                if i[0] == atual and i[1] == c:
                    atual = i[2]     # Atualiza o estado atual para o destino da transição
                    encontrou = True # Indica que encontrou uma transição válida
                    break
            
            # Se não encontrou uma transição compatível, a palavra é inválida
            if not encontrou:
                linhaValida = False
                break
        
        if linhaValida and atual in eFinal:
            print(f"{lAtual} → Válido")
            resultado = f"{lAtual} → Válido\n"
        else:
            print(f"{lAtual} → Inválido")
            resultado = f"{lAtual} → Inválido\n"

        # Escreve o resultado (válido/inválido) no arquivo "resultado.txt"
        saida.write(resultado)
