"""Presentation repair for individually reviewed standalone integral prompts."""
from math_format import MATH,normalize_prose
def display_integral(problem):
    # Called only at four audited generator problem-authoring boundaries.
    # Source evidence, solution references, banks and blank fragments are untouched.
    def replace(m):
        value=m[0]
        if value.startswith(('$$',r'\[',r'\(')) or r'\int' not in value:return value
        return '\n\n$$\n'+value[1:-1].strip()+'\n$$\n\n'
    return normalize_prose(MATH.sub(replace,problem))
