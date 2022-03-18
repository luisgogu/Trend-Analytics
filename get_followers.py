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

# k, M, mil, millon