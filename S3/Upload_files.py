import os
import boto3
import json
from os import remove

def get_product(f):
    return f.split(".")[0].lower()

def get_date(obj):
    return obj["datePublished"][0:10]

def get_year(date):
    return date[0:4]

def get_month(date):
    return date[5:7]

def get_day(date):
    return date[8:10]

def not_exists(obj, data):
    keys = [k['link'] for k in data]
    if obj['link'] in keys:
        return True
    return False

def generate_filename(date, product):
    return product + '_' + get_year(date) + '_' + get_month(date) + '_' + get_day(date) + '.json'
    
def generate_temporal_json(lista_jsons, filename_boto3):
    with open(filename_boto3, "w") as fout:
        json.dump(lista_jsons, fout)
           

def generate_path(date, product):
    return get_year(date) + '/' + get_month(date) + '/' + get_day(date) + '/' + product + '/' + generate_filename(date, product)

class Upload_Files():
    
    def __init__(self, directori = "items"):
        self.list_of_files = os.listdir(directori)
        self.s3_connection = boto3.resource('s3')
        self.bucket = self.s3_connection.Bucket('tracktrend.extracciones')
        self.list_files = [obj.key for obj in self.bucket.objects.all()]
        self.directori = directori
        self.load_all_files()
        
    def load_all_files(self):
        for f in self.list_of_files:
            self.load_single_file(f)
    
    def load_single_file(self, f):
        file = open(self.directori + '/' + f)
        self.classify_single_file(json.load(file), get_product(f))
        
    def classify_single_file(self,list_json, product):
        for obj in list_json:
            date = get_date(obj)
            if date != 'None':
                filename_boto3 = generate_path(date, product)
                if filename_boto3 not in self.list_files:
                    self.upload_obj_noexisfile(filename_boto3, obj, product, date)
                else:
                    self.upload_obj_exisfile(filename_boto3, obj, product, date)
                
    def upload_obj_noexisfile(self, filename_boto3, obj, product, date):
        generate_temporal_json([obj], generate_filename(date, product))
        self.s3_connection.meta.client.upload_file(generate_filename(date, product), 'tracktrend.extracciones', filename_boto3)
        remove(generate_filename(date, product))
     
    def upload_obj_exisfile(self, filename_boto3, obj, product, date):
        exist_file = self.s3_connection.Object('bucketpruebarichi', filename_boto3)
        data = json.loads(exist_file.get()['Body'].read().decode('utf-8'))
        if not_exists(obj,data):
            data.append(obj)
        generate_temporal_json(data, generate_filename(date, product))
        self.s3_connection.meta.client.upload_file(generate_filename(date, product), 'tracktrend.extracciones', filename_boto3)
        remove(generate_filename(date, product))