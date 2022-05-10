import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import math


def clean(text, stop_words, model):
    if text == None: 
        return []
    lang = langid.classify(text)[0]
    word_tokens = word_tokenize(text)
    filtered_sentence = [w.lower() for w in word_tokens if not w.lower() in stop_words[lang]]
    return filtered_sentence
    
def computeTF(wordDict, bagOfWords):
    tfDict = {}
    bagOfWordsCount = len(bagOfWords)
    for word, count in wordDict.items():
        tfDict[word] = count / float(bagOfWordsCount)
    return tfDict

def computeIDF(documents):
    
    N = len(documents)
    
    idfDict = dict.fromkeys(documents[0].keys(), 0)
    for document in idfDict:
        for word, val in document.items():
            if val > 0:
                idfDict[word] += 1
    
    for word, val in idfDict.items():
        idfDict[word] = math.log(N / float(val))
    return idfDict

def computeTFIDF(tfBagOfWords, idfs):
    tfidf = {}
    for word, val in tfBagOfWords.items():
        tfidf[word] = val * idfs[word]
    return tfidf

def TF(p, stop_words, model):
    uniqueWords = set()
    
    uniqueWords.update(clean(posts, stop_words, model))

    numOfWords = dict.fromkeys(uniqueWords, 0)

    for word in p:
        numOfWords[word] += 1

    return computeTF(numOfWords, bagOfWords)
    

def create_docs(posts):
    documents = []
    for p in posts:
        text = ''
        for label in ["id", "title", "description", "description2"]: 
            text = text + ' ' + p[label]

        for t in p["tags"]:
            text = text + ' ' + t

        documents.append(text)
    return documents

def main(posts ,stop_words, model):

    docs = create_docs(posts)
    idfs = computeIDF(docs)

    TFIDF = []

    for d in docs:
        ifDict = TF(d, stop_words, model)
        TFIDF.append(computeTFIDF(tfDict, idfs))

    df = pd.DataFrame(TFIDF)

    return df





