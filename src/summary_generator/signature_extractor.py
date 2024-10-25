import ast
from dataclasses import dataclass
from pathlib import Path
from typing import List, Set
from loguru import logger

@dataclass
class Signature:
    """Represents a Python function or class signature with documentation."""
    name: str
    kind: str  # 'function' or 'class'
    args: list[str]
    returns: str | None
    docstring: str | None
    decorators: list[str]

class SignatureExtractor:
    """Extracts detailed signatures from Python files."""
    
    def get_type_annotation(self, node: ast.AST) -> str:
        """Convert AST annotation node to string representation."""
        if isinstance(node, ast.Name):
            return node.id
        elif isinstance(node, ast.Constant):
            return repr(node.value)
        elif isinstance(node, ast.Subscript):
            # Handle generics, e.g., list[str]
            container = self.get_type_annotation(node.value)
            params = self.get_type_annotation(node.slice)
            return f"{container}[{params}]"
        elif isinstance(node, ast.BinOp):
            # Handle unions with |, e.g., str | None
            left = self.get_type_annotation(node.left)
            right = self.get_type_annotation(node.right)
            return f"{left} | {right}"
        elif isinstance(node, ast.Tuple):
            # Handle tuple types
            elts = [self.get_type_annotation(e) for e in node.elts]
            return f"[{', '.join(elts)}]"
        return "Any"  # Default fallback

    def get_arg_string(self, arg: ast.arg) -> str:
        """Convert function argument to string with type annotation."""
        arg_str = arg.arg
        if arg.annotation:
            type_str = self.get_type_annotation(arg.annotation)
            arg_str += f": {type_str}"
        return arg_str

    def extract_signatures(self, source: str) -> List[Signature]:
        """Extract all function and class signatures from source code."""
        try:
            tree = ast.parse(source)
            signatures = []
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
                    # Get args with type hints
                    args = []
                    for arg in node.args.args:
                        args.append(self.get_arg_string(arg))
                    
                    # Get return type
                    returns = None
                    if node.returns:
                        returns = self.get_type_annotation(node.returns)
                    
                    # Get decorators
                    decorators = []
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name):
                            decorators.append(f"@{decorator.id}")
                        elif isinstance(decorator, ast.Call):
                            if isinstance(decorator.func, ast.Name):
                                decorators.append(f"@{decorator.func.id}(...)")
                    
                    signatures.append(Signature(
                        name=node.name,
                        kind='async_function' if isinstance(node, ast.AsyncFunctionDef) else 'function',
                        args=args,
                        returns=returns,
                        docstring=ast.get_docstring(node),
                        decorators=decorators
                    ))
                    
                elif isinstance(node, ast.ClassDef):
                    bases = []
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            bases.append(base.id)
                    
                    decorators = []
                    for decorator in node.decorator_list:
                        if isinstance(decorator, ast.Name):
                            decorators.append(f"@{decorator.id}")
                    
                    signatures.append(Signature(
                        name=node.name,
                        kind='class',
                        args=bases,
                        returns=None,
                        docstring=ast.get_docstring(node),
                        decorators=decorators
                    ))
                    
            return signatures
        except Exception as e:
            logger.error(f"Error parsing source: {e}")
            return []

    def format_signature(self, sig: Signature) -> str:
        """Format a signature for display."""
        lines = []
        
        # Add decorators
        for decorator in sig.decorators:
            lines.append(decorator)
        
        # Format the signature line
        if sig.kind == 'class':
            base_str = f"({', '.join(sig.args)})" if sig.args else ""
            lines.append(f"class {sig.name}{base_str}")
        else:
            async_prefix = "async " if sig.kind == 'async_function' else ""
            args_str = ", ".join(sig.args)
            return_str = f" -> {sig.returns}" if sig.returns else ""
            lines.append(f"{async_prefix}def {sig.name}({args_str}){return_str}")
        
        # Add docstring if present
        if sig.docstring:
            # Format docstring with proper indentation
            doc_lines = sig.docstring.split('\n')
            if len(doc_lines) == 1:
                lines.append(f'    """{sig.docstring}"""')
            else:
                lines.append('    """')
                for doc_line in doc_lines:
                    if doc_line.strip():
                        lines.append(f"    {doc_line}")
                lines.append('    """')
        
        return "\n".join(lines)

def generate_python_summary(root_dir: str | Path) -> str:
    """Generate enhanced Python project structure summary.
    
    Args:
        root_dir: Root directory of the project
        
    Returns:
        Formatted markdown string of Python signatures
    """
    root_dir = Path(root_dir)
    extractor = SignatureExtractor()
    content = ["# Python Project Structure\n"]
    
    # Find all Python files
    for file in sorted(root_dir.rglob("*.py")):
        if any(part.startswith('.') for part in file.parts):
            continue
        if '__pycache__' in file.parts:
            continue
            
        try:
            # Get relative path
            rel_path = file.relative_to(root_dir)
            content.append(f"## {rel_path}")
            content.append("```python")
            
            # Extract and format signatures
            source = file.read_text()
            signatures = extractor.extract_signatures(source)
            
            if signatures:
                content.extend(extractor.format_signature(sig) for sig in signatures)
            
            content.append("```\n")
            
        except Exception as e:
            logger.error(f"Error processing {file}: {e}")
    
    return "\n".join(content)
