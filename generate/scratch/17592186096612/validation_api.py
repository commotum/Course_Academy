"""Reuse frozen generator QA definitions without rerunning its artifact-writing driver."""
import ast
from pathlib import Path
path = Path(__file__).with_name('validate.py')
tree = ast.parse(path.read_text())
body = []
for node in tree.body:
    if isinstance(node, ast.For):
        break
    body.append(node)
exec(compile(ast.Module(body=body, type_ignores=[]), str(path), 'exec'), globals())
