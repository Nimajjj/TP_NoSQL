import json
from pymongo import MongoClient

class DatabaseManager:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient("mongodb://mongo1:27017,mongo2:27017,mongo3:27017/?replicaSet=rs0")
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def import_data(self, data):
        self.collection.insert_many(data)

    def insert_record(self, record):
        self.collection.insert_one(record)

    def find_records(self, query):
        return self.collection.find(query)

    def update_records(self, query, update_data, multiple=True):
        if multiple:
            self.collection.update_many(query, update_data)
        else:
            self.collection.update_one(query, update_data)

    def delete_record(self, query):
        self.collection.delete_one(query)

    def close_connection(self):
        self.client.close()

def main():
    db_manager = DatabaseManager('my_db', 'users')

    with open("./data/users.json", "r") as file:
        data = json.load(file)
        db_manager.import_data(data)

    query = {"age": {"$gt": 30}}
    for user in db_manager.find_records(query):
        print(user)

    query = {}
    update_data = {"$inc": {"age": 5}}
    db_manager.update_records(query, update_data)

    new_user = {
        "name": "Benjamin Borello",
        "age": 23,
        "email": "bborello@example.com",
        "createdAt": "2024-04-12T00:00:00"
    }
    db_manager.insert_record(new_user)

    query = {"name": "Benjamin Borello"}
    db_manager.delete_record(query)

    db_manager.close_connection()

if __name__ == '__main__':
    main()

