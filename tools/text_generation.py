from transformers import pipeline

text_generator = pipeline("text-generation", model="Pierreguillou/gpt2-small-portuguese", device=0)

def generate_text(prompt):
    generated = text_generator(prompt, max_length=500 ,num_return_sequences=1)
    return generated[0]['generated_text']
