import faiss
from langchain.embeddings import OpenAIEmbeddings
import numpy as np
import json
import os

embedding_model = OpenAIEmbeddings(model="text-embedding-ada-002")
faiss_index_path = "faiss_index/reddit_index"
metadata_path = "faiss_index/metadata.json"

def save_to_faiss(posts, company_name):
    texts = [post['content'] for post in posts]
    metadata = [{"company": company_name, "subreddit": post['subreddit']} for post in posts]
    embeddings = embedding_model.embed_documents(texts)

    # Load or create FAISS index
    if os.path.exists(faiss_index_path):
        index = faiss.read_index(faiss_index_path)
        with open(metadata_path, "r") as f:
            existing_metadata = json.load(f)
    else:
        flat_index = faiss.IndexFlatL2(len(embeddings[0]))  # Base flat index
        index = faiss.IndexIDMap(flat_index)  # Wrap with IDMap
        existing_metadata = []

    # Add embeddings to the index
    ids = np.arange(len(existing_metadata), len(existing_metadata) + len(texts))
    index.add_with_ids(np.array(embeddings).astype("float32"), ids)

    # Save metadata
    existing_metadata.extend(metadata)
    with open(metadata_path, "w") as f:
        json.dump(existing_metadata, f)

    # Save FAISS index
    faiss.write_index(index, faiss_index_path)


def retrieve_from_faiss(query, top_n=5):
    if not os.path.exists(faiss_index_path) or not os.path.exists(metadata_path):
        return []

    # Load FAISS index and metadata
    index = faiss.read_index(faiss_index_path)
    with open(metadata_path, "r") as f:
        metadata = json.load(f)

    # Create query embedding
    query_embedding = embedding_model.embed_query(query)
    query_embedding = np.array(query_embedding).astype("float32").reshape(1, -1)

    # Perform FAISS search
    distances, indices = index.search(query_embedding, top_n)

    # Retrieve metadata for the top results
    results = []
    for idx in indices[0]:
        if idx != -1:  # Valid index
            results.append(metadata[idx])

    return results
