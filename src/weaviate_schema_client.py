import weaviate
from config_loader import weaviate_url
from typing import Dict


def create_local_weaviate_client(db_url: str):
    return weaviate.Client(
        url=db_url,
    )


def get_schema(vectorizer: str = "none"):
    return {
        "classes": [
            {
                "class": "Doc",
                "description": "A generic document class",
                "vectorizer": vectorizer,
                "properties": [
                    {
                        "name": "last_modified",
                        "dataType": ["text"],
                        "description": "Last modified date for the document",
                    },
                    {
                        "name": "player",
                        "dataType": ["text"],
                        "description": "Player related to the document",
                    },
                    {
                        "name": "position",
                        "dataType": ["text"],
                        "description": "Player Position related to the document",
                    },
                    {
                        "name": "text",
                        "dataType": ["text"],
                        "description": "Text content for the document",
                    },
                ],
            },
        ],
    }


def upload_schema(my_schema, weaviate):
    weaviate.schema.delete_all()
    weaviate.schema.create(my_schema)


def count_documents(client: weaviate.Client) -> Dict:
    response = (
        client.query
        .aggregate("Doc")
        .with_meta_count()
        .do()
    )
    count = response
    return count


client = create_local_weaviate_client(db_url=weaviate_url)
my_schema = get_schema()
upload_schema(my_schema, weaviate=client)
