import NLP_processing as cleaner
import json
from os import remove
import boto3


AWS_ACCESS_KEY_ID = 'AKIAQ6I2MOXSLD4G2YGT'
AWS_SECRET_ACCESS_KEY = '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'

def generate_filename(filename_boto3):
    return filename_boto3[-10:]

def generate_temporal_json(lista_jsons, filename_boto3):
    with open(filename_boto3, "w", encoding = 'utf-8') as fout:
        json.dump(lista_jsons, fout)

def exists(obj, data):
    keys = [k['link'] for k in data]
    if obj['link'] in keys:
        return True
    return False

def delete_obj(key, data):
    return [o for o in data if o['link'] != key]

class clean_S3_loader:
    def __init__(self):
        self.S3connection()
        self.bucket = self.s3.Bucket('tracktrend.cleaneddata')
        self.list_files = [obj.key for obj in self.bucket.objects.all()]
        Cleaned_data = cleaner.NLP_processing()
        print('---------------------------------')
        self.load_posts(Cleaned_data.cleaned_posts)
        self.load_products(Cleaned_data.cleaned_products)

    def S3connection(self):
        "Establishes connection with S3"
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.s3 = session.resource('s3', region_name='eu-west-3')
    
    def load_posts(self, posts):
        for p in posts:
            print(p["filename"])
            if p["filename"] not in self.list_files:
                self.upload_obj_noexisfile(p["filename"], p)
            else:
                self.upload_obj_exisfile(p["filename"], p)
        
    def load_products(self, products):
        generate_temporal_json(products, 'productes_temporal.json')
        self.s3.meta.client.upload_file('productes_temporal.json', 'tracktrend.cleanproducts', 'kavehome_cleanedproducts.json')
        #remove('productes_temporal.json')
        
    def upload_obj_noexisfile(self, filename_boto3, obj):
        generate_temporal_json([obj], generate_filename(filename_boto3))
        self.s3.meta.client.upload_file(generate_filename(filename_boto3), 'tracktrend.cleaneddata', filename_boto3)
        remove(generate_filename(filename_boto3))
        
    def upload_obj_exisfile(self, filename_boto3, obj):
        exist_file = self.s3.Object('tracktrend.cleaneddata', filename_boto3)
        data = json.loads(exist_file.get()['Body'].read().decode('utf-8'))
        if exists(obj,data):
            print('yes')
            data = delete_obj(obj['link'], data)
        data.append(obj)
        generate_temporal_json(data, generate_filename(filename_boto3))
        self.s3.meta.client.upload_file(generate_filename(filename_boto3), 'tracktrend.cleaneddata', filename_boto3)
        remove(generate_filename(filename_boto3))