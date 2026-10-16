"""Remove the earlier repair's augmented divider from explicitly labelled coefficient matrices."""
import re
from normalize import environment

def repair(text):
    replacements = []
    for formula in re.finditer(r'\$\$[\s\S]*?\$\$', text):
        paragraph = text[:formula.start()].rstrip().split('\n\n')[-1]
        if not re.search(r'\bcoefficient\s+matrix\b', paragraph, re.I): continue
        if re.search(r'\baugment', paragraph, re.I): continue
        block = formula[0]
        for matrix in re.finditer(r'\\left\[\s*\\begin\{array\}\{(c+\|c)\}', block):
            span = environment(block, block.index(r'\begin{array}', matrix.start()))
            if not span: continue
            closing = re.match(r'\s*\\right\]', block[span[2]:])
            if not closing: continue
            body = block[matrix.end():span[1]]
            replacements.append((formula.start() + matrix.start(), formula.start() + span[2] + closing.end(),
                                 r'\begin{bmatrix}' + body + r'\end{bmatrix}'))
    for start, end, value in sorted(replacements, reverse=True): text = text[:start] + value + text[end:]
    return text
