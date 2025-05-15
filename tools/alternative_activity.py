from .text_generation import generate_text
import re

def gerar_atividade_multiplas_alternativas(tema):
    prompt_ativ = (
        f"Crie uma questão de múltipla escolha sobre o tema: {tema}.\n"
        "Deve ter 4 alternativas (A, B, C, D).\n"
        "Inclua a resposta correta no final no formato: 'Gabarito: A'\n"
    )
    
    texto_gerado = generate_text(prompt_ativ)

    gabarito = None
    padrao = re.compile(r'(Gabarito|Resposta|Answer):\s*([A-D])', re.IGNORECASE)
    
    for linha in texto_gerado.split('\n'):
        m = padrao.search(linha)
        if m:
            gabarito = m.group(0).strip()
            break

    return texto_gerado.strip(), gabarito
