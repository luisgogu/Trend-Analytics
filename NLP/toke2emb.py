import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import os
import gensim

# Loading 200000 most common words for English (limit for loading time)
model_en = gensim.models.KeyedVectors.load_word2vec_format('/kaggle/input/fasttext-aligned-word-vectors/wiki.en.align.vec', limit=200000)
# Loading 200000 most common words for Spanish (limit for loading time)
model_es = gensim.models.KeyedVectors.load_word2vec_format('/kaggle/input/fasttext-aligned-word-vectors/wiki.es.align.vec', limit=200000)


# això ha de ser un diccionari {'language': model_name}
model = ['af', 'ar', 'bg', 'bn', 'ca', 'cs', 'cy', 'da', 'de', 'el', 'en', 'es', 'et', 'fa',
            'fi', 'fr', 'gu', 'he', 'hi', 'hr', 'hu', 'id', 'it', 'ja', 'kn', 'ko', 'lt', 'lv', 
            'mk', 'ml', 'mr', 'ne', 'nl', 'no', 'pa', 'pl', 'pt', 'ro', 'ru', 'sk', 'sl', 'so',
            'sq', 'sv', 'sw', 'ta', 'te', 'th', 'tl', 'tr', 'uk', 'ur', 'vi', 'zh-cn', 'zh-tw']
#af, am, an, ar, as, az, be, bg, bn, br, bs, ca, cs, cy, da, de, dz, el, en, eo, es, et, eu, fa, 
#fi, fo, fr, ga, gl, gu, he, hi, hr, ht, hu, hy, id, is, it, ja, jv, ka, kk, km, kn, ko, ku, ky,
#la, lb, lo, lt, lv, mg, mk, ml, mn, mr, ms, mt, nb, ne, nl, nn, no, oc, or, pa, pl, ps, pt, qu, ro, ru, rw, se, si, sk, sl, sq, sr, sv, sw, ta, te, th, tl, tr, ug, uk, ur, vi, vo, wa, xh, zh, zu
def text2emb(text):
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
    # lang = language detection
    embeddings = [model[lang][token] for token in filtered_sentence if token in model[lang].key_to_index]
    return embeddings