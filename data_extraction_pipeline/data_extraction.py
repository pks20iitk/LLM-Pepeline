import os
import requests
import json
from datetime import datetime
import time


def download_and_save_pdf(pdf_url, output_folder, filename_prefix="downloaded_file"):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = os.path.join(output_folder, f"{filename_prefix}_{timestamp}.pdf")

        # Add a short delay to ensure unique timestamps
        time.sleep(1)

        with open(file_name, 'wb') as file:
            file.write(response.content)
        print(f"PDF downloaded and saved as {file_name}")
        return file_name
    else:
        print(f"Failed to download PDF from {pdf_url}")
        return None


def create_pdf_from_text(text, output_folder, filename_prefix):
    file_name = os.path.join(output_folder, f"{filename_prefix}_created_file.pdf")
    with open(file_name, 'w') as file:
        file.write(text)
    print(f"PDF created and saved as {file_name}")
    return file_name


def process_json_file(json_file, output_folder):
    with open(json_file, 'r') as file:
        data = json.load(file)

    frontend_pdf_url = data.get("frontend_pdf_url")
    filename_prefix = os.path.splitext(os.path.basename(json_file))[0]

    if frontend_pdf_url:
        if frontend_pdf_url.endswith(".pdf"):
            return download_and_save_pdf(frontend_pdf_url, output_folder)
        else:
            text = "Extracted text from the frontend_pdf_url attribute"  # Replace with your text extraction logic
            return create_pdf_from_text(text, output_folder, filename_prefix)


def main():
    input_folder = r"C:\Project\LLM-Pepeline\case-data-json"  # Specify the path to the folder containing JSON files
    output_folder = r"C:\Project\LLM-Pepeline\case-data-pdf"  # Specify the path to the folder for saving PDF files

    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            json_file = os.path.join(input_folder, filename)
            print(json_file)
            pdf_file = process_json_file(json_file, output_folder)
            print(pdf_file)
            if pdf_file:
                print(f"PDF file generated for {json_file}: {pdf_file}")


if __name__ == "__main__":
    main()
