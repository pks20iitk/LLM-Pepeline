import yaml
from typing import List


def load_config(file_path=r'C:\Project\LLM-Pepeline\config.yml'):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config


config = load_config()

# Access individual configurations
output_dir = config.get('output_dir', None)
input_dir = config.get('input_dir', None)
weaviate_url = config.get('weaviate_url', None)
embedding_model_name = config.get('embedding_model_name', 'all-MiniLM-L6-v2')  # Default value added
topic_page_url = config.get('topic_page_url', None)
model_path = config.get('model_path', None)
api_url = config.get('api_url', None)
device = config.get('device', 'cpu')
numbers_of_doc = config.get('number_of_case_document', 10)# Default value added
