from pymongo.mongo_client import MongoClient
import os
import logging

class MongoConnection:
    def __init__(self):
        self.mongo_uri = os.environ.get("MONGO_URI")
        if not self.mongo_uri:
            raise ValueError("MONGO_URI environment variable not set")
        self.client = self.connect_to_database()

    def connect_to_database(self):
        try:
            client = MongoClient(self.mongo_uri)
            client.server_info()
            print(f'Successfully connected to MongoDB database: {client.get_database().name}')
            return client
        except Exception as e:
            # Log the error instead of printing
            logging.error(f"Error connecting to MongoDB: {e}")
            raise

    def get_database(self):
        return self.client.get_database()

    def get_collection(self, collection: str):
        return self.get_database()[collection]

    def drop_collection(self, collection):
        self.get_database().drop_collection(collection)

    def seed_collection(self, collection, data):
        self.get_database()[collection].insert_many(data)


mongo_connection = MongoConnection()
user_collection = mongo_connection.get_collection('users')
workout_collection = mongo_connection.get_collection('workouts')
nutrition_collection = mongo_connection.get_collection('nutrition')
