import chromadb
from chromadb.config import Settings
from app.config import VECTOR_DB_DIR

def get_vector_store():

    client = chromadb.Client(
        Settings(
            persist_directory=VECTOR_DB_DIR,
            anonymized_telemetry=False
        )
    )

    collection = client.get_or_create_collection(
        name="hellobooks"
    )

    return collection, client