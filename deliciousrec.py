import time

def fillItems(user_dict):
	all_items={}
	#find links posted by all users
	for user in user_dict:
		for i in range(3):
			try: #this is a function?
				posts=get_userposts(user)
				break
			except:
				print "Failed user " +user+", retrying"
				time.sleep(4) #what's this function
			for post in posts:
				url=post['href']
				user_dict[user][url]=1.0
				all_items[url]=1

	#fill in missing items with 0
	for ratings in user_dict.values( ):
		for item in all_items:
			if item not in ratings:
				ratings[item]=0.0

def initializeUserDict(tag,count=5):
	user_dict={}
	#get the top "count" popular posts
	for p1 in get_popular(tag=tag)[0:count]: #from api
		#find all users who posted this
		for p2 in get_urlposts(p1['href']):
			user=p2['user']
			user_dict[user]={} #looking at a key:value pair?
	return user_dict
