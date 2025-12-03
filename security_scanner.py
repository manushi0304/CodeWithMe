def scan_security_issues(code):
    """
    A heuristic-based security scanner. 
    It looks for dangerous patterns without needing an LLM.
    """
    issues = []
    
    if not code or len(code.strip()) == 0:
        return ["⚠️ No code provided."]
    
    # 1. Dangerous Executions
    if "eval(" in code:
        issues.append("🔴 **Critical**: `eval()` detected. This allows arbitrary code execution.")
    if "exec(" in code:
        issues.append("🔴 **Critical**: `exec()` detected. Highly unsafe if input is untrusted.")
        
    # 2. File Operations
    if "open(" in code and ("'w'" in code or '"w"' in code):
        issues.append("Ow **Risk**: File writing detected. Ensure paths are sanitized to prevent overwriting system files.")
        
    # 3. Input Handling
    if "input(" in code and "int(" not in code and "float(" not in code:
        issues.append("🟡 **Warning**: Raw `input()` usage. Ensure you validate or sanitize user input.")
        
    # 4. Serialization
    if "pickle.load" in code:
        issues.append("🔴 **Critical**: `pickle` is insecure. Use `json` or `yaml` for untrusted data.")
        
    # 5. Hardcoded Secrets (Basic Check)
    if "api_key" in code.lower() or "password" in code.lower() or "secret" in code.lower():
        if "=" in code and ('"' in code or "'" in code):
            issues.append("🟠 **Security**: Possible hardcoded secret/API key detected. Use environment variables.")

    # 6. SQL Injection (Basic Check)
    if "cursor.execute(" in code and ("%" in code or ".format(" in code or "fstring" in code):
        issues.append("🔴 **Critical**: Potential SQL Injection. Use parameterized queries `(?, ?)` instead of string formatting.")

    if not issues:
        return ["✅ No obvious security vulnerabilities found (Static Analysis)."]
    
    return issues