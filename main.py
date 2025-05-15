from tools.text_generation import generate_text
from tools.empty_gap_activity import gerar_texto_e_lacuna
from tools.summarization import summarize_text
from tools.question_answering import answer_question
from tools.alternative_activity import gerar_atividade_multiplas_alternativas
from tools.pdf_generation import gerar_pdf_completo

import gradio as gr
import os

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

with gr.Blocks(title="LexiBot") as iface:
    gr.Markdown("# 🤖 LexiBot - Assistente Pedagógico")

    with gr.Tab("📘 Perguntas e Respostas"):
        context = gr.Textbox(label="Digite seu texto base", lines=8)
        question = gr.Textbox(label="Faça uma pergunta")
        answer_btn = gr.Button("Responder")
        answer_output = gr.Textbox(label="Resposta")
        answer_btn.click(fn=answer_question, inputs=[context, question], outputs=answer_output)

    with gr.Tab("📝 Resumo de Texto"):
        text_input = gr.Textbox(label="Digite o texto para resumir", lines=10)
        summarize_btn = gr.Button("Resumir")
        summary_output = gr.Textbox(label="Resumo")
        summarize_btn.click(fn=summarize_text, inputs=text_input, outputs=summary_output)

    with gr.Tab("✍️ Geração de Texto"):
        prompt_input = gr.Textbox(label="Digite um prompt", lines=4)
        generate_btn = gr.Button("Gerar")
        generated_output = gr.Textbox(label="Texto Gerado", lines=8)
        generate_btn.click(fn=generate_text, inputs=prompt_input, outputs=generated_output)

    with gr.Tab("🚀 Atividade"):
        prompt_input2 = gr.Textbox(label="Digite um prompt", lines=3)
        gerar_atv_btn = gr.Button("Gerar")
        texto_output = gr.Textbox(label="Texto Gerado", lines=6)
        atividade_output2 = gr.Textbox(label="Atividade com Lacunas", lines=6)
        gerar_atv_btn.click(fn=gerar_texto_e_lacuna, inputs=prompt_input2,
                            outputs=[texto_output, atividade_output2])

    with gr.Tab("📝 Atividades de Múltipla Escolha"):
        tema_input = gr.Textbox(label="Digite o tema para a atividade", lines=2)
        gerar_btn = gr.Button("Gerar Atividade")
        atividade_output = gr.Textbox(label="Atividade", lines=8)
        gabarito_output = gr.Textbox(label="Gabarito", lines=1)
        gerar_btn.click(fn=gerar_atividade_multiplas_alternativas,
                        inputs=tema_input,
                        outputs=[atividade_output, gabarito_output])

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

iface.launch()
