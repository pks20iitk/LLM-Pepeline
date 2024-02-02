import weaviate
from flask import Flask, request, jsonify
from langchain.vectorstores.weaviate import Weaviate
from src.config_loader import weaviate_url
from src.Prompt import question_answer
app = Flask(__name__)


@app.route('/question-answer', methods=['POST'])
def handle_question_answer():
    client = weaviate.Client(weaviate_url)
    vectorstore = Weaviate(client, "Doc", "text")
    try:
        data = request.get_json()
        question = data.get('question')

        if not question:
            return jsonify({'error': 'Missing question parameter'}), 400

        answer, similar_docs = question_answer(question=question, vectorstore=vectorstore)

        response_data = {
            'question': question,
            'answer': answer,
            'similar_documents': [result.page_content for result in similar_docs]
        }

        return jsonify(response_data)

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
