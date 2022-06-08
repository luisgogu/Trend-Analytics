from datetime import datetime
import numpy as np
import gensim
import langid
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
from operator import itemgetter

# Language Models fasttext
def get_models(): 
    #model_ab = ['en', 'es', 'fr', 'pt', 'it']
    #model_ab = ['fr', 'pt', 'it']
    model_ab = ['en', 'es']
    model = {}
    for ab in model_ab:
        model[ab] = gensim.models.KeyedVectors.load_word2vec_format('/kaggle/input/fasttext-aligned-word-vectors/wiki.{}.align.vec'.format(ab))
    return model

# Language stopwords
def get_stopwords():
    nltk.download('stopwords')
    stop_words = {}
    stop_words["en"] = stopwords.words('english')
    stop_words["es"] = stopwords.words('spanish')
    #stop_words["fr"] = stopwords.words('french')
    #stop_words["pt"] = stopwords.words('portuguese')
    #stop_words["it"] = stopwords.words('italian')
    return stop_words


# Language detection
language_list = ['en','es']
langid.set_languages(language_list)


nfollow = [('k', 1000, 1), ('M', 1000000, 1), ('millon', 1000000, 0), ('mill.', 1000000, 0), ('mil', 1000, 0)]
# Returns the number of followers in int type
def get_followers(followers):
    if followers == "None":
        return None

    f = followers.split()
    for ab, num, s  in nfollow:

        if re.search(ab, followers):
            try:
                return int(f[0][:len(f[0])-s])*num
            except:
                return None
    
    return int(re.search(r'\d+', f[0]).group()) #in case of having a new string number abr, only the int number is returned


def text2emb(text, stop_words, model):
    if text == None: 
        return None
    lang = langid.classify(text)[0]
    word_tokens = word_tokenize(text)
    filtered_sentence = [w.lower() for w in word_tokens if not w.lower() in stop_words[lang]]
    embeddings = [model[lang][token] for token in filtered_sentence if token in model[lang].key_to_index]
    return embeddings

def relevant_info_post(post):
    post["followers"] = get_followers(post["followers"])
    post["datePublished"] = datetime.strptime(post["datePublished"][:10], '%Y-%m-%d')
    new_post = {}
    
    for label in ["id", "link", "image", "followers", "datePublished", "authorName", "authorProfile"]:
        new_post[label] = post[label]
    
    return new_post
    
def relevant_info_product(product):
    new_product = {}
    if product["Año de publicación"] != None:
        new_product["datePublished"] = datetime.strptime(product["Año de publicación"], '%d/%m/%y')
    
    for label in ["sku", "img_ambiente", "img", "id"]:
        new_product[label] = product[label]
    
    return new_product


def clean_posts(posts, stop_words, model):
    result = []
    for i in posts:
    
        emb = []

        for label in ["id", "title"]: # "description", "description2"
            emb += text2emb(i[label], stop_words, model)

        if len(i["tags"]) > 5:
            i["tags"] = i["tags"][:5]

        for t in i["tags"]:
            emb += text2emb(t, stop_words, model)
        
        # Ponderated Avg should go here
        info = relevant_info_post(i)
        info["embedding"] = np.average(emb, axis=0)
        result.append(info)
    
    return result
    
def clean_products(products, stop_words, model):
    result = []
    for i in products:
        emb = []
        for label in ["descripcion", "Material de las patas", "Materiales", "Construcción de la estructura", "Material principal", "Color principal", "Estancias"]:
            e = text2emb(i[label], stop_words, model)
            if e != None:
                emb.append(np.average(e, axis=0))
        for label in ["Colores"]:
            e = text2emb(i[label], stop_words, model)
            if e != None:
                emb.append(np.average(e, axis=0))
        for label in ["Estilo principal", "id"]:
            e = text2emb(i[label], stop_words, model)
            if e != None:
                emb.append(np.average(e, axis=0))
        for label in ["Forma del producto"]:
            e = text2emb(i[label], stop_words, model)
            if e != None:
                emb.append(np.average(e, axis=0))
        
        # Ponderated Avg should go here
        info = relevant_info_product(i)
        try:
            #info["embedding"] = np.average(emb, axis=1)
            info["embedding"] = emb
        except:
            print('emb:', emb)
            print('len emb:', len(emb))
        result.append(info)
    
    return result
    
def similarity(post, product):
    if np.isnan(product).any():
        return np.array([[0]])
    A=np.array(post)
    B=np.array(product)
    sim=cosine_similarity(A.reshape(1,-1),B.reshape(1,-1))
    return abs(sim)

def generate_scores(posts, products):

    for post in posts:

        scores = []

        if np.isnan(post["embedding"]).any():
            post["ranking"] = None
            continue

        for product in products:
            res = [product["sku"]]
            for emb in product["embedding"]:

                #if product["id"] == key_search:
                sim = similarity(post["embedding"], emb)
                res.append(sim[0][0])
            avg =np.average(res[1:], axis=0)
            res.append(avg)
            scores.append(res)
        
        post["ranking"] = sorted(scores,key=itemgetter(-1), reverse=True)[:10]

    return posts

def normalize_pop(posts):

    #v = np.random.rand(10)
    #normalized_v = v/np.linalg.norm(v)
    
    v = []
    for post in posts:
        f = post["followers"]
        if f in [np.nan, None]:  ## comentar aixo
            v.append(0)
        else:
            v.append(f)
    v = np.array(v)
    normalized_v = v/np.linalg.norm(v)

    for i in range(len(posts)):
        if normalized_v[i] == 0: ## comentar aixo
            posts[i]["followers"] = 1
        else:
            posts[i]["followers"] = normalized_v[i]
    
    return posts

# Generate dictionary of products with 0 score
def generate_dict(products):
    d = {}
    for product in products:
        d[product["sku"]] = 0
    return d

# Compute scores for each product in dictionary and sort them
def compute_scores(posts, products, d):
    for post in posts:
        for product in post["ranking"]:
            d[product[0]] += product[1] #* post["followers"]
    return sorted(d.items(), key=itemgetter(1), reverse=True)

