from encodings import utf_8
import nltk 

with open('dados/artigos.txt', 'r', encoding='utf8') as f:
    artigos = f.read()

lista_tokens = nltk.tokenize.word_tokenize(artigos) # Separa as palavras do texto. ex: ['Olá', ',', 'tudo', 'bem', '?']

def separa_palavras(lista_tokens):
    # Separar as palavras dos coisa (,.?!#@)
    lista_palavras = []
    for token in lista_tokens:
        if token.isalpha():
            lista_palavras.append(token)
    return lista_palavras

def normalizacao(lista_palavras):
    #Coloca todas as plavras em minusculas
    lista_normalizada = []
    for palavra in lista_palavras:
        lista_normalizada.append(palavra.lower())
    return lista_normalizada

def insere_letras(fatias):
    novas_palavras = []
    letras = 'abcdefghijklmnopqrstuvwxyzàáâãèéêìíîòóôõùúûç'
    for E, D in fatias:
        for letra in letras:
            novas_palavras.append(E + letra + D)
    return novas_palavras

def deletando_caracteres(fatias):
    novas_palavras = []
    for E, D in fatias:
        novas_palavras.append(E + D[1:])
    return novas_palavras

def troca_letra(fatias):
    novas_palavras = []
    letras = 'abcdefghijklmnopqrstuvwxyzáàãâéèêíìóòõôúùûç'
    for E, D in fatias:
        for letra in letras:
            novas_palavras.append(E + letra + D[1:])
    return novas_palavras

def inverte_letra(fatias):
    novas_palavras = []
    for E, D in fatias:
        if len(D) > 1:
            novas_palavras.append(E + D[1] + D[0] + D[2:])
    return novas_palavras

def gerador_palavras(palavra):
    fatias = []
    for i in range(len(palavra)+1):
        fatias.append((palavra[:i],palavra[i:]))
    palavras_geradas = insere_letras(fatias)
    palavras_geradas += deletando_caracteres(fatias)
    palavras_geradas += troca_letra(fatias)
    palavras_geradas += inverte_letra(fatias)
    return palavras_geradas
    
def gerador_turbinado(palavras_geradas):
    novas_palavras = []
    for palavra in palavras_geradas:
        novas_palavras += gerador_palavras(palavra)
    return novas_palavras
    
def corretor(palavra):
    palavras_geradas = gerador_palavras(palavra)
    palavra_correta = max(palavras_geradas, key=probabilidade)
    return palavra_correta

def novo_corretor(palavra):
    palavras_geradas = gerador_palavras(palavra)
    palavras_turbinado = gerador_turbinado(palavras_geradas)
    todas_palavras = set(palavras_geradas + palavras_turbinado)
    candidatos = [palavra]
    for palavra in todas_palavras:
        if palavra in vocabulario:
            candidatos.append(palavra)
    print(len(candidatos))
    palavra_correta = max(candidatos, key=probabilidade)
    return palavra_correta


def probabilidade(palavra_gerada):
    return frequencia[palavra_gerada]/total_palavras * 100

lista_palavras = separa_palavras(lista_tokens)
lista_normalizada = normalizacao(lista_palavras)
frequencia = nltk.FreqDist(lista_normalizada) # Frequencia em que as palavras apareceram
total_palavras = len(lista_normalizada)


#print(corretor('lgica'))

def cria_dados_teste(nome_arquivo):
    lista_palavras_teste = []
    f = open(nome_arquivo, 'r', encoding='utf8')
    for linha in f:
        correta = linha.split()[0]
        errada = linha.split()[1]
        lista_palavras_teste.append((correta, errada))
    f.close()
    return lista_palavras_teste

lista_teste = cria_dados_teste("dados/palavras.txt")

def avaliador(testes, vocabulario):
    numero_palavras = len(testes)
    acertou = 0
    desconhecida = 0
    for correta, errada in testes:
        palavra_corrigida = corretor(errada)
        if palavra_corrigida == correta:
            acertou += 1
        else:
            desconhecida += (correta not in vocabulario)
    taxa_acerto = round(acertou*100/numero_palavras, 2)
    taxa_desconhecida = round(desconhecida*100/numero_palavras, 2)
    print(f"{taxa_acerto}% de {numero_palavras} palavras, desconhecidas é {taxa_desconhecida}%")


vocabulario = set(lista_normalizada)
avaliador(lista_teste, vocabulario)

palavra = "lóigica"
print(novo_corretor(palavra))
print(corretor(palavra))
