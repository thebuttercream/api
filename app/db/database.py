from pymongo import MongoClient
from pymongo.collection import Collection
import os

def get_db() -> Collection:
    mongodb_url = os.getenv('MONGODB_URL')
    if mongodb_url is None:
        raise ValueError("A Variável de Ambiente 'MONGODB_URL' Não Está Definida!!!")
    try:
        client = MongoClient(mongodb_url)
        return client.buttercream
    except Exception as error:
        print(f"Erro ao Conectar ao MongoDB: {error}!!!")
        raise


try:
    db = get_db()
    print(db.list_collection_names())
except Exception as e:
    print(f"Erro ao Acessar o Banco de Dados: {e}!!!")
