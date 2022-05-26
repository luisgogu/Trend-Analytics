import boto3
import datetime
import json
import re


AWS_ACCESS_KEY_ID = 'AKIAQ6I2MOXSLD4G2YGT'
AWS_SECRET_ACCESS_KEY = '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'


def extract_product(filename):
    return filename.split('/')[3]

def treat_number(num_in_str):
    "From day in string to integer"
    # Day in range 1-9
    if num_in_str[0] == '0':
        return int(num_in_str[1])
    return int(num_in_str)

def treat_scores(p):
    scores = []
    if p["ranking"] is None:
        return p
    for score_p in p["ranking"]:
        scores.append([score_p[0], float(score_p[2])])
    p["ranking"] = scores
    return p

def is_contained(filename, initial_date, end_date):
    "Checks if the date of the filename is contained in the desired interval"
    # extract initial day from filename date
    day = datetime.date(int(filename[0:4]), treat_number(filename[5:7]), treat_number(filename[8:10]))
    # true if filename date in range: [initial date, end date]
    return day >= initial_date and day <= end_date


class clean_S3_extractor:
    def __init__(self, initial_date=None, end_date=None,products=[]):
        self.S3connection()
        self.products = products
        self.my_bucket = self.s3.Bucket('tracktrend.cleaneddata')
        self.filtered_posts = []
        self.list_of_docs = [flnm for flnm 
                             in self.filter_by_date(initial_date, end_date) 
                             ]
        self.filtered_products = []
        self.extract_posts()
        self.extract_products()
    
    def S3connection(self):
        "Establishes connection with S3"
        session = boto3.Session(
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        )
        self.s3 = session.resource('s3', region_name='eu-west-3')
                    
    def filter_by_date(self, initial_date, end_date):
        "Contemplates all possible cases of entry of date parameters"
        # Both dates have been defined
        if (isinstance(initial_date, datetime.date) and 
                isinstance(end_date, datetime.date)):
            return self.filter_by_date_complete_range(initial_date, end_date)
        # Only initial date has been defined
        elif (isinstance(initial_date, datetime.date) and 
                end_date is None):
            return self.filter_by_initial_date(initial_date)
        # Only end date has been defined
        elif (isinstance(end_date, datetime.date) and 
                    initial_date is None):
            return self.filter_by_end_date(end_date)
        # Both dates not defined
        elif (initial_date is None and 
                end_date is None):
            candidates = [f.key for f in self.my_bucket.objects.filter(Prefix="2")]
            if self.products is not None:
                filtered_posts = []
                for filename in candidates:
                    if extract_product(filename) in self.products:
                        filtered_posts.append(filename)
                    elif len(self.products) == 0:
                        filtered_posts.append(filename)
                return filtered_posts
            return candidates
        # Other case (error)
        else:
            raise 'error(formato fecha incorrecto)'
                
    def filter_by_date_complete_range(self,initial_date, end_date):
        "Extracts iniatitives for the case of having both dates defined"
        if initial_date.year > end_date.year:
            raise 'error(fecha fin mas grande que inicio)'
        # Access only one folder
        if initial_date.year == end_date.year:
            return self.filter_by_weeks_same_year(initial_date, end_date)
        # Access more than one folder
        else:
            return self.filter_by_weeks_dif_year(initial_date, end_date)
        
    def filter_by_initial_date(self, initial_date):
        """Extracts initiatives for the case of only initial date defined"""
        # Extract initiatives in range: [initial date , end of year of initial date]
        filtered_posts = self.filter_by_weeks_same_year(initial_date, 
                                    datetime.date(initial_date.year, 12, 31))
        following_year = initial_date.year + 1
        # Sequentially access the following available years
        while following_year < 2023:
            # Extract initiatives of whole year (extract all folder)
            candidates = [obj.key for obj 
                in self.my_bucket.objects.filter(Prefix= str(following_year)).all()]
            if self.products is not None:
                for filename in candidates:
                    if extract_product(filename) in self.products:
                        filtered_posts.append(filename)
                    elif len(self.products) == 0:
                        filtered_posts.append(filename)
            else:
                filtered_posts += candidates
            following_year += 1
        return filtered_posts
        
    def filter_by_end_date(self, end_date):
        """Extracts initiatives for the case of only end date defined"""
        # Extract initiatives in range: [beginning of year of end date, end date]
        filtered_posts = self.filter_by_weeks_same_year(
            datetime.date(end_date.year, 1, 1), end_date)
        previous_year = end_date.year - 1
        # Sequentially access the previous available years
        while previous_year > 2006:
            # Extract initiatives of whole year (extract all folder)
            candidates = [obj.key for obj 
                in self.my_bucket.objects.filter(Prefix= str(previous_year)).all()]
            if self.products is not None:
                for filename in candidates:
                    if extract_product(filename) in self.products:
                        filtered_posts.append(filename)
                    elif len(self.products) == 0:
                        filtered_posts.append(filename)
            else:
                filtered_posts += candidates
            previous_year -= 1
        return filtered_posts
        
    def filter_by_weeks_dif_year(self, initial_date, end_date):
        "Extracts initatives when initial date and end date belong to different years"
        # Extract initiatives in range: [initial date , end of year of initial date]
        filtered_posts = self.filter_by_weeks_same_year(
            initial_date, datetime.date(initial_date.year, 12, 31))        
        following_year = initial_date.year + 1
        # Sequentially access the years before the year of end date
        while following_year < end_date.year:
            # Extract initiatives of whole year (extract all folder)
            candidates = [obj.key for obj 
                           in self.my_bucket.objects.filter(Prefix= str(following_year)).all()]
            if self.products is not None:
                for filename in candidates:
                    if extract_product(filename) in self.products:
                        filtered_posts.append(filename) 
                    elif len(self.products) == 0:
                        filtered_posts.append(filename)
            else:
                filtered_posts += candidates
            following_year += 1
        # Extract initiatives in range: [beginning of year of end date, end date]
        return filtered_posts + self.filter_by_weeks_same_year(
            datetime.date(end_date.year, 1, 1), end_date)
        
    def filter_by_weeks_same_year(self,initial_date, end_date):
        "Extracts initatives when initial date and end date belong to same years"
        filtered_posts = []
        # Extract initiatives of whole year
        candidates = self.my_bucket.objects.filter(Prefix= str(initial_date.year))  
        # Select initatives between range: [initial date, end date]
        for filename in candidates.all():
            if len(filename.key) > 10:
                if len(self.products) > 0:
                    if extract_product(filename.key) in self.products and is_contained(filename.key, initial_date, end_date):
                        filtered_posts.append(filename.key)
                else:
                    if is_contained(filename.key, initial_date, end_date):
                        filtered_posts.append(filename.key)
        return filtered_posts
    
    def extract_products(self):
        "Extract the files selected from bigpapa project and treat data extracted"
        obj = self.s3.Object('tracktrend.cleanproducts', 'kavehome_cleanedproducts.json')
        data = ''
        # read the data
        data += obj.get()['Body'].read().decode('utf-8')
        # pass data to json format
        self.lista_json_products = json.loads(data)
        # filter and clean list of dictionaries
        self.filter_products()
        
    def filter_products(self):
        "For each dictionary clean the data"
        for json_obj in self.lista_json_products:
            self.filtered_products.append(json_obj)
        
    def extract_posts(self):
        "Extract the files selected from bigpapa project and treat data extracted"
        for filename in self.list_of_docs:
            print(filename)
            obj = self.s3.Object('tracktrend.cleaneddata', filename)
            data = ''
            # read the data
            data += obj.get()['Body'].read().decode('utf-8')
            # pass data to json format
            new_p = []
            for k in json.loads(data):
                new_p.append(treat_scores(k))
            self.filtered_posts += new_p