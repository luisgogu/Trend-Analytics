from datetime import datetime
import numpy as np
import gensim
import langid
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import string
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
from operator import itemgetter

#-------------------------------Model2-------------------------------
import cat_detector as det
from cat_detector import known

knn = det.load_knn("second_model.sav")
#---------------------------------------------------------------------

# Language Models fasttext
def get_models(): 
    model_ab = ['en', 'es', 'fr', 'pt', 'it']

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
    stop_words["fr"] = stopwords.words('french')
    stop_words["pt"] = stopwords.words('portuguese')
    stop_words["it"] = stopwords.words('italian')
    return stop_words


# Language detection
language_list = ['en','es', 'fr', 'pt', 'it']
langid.set_languages(language_list)

# Traductor
translator = {'sofás': 'sofá', 'mesas': 'mesa', 'sillas': 'silla', 'sillones': 'sillón', 'camas': 'cama', 'alfombras': 'alfombra', 'jarrones': 'jarrón', 'estanterías': 'estantería', 'escritorios': 'escritorio', 'colchones': 'colchón', 'muebles': 'mueble', 'taburetes': 'taburete', 'espejos': 'espejo', 'armarios':'armario', 'percheros': 'perchero', 'lámparas': 'lámpara', 'butacas': 'butaca', 'cambiadores': 'cambiador', 'chaiselongues': 'chaiselongue', 'cojines': 'cojín', 'cuadros': 'cuadro', 'jarras': 'jarra', 'colgadores': 'colgador', 'asientos': 'asiento', 'relojes': 'reloj', 'papeles': 'papel', 'cestos': 'cesto', 'cesta': 'cesto', 'cestas': 'cesto', 'sofas': 'sofás','sofa': 'sofá','couch': 'sofá','chairs': 'silla', 'chair': 'silla', 'armchair': 'butaca','armchairs': 'butaca','rug': 'alfombra','carpets': 'alfombra','vase': 'jarrón','vases': 'jarrones','shelving': 'estantería','shelves': 'estantería','bookstore': 'estantería','libraries': 'estantería','desk': 'escritorio','desks': 'escritorio','mattress': 'colchon','mattresses': 'colchon', 'furniture': 'mueble','library': 'estantería', 'stool': 'taburete','stools': 'taburetes','mirror': 'espejo','mirrors': 'espejo','closet': 'armario','wardrove': 'armario', 'dresser': 'cómoda','lamp': 'lámpara','lamps': 'lámpara','seat': 'silla','seats': 'silla','changer': 'armario','changers': 'armarios','cushion': 'cojín','cushions': 'cojín','picture': 'cuadro','jug': 'jarra','jugs': 'jarra','hanger': 'perchero','hangers': 'perchero','seating': 'butaca','paper': 'papel','papers': 'papel','baskets': 'cesto','table': 'mesa', 'pillow': 'almohada', 'almohadas': 'almohada', 'pillows': 'almohada', 'drawer': 'cajón', 'cajones': 'cajón', 'drawers': 'cajón', 'zapateros': 'zapatero', 'shoerack': 'zapatero', 'shoeracks': 'zapatero'}


def classify_tags(labels, emb, words, model):
    mat, hab, col, est, mueb, form = [], [], [], [], [], []
    for tag, e, w in zip(labels, emb, words):
        if tag == 'Color':
            col.append(e)
        elif tag == 'Habitación':
            hab.append(e)
        elif tag == 'Estilo':
            est.append(e)
        elif tag == 'Material':
            mat.append(e)
        elif tag == 'Forma':
            form.append(e)
        elif tag == 'Mueble':
            if w[0] in translator:
                mueb.append(translator[w[0]])
            else:
                mueb.append(w[0])

    return mat, hab, col, est, form, mueb


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

def text2token(text, stop_words):
    if text == None: 
        return []
    lang = langid.classify(text)[0]
    text = text.translate(str.maketrans('', '', string.punctuation))
    word_tokens = word_tokenize(text)
    filtered_sentence = [(w.lower(), lang) for w in word_tokens if not w.lower() in stop_words[lang]]
    return filtered_sentence

def token2emb(filtered_sentence, model):
    embeddings = []
    for t in filtered_sentence:
        w = t[0]
        lang = t[1]
        if w in model[lang].key_to_index:
            embeddings.append(model[lang][w])
    return embeddings

def text2emb(text, stop_words, model):
    if text == None: 
        return []
    lang = langid.classify(text)[0]
    text = text.translate(str.maketrans('', '', string.punctuation))
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
        embedding = []
        labels = []
        mat, mat2, hab, hab2, col, col2, est, est2, form, form2, mueb, mueb2 = [], [], [], [], [], [], [], [], [], [], [], []

        for label in ["id", "title"]: # "description", "description2"
            emb += text2emb(i[label], stop_words, model)

        if len(i["tags"]) > 5:
            i["tags"] = i["tags"][:5]
            
        for t in i["tags"]:
            emb += text2emb(t, stop_words, model)
            words1= text2token(t, stop_words)
            labels = det.get_attr_cat(words1, model, knn, known)
            words = token2emb(words1, model)
            emb += words
            mat2, hab2, col2, est2, form2, mueb2 = classify_tags(labels, words, words1, model)
            mat += mat2
            hab += hab2
            col += col2
            est += est2
            form += form2
            mueb += mueb2

        for label in ["title", "description", "description2"]:
            words1 = text2token(i[label], stop_words)
            labels = det.get_attr_cat(words1, model, knn, known)
            words = token2emb(words1, model)
            mat2, hab2, col2, est2, form2, mueb2 = classify_tags(labels, words, words1, model)
            mat += mat2
            hab += hab2
            col += col2
            est += est2
            form += form2
            mueb += mueb2

        if mat != []:
            mat = np.average(mat, axis=0)
        embedding.append(mat)
        if hab != []:
            hab = np.average(hab, axis=0)
        embedding.append(hab)
        if col != []:
            col = np.average(col, axis=0)
        embedding.append(col)
        if est != []:
            est = np.average(est, axis=0)
        embedding.append(est)
        if form != []:
            form = np.average(form, axis=0)
        embedding.append(form)

        if emb != []:
            emb = np.average(emb, axis=0)
        embedding.append(emb)

        # Ponderated Avg should go here
        info = relevant_info_post(i)
        info["embedding"] = embedding
        info["category"] = mueb
        result.append(info)
    
    return result
    
def clean_products(products, stop_words, model):
    result = []
    for i in products:
        embedding = []

        emb = []
        for label in ["Material de las patas", "Materiales"]:
            emb += text2emb(i[label], stop_words, model)
        if emb != []:
            emb = np.average(emb, axis=0)
        embedding.append(emb)

        emb = []
        for label in ["Estancias"]:
            emb += text2emb(i[label], stop_words, model)
        if emb != []:
            emb = np.average(emb, axis=0)
        embedding.append(emb)

        emb = []
        for label in ["Colores"]:
            emb += text2emb(i[label], stop_words, model)
        if emb != []:
            emb = np.average(emb, axis=0)
        embedding.append(emb)

        emb = []
        for label in ["Estilo principal"]:
            emb += text2emb(i[label], stop_words, model)
        if emb != []:
            emb = np.average(emb, axis=0)
        embedding.append(emb)

        emb = []
        for label in ["Forma del producto"]:
            emb += text2emb(i[label], stop_words, model)
        if emb != []:
            emb = np.average(emb, axis=0)
        embedding.append(emb)

        emb = []
        for label in ["id"]:
            emb += text2emb(i[label], stop_words, model)
        if emb != []:
            emb = np.average(emb, axis=0)
        embedding.append(emb)
        
        # Ponderated Avg should go here
        info = relevant_info_product(i)
        try:
            info["embedding"] = embedding
        except:
            print('emb:', embedding)
            print('len emb:', len(embedding))
        result.append(info)
    
    return result
    
def similarity(post, product):
    if product == [] or post == []:
        return np.array([[0]])
    A=np.array(post)
    B=np.array(product)
    sim=cosine_similarity(A.reshape(1,-1),B.reshape(1,-1))
    return abs(sim)

def generate_scores(posts, products):
    print('NUM POSTS:', len(posts))

    for i, post in enumerate(posts):
        print('pos num:', i)
        print(post['category'])

        scores = []

        if post["embedding"] == [[],[],[],[],[]]:
            post["ranking"] = None
            continue

        
        elif post['category'] != []:
            for product in products:

                if product['id'].lower() in post['category']:
                    res = []

                    for emb1, emb2 in zip(post["embedding"], product["embedding"]):

                        sim = similarity(emb1, emb2)
                        res.append(sim[0][0])

                    avg = np.average(res, axis=0)
                    scores.append((product["sku"], res, avg))
        else:
            for product in products:
                res = []

                for emb1, emb2 in zip(post["embedding"], product["embedding"]):

                    sim = similarity(emb1, emb2)
                    res.append(sim[0][0])

                avg = np.average(res, axis=0)
                scores.append((product["sku"], res, avg))

        if scores != []:
            post["ranking"] = sorted(scores,key=itemgetter(2), reverse=True)[:10]
        else:
            post['ranking'] = None

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
            d[product[0]] += product[2] #* post["followers"]
    return sorted(d.items(), key=itemgetter(1), reverse=True)

