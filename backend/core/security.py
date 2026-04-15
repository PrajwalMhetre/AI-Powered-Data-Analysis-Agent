import ast
from core.config import settings

def is_safe_python_code(code: str) -> bool:
    """
    Analyzes Python code AST to ensure no destructive built-in modules like 
    os, sys, subprocess, or shutil are imported/used if restricted.
    """
    if not settings.RESTRICT_FILE_OPERATIONS:
        return True
        
    restricted_modules = {"os", "sys", "subprocess", "shutil", "pathlib"}
    
    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split('.')[0] in restricted_modules:
                        return False
            elif isinstance(node, ast.ImportFrom):
                if node.module and node.module.split('.')[0] in restricted_modules:
                    return False
    except SyntaxError:
        # If code is invalid, standard python exec will catch it during runtime, 
        # but LangChain agents handle their own tracebacks.
        pass
        
    return True

def sanitize_dataframe(df):
    """
    Data Anonymization stub.
    In a real industrial setting, PII detection algorithms (like Presidio) 
    would strip columns like 'Email', 'SSN', 'Phone', etc.
    """
    potential_pii = ["email", "ssn", "phone", "password", "card_number"]
    cols_to_drop = [c for c in df.columns if any(pii in c.lower() for pii in potential_pii)]
    if cols_to_drop:
        df = df.drop(columns=cols_to_drop)
    return df
