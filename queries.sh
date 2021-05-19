#!/bin/bash


#Query1
curl --location --request GET 'http://localhost:5000/api/v1/authors/publications/query1?name_author=Moritz%20Lipp'
	
#Query2
curl --location --request GET 'http://localhost:5000/api/v1/authors/coauthors/query2?name_author=Moritz%20Lipp&year=2018'

#Query3
curl --location --request GET 'http://localhost:5000/api/v1/authors/topk/query3?category=article&k=5'

#Query4
curl --location --request GET 'http://localhost:5000/api/v1/authors/topk/query4?k=100'

#Query5
curl --location --request GET 'http://localhost:5000/api/v1/authors/topk/query5?k=20&year=2019'

#Query6
curl --location --request GET 'http://localhost:5000/api/v1/authors/topk/query6?k=10'

#Query7
curl --location --request GET 'http://localhost:5000/api/v1/authors/topk/query7?k=5'

#Query8 
curl --location --request GET 'http://localhost:5000/api/v1/authors/topk/query8?k=15'

#Query9
curl --location --request GET 'http://localhost:5000/api/v1/authors/topk/query9?k=10&author_name=Paul%20Partlow'

#Query10
curl --location --request GET 'http://localhost:5000/api/v1/authors/publications/query10?year=2012'

#Query11
curl --location --request GET 'http://localhost:5000/api/v1/authors/pages/query11?year=2020&author_name=Rafi%20Rashid'

#Query12 
curl --location --request GET 'http://localhost:5000/api/v1/authors/topk/query12?journal_name=Sci.%20Eng.%20Ethics&position=first&year=2018&k=10'

#Query13
curl --location --request GET 'http://localhost:5000/api/v1/authors/three_coauthors/query13?journal_name=Sci.%20Eng.%20Ethics'

#Query14
curl --location --request GET 'http://localhost:5000/api/v1/authors/query14'

#Query15
curl --location --request GET 'http://localhost:5000/api/v1/authors/kconsecutive/query15?k=4'

#Query16
curl --location --request GET 'http://localhost:5000/api/v1/authors/topk/query16?k=20'

#Query17
curl --location --request GET 'http://localhost:5000/api/v1/authors/nconsecutive/query17?num_years=4'

#Query18
curl --location --request GET 'http://localhost:5000/api/v1/authors/query18'