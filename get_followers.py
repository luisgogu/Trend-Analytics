import re

nfollow = [('k', 1000, 1), ('M', 1000000, 1), ('millon', 1000000, 0), ('mill.', 1000000, 0), ('mil', 1000, 0)]

# Returns the number of followers in int type
def get_followers2(followers):
	if followers == "None":
		return None
		
	f = followers.split()
	for ab, num, s  in nfollow:
		if re.search(ab, followers):
			return int(f[0][:len(f[0])-s])*num
			
	return int(re.search(r'\d+', f[0]).group()) #in case of having a new string number abr, only the int number is returned