import chromadb
from pathlib import Path

client = chromadb.PersistentClient(path='app/rag/chroma_db')
collection = client.get_or_create_collection(name='security_knowledge')

DATA_DIR = Path('data')

for file in DATA_DIR.glob('*.txt'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    collection.add(
        documents=[content],
        ids=[file.stem],
        metadatas=[{'source': str(file)}]
    )

print('Knowledge base ingestion complete.')
