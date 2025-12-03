import os
import ast

def analyze_codebase(directory):
    summary = {
        "total_files": 0,
        "python_files": 0,
        "total_lines": 0,
        "code_lines": 0,
        "comment_lines": 0,
        "classes": 0,
        "functions": 0,
        "duplicate_blocks": 0
    }
    
    # Use a hash set for memory efficiency, not full strings
    seen_lines = set()

    for root, _, files in os.walk(directory):
        for f in files:
            summary["total_files"] += 1
            
            if f.endswith(".py"):
                summary["python_files"] += 1
                filepath = os.path.join(root, f)
                
                try:
                    with open(filepath, 'r', encoding="utf-8", errors="ignore") as file:
                        content = file.read()
                        lines = content.splitlines()
                        summary["total_lines"] += len(lines)
                        
                        # 1. Smart Line Analysis
                        for line in lines:
                            stripped = line.strip()
                            # Ignore empty lines and short lines (like 'pass', 'else:') for dup detection
                            if not stripped:
                                continue
                            
                            if stripped.startswith("#"):
                                summary["comment_lines"] += 1
                            else:
                                summary["code_lines"] += 1
                                # Only check duplicates for substantial lines (> 15 chars)
                                if len(stripped) > 15:
                                    line_hash = hash(stripped)
                                    if line_hash in seen_lines:
                                        summary["duplicate_blocks"] += 1
                                    else:
                                        seen_lines.add(line_hash)

                        # 2. AST Analysis (Structure)
                        try:
                            tree = ast.parse(content)
                            for node in ast.walk(tree):
                                if isinstance(node, ast.ClassDef):
                                    summary["classes"] += 1
                                elif isinstance(node, ast.FunctionDef):
                                    summary["functions"] += 1
                                elif isinstance(node, ast.AsyncFunctionDef):
                                    summary["functions"] += 1
                        except SyntaxError:
                            pass # Skip files with syntax errors

                except Exception as e:
                    print(f"Error reading {f}: {e}")

    return summary