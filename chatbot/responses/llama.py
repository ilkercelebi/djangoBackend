from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel
import torch

class ModelSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelSingleton, cls).__new__(cls)

            base_model_path = "meta-llama/Llama-3.2-3B"
            adapter_path = "C:\\Users\\furkan\\Desktop\\gitBackend\\djangoBackend\\chatbot\\responses\\checkpoint-100000"

            cls._instance.tokenizer = AutoTokenizer.from_pretrained(base_model_path)
            base_model = AutoModelForCausalLM.from_pretrained(base_model_path, torch_dtype=torch.float16)
            cls._instance.model = PeftModel.from_pretrained(base_model, adapter_path)

            cls._instance.model.eval()

        return cls._instance

def generate_response(input_text):
    model_instance = ModelSingleton()
    tokenizer = model_instance.tokenizer
    model = model_instance.model

    inputs = tokenizer(input_text, return_tensors="pt")

    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            max_length=128,
            num_beams=2,
            no_repeat_ngram_size=2,
            early_stopping=True,
        )

    output_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return output_text
