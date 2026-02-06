import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

PAST_CASES = [
    {
        "incident": "Login failures due to token validation error",
        "root_cause": "Expired JWT cache",
        "resolution": "Refresh authentication cache"
    },
    {
        "incident": "Website slow and CPU at 100%",
        "root_cause": "Memory leak in API service",
        "resolution": "Restart service and patch memory issue"
    },
    {
        "incident": "Database connection timeout",
        "root_cause": "Connection pool exhaustion",
        "resolution": "Increase pool size and restart DB"
    }
]

incident_texts = [case["incident"] for case in PAST_CASES]
embeddings = model.encode(incident_texts)

dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(np.array(embeddings))


def retrieve_similar_cases(query: str, top_k: int = 2):
    query_vec = model.encode([query])
    distances, indices = index.search(np.array(query_vec), top_k)

    results = []
    for idx in indices[0]:
        results.append(PAST_CASES[idx])

    return results
