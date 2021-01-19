from elasticsearch import Elasticsearch
import ast
import csv

es = Elasticsearch()

class Return:

	def __init__(self, title, file):
		self.title = title
		self.file = file 

	def avg_user_score(self, movie_id, file):
		with open (file, newline='', encoding="utf8") as score:
			f = csv.reader(score, delimiter=',', quotechar='"')
			count = 0
			summ = 0
			for line in f:
				if line[1] == str(movie_id):
					summ = summ + float(line[2])
					count = count + 1
		avg_score = summ / count
		return avg_score

	def user_score(self, user_id, movie_id, file):
		with open (file, newline='', encoding="utf8") as score:
			f = csv.reader(score, delimiter=',', quotechar='"')
			for line in f:
				if line[0] == str(user_id) and line[1] == str(movie_id):
					user_score = line[2]
				else:
					user_score = 0
		return user_score

	def final_score(self, user_score, avg_score, es_score):
		final_score = user_score / 3 + avg_score / 3 + es_score / 3
		return final_score

	def evaluation(self, hit):
		user_id = input("Enter your user id: ")
		for output in hit:
			temp = ast.literal_eval(output["_id"])
			movie_id = temp["id"]
			new_score = self.final_score(self.user_score(user_id, movie_id, self.file), self.avg_user_score(movie_id, self.file), output["_score"])
			output["_score"] = new_score
		self.sort_print(hit)

	def sort_print(self, hit):
		print("Results of your searching (our own algorithm):")
		for x in hit:
			maxy = 0
			for x in hit:
				if x["_score"] > maxy:
					maxy = x["_score"]
			for x in hit:
				if x["_score"] == maxy:
					print(x["_source"]["movie title"],f"{maxy:.2f}")
					x["_score"] = 0
			
	def search_title(self):
		query = es.search(index="movies", body={"query": {"match": {"movie title": self.title}}})
		hits = query['hits']['hits']
		self.evaluation(hits)





search = Return(input("Enter the movie title you want to find: "), "C:\\Users\\30694\\Desktop\\PROJECTS\\ProjectIR\\ratings.csv")
search.search_title()
