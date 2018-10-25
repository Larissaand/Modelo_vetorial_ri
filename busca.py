import unicodedata
import re
import heapq
import pickle
from score import ModelScore
import nltk
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, word_tokenize

try:
    t = word_tokenize('dog')
except:
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('wordnet')

def postag(word):
    p = pos_tag(word_tokenize(word))
    return p[0][1]

def lemmatize(word):
    lemmatizer = WordNetLemmatizer()
    p = postag(word)
    if (p[0]=='J'):
         p= 'a'
    elif (p[0]=='V'):
        p= 'v'
    elif (p[0]=='N'):
        p= 'n'
    elif (p[0]=='R'):
        p= 'r'
    else:
        p= 'n'
    return lemmatizer.lemmatize(word,pos=p)

def tokenize(palavra):
    palavra = palavra.lower()
    nfkd = unicodedata.normalize('NFKD', palavra)
    token = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return [lemmatize(w) for w in re.sub('[^a-z0-9 \\\]', '', token).split(' ') if len(w) > 1]

class Busca(object):
    def __init__(self):
        infile = open('dumps/dictionary_lemmatized','rb')
        self.dict = pickle.load(infile)
        infile.close()
        
        infile = open('dumps/post_list','rb')
        self.post_list = pickle.load(infile)
        infile.close()

        infile = open('dumps/idf_lem','rb')
        self.idf = pickle.load(infile)
        infile.close()

        infile = open('dumps/norma_doc','rb')
        self.norma_doc = pickle.load(infile)
        infile.close()

    def post(self, token):
        return self.post_list[self.dict[token]]

    def head(self, token):
        p = self.post(token)
        ponteiro = self.tokens_consulta[token]
        index = self.post_list_consulta[ponteiro]
        return p[index]
    
    def next(self,token):
        p = self.post(token)
        tam = len(p) - 1
        index = self.tokens_consulta[token]
        ponteiro = self.post_list_consulta[index]
        if(ponteiro < tam):
            ponteiro += 1
            self.post_list_consulta[index] = ponteiro
            return True
        else:
            return False

    def consulta(self):
        _S = ModelScore()
        print("Digite uma consulta:\n(Digite q para sair)")
        query = input()
        while query != 'q':
            tokens = tokenize(query)
            relevantes = self.busca(tokens)
            for i in relevantes:
                similaridade, id_doc = i
                print('id_doc:', id_doc, 'similaridade:', similaridade)
            _S.tl(query, relevantes)
            print('\n')
            print("Digite uma nova consulta:\n(Digite q para sair)")
            query = input()
        _S.mrr()
            

    def busca(self, tokens):
        tokens_sr = {}
        self.tokens_consulta = {}
        freq_token=0
        index=0
        for token in tokens:
            if token not in self.dict:
                pass
            elif token not in tokens_sr:
                for comp_token in tokens:
                    if token==comp_token:
                        freq_token+=1
                tokens_sr[token] = freq_token
                self.tokens_consulta[token] = index
                index += 1
            freq_token = 0

        self.post_list_consulta = []
        for i in range(len(tokens_sr)):
            self.post_list_consulta.append(1)

        heap_doc = []
        heap_simi = []
        id_doc = -1 
        soma = 0.0
        if len(heap_doc)==0:		
            for token in tokens_sr:
                doc_freq = self.head(token)
                entrada_heap = ((doc_freq),token)
                heapq.heappush(heap_doc, entrada_heap)

        while len(heap_doc) != 0:
            doc_freq, token =  heapq.heappop(heap_doc)
            id_retirado, freq_retirado = doc_freq
            if self.next(token):
                doc_freq_novo = self.head(token)
                entrada_heap = ((doc_freq_novo),token)
                heapq.heappush(heap_doc, entrada_heap)
            if id_doc == -1:
                id_doc = id_retirado
                soma = self.idf[token]*self.idf[token]*freq_retirado*tokens_sr[token]
            elif id_doc == id_retirado:
                soma = soma + self.idf[token]*self.idf[token]*freq_retirado*tokens_sr[token]
            else:
                similaridade = soma/self.norma_doc[id_doc]
                entrada_heap_simi = similaridade, id_doc

                if len(heap_simi) < 20:
                    heapq.heappush(heap_simi, entrada_heap_simi)
                else:
                    menor_similaridade, id_menor = heapq.heappop(heap_simi)
                    if similaridade > menor_similaridade:
                        heapq.heappush(heap_simi, entrada_heap_simi)
                    else:
                        entrada_heap_simi = menor_similaridade, id_menor
                        heapq.heappush(heap_simi, entrada_heap_simi)
                id_doc = id_retirado
                soma = self.idf[token]*self.idf[token]*freq_retirado*tokens_sr[token]

        similaridade = soma/self.norma_doc[id_doc]
        entrada_heap_simi = similaridade, id_doc

        if len(heap_simi) < 20:
            heapq.heappush(heap_simi, entrada_heap_simi)
        else:
            menor_similaridade, id_menor = heapq.heappop(heap_simi)
            if (similaridade > menor_similaridade):
                heapq.heappush(heap_simi, entrada_heap_simi)
            else:
                entrada_heap_simi = menor_similaridade, id_menor
                heapq.heappush(heap_simi, entrada_heap_simi)

        relevantes = []
        for i in range(20):
            if heap_simi:
                relevantes.insert(0, heapq.heappop(heap_simi))
            else:
                break

        return relevantes
        
        
if __name__ == '__main__':
    _M = Busca()
    _M.consulta()
