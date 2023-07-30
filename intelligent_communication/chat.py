import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer
import json
import torch.nn.functional as F


def load_model_and_tokenizer():
    model_name = "gpt2-large"
    tokenizer = GPT2Tokenizer.from_pretrained(model_name)
    model = GPT2LMHeadModel.from_pretrained(model_name)
    return model, tokenizer


def load_custom_responses(filename):
    with open(filename, 'r') as file:
        custom_responses = json.load(file)
    return custom_responses["Custom_questions"]


def generate_response(model, tokenizer, prompt, max_length=150, top_k=50, temperature=0.7):
    input_ids = tokenizer.encode(prompt, return_tensors='pt')
    attention_mask = torch.ones(input_ids.shape, dtype=torch.long, device=input_ids.device)
    pad_token_id = tokenizer.eos_token_id

    with torch.no_grad():
        output = model.generate(
            input_ids,
            max_length=max_length,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            attention_mask=attention_mask,
            pad_token_id=pad_token_id,
            top_k=top_k,
            temperature=temperature,

        )

    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response


def get_custom_response(prompt, custom_responses):
    for item in custom_responses:
        if prompt.lower() in item["question"].lower():
            return item["answer"]
    return None


def calculate_confidence(logits):
    probabilities = F.softmax(logits, dim=-1)[0]
    confidence_score = torch.max(probabilities).item()
    print("Confidence Score:", confidence_score)
    return confidence_score


def ask_for_clarification():
    polite_request = "I apologize, but I'm not quite sure what you mean. Could you please provide more context or " \
                     "clarify your question?"
    return polite_request


def chat_with_bot(model, tokenizer, custom_responses):
    print("Chatbot: Hi! How can I assist you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("Chatbot: Goodbye!")
            break

        custom_response = get_custom_response(user_input, custom_responses)
        if custom_response:
            print("Chatbot:", custom_response)
        else:
            response = generate_response(model, tokenizer, user_input)
            logits = model(torch.tensor(tokenizer.encode(response)).unsqueeze(0)).logits
            confidence_score = calculate_confidence(logits)
            if confidence_score < 0.5:
                print("Chatbot:", ask_for_clarification())
            else:
                print("Chatbot:", response)


if __name__ == "__main__":
    model, tokenizer = load_model_and_tokenizer()
    custom_responses = load_custom_responses("custom_responses.json")
    chat_with_bot(model, tokenizer, custom_responses)
