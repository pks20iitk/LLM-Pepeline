import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import fitz  # PyMuPDF
import re
from src.config_loader import numbers_of_doc, api_url


class CsvDataIngestion:
    def __init__(self, number_of_case_document):
        self.number_of_case_document = number_of_case_document

    @staticmethod
    def extract_text_from_pdf(url):

        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for any HTTP errors
            pdf_content = response.content

            # Using PyMuPDF to extract text from PDF
            pdf_document = fitz.open(stream=pdf_content, filetype='pdf')
            text = ""
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                text += page.get_text()

            return text
        except Exception as e:
            print(f"Error extracting text from {url}: {str(e)}")
            return None

    @staticmethod
    def preprocess_text(text):
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def get_and_process_case_data(self):
        url = api_url + str(numbers_of_doc)
        response = requests.get(url)
        topic_doc = BeautifulSoup(response.text, 'html.parser')
        data = json.loads(str(topic_doc))
        print(data)

        df = pd.DataFrame(columns=['frontend_pdf_url', 'reporter', 'provenance', 'court', 'jurisdiction', 'citations',
                                   'url', 'name', 'cites_to', 'name_abbreviation'])

        for item in data['results']:
            df.loc[len(df)] = [item['frontend_pdf_url'], item['reporter'], item['provenance'], item['court'],
                               item['jurisdiction'], item['citations'], item['url'], item['name'], item['cites_to'],
                               item['name_abbreviation']]

        df['extracted_text'] = df['frontend_pdf_url'].apply(self.extract_text_from_pdf)
        df['extracted_text'] = df['extracted_text'].apply(self.preprocess_text)

        return df

