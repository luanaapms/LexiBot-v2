import random
from transformers import pipeline


qa = pipeline("question-answering", model="distilbert/distilbert-base-cased-distilled-squad")
summarizer = pipeline("summarization", model="facebook/bart-base")
text_generator = pipeline("text-generation", model="gpt2")


def answer_question(context, question):
    result = qa(context=context, question=question)
    return result['answer']

def summarize_text(text):
    summary = summarizer(text, max_length=150, min_length=90, do_sample=False)
    return summary[0]['summary_text']

def generate_text(prompt):
    generated = text_generator(prompt, max_length=150, num_return_sequences=1)
    return generated[0]['generated_text']


def gerar_completar_lacunas(texto):
    palavras = texto.split()
    if len(palavras) < 6:
        return "Texto muito curto para gerar lacunas."

    indices = random.sample(range(1, len(palavras)-1), min(3, len(palavras)-2))
    texto_com_lacunas = palavras[:]
    for i in indices:
        palavra_original = palavras[i]
        underline = "_" * len(palavra_original)
        texto_com_lacunas[i] = underline
    return ' '.join(texto_com_lacunas)

def gerar_texto_e_lacuna(prompt):
    texto = generate_text(prompt)
    atividade = gerar_completar_lacunas(texto)
    return texto, atividade