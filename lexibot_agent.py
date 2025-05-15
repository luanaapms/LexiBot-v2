from tools.text_generation import generate_text
from tools.summarization import summarize_text
from tools.empty_gap_activity import gerar_texto_e_lacuna
from tools.alternative_activity import gerar_atividade_multiplas_alternativas
from tools.pdf_generation import gerar_pdf_completo

class LexiAgent:
    def __init__(self):
        self.generated_text = ""
        self.summary = ""
        self.lacuna_activity = ("", "")
        self.multiple_choice_activity = ("", "")

    def executar_pipeline(self, tema, texto_base):
        # Etapa 1: Gerar texto a partir do tema
        print("Gerando texto base...")
        self.generated_text = generate_text(texto_base)

        # Etapa 2: Resumir o texto gerado
        print("Gerando resumo...")
        self.summary = summarize_text(self.generated_text)

        # Etapa 3: Gerar atividade de lacunas sobre o resumo
        print("Gerando atividade de lacunas...")
        self.lacuna_activity = gerar_texto_e_lacuna(self.summary)

        # Etapa 4: Gerar atividade de múltipla escolha sobre o tema
        print("Gerando atividade de múltipla escolha...")
        self.multiple_choice_activity = gerar_atividade_multiplas_alternativas(tema)

    def gerar_pdf(self, nome_arquivo="lexibot_material.pdf"):
        print("Gerando PDF final...")
        atividades_mult_escolha = [{
            'questao': self.multiple_choice_activity[0],
            'alternativas': self.multiple_choice_activity[0].split('\n')[:4],
            'gabarito': self.multiple_choice_activity[1]
        }] if self.multiple_choice_activity[0] else []

        atividades_lacunas = [{
            'texto_original': self.lacuna_activity[0],
            'atividade_lacuna': self.lacuna_activity[1]
        }] if self.lacuna_activity[0] else []

        resumos = [self.summary] if self.summary else []

        gerar_pdf_completo(atividades_mult_escolha, atividades_lacunas, resumos, nome_arquivo)
        return nome_arquivo
