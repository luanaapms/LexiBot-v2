from tools.text_generation import generate_text
from tools.empty_gap_activity import gerar_texto_e_lacuna
from tools.summarization import summarize_text
from tools.question_answering import answer_question
from tools.alternative_activity import gerar_atividade_multiplas_alternativas
from tools.pdf_generation import gerar_pdf_completo
from lexibot_agent import LexiAgent

import gradio as gr

# Função para gerar PDF na aba "Gerar PDF com Atividades"
def gerar_pdf_interface(context, question, text_to_summarize, prompt_texto, prompt_lacunas, prompt_mult_escolha, atividade_mult, gabarito_mult, texto_lacunas, atividade_lacunas, resumo_texto):
    atividades_mult_escolha = [{
        'questao': prompt_mult_escolha,
        'alternativas': atividade_mult.split('\n')[:4],
        'gabarito': gabarito_mult
    }] if atividade_mult else []

    atividades_lacunas = [{
        'texto_original': texto_lacunas,
        'atividade_lacuna': atividade_lacunas
    }] if texto_lacunas else []

    resumos = [resumo_texto] if resumo_texto else []

    nome_arquivo = "lexibot_material.pdf"
    gerar_pdf_completo(atividades_mult_escolha, atividades_lacunas, resumos, nome_arquivo=nome_arquivo)

    return nome_arquivo

# Função para executar o pipeline automatizado do LexiAgent
def executar_pipeline_interface(tema, texto_base):
    agente = LexiAgent()
    agente.executar_pipeline(tema, texto_base)

    return (agente.generated_text, agente.summary,
            agente.lacuna_activity[1],
            agente.multiple_choice_activity[0],
            agente.multiple_choice_activity[1])

# Função para gerar PDF a partir do pipeline automatizado
def gerar_pdf_auto(tema, texto_base):
    agente = LexiAgent()
    agente.executar_pipeline(tema, texto_base)
    arquivo_pdf = agente.gerar_pdf()
    return arquivo_pdf

# Interface Gradio
with gr.Blocks(title="LexiBot") as iface:
    gr.Markdown("# 🤖 LexiBot - Assistente Pedagógico")

    # Perguntas e Respostas
    with gr.Tab("📘 Perguntas e Respostas"):
        context = gr.Textbox(label="Digite seu texto base", lines=8)
        question = gr.Textbox(label="Faça uma pergunta")
        answer_btn = gr.Button("Responder")
        answer_output = gr.Textbox(label="Resposta")
        answer_btn.click(fn=answer_question, inputs=[context, question], outputs=answer_output)

    # Resumo de Texto
    with gr.Tab("📝 Resumo de Texto"):
        text_input = gr.Textbox(label="Digite o texto para resumir", lines=10)
        summarize_btn = gr.Button("Resumir")
        summary_output = gr.Textbox(label="Resumo")
        summarize_btn.click(fn=summarize_text, inputs=text_input, outputs=summary_output)

    # Geração de Texto
    with gr.Tab("✍️ Geração de Texto"):
        prompt_input = gr.Textbox(label="Digite um prompt", lines=4)
        generate_btn = gr.Button("Gerar")
        generated_output = gr.Textbox(label="Texto Gerado", lines=8)
        generate_btn.click(fn=generate_text, inputs=prompt_input, outputs=generated_output)

    # Atividade de Lacunas
    with gr.Tab("🚀 Atividade"):
        prompt_input2 = gr.Textbox(label="Digite um prompt", lines=3)
        gerar_atv_btn = gr.Button("Gerar")
        texto_output = gr.Textbox(label="Texto Gerado", lines=6)
        atividade_output2 = gr.Textbox(label="Atividade com Lacunas", lines=6)
        gerar_atv_btn.click(fn=gerar_texto_e_lacuna, inputs=prompt_input2,
                            outputs=[texto_output, atividade_output2])

    # Atividades de Múltipla Escolha
    with gr.Tab("📝 Atividades de Múltipla Escolha"):
        tema_input = gr.Textbox(label="Digite o tema para a atividade", lines=2)
        gerar_btn = gr.Button("Gerar Atividade")
        atividade_output = gr.Textbox(label="Atividade", lines=8)
        gabarito_output = gr.Textbox(label="Gabarito", lines=1)
        gerar_btn.click(fn=gerar_atividade_multiplas_alternativas,
                        inputs=tema_input,
                        outputs=[atividade_output, gabarito_output])

    # Gerar PDF manualmente
    with gr.Tab("📄 Gerar PDF com Atividades"):
        gr.Markdown("## Exporte as atividades que você gerou acima em um PDF")

        gerar_pdf_btn = gr.Button("Gerar PDF")

        pdf_file_output = gr.File(label="Download do PDF")

        gerar_pdf_btn.click(
            fn=gerar_pdf_interface,
            inputs=[
                context, question,
                text_input,
                prompt_input,
                prompt_input2,
                tema_input, atividade_output, gabarito_output,
                texto_output, atividade_output2,
                summary_output
            ],
            outputs=pdf_file_output
        )

    # NOVA ABA: Automatizar Atividades com LexiAgent
    with gr.Tab("🚀 Automatizar Atividades"):
        gr.Markdown("## Informe o tema e o texto base")

        tema_auto_input = gr.Textbox(label="Tema", lines=2)
        texto_base_input = gr.Textbox(label="Texto base", lines=6)
        auto_run_btn = gr.Button("Executar Pipeline")

        auto_generated_output = gr.Textbox(label="Texto Gerado", lines=6)
        auto_summary_output = gr.Textbox(label="Resumo", lines=6)
        auto_lacuna_output = gr.Textbox(label="Atividade Lacunas", lines=6)
        auto_mult_output = gr.Textbox(label="Atividade Múltipla Escolha", lines=6)
        auto_gabarito_output = gr.Textbox(label="Gabarito", lines=1)

        auto_run_btn.click(
            fn=executar_pipeline_interface,
            inputs=[tema_auto_input, texto_base_input],
            outputs=[
                auto_generated_output,
                auto_summary_output,
                auto_lacuna_output,
                auto_mult_output,
                auto_gabarito_output
            ]
        )

        gerar_pdf_auto_btn = gr.Button("Gerar PDF Final")
        pdf_file_auto_output = gr.File(label="Download do PDF")

        gerar_pdf_auto_btn.click(
            fn=gerar_pdf_auto,
            inputs=[tema_auto_input, texto_base_input],
            outputs=pdf_file_auto_output
        )

iface.launch()
