from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=0)

def summarize_text(text):
    summary = summarizer(text, max_length=500, min_length=90, do_sample=False)
    return summary[0]['summary_text']