from elasticsearch import ElasticSearch, helpers

import json, uuid


class ElasticSearch:

    def __init__(self, index):
        self.server = ElasticSearch(timeout=300)
        self.index = index

    def create_index(self, schemapath):
        '''
            Creates an index based on schema defintion
            @params:
                schemapath: path to schema definition
        '''
        schema = json.load(open(schemapath, "r"))
        self.server.indices.create(index=self.index, body=schema, ignore=400)

        return True
    

    def load(self, data):
        '''
            Bulk load all the data into index
            @params:
                data: list of data
        '''
        generator = self.__generator(data)

        try:
            helpers.bulk(self.server, generator, self.index)
        except Exception as e:
            print("Error: ", e)
    

    def __generator(self, data):
        '''
            Returns a single line of data without loading document into memory
            @params:
                data:   list of data
        '''
        for doc in data:
            if '{"index"' not in doc:
                yield {
                    "_index": self.index,
                    "_id": uuid.uuid(4),
                    "_source": doc
                }
