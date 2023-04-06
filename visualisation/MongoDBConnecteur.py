from pymongo import MongoClient

class MongoDBConnecteur:
    def __init__(self, db_name) -> None: # username, password, cluster,
        #self.client = MongoClient(f"mongodb+srv://{username}:{password}@{cluster}/{db_name}?retryWrites=true&w=majority")
        self.client = MongoClient(f"mongodb+srv://Stinson:Stinson@stinson.rcfzhzz.mongodb.net/?retryWrites=true&w=majority") 
        self.db = self.client[db_name]

    def get_collection(self, collection_name):
        return self.db[collection_name]

    def get_data(self, collection_name):
        return self.get_collection(collection_name).find()