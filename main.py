from Utils import Utils
from ElasticSearch import ElasticSearch


utils = Utils()
server = ElasticSearch(index="arxiv")


utils.wrap_in_json("path to data")

utils.load_to_index("path to formatted data", server)