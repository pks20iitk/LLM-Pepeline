import os
import requests
from bs4 import BeautifulSoup
import json
import re
import fitz
from src.config_loader import numbers_of_doc


class CaseDataExtractor:
    def __init__(self, number_of_case_document, output_folder=r'C:\Project\LLM-Pepeline\case-data-json'):
        self.number_of_case_document = number_of_case_document
        self.output_folder = output_folder
        self.case_data_list = []

        # Create the output folder if it doesn't exist
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

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
        except requests.exceptions.RequestException as e:
            print(f"Error fetching PDF from {url}: {str(e)}")
            return None
        except Exception as e:
            print(f"Error extracting text from {url}: {str(e)}")
            return None

    @staticmethod
    def preprocess_text(text):
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def fetch_case_data(self):
        try:
            topic_page_url = f"https://api.case.law/v1/cases/?jurisdiction=ill&page_size={self.number_of_case_document}"
            response = requests.get(topic_page_url)
            response.raise_for_status()  # Check for any HTTP errors

            topic_doc = BeautifulSoup(response.text, 'html.parser')
            data = json.loads(str(topic_doc))

            for item in data['results']:
                case_data = {
                    'frontend_pdf_url': item['frontend_pdf_url'],
                    'reporter': item['reporter'],
                    'provenance': item['provenance'],
                    'court': item['court'],
                    'jurisdiction': item['jurisdiction'],
                    'citations': item['citations'],
                    'url': item['url'],
                    'name': item['name'],
                    'cites_to': item['cites_to'],
                    'name_abbreviation': item['name_abbreviation'],
                }

                extracted_text = self.extract_text_from_pdf(item['frontend_pdf_url'])
                if extracted_text:
                    case_data['extracted_text'] = self.preprocess_text(extracted_text)

                self.case_data_list.append(case_data)
                self.save_to_json(case_data, f"{item['name']}.json")

        except requests.exceptions.RequestException as e:
            print(f"Error fetching case data: {str(e)}")

    def save_to_json(self, data, filename):
        with open(os.path.join(self.output_folder, filename), 'w') as json_file:
            json.dump(data, json_file, indent=4)


if __name__ == "__main__":
    extractor = CaseDataExtractor(number_of_case_document=numbers_of_doc)
    extractor.fetch_case_data()
