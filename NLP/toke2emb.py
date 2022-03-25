import datetime

nfollowers = {'k': 1, 'M': 1, 'l': 3, 'n': 6, '0': 0, '1': 0, '2': 0, '3': 0, '4': 0, '5': 0, '6': 0, '7': 0, '8': 0, '9': 0}

# Returns the number of followers in int type
def get_followers(followers):
	f = followers.split()
	last_char = f[0][-1] # Extracts the last character of the number of followers

	if last_char in nfollowers:
		f = int(f[0][:-nfollowers[last_char]]) 

	else:
		print('It has occurred some error! Num followers = ', f) # check if there is some error

	return f


def text2emb(text):
    lang = langid.classify(text)[0]
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words[lang]]
    embeddings = [model[lang][token] for token in filtered_sentence if token in model[lang].key_to_index]
    return embeddings

def relevant_info(post):
    post["followers"] = get_followers(post["followers"])
    post["datePublished"] = datetime.strptime(post["datePublished"], '%Y-%m-%d %H:%M:%S')
    new_post = {}
    
    for label in ["link", "image", "followers", "datePublished"]:
        new_post[label] = post[label]
    
    return new_post

def clean_posts(posts):
    result = []
    for i in posts:
    
        emb = []
        for label in ["title", "description", "description2"]:
            emb += text2emb(i[label])
        
        # Ponderated Avg should go here
        result.append(relevant_info(i)|{"embedding":np.average(total, axis=0)}))
    
    return result