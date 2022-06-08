import boto3
import datetime
import json
import re

nfollow = [('k', 1000, 1), ('M', 1000000, 1), ('millon', 1000000, 0), ('mill.', 1000000, 0), ('mil', 1000, 0)]

def get_followers(followers):
    if followers == "None":
        return None
    
    f = followers.split()
    for ab, num, s  in nfollow:
        if re.search(ab, followers):
            return int(f[0][:len(f[0])-s])*num
    
    return int(re.search(r'\d+', f[0]).group()) #in case of having a new string number abr, only the int number is returned

def clean_post(json_obj):
    new_post = {}
    new_post['followers'] = get_followers(json_obj["followers"])
    new_post['datePublished'] = datetime.datetime.strptime(json_obj["datePublished"][:10], '%Y-%m-%d')
    new_post['title'] = json_obj['title']
    new_post['description'] = json_obj['description']
    new_post['description2'] = json_obj['description2']
    new_post['link'] = json_obj['link']
    new_post['image'] = json_obj['image']
    return new_post

def extract_product(filename):
    return filename.split('/')[3]

def treat_number(num_in_str):
    "From day in string to integer"
    # Day in range 1-9
    if num_in_str[0] == '0':
        return int(num_in_str[1])
    return int(num_in_str)

def is_contained(filename, initial_date, end_date):
    "Checks if the date of the filename is contained in the desired interval"
    # extract initial day from filename date
    print(filename)
    day = datetime.date(int(filename[0:4]), treat_number(filename[5:7]), treat_number(filename[8:10]))
    # true if filename date in range: [initial date, end date]
    return day >= initial_date and day <= end_date


class S3_extractor:
    def __init__(self, initial_date=None, end_date=None,products=None,select_attrs = None):
        self.S3connection()
        self.products = products
        self.my_bucket = self.s3.Bucket('bucketpruebarichi')
        self.filtered_posts = []
        self.list_of_docs = [flnm for flnm 
                             in self.filter_by_date(initial_date, end_date) 
                             if len(flnm) > 10
                             ]
        self.extract_docs(select_attrs)
        
    def S3connection(self):
        "Establishes connection with S3"
        sqs = boto3.resource('sqs')
        self.s3 = boto3.resource('s3')
                    
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
                if self.products is not None:
                    if extract_product(filename.key) in self.products and is_contained(filename.key, initial_date, end_date):
                        filtered_posts.append(filename.key)
                else:
                    if is_contained(filename.key, initial_date, end_date):
                        filtered_posts.append(filename.key)
        return filtered_posts
    
    def extract_docs(self, select_attrs):
        "Extract the files selected from bigpapa project and treat data extracted"
        for filename in self.list_of_docs:
            print(filename)
            obj = self.s3.Object('bucketpruebarichi', filename)
            data = ''
            # read the data
            data += obj.get()['Body'].read().decode('utf-8')
            # pass data to json format
            self.lista_json = json.loads(data)
            # filter and clean list of dictionaries
            self.filter_and_convert_json(select_attrs)

    def filter_and_convert_json(self, select_attrs):
        "For each dictionary (initiative) clean the data and filter attributes"
        if select_attrs is not None:
            for json_obj in self.lista_json:
                self.filtered_posts.append(clean_and_select(json_obj, select_attrs))
        else:
            for json_obj in self.lista_json:
                self.filtered_posts.append(clean_post(json_obj))