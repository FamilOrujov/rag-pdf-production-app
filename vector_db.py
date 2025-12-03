import os
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct


class QdrantStorage:
    def __init__(self, url=None, collection="docs", dim=3072):
        # Use environment variable if available, fallback to localhost
        url = url or os.getenv("QDRANT_URL", "http://localhost:6333")
        self.client = QdrantClient(url=url, timeout=30)
        self.collection = collection
        self.dim = dim
        if not self.client.collection_exists(self.collection):
            self.client.create_collection(
                collection_name=self.collection,
                vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
            )


    def upsert(self, ids, vectors, payloads):
        points = [PointStruct(id=ids[i], vector=vectors[i], payload=payloads[i]) for i in range(len(ids))]
        self.client.upsert(self.collection, points=points)


    def search(self, query_vector, top_k: int = 5):
        response = self.client.query_points(
            collection_name=self.collection,
            query=query_vector,
            with_payload=True,
            limit=top_k
        )
        results = response.points
        context = []
        sources = set()

        for r in results:
            payload = getattr(r, "payload", None) or {}
            text = payload.get("text", "")
            source = payload.get("source", "")
            if text:
                context.append(text)
                sources.add(source)

        return {"context": context, "sources": list(sources)}
