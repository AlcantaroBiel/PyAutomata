# Ler autômato
with open("saida.txt", "r", encoding="utf-8") as f:
    linhas = f.readlines()

estados = linhas[0].strip().split()
eInicial = linhas[1].strip()
eFinal = linhas[2].strip().split()

instrucoes = []
alfabeto = []

for lAtual in linhas[3:]:
    lAtual = lAtual.strip().split()
    if len(lAtual) != 3:
        print(f'Linha inválida: {lAtual}')
        continue
    if lAtual[0] in estados:
        if lAtual[2] in estados:
            instrucoes.append(lAtual)
        else:
            print(f'Estado destino inválido: {lAtual[2]}')
    else:
        print(f'Estado origem inválido: {lAtual[0]}')

# Ler palavras
with open("palavras.txt", "r", encoding="utf-8") as f:
    palavras = f.readlines()

# Cria (ou substitui) o arquivo de saída
with open("resultado.txt", "w", encoding="utf-8") as saida:
    for lAtual in palavras:
        atual = eInicial
        linhaValida = True
        lAtual = lAtual.strip()
        for c in lAtual:
            encontrou = False
            for i in instrucoes:
                if i[0] == atual and i[1] == c:
                    atual = i[2]
                    encontrou = True
                    break
            if not encontrou:
                linhaValida = False
                break

        if linhaValida and atual in eFinal:
            print(f"{lAtual} → Válido")
            resultado = f"{lAtual} → Válido\n"
        else:
            print(f"{lAtual} → Inválido")
            resultado = f"{lAtual} → Inválido\n"

        # Escreve no arquivo
        saida.write(resultado)
