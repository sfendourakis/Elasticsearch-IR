from elasticsearch import Elasticsearch
import csv

es = Elasticsearch()

class Import:

	def __init__(self, index, doctype, file):
		self.index = index
		self.doctype = doctype
		self.file = file

	def check_connection(self):
		if es.ping():
			print("Connected")
		else:
			print("Not Connected")

	def import_data(self):
		def import_index(id, body):
			res = es.index(index=self.index, doc_type=self.doctype, id=ID, body=BODY)
			print(res)

		with open (self.file, newline='', encoding="utf8") as movies:
			file = csv.reader(movies, delimiter=',', quotechar='"')
			for line in file:
				ID = {"id" : line[0]}
				BODY = {"movie title" : line[1], "genre" : line[2]}
				print(ID,BODY)
				import_index(ID,BODY)



elastic = Import("movies", "doc", r'C:\Users\30694\Desktop\PROJECTS\ProjectIR\movies.csv')
elastic.check_connection()
elastic.import_data()