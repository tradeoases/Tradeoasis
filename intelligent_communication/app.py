from flask import Flask, request, jsonify
import torch
from chat import *
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import json
import torch.nn.functional as F

# Load the model and tokenizer (you can reuse the existing functions)
model, tokenizer = load_model_and_tokenizer()
custom_responses = load_custom_responses("custom_responses.json")

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('input_text')

    if user_input.lower() in ['exit', 'quit', 'bye']:
        response = "Chatbot: Goodbye!"
    else:
        custom_response = get_custom_response(user_input, custom_responses)
        if custom_response:
            response = "Chatbot: " + custom_response
        else:
            response = generate_response(model, tokenizer, user_input)
            logits = model(torch.tensor(tokenizer.encode(response)).unsqueeze(0)).logits
            confidence_score = calculate_confidence(logits)
            if confidence_score < 0.5:
                response = "Chatbot: " + ask_for_clarification()
            else:
                response = "Chatbot: " + response

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
