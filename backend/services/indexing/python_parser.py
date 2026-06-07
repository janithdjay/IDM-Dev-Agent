import ast

from .models import SymbolEntry
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

        # -----------------------
        # Top-level functions
        # -----------------------

        for node in tree.body:

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):

                visitor = CallVisitor()
                visitor.visit(node)

                symbols.append(
                    SymbolEntry(
                        symbol_id=generate_id(),
                        name=node.name,
                        type="function",
                        file=file_path,
                        start_line=node.lineno,
                        end_line=getattr(node, "end_lineno", node.lineno),
                        parent=None,
                        calls=visitor.calls,
                        referenced_vars=[]
                    )
                )

            # -----------------------
            # Classes
            # -----------------------

            elif isinstance(node, ast.ClassDef):
                class_visitor = CallVisitor()
                class_visitor.visit(node)

                symbols.append(
                    SymbolEntry(
                        symbol_id=generate_id(),
                        name=node.name,
                        type="class",
                        file=file_path,
                        start_line=node.lineno,
                        end_line=getattr(node, "end_lineno", node.lineno),
                        parent=None,
                        calls=class_visitor.calls,
                        referenced_vars=[]
                    )
                )

                # -----------------------
                # Methods
                # -----------------------

                for child in node.body:
                    if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        method_visitor = CallVisitor()
                        method_visitor.visit(child)

                        symbols.append(
                            SymbolEntry(
                                symbol_id=generate_id(),
                                name=child.name,
                                type="method",
                                file=file_path,
                                start_line=child.lineno,
                                end_line=getattr(
                                    child,
                                    "end_lineno",
                                    child.lineno
                                ),
                                parent=node.name,
                                calls=method_visitor.calls,
                                referenced_vars=[]
                            )
                        )

        return symbols, imports