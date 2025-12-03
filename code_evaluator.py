def evaluate_code(code):
    feedback = []

    if not code or len(code) > 10000:  
        return ["Invalid code input"]
    
    if len(code) > 500:
        feedback.append("Consider breaking down large functions into smaller ones.")

    if "eval(" in code:
        feedback.append("Avoid using `eval()` for security reasons.")

    if "for" in code and "range(len" in code:
        feedback.append("Consider using `enumerate()` instead of `range(len())`.")

    if "import *" in code:
        feedback.append("Avoid wildcard imports. Use explicit imports.")

    return feedback if feedback else ["No major issues found! Code looks good."]