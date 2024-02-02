from unstructured.chunking.title import chunk_by_title
from unstructured.documents.elements import DataSourceMetadata
from unstructured.partition.json import partition_json
from sentence_transformers import SentenceTransformer
from weaviate.util import get_valid_uuid
from typing import List
from src.config_loader import output_dir
from src.config_loader import embedding_model_name, device
from src.ingestion_and_preprocess import get_result_files, get_my_documents
from src.config_loader import weaviate_url
from src.schema_client import create_local_weaviate_client, count_documents
import uuid

embedding_model = SentenceTransformer(embedding_model_name, device)


def compute_embedding(chunk_text: List[str]):
    embeddings = embedding_model.encode(chunk_text, device=device)
    return embeddings


def get_chunks(elements, chunk_under_n_chars=500, chunk_new_after_n_chars=1500):
    for element in elements:
        if not type(element.metadata.data_source) is DataSourceMetadata:
            delattr(element.metadata, "data_source")

        if hasattr(element.metadata, "coordinates"):
            delattr(element.metadata, "coordinates")

    chunks = chunk_by_title(
        elements,
        combine_under_n_chars=chunk_under_n_chars,
        new_after_n_chars=chunk_new_after_n_chars
    )

    for i in range(len(chunks)):
        chunks[i] = {"last_modified": chunks[i].metadata.last_modified, "text": chunks[i].text}

    chunk_texts = [x['text'] for x in chunks]
    embeddings = compute_embedding(chunk_texts)
    return chunks, embeddings


def add_data_to_weaviate(files, client, chunk_under_n_chars=500, chunk_new_after_n_chars=1500):
    for filename in files:
        try:
            elements = partition_json(filename=filename)
            chunks, embeddings = get_chunks(elements, chunk_under_n_chars, chunk_new_after_n_chars)
        except IndexError as e:
            print(e)
            continue

        print(f"Uploading {len(chunks)} chunks for {str(filename)}.")
        for i, chunk in enumerate(chunks):
            print(i, chunk)
            client.batch.add_data_object(
                data_object=chunk,
                class_name="doc",
                uuid=get_valid_uuid(uuid.uuid4()),
                vector=embeddings[i]
            )

    client.batch.flush()


files = get_result_files(output_dir)
client = create_local_weaviate_client(db_url=weaviate_url)
add_data_to_weaviate(
    files=files,
    client=client,
    chunk_under_n_chars=250,
    chunk_new_after_n_chars=500
)

print(count_documents(client=client)['data']['Aggregate']['Doc'])
