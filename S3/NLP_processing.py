import RawExtractor as raw_extract
import numpy as np
import gensim
import langid
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re
import string
import cat_detector as det
from cat_detector import known
import random
import spacy
from sklearn.metrics.pairwise import cosine_similarity,cosine_distances
import operator

translator = {'sofás': 'sofa', 'mesas': 'mesa', 'sillas': 'silla', 'sillones': 'sillon', 'camas': 'cama', 'alfombras': 'alfombra', 'jarrones': 'jarron', 'estanterías': 'estanteria', 'escritorios': 'escritorio', 'colchones': 'colchon', 'taburetes': 'taburete', 'espejos': 'espejo', 'armarios':'armario', 'percheros': 'perchero', 'lámparas': 'lampara', 'butacas': 'butaca', 'cambiadores': 'cambiador', 'chaiselongues': 'chaiselongue', 'cojines': 'cojin', 'cuadros': 'cuadro', 'jarras': 'jarra', 'colgadores': 'colgador', 'asientos': 'asiento', 'relojes': 'reloj', 'papeles': 'papel', 'cestos': 'cesto', 'cesta': 'cesto', 'cestas': 'cesto', 'sofas': 'sofa','sofa': 'sofa','couch': 'sofa','chairs': 'silla', 'chair': 'silla', 'armchair': 'butaca','armchairs': 'butaca','rug': 'alfombra','carpets': 'alfombra','vase': 'jarron','vases': 'jarrones','shelving': 'estanteria','shelves': 'estanteria','bookstore': 'estanteria','libraries': 'estanteria','desk': 'escritorio','desks': 'escritorio','mattress': 'colchon','mattresses': 'colchon', 'library': 'estanteria', 'stool': 'taburete','stools': 'taburetes','mirror': 'espejo','mirrors': 'espejo','closet': 'armario','wardrove': 'armario', 'dresser': 'comoda','lamp': 'lámpara','lamps': 'lampara','seat': 'silla','seats': 'silla','changer': 'armario','changers': 'armarios','cushion': 'cojin','cushions': 'cojin','picture': 'cuadro','jug': 'jarra','jugs': 'jarra','hanger': 'perchero','hangers': 'perchero','seating': 'butaca','paper': 'papel','papers': 'papel','baskets': 'cesto','table': 'mesa', 'pillow': 'almohada', 'almohadas': 'almohada', 'pillows': 'almohada', 'drawer': 'cajon', 'cajones': 'cajon', 'drawers': 'cajon', 'zapateros': 'zapatero', 'shoerack': 'zapatero', 'shoeracks': 'zapatero',}

import spacy 
language_list = ['en','es', 'fr', 'pt', 'it']
langid.set_languages(language_list)

def syntax_detection(text, lan):
    dic = {}
    if lan == 'en':
        lan += "_core_web_sm"
    else:
        lan += "_core_news_sm"
    nlp = spacy.load(lan)
    doc = nlp(text)
    for token in doc:
        aux = {token.text: token.pos_}
        dic.update(aux)
    return dic

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
            if w in translator:
                mueb.append(translator[w])
            else:
                mueb.append(w)

    return mat, hab, col, est, form, mueb

def token2emb(filtered_sentence, model, lang):
    embeddings = []
    for w in filtered_sentence:
        if w in model[lang].key_to_index:
            embeddings.append(model[lang][w])
    return embeddings

def similarity(post, product):
    if product == [] or post == []:
        return np.array([[0]])
    A=np.array(post)
    B=np.array(product)
    sim=cosine_similarity(A.reshape(1,-1),B.reshape(1,-1))
    return abs(sim)

def relevant_info_product(product):
    new_product = {}
    for label in ["sku", "img_ambiente", "img","id"]:
        new_product[label] = product[label]
    if product["datePublished"] is not None:
        new_product["datePublished"] = product["datePublished"].isoformat()
    else:
        new_product["datePublished"] = product["datePublished"]
    return new_product

def relevant_info_post(post):
    new_post = {}
    for label in ["link", "image", "followers", "filename"]:
        new_post[label] = post[label]
    return new_post

def text2token(text, stop_words):
    if text == None: 
        return []
    text =  re.sub('[0-9]', '', text)
    lang = langid.classify(text)[0]
    text = text.translate(str.maketrans('', '', string.punctuation))
    word_tokens = word_tokenize(text)
    filtered_sentence = [w.lower() for w in word_tokens if not w.lower() in stop_words[lang]]
    return filtered_sentence, lang

def token2emb(filtered_sentence, model, lang):
    embeddings = []
    for w in filtered_sentence:
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

def classify_words(text, stop_words, model,attr, knn):
    text =  re.sub(r'[^\w\s]', '', text)
    text =  re.sub('[0-9]', '', text)
    lang = langid.classify(text)[0]
    type_word = syntax_detection(text, lang)
    if lang in model:
        for w in type_word:
            if not w.lower() in stop_words[lang]:
                if type_word[w] in ['NOUN','ADJ']:
                    clas = det.get_attr_cat(w.lower(), model[lang], knn, known)
                    if clas is not None:
                        attr[clas].append(w.lower())
                    

def generate_scores(post, products, embedding):
    scores = []

    if embedding == [[],[],[],[],[]]:
        return None
        
    elif post['category'] != []:
        for product in products:

            if product['id'].lower() in post['category']:
                res = []

                for emb1, emb2 in zip(embedding, product["embedding"]):

                    sim = similarity(emb1, emb2)
                    res.append(sim[0][0])

                avg = np.average(res, axis=0)
                scores.append((product["sku"], res, avg))
    else:
        for product in products:
            res = []

            for emb1, emb2 in zip(embedding, product["embedding"]):

                sim = similarity(emb1, emb2)
                res.append(sim[0][0])

            avg = np.average(res, axis=0)
            scores.append((product["sku"], res, avg))

    if scores != []:
        result = []
        #print(scores)
        for k in sorted(scores,key=operator.itemgetter(2), reverse=True)[:10]:
            result.append((k[0], str(k[1]),str(k[2])))
        return result
    else:
        return None

                    
class NLP_processing:
    def __init__(self):
        Extraction = raw_extract.raw_S3_extractor()
        print('-------------------------------')
        posts = Extraction.clean_posts
        products = Extraction.clean_products
        stop_words = Extraction.stopwords
        model = Extraction.models
        knn = Extraction.knn
        self.products = self.clean_products(products, stop_words, model)
        self.cleaned_posts = self.clean_posts(posts, stop_words, model, knn)
        self.eliminate_embeddings()
    
    def clean_posts(self,posts, stop_words, model, knn):
        result = []

        for i in posts:
            print(i["filename"])
            attr = {"Material":[],"Color":[],"Forma":[],"Estilo":[],"Habitación":[],"not_an_attr":[], "Mueble":[]}
            emb = []
            embedding = []
            labels = []
            mat, mat2, hab, hab2, col, col2, est, est2, form, form2, mueb, mueb2 = [], [], [], [], [], [], [], [], [], [], [], []

            for label in ["id", "title"]: # "description", "description2"
                emb += text2emb(i[label], stop_words, model)

            if len(i["tags"]) > 5:
                i["tags"] = i["tags"][:5]

            for t in i["tags"]:
                aux_t = t
                classify_words(aux_t, stop_words, model,attr, knn)
                emb += text2emb(t, stop_words, model)
                words1, lang = text2token(t, stop_words)
                labels = det.get_attr_cat(words1, model[lang], knn, known)
                words = token2emb(words1, model, lang)
                emb += words
                mat2, hab2, col2, est2, form2, mueb2 = classify_tags(labels, words, words1, model)
                mat += mat2
                hab += hab2
                col += col2
                est += est2
                form += form2
                mueb += mueb2

            for label in ["title", "description", "description2"]:
                aux_t = i[label]
                classify_words(aux_t, stop_words, model,attr, knn)
                words1, lang = text2token(i[label], stop_words)
                labels = det.get_attr_cat(words1, model[lang], knn, known)
                words = token2emb(words1, model, lang)
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
            info["category"] = mueb
            info["attributes"] = attr
            info["ranking"] = generate_scores(info, self.products, embedding)
            result.append(info)

        return result

    def clean_products(self,products, stop_words, model):
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
    
    def eliminate_embeddings(self):
        self.cleaned_products = []
        for p in self.products:
            p.pop("embedding")
            self.cleaned_products.append(p)
            