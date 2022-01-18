'''
    Utility functions
'''

from ElasticSearchServer import ElasticSearchServer


import json, re
from datetime import date, datetime


class Utils:

    def __init__(self):
        pass

    def __clean(self, t):
        t = re.sub("\n"," ", t)
        return t

    def __author_parser__(self, authors):

        _authors = []

        for author in authors:
            _authors.append({
                "fname": author[1],
                "lname": author[0],
                "full_name": author[1] + " " + author[0],
                "affiliation": author[2]
            })
        return _authors

    def __date_parser__(self, d):
        d = datetime.strptime(d, "%a, %d %b %Y %H:%M:%S %Z").date()
        return d, {"year": d.year, "month": d.month, "day": d.day}

    def wrap_in_json(self, datapath):
        '''
            Wrap data in JSON format ready to be ingested into an index
            @params
                datapath:   path to data 
        '''
        data = json.load(open(datapath, "r"))
        wf = open("data/data.json","w+")

        for i, doc in enumerate(data):
            
            obj = {
                "pid": doc["id"],
                "title": self.__clean(doc["title"]),
                "journal": doc["journal-ref"],
                "doi": "https://arxiv.org/pdf/" + doc["id"] + ".pdf",
                "authors": self.__author_parser__(doc["authors_parsed"]),
                "categories": [c for c in doc['categories'].split(" ")],
                "license": doc["license"],
                "abstract": self.__clean(doc["abstract"]),
                "date": self.__date_parser__(doc["versions"][0]["created"])[0],
                "date_parsed": self.__date_parser__(doc["versions"][0]["created"])[1]
            }

            json.dump({"index": {"_id": i}}, wf)
            wf.write("\n")
            json.dump(obj, wf)
            wf.write("\n")

    def load_to_index(self, datapath, server):
        '''
            Load the JSON formatted data to index
            @params
                datapath:   path to json file
                server:     elastic search server
        '''

        with open(datapath, encoding='utf-8', errors='ignore') as f:
            data = f.readlines()
        
        server.load(data)