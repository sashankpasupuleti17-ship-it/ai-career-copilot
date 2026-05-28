import chromadb
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client()

def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap

    return chunks


def create_vector_store(text, collection_name="career_copilot_collection"):
    chunks = chunk_text(text)

    try:
        client.delete_collection(name=collection_name)
    except:
        pass

    collection = client.create_collection(name=collection_name)

    for i, chunk in enumerate(chunks):
        embedding = embedding_model.encode(chunk).tolist()

        collection.add(
            ids=[f"chunk_{i}"],
            documents=[chunk],
            embeddings=[embedding]
        )

    return collection


def retrieve_relevant_chunks(collection, query, top_k=3):
    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]

    return "\n\n".join(documents)