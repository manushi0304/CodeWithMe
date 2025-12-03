from transformers import pipeline
from accelerate import Accelerator
import torch

accelerator = Accelerator()

@accelerator.on_main_process
def load_model():
    return pipeline("text2text-generation", 
                   model="t5-small",  
                   device_map="cpu")

def translate_code(code, from_lang="python", to_lang="java"):
    lang_map = {"python": "py", "java": "java", "cpp": "cpp", "javascript": "js"}
    source_lang = lang_map.get(from_lang, "en")
    target_lang = lang_map.get(to_lang, "en")
    
    with accelerator.local_main_process_first():
        translator = load_model()
        return translator(
            f"{source_lang} {code}",
            src_lang=source_lang,
            tgt_lang=target_lang,
            max_length=1024
        )[0]['generated_text']