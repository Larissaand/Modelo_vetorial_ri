from lista_invertida import ListaInvertida
from busca import Busca
from dumps import tokenize, lemmatize
from wand import Wand
from vet import Vetorial
import timeit

def wrapper(func, *args, **kwargs):
    def wrapped():
        return func(*args, **kwargs)
    return wrapped

def main():
    print('Buscando lista invertida')
    try:
        arq = open('listas/lista_invertida')
        arq.close()
    except:
        print('Gerando lista invertida ...')
        print('Esse processo pode levar alguns minutos')
        l = ListaInvertida()
        print('...')
        l.get_dict()

    print('Lista invertida encontrada')
    _M = Busca()
    _W = Wand()
    _V = Vetorial()
    print('Digite "c" para fazer uma consulta.')
    print('Acrescente "t" para contar o tempo de execução.')
    print('Acrescente "w" para usar o algoritmo wand.')
    print('Acrescente "v" para usar o modelo vetorial sem stemming dos tokens.')
    print("(Digite q para cancelar)")
    p = input().lower()
    while p != 'q':
            
        if 't' in p and 'w' in p and 'c' in p:
            print("Digite uma consulta:")
            print("(Digite q para cancelar)")
            query = input()
            while query != 'q':
            	tokens = [lemmatize(w) for w in tokenize(query).split(' ') if len(w) > 1]
            	print(tokens)
            	relevantes = _W.wand(tokens)
            	for i in relevantes:
            		id_doc, similaridade = i
            		print('id_doc:', id_doc, 'similaridade:', similaridade)
            	w = wrapper(Wand.wand, _W, query)
            	time = timeit.timeit(w, number=1)
            	print('\nSua consulta demorou:', time, "s")
            	print('\n')
            	print("Digite uma nova consulta:")
            	print("(Digite 'q' para sair ou trocar de algoritmo)")
            	query = input()

        elif 'w' in p and 'c' in p:
            _W.consulta()
                      
        elif 't' in p and 'v' in p :
            print("Digite uma consulta:")
            print("(Digite q para cancelar)")
            query = input()
            while query != 'q':
                relevantes = _V.busca(tokenize(query).split(' '))
                for i in relevantes:
                    similaridade, id_doc = i
                    print('id_doc:', id_doc, 'similaridade:', similaridade)
                w = wrapper(Busca.busca, _V, query)
                time = timeit.timeit(w, number=1)
                print('\nSua consulta demorou:', time, "s")
                print('\n')
                print("Digite uma nova consulta:")
                print("(Digite 'q' para sair ou trocar de algoritmo)")
                query = input()

        elif 'v' in p and 'c' in p:
            _V.consulta()

        elif 't' in p and 'c' in p :
            print("Digite uma consulta:")
            print("(Digite q para cancelar)")
            query = input()
            while query != 'q':
                relevantes = _M.busca([lemmatize(w) for w in tokenize(query).split(' ') if len(w) > 1])
                for i in relevantes:
                    similaridade, id_doc = i
                    print('id_doc:', id_doc, 'similaridade:', similaridade)
                w = wrapper(Busca.busca, _M, query)
                time = timeit.timeit(w, number=1)
                print('\nSua consulta demorou:', time, "s")
                print('\n')
                print("Digite uma nova consulta:")
                print("(Digite 'q' para sair ou trocar de algoritmo)")
                query = input()
                      
        elif 'c' in p:
            _M.consulta()
                      
        print('Digite "c" para fazer uma consulta.')
        print('Acrescente "t" para contar o tempo de execução.')
        print('Acrescente "w" para usar o algoritmo wand.')
        print('Acrescente "v" para usar o modelo vetorial sem stemming dos tokens.')
        print("(Digite q para cancelar)")
        p = input().lower()
    
if __name__ == '__main__':
    main()
