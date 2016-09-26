#new data set - ??
#doing user-based or item based recommendations?
#sparse dataset = item based [more than 1,000 users]
# user recommending - music


from math import sqrt
import csv


# Returns a distance-based similarity score for person1 and person2
def sim_distance(prefs,person1,person2):
  # Get the list of shared_items
  si={}
  for item in prefs[person1]:
    if item in prefs[person2]:
       si[item]=1

  # if they have no ratings in common, return 0
  if len(si)==0: return 0

  # Add up the squares of all the differences
  sum_of_squares=sum([pow(prefs[person1][item]-prefs[person2][item],2)
                      for item in si])

  return 1/(1+sqrt(sum_of_squares))


#Returns the Pearson correlation coefficient for p1 and p2
def sim_pearson(prefs, p1, p2):
 	#Get the list of mutually rated tiems
 	si={}
 	for item in prefs[p1]:
 		if item in prefs[p2]:
 			si[item]=1

 	#Find the number of elements
 	n=len(si)

 	# if they have no ratings in common, return 0
 	if n==0: return 0

 	#Add up all the preferences
 	sum1=sum([prefs[p1][it] for it in si])
 	sum2=sum([prefs[p2][it] for it in si])

 	#sum up the squares
 	sum1Sq=sum([pow(prefs[p1][it],2) for it in si])
 	sum2Sq=sum([pow(prefs[p2][it],2) for it in si])

 	#Sum up the products
 	pSum=sum([prefs[p1][it]*prefs[p2][it] for it in si])

 	#Calculate Pearson score

 	num=pSum-(sum1*sum2/n)
 	den=sqrt((sum1Sq-pow(sum1,2)/n)*(sum2Sq-pow(sum2,2)/n))
 	if den==0: return 0
 	r=num/den

 	return r

#Returns the best matches for person from the prefs dictionary.
#number of results and similarity function are optional parms
def topMatches(prefs,person, n=5, similarity=sim_pearson): #n = number of movies?
	#list comprehension
	scores=[(similarity(prefs,person,other),other) for other in prefs if other!=person]

	#sort the list so the highest scores appear at the top
	scores.sort( )
	scores.reverse( )
	return scores[0:n]


# Gets recommendations for a person by using a weighted average
# of every other user's rankings
def getRecommendations(prefs,person,similarity=sim_pearson): # can change to euclid when run
  totals={}
  simSums={}
  for other in prefs:
    # don't compare me to myself
    if other==person: continue
    sim=similarity(prefs,person,other)

    # ignore scores of zero or lower
    if sim<=0: continue
    for item in prefs[other]:

      # only score movies I haven't seen yet
      if item not in prefs[person] or prefs[person][item]==0:
        # Similarity * Score
        totals.setdefault(item,0)
        totals[item]+=prefs[other][item]*sim #key part
        # Sum of similarities
        simSums.setdefault(item,0)
        simSums[item]+=sim

  # Create the normalized list
  rankings=[(total/simSums[item],item) for item,total in totals.items(  )]

  # Return the sorted list
  rankings.sort(  )
  rankings.reverse(  )
  return rankings


#load a dataset
def loadDataSet(path='data/book_dump'):
	# to create new csv
	# data = []
	# with open(path+'/BX-Book-Ratings2.csv', 'rb') as f:
	# 	while True:
	# 		rating_line = f.readline().replace(';', ',')

	# 		data.append(rating_line)

	# 		if rating_line == '':
	# 			break

	# data='\n'.join(data)

	# with open(path+'/fixed_books.csv', 'wb') as f:
	# 	f.write(data)

	#print path+'/u.item'
	#get movie titles
	books={}
	with open(path+'/fixed_books.csv') as csvfile:
		reader = csv.DictReader(csvfile)
		# reader = csv.reader(open(csvfile, 'rU'), dialect=csv.excel_tab)
		for row in reader:
			(id,title)=str(row).split(',')[0:2]
			books[id] = title #but not title, just isbn
			# print books[id] > still, got this to work

		



	# load data
	prefs={}
	with open(path+'/fixed_books.csv') as csvfile:

		reader = csv.DictReader(csvfile)

		for row in reader:

			#rating=str(row).split(',')[2:3]

			(user,bookid,rating)=str(row).split(',')[0:3] #too many values to unpack?
			prefs.setdefault(user,{})

			new_rating = rating.strip("'',""") 

			
			if new_rating == 0:
				prefs[user][books[bookid]] = 0
			elif new_rating > 0:
				prefs[user][books[bookid]] = new_rating

		# return prefs

		# print prefs

		return new_rating
		




print loadDataSet()




