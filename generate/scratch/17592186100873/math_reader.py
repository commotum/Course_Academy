"""Parse the displayed mathematical task independently of generation metadata."""
import re

def matrices(q):
    blocks=re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',q[':question/problem'],re.S)
    if not blocks and 'images/c6/c6c7e580cfd96bc23c55742535ceb40a94635c2a44b911e0d08311c3a599c2fa.png' in q[':question/problem']:
        # Visually inspected canonical-only asset; see plot-extraction.md.
        return [[[1,2],[-2,0],[1,2]],[[3,4,-1],[1,-2,2]]]
    return [[[int(x.strip()) for x in row.split('&')] for row in b.split(r'\\')] for b in blocks]
def target(q):
    text=q[':question/problem'];match=re.search(r'What is the value of \$\{?([a-z])\}?_\{(\d)(\d)\}',text)
    if not match:raise ValueError('Unrecognized target')
    return match[1],int(match[2])-1,int(match[3])-1
def fingerprint(q):
    A,B=matrices(q);_,i,j=target(q)
    # Incidental labels, matrix entries outside selected vectors, bank, field and seed do not create tasks.
    return (tuple(A[i]),tuple(row[j] for row in B))
def value(q):
    row,col=fingerprint(q);return sum(a*b for a,b in zip(row,col))
