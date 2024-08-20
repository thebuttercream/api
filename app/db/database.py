from pymongo import MongoClient
from pymongo.collection import Collection
import os


def get_db() -> Collection:
    mongodb_url = os.getenv('MONGODB_URL', 'mongodb://admin:admin@mongodb:27017/?authSource=admin')
    client = MongoClient(mongodb_url)
    return client.buttercream


# Exemplo de uso
db = get_db()
print(db.list_collection_names())
