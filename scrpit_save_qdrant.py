import json
from sentence_transformers import SentenceTransformer
from services.qdrant import QdrantDatabase, QdrantOperations
from qdrant_client.models import Distance, VectorParams
from qdrant_client.models import PointStruct

FAQ_FILE = "data/faq_minecraft.json"

model = SentenceTransformer("all-MiniLM-L6-v2")

qdrantDatabase = QdrantDatabase()

qdrantOperations = QdrantOperations(qdrantClient=qdrantDatabase)

qdrantOperations.create_new_collection(
    collection_name="faq_minecraft",
    vectors_config=VectorParams(size=384, distance=Distance.DOT),
)

with open(FAQ_FILE, "r", encoding="utf-8") as file:
    faq_data = json.load(file)

points = []
for idx, item in enumerate(faq_data["faq"]):
    embedding = model.encode(item["text"])
    points.append(
        PointStruct(
            id=idx,
            vector=embedding,
            payload=item
        )
    )

operation_info = qdrantOperations.create(
    collection_name="faq_minecraft",
    points=points
)

print(operation_info)