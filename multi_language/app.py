from flask import Flask, request, jsonify
import torch
from transformers import MBartForConditionalGeneration, MBartTokenizer

app = Flask(__name__)

# Load the pre-trained mBART model and tokenizer
model_name = "facebook/mbart-large-50-many-to-many-mmt"  # Multi-language translation model
tokenizer = MBartTokenizer.from_pretrained(model_name)
model = MBartForConditionalGeneration.from_pretrained(model_name)
model.eval()

# Function to translate text between multiple languages
def translate_text(text, src_lang="en_XX", tgt_lang="de_DE"):
    # Encode the input text using the source language tokenizer
    encoded_text = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)

    # Set the source and target language for translation
    model.config.src_lang = src_lang
    model.config.tgt_lang = tgt_lang

    # Translate the encoded input text using the pre-trained model
    with torch.no_grad():
        translation = model.generate(**encoded_text)

    # Decode the translated output tokens using the target language tokenizer
    translated_text = tokenizer.decode(translation[0], skip_special_tokens=True)

    return translated_text


@app.route('/translate', methods=['POST'])
def translate():
    data = request.json
    text = data['text']
    src_lang = data.get('src_lang', 'en_XX')
    tgt_lang = data.get('tgt_lang', 'de_DE')

    translated_output = translate_text(text, src_lang=src_lang, tgt_lang=tgt_lang)
    return jsonify({'translated_text': translated_output})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
