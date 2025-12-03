from transformers import pipeline
import torch
import streamlit as st

# Cache the model so it doesn't reload on every prompt
@st.cache_resource
def load_code_model():
    """
    Loads the model for code generation.
    """
    print("⏳ Loading AI model for prompt_to_code...")
    try:
        # CLEAN string - no spaces!
        model_id = "Qwen/Qwen2.5-1.5B-Instruct" 
        
        return pipeline("text-generation", 
                        model=model_id, 
                        model_kwargs={"torch_dtype": torch.bfloat16},
                        device_map="auto") # Use 'cpu' if 'auto' fails
    except Exception as e:
        print(f"⚠️ Failed to load model: {e}")
        return None

def prompt_to_code(user_prompt):
    """
    Generates code based on natural language.
    """
    generator = load_code_model()
    
    if generator is None:
        return "# Error: AI model could not be loaded."
    
    try:
        # Structuring the prompt for Qwen-Instruct to act as a coder
        messages = [
            {"role": "system", "content": "You are an expert Python programmer. Return ONLY valid Python code. No explanations."},
            {"role": "user", "content": user_prompt}
        ]
        
        outputs = generator(
            messages, 
            max_new_tokens=512, 
            do_sample=True, 
            temperature=0.2, # Low temp for precise code
            top_p=0.9
        )
        
        return outputs[0]['generated_text'][-1]['content']
        
    except Exception as e:
        return f"# Error generating code: {e}"