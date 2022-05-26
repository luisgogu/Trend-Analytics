import boto3
import datetime
import S3extractor_clean as ext
import tools

AWS_ACCESS_KEY_ID = 'AKIAQ6I2MOXSLD4G2YGT'
AWS_SECRET_ACCESS_KEY = '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'

translate = {"rug": "alfombra", "pillow": "almohada", "wardrobe": "armario", "seat": "asiento", "tray": "bandeja", "bag": "bolsa", "armchair": "butaca", "box": "caja", "drawer": "cajón", "bed": "cama", "changing mat": "cambiador", "storage bed": "canapé", "basket": "cesto", "chaise longue": "chaiselongue", "cushion": "cojín", "mat": "colchoneta", "mattress": "colchón", "hanger": "colgador", "curtain": "cortina", "picture": "cuadro", "ladder": "escalera", "desk": "escritorio", "mirror": "espejo", "shelf": "estante", 
"shelves": "estantería", "jar": "jarra", "vase": "jarrón", "lamp": "lámpara", "frame": "marco", "table": "mesa", "lampshade": "pantalla", "wallpaper": "papel", "coat racks": "perchero", "kids protector": "protector", "puff": "puff", "clock": "reloj", "footstool": "reposapies", "chair": "silla", "couch": "sillón", "sofa": "sofá", "stool": "taburete", "suction pad": "ventosa", "shoerack": "zapatero"}

def extract_date(l):
    if l is None:
        return l
    return datetime.date(int(l[0:4]), int(l[5:7]), int(l[8:10]))

class Answer_Query_Alg1:
    def __init__(self, query):
        self.S3connection()
        products = [translate[p] for p in query['product']]
        self.extraction = ext.clean_S3_extractor(initial_date = extract_date(query['from']),end_date = extract_date(query['to']),products = products)
        self.dic = tools.generate_dict(self.extraction.filtered_products)
        #self.scored_posts = tools.generate_scores(extraction.filtered_posts, extraction.filtered_products)
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
        self.dic = tools.compute_ranking_characteristics(self.extraction.filtered_posts, query["feature"])

    def S3connection(self):
        "Establishes connection with S3"
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.s3 = session.resource('s3', region_name='eu-west-3')  