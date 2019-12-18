from elasticsearch import Elasticsearch

es = Elasticsearch()

class Return:

	def __init__(self, title):
		self.title = title

	def search_title(self):
		res = es.search(index="test", body={"query": {"match": {"movie title": self.title}}})
		temp = res['hits']['hits']
		print("Results of your searching (B25 ranking algorithm):")
		for output in temp:
			print(output["_source"]["movie title"], (output["_score"]))

search = Return(input("Enter the movie title you want to find: "))
search.search_title()
