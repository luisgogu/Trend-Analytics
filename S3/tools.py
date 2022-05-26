from datetime import datetime
import numpy as np
import langid
from operator import itemgetter
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
from translate import Translator

language_list = ['en','es', 'fr', 'pt', 'it']
langid.set_languages(language_list)

def similarity(post, product):
    A=np.array(post)
    B=np.array(product)
    sim = cosine_similarity(A.reshape(1,-1),B.reshape(1,-1))
    return sim

def generate_scores(posts, products):

    for post in posts:

        scores = []

        for product in products:
            try:
                sim = similarity(post["embedding"], product["embedding"])
            except:
                sim = np.array([[0]])
            scores.append((product["sku"], list(sim)[0][0]))
        
        post["ranking"] = sorted(scores,key=itemgetter(1), reverse=True)[:10]

    return posts

def normalize_pop(posts):

    v = np.random.rand(10)
    normalized_v = v/np.linalg.norm(v)
    
    v = []
    for post in posts:
        v.append(post["followers"])
    v = numpy.array(v)
    normalized_v = v/np.linalg.norm(v)

    for i in range(len(posts)):
        posts[i]["followers"] = normalized_v[i]
        
# Generate dictionary of products with 0 score
def generate_dict(products):
    d = {}
    for product in products:
        d[product["sku"]] = (0,product['id'],product['img'])
    return d


def compute_scores(posts, products, d):
    for post in posts:
        if post["followers"] is None:
            continue
        if post['ranking'] is not None:
            for product in post["ranking"]:
                d[product[0]] = (d[product[0]][0] + product[1]*post["followers"], d[product[0]][1], d[product[0]][2])  
    result = {"products":[]}
    for t in sorted(d.items(), key=itemgetter(1), reverse=True)[:10]:
        result["products"].append({"product": t[1][1],"popularity": t[1][0],"url": t[1][2]}) 
    return result
               
def intersect(searched, substring_search):
    return sum([1 for i in range(len(searched)) if searched[i] == substring_search[i]])

def compute_conv(i, searched, string_search):
    # zero padding
    if i - len(searched) + 1 < 0:
        return intersect(searched[-(i+1):], string_search[0:i+1])/len(searched)
    elif i > len(string_search):
        return intersect(searched[:len(searched)-(i-len(string_search))], string_search[i-len(searched):])/len(searched)
    elif i == len(string_search):
        return intersect(searched, string_search[i-len(searched):])/len(searched)
    else:
        return intersect(searched, string_search[i-len(searched)+1:i+1])/len(searched)

def max_convolution(w1, w2):
    if len(w1) > len(w2):
        return max([compute_conv(i,w2, w1) for i in range(len(w1)+len(w2))])
    return max([compute_conv(i,w1, w2) for i in range(len(w1)+len(w2))])

def exists(m,d):
    if len(list(d.keys())) == 0:
        return (None, False)
    conv_res = [max_convolution(m, w) for w in list(d.keys())]
    if max(conv_res) > 0.85:
        word_hit = list(d.keys())[conv_res.index(max(conv_res))]
        return (word_hit, True)
    return (None, False)

def compute_ranking_characteristics(posts,feature):
    d = {"Feature":{}}
    for p in posts:
        if p["followers"] is None:
            p["followers"] = 0
        for m in p["attributes"][feature]:
            w = exists(m,d["Feature"])
            if w[1]:
                d["Feature"][w[0]] += p["followers"]
            else:
                d["Feature"][m] = p["followers"]
    d = translate(d)
    result = {"Feature": []}          
    for t in sorted(d["Feature"].items(), key=itemgetter(1), reverse=True)[:10]:
        result["Feature"].append(t[0])
    return result
                
def translate(d):
    new_d = {"Feature":{}}
    for c in d:
        for w in d[c]:
            lang = langid.classify(w)[0]
            translator = Translator(from_lang=lang,to_lang="es")
            new_w = translator.translate(w)
            if new_w not in new_d:
                new_d[c][new_w] = d[c][w]
            else:
                new_d[c][new_w] += d[c][w]
    return new_d