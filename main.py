from Utils import Utils
from ElasticSearchServer import ElasticSearchServer


import sys, getopt


utils = Utils()


def main(argv):

    try:
        opts, args = getopt.getopt(argv, "hi:s:d:p:",["index=","schema=","data=","port="])
    except getopt.GetoptError:
        print("Argument error: try main.py -h for help")
        sys.exit(2)
    
    index, schema, datapath, port = None, None, None, None

    for opt, arg in opts:
        if opt == '-h':
            print("-h                       for help")
            print("-i index_name            to create new index")
            print("-s schemapath            path to schema definition file")
            print("-d datapath              path to data file")
            print("-p port                  port number")
        elif opt in ("-i", "--index"):
            index = arg
        elif opt in ("-s", "--schema"):
            schema = arg
        elif opt in ("-d", "--data"):
            datapath = arg
        elif opt in ("-p", "--port"):
            port = arg
    
    if index:
        if port:
            server = ElasticSearchServer(index, port=port)
        else:
            server = ElasticSearchServer(index)
    else:
        print("Index name not specified, see main.py -h for help")
        sys.exit(2)

    if schema:
        if index:
            server.create_index(schema)
        else:
            print("Index name not specified, see main.py -h for help")
            sys.exit(2)
            
    if datapath:
        utils.wrap_in_json(arg)
        utils.load_to_index("data/data.json", server)


if __name__ =="__main__":
    main(sys.argv[1:])