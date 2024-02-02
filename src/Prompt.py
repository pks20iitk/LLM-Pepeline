from src.indexing import compute_embedding
from langchain.vectorstores.weaviate import Weaviate
from langchain.prompts import PromptTemplate
from src.LLM_model import llm


def question_answer(question: str, vectorstore: Weaviate):
    embedding = compute_embedding([question])
    similar_docs = vectorstore.max_marginal_relevance_search_by_vector(embedding)
    content = [x.page_content for x in similar_docs]
    prompt_template = PromptTemplate.from_template(
        """\
    Given context about the subject, answer the question based on the context provided to the best of your ability.
    Context: {context}
    Question:
    {question}
    Answer:
    """
    )
    prompt = prompt_template.format(context=content, question=question)
    answer = llm(prompt)
    return answer, similar_docs
