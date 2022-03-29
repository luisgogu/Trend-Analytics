from datetime import datetime
import numpy as np
import gensim
import langid
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import re

# Language Models fasttext 
model_ab = ['en', 'es']
model = {}
for ab in model_ab:
    model[ab] = gensim.models.KeyedVectors.load_word2vec_format('/kaggle/input/fasttext-aligned-word-vectors/wiki.{}.align.vec'.format(ab))

# Language stopwords
nltk.download('stopwords')
stop_words = {}
stop_words["en"] = stopwords.words('english')
stop_words["es"] = stopwords.words('spanish')


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

def relevant_info(post):
    post["followers"] = get_followers(post["followers"])
    post["datePublished"] = datetime.strptime(post["datePublished"][:10], '%Y-%m-%d')
    new_post = {}
    
    for label in ["link", "image", "followers", "datePublished"]:
        new_post[label] = post[label]
    
    return new_post


def clean_posts(posts):
    result = []
    for i in posts:
    
        emb = []
        for label in ["title", "description", "description2"]:
            emb += text2emb(i[label])
        
        # Ponderated Avg should go here
        info = relevant_info(i)
        info["embedding"] = np.average(emb, axis=0)
        result.append(info)
    
    return result