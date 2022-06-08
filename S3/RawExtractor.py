import boto3
from datetime import datetime
import json
import re
import gensim
import pickle

AWS_ACCESS_KEY_ID = 'AKIAQ6I2MOXSLD4G2YGT'
AWS_SECRET_ACCESS_KEY = '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'
nfollow = [('k', 1000, 1), ('M', 1000000, 1), ('millon', 1000000, 0), ('mill.', 1000000, 0), ('mil', 1000, 0)]

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
    if isinstance(f[0], int):
        return int(re.search(r'\d+', f[0]).group()) #in case of having a new string number abr, only the int number is returned
    return None

def clean_post(json_obj, filename):
    new_post = {}
    new_post["filename"] = filename
    new_post['followers'] = get_followers(json_obj["followers"])
    if json_obj["datePublished"] is not None:
        new_post['datePublished'] = datetime.strptime(json_obj["datePublished"][:10], '%Y-%m-%d')
    else:
        new_post['datePublished'] = json_obj["datePublished"]
    new_post['id'] = json_obj['id']
    new_post['title'] = json_obj['title']
    new_post['description'] = json_obj['description']
    new_post['description2'] = json_obj['description2']
    new_post['link'] = json_obj['link']
    new_post['image'] = json_obj['image']
    new_post['tags'] = json_obj['tags']
    return new_post

def clean_product(json_obj):
    new_product = {}
    for label in ["descripcion", "Material de las patas", "Materiales", "Estancias",
                  "Construcción de la estructura", "img","sku", "img_ambiente","id","Estilo principal",
                  "Forma del producto", "Material principal", "Color principal", "Colores"]:
        new_product[label] = json_obj[label]
    if json_obj["Año de publicación"] is not None:
        new_product["datePublished"] = datetime.strptime(json_obj["Año de publicación"], '%d/%m/%y')
    else:
        new_product["datePublished"] = None
    return new_product

class raw_S3_extractor:
    def __init__(self):
        self.S3connection()
        self.bucketPosts = self.s3.Bucket('tracktrend.extracciones')
        self.clean_posts = []
        self.clean_products = []
        self.list_of_posts = [obj.key for obj 
                in self.bucketPosts.objects.filter(Prefix= "2013/").all()]
        self.extract_docs_products()
        self.extract_docs_posts()
        self.stopwords = self.get_stopwords()
        self.models = self.get_models()
        self.knn = self.get_knn()
        
    def S3connection(self):
        "Establishes connection with S3"
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.s3 = session.resource('s3', region_name='eu-west-3')
        
    def get_stopwords(self):
        obj = self.s3.Object('tracktrend.models', 'stop_words.pickle')
        body_string = obj.get()['Body'].read()
        stop1 = pickle.loads(body_string)
        obj = self.s3.Object('tracktrend.models', 'stop_words-2.pickle')
        body_string = obj.get()['Body'].read()
        stop2 = pickle.loads(body_string)
        stop = {}
        for k in stop1.keys():
            stop[k] = stop1[k]

        for k in stop2.keys():
            stop[k] = stop2[k]
        return stop
    
    def get_models(self):
        file_to_read1 = open("models/model.pickle", "rb")
        model1 = pickle.load(file_to_read1)
        file_to_read1.close()
        file_to_read2 = open("models/model2.pickle", "rb")
        model2 = pickle.load(file_to_read2)
        file_to_read2.close()
        model = {}
        for k in model1.keys():
            model[k] = model1[k]

        for k in model2.keys():
            model[k] = model2[k]
        return model
    
    def get_knn(self):
        path = "models/model_v6.sav"
        return pickle.load(open(path, 'rb'))
   
    def extract_docs_posts(self):
        "Extract the files selected from bigpapa project and treat data extracted"
        for filename in self.list_of_posts:
            print(filename)
            obj = self.s3.Object('tracktrend.extracciones', filename)
            data = ''
            # read the data
            data += obj.get()['Body'].read().decode('utf-8')
            # pass data to json format
            self.lista_json_posts = json.loads(data)
            # filter and clean list of dictionaries
            self.convert_json_post(filename)
            
    def extract_docs_products(self):
        "Extract the files selected from bigpapa project and treat data extracted"
        obj = self.s3.Object('tracktrend.kaveproducts', 'kavehome-clean.json')
        data = ''
        # read the data
        data += obj.get()['Body'].read().decode('utf-8')
        # pass data to json format
        self.lista_json_products = json.loads(data)
        # filter and clean list of dictionaries
        self.convert_json_product()

    def convert_json_post(self, filename):
        "For each dictionary clean the data"
        for json_obj in self.lista_json_posts:
            self.clean_posts.append(clean_post(json_obj, filename))
            
    def convert_json_product(self):
        "For each dictionary clean the data"
        for json_obj in self.lista_json_products:
            self.clean_products.append(clean_product(json_obj))