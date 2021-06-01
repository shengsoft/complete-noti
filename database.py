from flask_pymongo import pymongo
import json

class Database:
    @classmethod
    def initialize(cls):
        client = pymongo.MongoClient('MONGO URI HERE')
        cls.database = client.get_database('DATABASE HERE')
    
    @classmethod
    def save_record(cls, collection_name, data):
        cls.database[collection_name].insert_one(data)

    @classmethod
    def save_records(cls, collection_name, data):
        cls.database[collection_name].insert_many(data)   

    @classmethod
    def update_record(cls, collection_name, id, data):
        cls.database[collection_name].update_one(id, data)

    @classmethod
    def update_records(cls, collection_name, query, data):         
        cls.database[collection_name].update_many(query, data)

    @classmethod
    def get_records(cls, collection_name, query):
        return cls.database[collection_name].find(query)

    @classmethod
    def get_record(cls, collection_name, query):
        return cls.database[collection_name].find_one(query)   

    @classmethod
    def exclude(cls, collection_name, query):
        return cls.database[collection_name].aggregate(query)  

    @classmethod
    def message_count(cls, collection_name, query):
        return cls.database[collection_name].aggregate(query)       





