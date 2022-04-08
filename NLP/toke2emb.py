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
			return int(f[0][:len(f[0])-s])*num
			
	return int(re.search(r'\d+', f[0]).group()) #in case of having a new string number abr, only the int number is returned


def text2emb(text):
    lang = langid.classify(text)[0]
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words[lang]]
    embeddings = [model[lang][token] for token in filtered_sentence if token in model[lang].key_to_index]
    return embeddings

def relevant_info_post(post):
    post["followers"] = get_followers(post["followers"])
    post["datePublished"] = datetime.strptime(post["datePublished"][:10], '%Y-%m-%d')
    new_post = {}
    
    for label in ["link", "image", "followers", "datePublished"]:
        new_post[label] = post[label]
    
    return new_post
    
def relevant_info_product(product):
    new_product = {}
    new_product["datePublished"] = datetime.strptime(product["Año de publicación"], '%d/%m/%Y')
    
    for label in ["sku", "img_ambiente", "img"]:
        new_product[label] = product[label]
    
    return new_product


def clean_posts(posts):
    result = []
    for i in posts:
    
        emb = []
        for label in ["title", "description", "description2"]:
            emb += text2emb(i[label])
        
        # Ponderated Avg should go here
        info = relevant_info_post(i)
        info["embedding"] = np.average(emb, axis=0)
        result.append(info)
    
    return result
    
def clean_products(products):
    result = []
    for i in products:
        emb = []
        for label in ["descripcion", "Material de las patas", "Materiales", "Construcción de la estructura", "Forma del producto", "Material principal", "Color principal", "Colores", "Estancias", "id"]:
            emb += text2emb(i[label])
        
        # Ponderated Avg should go here
        info = relevant_info_product(i)
        info["embedding"] = np.average(emb, axis=0)
        result.append(info)
    
    return result
    
def similarity(post, product):
    A=np.array(post)
	B=np.array(product)
	sim=cosine_similarity(A.reshape(1,-1),B.reshape(1,-1))
	return sim

def generate_scores(posts, products):

    for post in posts:

        scores = []

        for product in products:

            sim = similarity(post["embedding"], product["embedding"])
            scores.append((post["sku"], sim))
        
        post["ranking"] = sorted(scores,key=itemgetter(1), reverse=True)[:10]

    return posts

def nor_malize_pop(posts):

    v = np.random.rand(10)
    normalized_v = v/np.linalg.norm(v)
    
    v = []
    for post in posts:
        v.append(post["followers"])
    v = numpy.array(v)
    normalized_v = v/np.linalg.norm(v)

    for i in range(len(posts)):
        posts[i]["followers"] = normalized_v[i]
    
    return posts
