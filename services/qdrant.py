from qdrant_client import QdrantClient
from typing import Optional
from qdrant_client.models import Distance, VectorParams

class QdrantDatabase:
    _instance = None
    _client = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_client()
        return cls._instance
    
    def _initialize_client(self):
        if QdrantDatabase._client is None:
            QdrantDatabase._client = QdrantClient(
            host="localhost",
            port=6333,
        )

    def get_client(self):
        if QdrantDatabase._client is None:
            self._initialize_client()
        return QdrantDatabase._client
    

class QdrantOperations:
    def __init__(self, qdrantClient: QdrantClient):
        self.qdrantClient = qdrantClient

    def create_new_collection(self, collection_name: str, vectors_config: VectorParams):
        self.qdrantClient._client.create_collection(
            collection_name=collection_name,
            vectors_config=vectors_config,
        )

    def create(self, collection_name: str, points: list):
        return self.qdrantClient._client.upsert(
            collection_name=collection_name,
            points=points,
        )

    def read(self, collection_name: str, point_id: int):
        result = self.qdrantClient._client.retrieve(
            collection_name=collection_name,
            ids=[point_id]
        )
        if result:
            return result[0]
        else:
            print(f"Ponto com ID {point_id} não encontrado na coleção {collection_name}.")
            return None

    def update(self, collection_name: str, point_id: int, vector: list, payload: dict):
        self.create(collection_name, point_id, vector, payload)

    def delete(self, collection_name: str, point_id: int):
        self.qdrantClient._client.delete(
            collection_name=collection_name,
            ids=[point_id]
        )
        print(f"Ponto com ID {point_id} deletado da coleção {collection_name} com sucesso!")

    def search(self, collection_name: str, query_vector: list, limit: int = 10):
        results = self.qdrantClient._client.search(
            collection_name=collection_name,
            query_vector=query_vector,
            limit=limit
        )
        return results