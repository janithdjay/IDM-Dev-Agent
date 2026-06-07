import ast
from typing import List, Tuple
from .models import SymbolEntry, ImportEntry
from .utils import generate_id

class CallVisitor(ast.NodeVisitor): 
    def __init__(self): 
        self.calls = [] 
        
    def visit_Call(self, node): 
        if isinstance(node.func, ast.Name): 
            self.calls.append(node.func.id) 
        elif isinstance(node.func, ast.Attribute): 
            self.calls.append(node.func.attr) 
            self.generic_visit(node)

class PythonParser:

    def parse(self, file_path: str, source_code: str):
        tree = ast.parse(source_code)

        symbols = []
        imports = []

        for node in ast.walk(tree):

            # FUNCTIONS
            if isinstance(node, ast.FunctionDef):

                visitor = CallVisitor()
                visitor.visit(node)

                symbols.append(SymbolEntry(
                    symbol_id=generate_id(),
                    name=node.name,
                    type="function",
                    file=file_path,
                    start_line=node.lineno,
                    end_line=getattr(node, "end_lineno", node.lineno),
                    calls=visitor.calls
                ))

            # CLASSES
            elif isinstance(node, ast.ClassDef):

                visitor = CallVisitor()
                visitor.visit(node)

                symbols.append(SymbolEntry(
                    symbol_id=generate_id(),
                    name=node.name,
                    type="class",
                    file=file_path,
                    start_line=node.lineno,
                    end_line=getattr(node, "end_lineno", node.lineno),
                    calls=visitor.calls
                ))

        return symbols, imports