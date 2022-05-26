import boto3
import datetime
import S3extractor_clean as ext
import tools

AWS_ACCESS_KEY_ID = 'AKIAQ6I2MOXSLD4G2YGT'
AWS_SECRET_ACCESS_KEY = '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'

def extract_date(l):
    if l is None:
        return l
    return datetime.date(int(l[0:4]), int(l[5:7]), int(l[8:10]))

class Answer_Query_Alg1:
    def __init__(self, query):
        self.S3connection()
        self.extraction = ext.clean_S3_extractor(initial_date = extract_date(query['from']),end_date = extract_date(query['to']),products = query['product'])
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
        self.extraction = ext.clean_S3_extractor(products = query['product'])
        self.dic = tools.compute_ranking_characteristics(self.extraction.filtered_posts, query["feature"])

    def S3connection(self):
        "Establishes connection with S3"
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.s3 = session.resource('s3', region_name='eu-west-3')  