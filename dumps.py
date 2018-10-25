import pickle
import unicodedata
import re
import os

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
	return re.sub('[^a-z0-9 \\\]', '', token)

def sort_tp(tp, mode='v'):
    new_tp = [tp.pop()]
    for e in tp:
        i = 0
        if mode == 'v':
            while i < len(new_tp) and e[0] < new_tp[i][0]:
                i+=1
        else:
            while i < len(new_tp) and e[1] > new_tp[i][1]:
                i+=1
        if i < len(new_tp):
            new_tp.insert(i, e)
        else:
            new_tp.append(e)
    return new_tp

def generate_dumps(ndocs):
    arq = open("listas/lista_invertida", 'r')
    txt = arq.readlines()
    arq.close()

    idf = {}
    idf_lem = {}
    dictionary = {}
    dictionary_lemmatized = {}
    post_list = {}
    post_w = {}
    count = 0
    for i in range(len(txt)):
        line = txt[i].split(' ')
        token = line[0]
        token = tokenize(token)
        if len(token) > 0:
            idf[token] = float(line[1])
            dictionary[token] = count
            token_lem = lemmatize(token) 
            dictionary_lemmatized[token_lem] = count
            idf_lem[token_lem] = float(line[1])
            post_list[count] = [len(line[2::])]
            post_w[count] = [len(line[2::])]
            tuple_list = []
            for tupla in line[2::]:
                try:
                    tuple_list.append(eval(tupla))
                except:
                    pass
            tl = []
            for i in tuple_list:
                tl.append(i)
            post_list[count] += sort_tp(tuple_list)
            post_w[count] += sort_tp(tl, mode='w')
            count += 1
        
    freq_doc = {}
    for doc_id in range(1, ndocs+1):
        freq_doc[doc_id] = {}
        for token in dictionary:
            index = dictionary[token]
            for l in post_list[index][1::]:
                if l[0] == doc_id:
                    freq_doc[doc_id][token] = l[1]

    norma_doc = {}
    doc_temp = {}
    pal_rep = {}
    for doc_index in range(1, ndocs+1):
        s = 0
        doc_temp = freq_doc[doc_index]
        for token in freq_doc[doc_index]:	
            if token not in pal_rep:
                pal_rep[token] = 1
                tf = doc_temp[token]  
                w = tf*idf[token]
                s = s + (w*w)
        n_doc = s**0.5
        norma_doc[doc_index] = n_doc
        doc_temp = {}
        pal_rep = {}            


    try:
        outfile = open('dumps/dictionary','wb')
    except:
        os.mkdir('./dumps')
        outfile = open('dumps/dictionary','wb')
    pickle.dump(dictionary, outfile)
    outfile.close()

    outfile = open('dumps/dictionary_lemmatized','wb')
    pickle.dump(dictionary_lemmatized, outfile)
    outfile.close()

    outfile = open('dumps/post_list','wb')
    pickle.dump(post_list,outfile)
    outfile.close()

    outfile = open('dumps/post_w','wb')
    pickle.dump(post_w,outfile)
    outfile.close()

    outfile = open('dumps/idf','wb')
    pickle.dump(idf,outfile)
    outfile.close()

    outfile = open('dumps/idf_lem','wb')
    pickle.dump(idf_lem,outfile)
    outfile.close()

    outfile = open('dumps/norma_doc','wb')
    pickle.dump(norma_doc,outfile)
    outfile.close()
