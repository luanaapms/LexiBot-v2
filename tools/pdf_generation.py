from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, ListFlowable, ListItem
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.units import cm

def gerar_pdf_completo(atividades_multiplas, atividades_lacunas, resumos, nome_arquivo="material.pdf"):
    doc = SimpleDocTemplate(nome_arquivo, pagesize=A4, rightMargin=2*cm, leftMargin=2*cm, topMargin=2*cm, bottomMargin=2*cm)
    elements = []
    styles = getSampleStyleSheet()

    # Estilos customizados
    title_style = ParagraphStyle('title_style', parent=styles['Heading1'], fontSize=20, alignment=TA_CENTER, spaceAfter=20)
    section_style = ParagraphStyle('section_style', parent=styles['Heading2'], fontSize=16, spaceBefore=20, spaceAfter=10)
    normal_style = styles['Normal']
    list_style = ParagraphStyle('list_style', parent=styles['Normal'], leftIndent=20, spaceAfter=5)

    # Título principal
    elements.append(Paragraph("📚 Material Didático Gerado", title_style))

    # Atividades de Múltipla Escolha
    if atividades_multiplas:
        elements.append(Paragraph("Atividades de Múltipla Escolha", section_style))
        for idx, atividade in enumerate(atividades_multiplas, start=1):
            elements.append(Paragraph(f"{idx}. {atividade['questao']}", normal_style))
            elements.append(Spacer(1, 5))

            alternativas_letras = ['a)', 'b)', 'c)', 'd)']
            for i, alt in enumerate(atividade['alternativas']):
                if i < len(alternativas_letras):
                    alt_formatada = f"<b>{alternativas_letras[i]}</b> {alt}"
                    elements.append(Paragraph(alt_formatada, list_style))

            if atividade['gabarito']:
                elements.append(Spacer(1, 5))
                elements.append(Paragraph(f"<b>Gabarito:</b> {atividade['gabarito']}", normal_style))

            elements.append(Spacer(1, 15))


    # Atividades de Completar Lacunas
    if atividades_lacunas:
        elements.append(Paragraph("Atividades de Completar Lacunas", section_style))
        for idx, atividade in enumerate(atividades_lacunas, start=1):
            elements.append(Paragraph(f"{idx}. Complete as lacunas do texto abaixo:", normal_style))
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(atividade['atividade_lacuna'], normal_style))
            elements.append(Spacer(1, 10))

    # Resumos
    if resumos:
        elements.append(Paragraph("Resumos Gerados", section_style))
        for idx, resumo in enumerate(resumos, start=1):
            elements.append(Paragraph(f"Resumo {idx}:", normal_style))
            elements.append(Paragraph(resumo, normal_style))
            elements.append(Spacer(1, 10))

    doc.build(elements)
