import torch
import streamlit as st
from transformers import pipeline

# --- 1. CACHED MODEL LOADING (Crucial for Speed) ---
@st.cache_resource
def load_review_model():
    print("⏳ Loading AI for Code Review...")
    try:
        return pipeline(
            "text-generation",
            model="Qwen/Qwen2.5-1.5B-Instruct",
            model_kwargs={"torch_dtype": torch.bfloat16},
            device_map="auto", 
        )
    except Exception as e:
        print(f"⚠️ Error loading model: {e}")
        return None

def review_code_as_senior(code, context=None):
    """
    Uses Qwen to act as a Senior Developer and critique code.
    """
    pipe = load_review_model()
    
    if not pipe:
        return "⚠️ AI Reviewer is offline. Check your console logs."

    # --- 2. CONSTRUCT PROMPT ---
    system_msg = "You are a Senior Software Engineer. Review the code strictly. Be concise. Use bullet points."
    
    user_msg = f"""
    Review this code snippet:
    
    ```python
    {code}
    ```
    
    {f"Context: {context}" if context else ""}
    
    **PROVIDE FEEDBACK ON:**
    1. 🛡️ **Security**: (Vulnerabilities, injection risks)
    2. ⚡ **Performance**: (Time complexity, memory usage)
    3. 🧹 **Clean Code**: (Naming, readability, structure)
    4. ✅ **Best Practices**: (Pythonic idioms, error handling)
    
    Keep it constructive and short.
    """

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg}
    ]

    # --- 3. GENERATE ---
    try:
        outputs = pipe(
            messages,
            max_new_tokens=800,
            do_sample=True,
            temperature=0.4, # Lower temp = more professional/critical
            top_p=0.9,
        )
        return outputs[0]["generated_text"][-1]["content"]
    except Exception as e:
        return f"Error generating review: {e}"