from transformers import pipeline

qa = pipeline("question-answering", model="pierreguillou/bert-base-cased-squad-v1.1-portuguese", device=0)

def answer_question(context, question):
    result = qa(context=context, question=question)
    return result['answer']