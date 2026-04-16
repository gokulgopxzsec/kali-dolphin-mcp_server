import chromadb
from chromadb.utils import embedding_functions

client = chromadb.PersistentClient(path='app/rag/chroma_db')
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-v2')

collection = client.get_or_create_collection(
    name='security_knowledge',
    embedding_function=embedding_fn
)


def search_knowledge_base(query):
    results = collection.query(
        query_texts=[query],
        n_results=5
    )
    return results
