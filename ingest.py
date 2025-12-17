import uuid
from pathlib import Path
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct

# ================= CONFIG =================

BOOK_PATH = Path("Humanoid-robotics-book")
COLLECTION_NAME = "humanoid_robotics_book"

QDRANT_HOST = "localhost"
QDRANT_PORT = 6333

# =========================================


def load_documents():
    documents = []
    for file in BOOK_PATH.rglob("*.md"):
        text = file.read_text(encoding="utf-8", errors="ignore")
        documents.append({
            "id": str(uuid.uuid4()),
            "text": text,
            "source": str(file)
        })
    return documents


def main():
    print("🔹 Loading embedding model...")
    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("🔹 Connecting to Qdrant...")
    client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)

    collections = [c.name for c in client.get_collections().collections]
    if COLLECTION_NAME not in collections:
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )
        print("✅ Qdrant collection created")

    docs = load_documents()
    print(f"📄 Loaded {len(docs)} markdown files")

    points = []
    for doc in docs:
        vector = model.encode(doc["text"]).tolist()
        points.append(
            PointStruct(
                id=doc["id"],
                vector=vector,
                payload={
                    "text": doc["text"],
                    "source": doc["source"]
                }
            )
        )

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

    print("🎉 BOOK INDEXED SUCCESSFULLY!")


if __name__ == "__main__":
    main()
 