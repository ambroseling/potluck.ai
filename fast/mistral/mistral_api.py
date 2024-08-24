from transformers import MistralForCausalLM
from transformers import AutoTokenizer
from fastapi import WebSocket


tokenizer = AutoTokenizer.from_pretrained('/home/tiny_ling/projects/potluckai/fast/Mistral-7B-v0.1')

prompt = "What are the roots of unity?"
tokenized_prompts = tokenizer(prompt, return_tensors="pt") 

model = MistralForCausalLM.from_pretrained('/home/tiny_ling/projects/potluckai/fast/Mistral-7B-v0.1')


def run_mistral_inference(prompt:str,websocket:WebSocket):
    generation = model.generate(**tokenized_prompts, max_new_tokens=512)
    return generation