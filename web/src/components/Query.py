import boto3
import datetime
import S3extractor_clean as ext
import tools
import json
import pickle

AWS_ACCESS_KEY_ID = 'AKIAQ6I2MOXSLD4G2YGT'
AWS_SECRET_ACCESS_KEY = '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'

translate = {"Rug": "alfombra", "Pillow": "almohada", "Wardrobe": "armario", "Seat": "asiento", "Tray": "bandeja", "Bag": "bolsa", "Armchair": "butaca", "Box": "caja", "Drawer": "cajón", "Bed": "cama", "Changing mat": "cambiador", "Storage bed": "canapé", "Basket": "cesto", "Chaise longue": "chaiselongue", "Cushion": "cojín", "Mat": "colchoneta", "Mattress": "colchón", "Hanger": "colgador", "Curtain": "cortina", "Picture": "cuadro", "Ladder": "escalera", "Desk": "escritorio", "Mirror": "espejo", "Shelf": "estante", 
"Shelves": "estantería", "Jar": "jarra", "Vase": "jarrón", "Lamp": "lámpara", "Frame": "marco", "Table": "mesa", "Lampshade": "pantalla", "Wallpaper": "papel", "Coat racks": "perchero", "Kids protector": "protector", "Puff": "puff", "Clock": "reloj", "Footstool": "reposapies", "Chair": "silla", "Couch": "sillón", "Sofa": "sofá", "Stool": "taburete", "Suction pad": "ventosa", "Shoerack": "zapatero"}

translate2 = {"Style":"Estilo","Room":"Habitación","Color":"Color","Material":"Material"}

def extract_date(l):
    if l is None:
        return l
    print(l)
    return datetime.date(l[0:4], l[5:7], l[8:10])

def treat_scores(p):
    scores = []
    if p["ranking"] is None:
        return p
    for score_p in p["ranking"]:
        scores.append([score_p[0], float(score_p[2])])
    p["ranking"] = scores
    return p

class Answer_Query_Alg1:
    def __init__(self, query):
        self.S3connection()
        print(query)
        print(query['from'])
        products = [translate[p] for p in query['product']]
        
        self.extraction = ext.clean_S3_extractor(initial_date = extract_date(query['from']),end_date = extract_date(query['to']),products = products)
        self.dic = tools.generate_dict(self.extraction.filtered_products)
        self.ranking = tools.compute_scores(self.extraction.filtered_posts, self.extraction.filtered_products, self.dic)

    def S3connection(self):
        "Establishes connection with S3"
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.s3 = session.resource('s3', region_name='eu-west-3')
        
class Answer_Query_Alg2:
    def __init__(self, query):
        self.S3connection()
        products = [translate[p] for p in query['product']]
        
        self.extraction = ext.clean_S3_extractor(products = products)
        self.dic = tools.compute_ranking_characteristics(self.extraction.filtered_posts, translate2[query["feature"]])

    def S3connection(self):
        "Establishes connection with S3"
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.s3 = session.resource('s3', region_name='eu-west-3')  