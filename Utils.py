'''
    Utility functions
'''

from ElasticSearch import ElasticSearch


class Utils:

    def __init__(self):
        pass

    def wrap_in_json(self, datapath):
        '''
            Wrap data in JSON format ready to be ingested into an index
            @params
                datapath:   path to data 
        '''
        pass


    def load_to_index(self, datapath, server):
        '''
            Load the JSON formatted data to index
            @params
                datapath:   path to json file
                server:     elastic search server
        '''

        with open(datapath, encoding='utf-8', errors='ignore') as f:
            data = f.readlines()
        
        server.load(server.index, data)