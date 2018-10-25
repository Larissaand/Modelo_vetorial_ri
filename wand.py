import unicodedata
import re
from heap import myheap
import heapq
import pickle
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

def sort_tp(tp):
    if len(tp) > 0:
        new_tp = [tp.pop()]
        for e in tp:
            i = 0
            while i < len(new_tp) and e[1] < new_tp[i][1]:
                i+=1
            if i < len(new_tp):
                new_tp.insert(i, e)
            else:
                new_tp.append(e)
        return new_tp
    else:
        return []

def tokenize(palavra):
    palavra = palavra.lower()
    nfkd = unicodedata.normalize('NFKD', palavra)
    token = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    return [lemmatize(w) for w in re.sub('[^a-z0-9 \\\]', '', token).split(' ') if len(w) > 1]

class Wand(object):
    def __init__(self):
        infile = open('dumps/dictionary_lemmatized','rb')
        self.dict = pickle.load(infile)
        infile.close()
        
        infile = open('dumps/post_w','rb')
        self.post_list = pickle.load(infile)
        infile.close()

        infile = open('dumps/idf_lem','rb')
        self.idf = pickle.load(infile)
        infile.close()

        infile = open('dumps/norma_doc','rb')
        self.norma_doc = pickle.load(infile)
        infile.close()


    def post(self, token):
         return self.post_list[self.dict[token]][1::]

    def consulta(self):
        print("Digite uma consulta:\n(Digite q para sair)")
        query = input()
        while query != 'q':
            tokens = tokenize(query)
            relevantes = self.wand(tokens)
            for i in relevantes:
                id_doc, similaridade = i
                print('id_doc:', id_doc, 'similaridade:', similaridade)
            print('\n')
            print("Digite uma nova consulta:\n(Digite q para sair)")
            query = input()

    def wand(self, tokens):
        tokens_sr = {}
        freq_token=0
        for token in tokens:
            if token not in tokens_sr:
                for comp_token in tokens:
                    if token==comp_token:
                        freq_token+=1
                tokens_sr[token] = freq_token
            freq_token = 0
            
        tresh = 0
        flag = True
        i = 0
        heap = myheap()
        listas = {}
        listas2 = {}
        relevantes = []
        for token in tokens:
            if token in self.dict:
                l = self.post(token)
                if len(l) > 65:
                    listas[token] = l[1:66:]
                    listas2[token] = l[66::]
                else:
                    listas[token] = l

        for i in range(64):
            for token in listas:
                if i < len(listas[token]):
                    tp = listas[token][i]
                    peso = tp[1]*self.idf[token]*self.idf[token]*tokens_sr[token]
                    heap.push((tp[0],peso))
        for token in listas2:
            tp = listas2[token][0][1]*self.idf[token]*self.idf[token]*tokens_sr[token]
            if listas2[token][0][0] in heap.d:
                if tp + heap.d[listas2[token][0][0]] > heap.tail()[1]:
                    for i in listas2[token]:
                        heap.push((i[0], tp))

        for i in range(20):
            if heap.heap:
                tp = heap.pop()
                relevantes.append((tp[0], tp[1]/self.norma_doc[tp[0]]))
            else:
                break
            
        relevantes = sort_tp(relevantes)
        return relevantes
        
            

if __name__ == '__main__':
    _M = Wand()
    _M.consulta()           
            
        

        
        
                
                    
                
            
        
                

                
                
            










    
