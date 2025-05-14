from tools.agent_functions import answer_question, summarize_text, generate_text, gerar_texto_e_lacuna
import gradio as gr


with gr.Blocks(title="Agente de IA") as iface:
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

iface.launch()
