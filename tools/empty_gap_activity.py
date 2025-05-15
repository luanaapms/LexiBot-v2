import random
from .text_generation import generate_text

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