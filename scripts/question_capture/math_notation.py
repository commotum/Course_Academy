"""Structural identities for common displayed math notation, without algebra."""
import re


# Use the same symbol spellings as the live MathML extractor. ASCII letters
# remain letters: the variable product pi must never turn into the symbol π.
SYMBOLS = dict(zip('αβγδθλμρσωπ∞±∓≤≥≠→∈∉∪∩∫∑∏×⋅·÷',
    ('alpha beta gamma delta theta lambda mu rho sigma omega pi infty pm mp '
     'leq geq neq rightarrow in notin cup cap int sum prod times cdot cdot div').split()))
ALIASES = {'dfrac':'frac', 'tfrac':'frac', 'le':'leq', 'ge':'geq', 'ne':'neq',
           'to':'rightarrow'}
LAYOUT = {'displaystyle','textstyle','scriptstyle','scriptscriptstyle','left','right',
          'big','Big','bigg','Bigg','bigl','bigr','Bigl','Bigr','biggl','biggr',
          'Biggl','Biggr','quad','qquad','enspace','thinspace'}
OPERATORS = {'sin','cos','tan','sec','csc','cot','sinh','cosh','tanh','ln','log',
             'exp','arcsin','arccos','arctan','arg','lim','min','max'}
SUPERSCRIPTS = str.maketrans('⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻', '0123456789+-')
SUBSCRIPTS = str.maketrans('₀₁₂₃₄₅₆₇₈₉₊₋', '0123456789+-')


def tokens(value):
    value = value.strip().strip('$').replace('−','-')
    value = re.sub('[⁰¹²³⁴⁵⁶⁷⁸⁹⁺⁻]+', lambda m:'^{'+m[0].translate(SUPERSCRIPTS)+'}', value)
    value = re.sub('[₀₁₂₃₄₅₆₇₈₉₊₋]+', lambda m:'_{'+m[0].translate(SUBSCRIPTS)+'}', value)
    result = []
    for match in re.finditer(r'\\[A-Za-z]+|\\.|[\s\S]', value):
        token = match[0]
        if token in SYMBOLS:
            token = '\\' + SYMBOLS[token]
        if token.startswith('\\'):
            name = token[1:]
            if name in LAYOUT or name in (',',';','!',':',' '):
                continue
            token = '\\' + ALIASES.get(name,name)
        elif token.isspace():
            continue
        result.append(token)
    return tuple(result)


def sequence_identity(nodes):
    nodes = tuple(nodes)
    # Convert only a whole numeric ratio, including one used as an exponent.
    # Do not change x^1/3, 1/(3x), or a fraction's argument boundaries.
    if all(n[0] == 'char' for n in nodes):
        ratio = re.fullmatch(r'([+-]?\d+)/([+-]?\d+)', ''.join(n[1] for n in nodes))
        if ratio:
            return (('frac', tuple(('char',c) for c in ratio[1]),
                     tuple(('char',c) for c in ratio[2])),)
    return nodes


class Parser:
    def __init__(self, source):
        self.source, self.position = source, 0

    def take(self):
        if self.position == len(self.source):
            raise ValueError('Incomplete mathematical notation')
        token = self.source[self.position]
        self.position += 1
        return token

    def argument(self):
        if self.position < len(self.source) and self.source[self.position] == '{':
            self.position += 1
            return self.sequence('}')
        return (self.atom(),)

    def sequence(self, closing=None):
        nodes = []
        while self.position < len(self.source):
            token = self.source[self.position]
            if token == closing:
                self.position += 1
                return sequence_identity(nodes)
            if token == '}':
                raise ValueError('Unexpected closing group')
            if token in ('^','_') and nodes:
                self.position += 1
                argument = self.argument()
                base = nodes.pop()
                slot = 2 if token == '_' else 3
                if base[0] == 'script' and not base[slot]:
                    parts = list(base)
                else:
                    parts = ['script',base,(),()]
                parts[slot] = argument
                nodes.append(tuple(parts))
            elif token == '⁡':
                self.position += 1
                start = len(nodes)
                while start and nodes[start-1][0] == 'char' and nodes[start-1][1].isalpha():
                    start -= 1
                name = ''.join(n[1] for n in nodes[start:])
                if name in OPERATORS:
                    nodes[start:] = [('operator',name)]
                else:
                    nodes.append(('apply',))
            else:
                nodes.append(self.atom())
        if closing is not None:
            raise ValueError('Unclosed mathematical group')
        return sequence_identity(nodes)

    def atom(self):
        token = self.take()
        if token == '{':
            content = self.sequence('}')
            return content[0] if len(content) == 1 else ('group',content)
        if token in ('(', '[', r'\{'):
            end = {'(':')','[':']',r'\{':r'\}'}[token]
            return ('fence',token,self.sequence(end),end)
        if token == r'\frac':
            numerator = self.argument()
            denominator = self.argument()
            return ('frac',numerator,denominator)
        if token == r'\sqrt':
            index = ()
            if self.position < len(self.source) and self.source[self.position] == '[':
                self.position += 1
                index = self.sequence(']')
            return ('root',index,self.argument())
        if token == r'\operatorname':
            argument = self.argument()
            if all(n[0] == 'char' for n in argument):
                name = ''.join(n[1] for n in argument)
                if name in OPERATORS:
                    return ('operator',name)
            return ('operatorname',argument)
        if token in (r'\mathrm',r'\mathit',r'\text'):
            argument = self.argument()
            if len(argument) == 1 and argument[0][0] == 'char' and argument[0][1].isalnum():
                return argument[0]
            return ('styled',token,argument)
        if token[0] == '\\':
            name = token[1:]
            return ('operator',name) if name in OPERATORS else ('command',name)
        return ('char',token)


def identity(value):
    source = tokens(value)
    try:
        return repr(('math',Parser(source).sequence()))
    except ValueError:
        # Unsupported/unbalanced notation still has a stable token identity.
        # It cannot collide with a successfully parsed expression.
        return repr(('tokens',source))
