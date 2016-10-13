import csv
import requests
from pattern.web import Element
from pattern.web import plaintext
from unidecode import unidecode

################## Bib Gourmand List ##################
# we use this later to exclude found resturants
# https://www.washingtonpost.com/news/going-out-guide/wp/2016/10/06/michelin-announces-its-first-d-c-honors-the-bib-gourmand-list-of-affordable-restaurants/?tid=hybrid_collaborative_3_na
bib_gourmand = ["Bad Saint", "Bidwell", "Boqueria", "Chercher", "China Chilcano", "Das", "Doi Moi", "Jaleo", "Kyirisan", "Lapis", "Maketto", "Ottoman Taverna", "Oyamel", "Pearl Dive Oyster Palace", "Red Hen", "Royal", "Thip Khao", "2Amys", "Zaytinya"]


################## Washington Post 3+ Star Reviews ##################
# we use this list to get an idea of restaurants that are ranked by the washington post (I believe this to be a good source)
page_content = requests.get("http://www.washingtonpost.com/gog/search/q,categories_Restaurants,locations_D.C.,searchType_facet,showResultsTab_GOG,starrating_3.html").content
elm = Element(page_content)
wo_po_restaurants = []
for e in elm("div.titles > h3 > a"):
	wo_po_restaurants.append(unidecode(plaintext(e.content)))

################## Washingtonian top 100 ##################
# gets washingtonian top 100 (I don't believe this to have great corrilation to the guide)
page_content = requests.get("https://www.washingtonian.com/2016/02/08/100-very-best-restaurants/").content
elm = Element(page_content)
washingtonian_restaurants = []
for e in elm("span.name"):
	washingtonian_restaurants.append(unidecode(plaintext(e.content)))

################## Analysis of star quantity from previous guides ##################
# This is more for me to see if my numbers are looking close
'''
http://la.eater.com/2007/11/9/6809859/breaking-michelin-stars-are-out
3: 1
2: 6
1: 27
total: 34

https://en.wikipedia.org/wiki/List_of_Michelin_starred_restaurants_in_San_Francisco
3: 1
2: 4
1: 21
total: 26

https://en.wikipedia.org/wiki/List_of_Michelin_starred_restaurants_in_Chicago
3: 2
2: 3
1: 18
total: 23

https://en.wikipedia.org/wiki/List_of_Michelin_starred_restaurants_in_New_York_City
3: 4
2: 4
1: 31
total: 39

dc numbers (based only on chi, la, sf)
3: 1-2
2: 4.3
total: 27.7
'''


################## Manually Pulled List from Critics ##################
# Pulled from Todd Kilman's twitter 
# (I believe his thoughts to be highly reputable, and also the only person to offer an idea of star ratings)
'''
### Todd Kliman
https://twitter.com/toddkliman/status/737774771253972992
Twitter estimate
3 stars: 
	Fiola Mare. 
	Komi. 
2 stars:
	Plume
	Rasika
	Metier
	Minibar
	Little Serow
1 star:
	Rose's

# Highly reputable, but not the same critria as the guide, so again, related but not perfect
### Tom Sietsema
https://www.washingtonpost.com/lifestyle/magazine/tom-sietsemas-top-10-rasika-is-no-9/2016/09/30/32fc53fc-84e6-11e6-92c2-14b64f3d453f_story.html
Tom Sistema Top 10
No. 10 Komi

No. 9 Rasika

No. 8 Little Serow

No. 7 Inn at Little Washington (removed because it's not in DC)

No. 6 Minibar

No. 5 Convivial

No. 4 Kinship

No. 3 Bad Saint

No. 2 Pineapple and Pearls

No. 1 All Purpose
'''
todd_three = ['Fiola Mare', 'Komi']
todd_two = ['Plume', 'Rasika Penn Quarter', 'Metier', 'MiniBar', 'Little Serow']
todd_one = ["Rose's Luxury"]
todd_kliman = ['Fiola Mare', 'Komi', 'Plume', 'Rasika Penn Quarter', 'Metier', 'MiniBar', 'Little Serow', "Rose's Luxury"] 
tom_sietsema = ["Komi", "Rasika", "Little Serow", "MiniBar", "Convivial", "Kinship", "Bad Saint", "Pineapple and Pearls", "All Purpose"]


################## Online discussions ##################
# Lists found on online discussions
'''
Pineapple and Pearls
Rose's Luxury 
Komi
Little Serrow 
Marcel's
Rasika
Fiola
Fiola Mare
Sushi Taro
MiniBar

Komi 
Fiola Mare
Minibar 
Rasika
Fiola
Roses Luxury
Kinship
Little Serow 
Marcel's 
Plume 
Bad Saint
Masseria 
Rasika West End

minibar
Pineapple and Pearls
Metier
Komi
Omakase Counter at Sushi Taro
Rasika West End
Rasika Penn Quarter
Fiola 
Fiola Mare
Marcel's
Little Serow
M
Plume
Rose's Luxury

Komi
Fiola Mare
Metier
Sushi Taro
MiniBar
Marcels
Pinapples and Pearls
Rose's
Little Serrow
Fiola
Casa Luca
Rasika
Garrison 
Masseria 
Izakaya Seki
Bad Saint
Plume
The Source
'''
online_0 = ["Komi", "Fiola Mare", "Metier", "Sushi Taro", "MiniBar", "Marcel's", "Pineapple and Pearls", "Rose's Luxury", "Little Serrow", "Fiola", "Casa Luca", "Garrison", "Masseria", "Izakaya Seki", "Bad Saint", "Plume", "The Source"]
online_1 = ["MiniBar",  "Pineapple and Pearls",  "Metier",  "Komi", "Rasika West End",  "Rasika Penn Quarter",  "Fiola",  "Fiola Mare",  "Marcel's",  "Little Serow",  "Masseria",   "Plume",  "Rose's Luxury"]
online_2 = ["Komi", "Fiola Mare", "MiniBar", "Fiola", "Rose's Luxury", "Kinship", "Little Serow", "Marcel's", "Plume", "Bad Saint", "Masseria", "Rasika West End", "Restaurant Nora"]
online_3 = ["Pineapple and Pearls", "Rose's Luxury", "Komi", "Little Serrow", "Marcel's", "Fiola", "Fiola Mare", "Sushi Taro", "MiniBar", "Blue Duck Tavern", "Obelisk"]
online = list(set(online_0 + online_1 + online_2 + online_3))


# compile various lists into a dictionary with scores
compiled_list = {"Restaurant": 0,}

for r in online: 
	if r in bib_gourmand: continue  
	if r in compiled_list.keys():
		compiled_list[r] += 4
	else:
		compiled_list[r] = 4

for r in todd_kliman: 
	if r in bib_gourmand: continue  
	if r in compiled_list.keys():
		compiled_list[r] += 5
	else:
		compiled_list[r] = 5

for r in tom_sietsema:
	if r in bib_gourmand: continue  
	if r in compiled_list.keys():
		compiled_list[r] += 3
	else:
		compiled_list[r] = 3

for r in washingtonian_restaurants: 
	if r in bib_gourmand: continue  
	if r in compiled_list.keys():
		compiled_list[r] += 1
	else:
		compiled_list[r] = 1

for r in wo_po_restaurants:
	if r in bib_gourmand: continue  
	if r in compiled_list.keys():
		compiled_list[r] += 2
	else:
		compiled_list[r] = 2


# skim list for the ones that score over three and add Todd Kliman's Star predictions
final_dictionary = {}
for k, v in compiled_list.iteritems():
	if v > 3:
		print k
		if k in todd_two:
			final_dictionary[k] = 2
		elif k in todd_three:
			final_dictionary[k] = 3
		else:
			final_dictionary[k] = 1

# for v, k in final_dictionary.iteritems(): print v, k


with open('michaelGasparovic-submititon.csv', 'wb') as f:
    w = csv.DictWriter(f, final_dictionary.keys())
    w.writeheader()
    w.writerow(final_dictionary)


