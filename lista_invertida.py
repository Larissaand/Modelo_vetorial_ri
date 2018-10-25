import glob
import math
import dumps as dp
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


class ListaInvertida(object):
    keywords = ["PN","RN","AN","SO","RF","CT"]
    text_keywords = ["AU","TI","MJ","MN","AB","EX"]
    def __init__(self, col=None):
        if col:
            self.col = glob.glob(col)
        else:
            self.col = glob.glob("cfc/cf7*")
        self.dict = {}
        self.lista = {}

    def get_dict(self):
        self.ndocs = 1
        doc = 1
        for file in self.col:
            try:
                arq = open(file, "r")
            except FileNotFoundError:
                return
            lines = arq.readlines()
            if len(lines) > 0:
                line = 1
            else:
                arq.close()
                print('ERROR reading lines in', file)
                return
            while line < len(lines):
                if lines[line][:2:1] == "RN":
                        for i in range(len(lines[line].replace('\n',"").replace(' ',""))):
                            try:
                                doc = int(lines[line][i::])
                                break
                            except:
                                pass
                        self.ndocs += 1
                elif lines[line][:2:1] in self.text_keywords:
                    for word in lines[line][3::1].lower().replace(')',"").replace('(',"").replace('"',"").replace(";","").replace(",","").replace("\n", "").replace(".","").replace(":","").split(" "):
                        if len(word) > 1:
                            word = lemmatize(word)
                        if len(word) > 1 and word not in self.keywords:
                            if word in self.dict.keys() and doc in self.dict[word].keys():
                                self.dict[word][doc] += 1
                            elif word in self.dict.keys():
                                self.dict[word][doc] = 1
                            else:
                                try:
                                    k = int(word)
                                except:
                                    self.dict[word] = {doc:1}
                elif lines[line][:2:1] == "RF":
                    while lines[line][:2:1] not in self.keywords:
                        line += 1
                elif lines[line][:2:1] in self.keywords and lines[line][:2:1] != "PN":
                    pass
                else:
                    for word in lines[line].lower().replace('"',"").replace(";","").replace(",","").replace("\n", "").replace(".","").replace(":","").replace("(","").replace(")","").split(" "):
                        if len(word) > 0 and word not in self.keywords:
                            if word in self.dict.keys() and doc in self.dict[word].keys():
                                self.dict[word][doc] += 1
                            elif word in self.dict.keys():
                                self.dict[word][doc] = 1
                            else:
                                try:
                                    k = int(word)
                                except:
                                    self.dict[word] = {doc:1}
                line += 1
            arq.close()
        self.generate_list()

    def generate_list(self):
        arq = open("lista_invertida", 'w')
        for word in self.dict.keys():
            idf = math.log(self.ndocs/len(list(self.dict[word].keys())),2)
            arq.write(word+" "+str(idf)+" ")
            for doc in self.dict[word].keys():
                arq.write("("+str(doc)+','+ str(self.dict[word][doc])+ ") ")
            arq.write("\n")
        arq.close()
        dp.generate_dumps(self.ndocs)

     
        

if __name__ == '__main__':
    l = ListaInvertida()
    l.get_dict()
