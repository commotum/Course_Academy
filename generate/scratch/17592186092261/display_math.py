"""Private strict reader for the displayed source/general-exponential grammar.

No generator AST dependencies. Unsupported characters or unconsumed tokens fail.
Implicit x3^u parses as x times 3^u; a displayed numeric 43^u parses as base 43.
"""
import re
import sympy as sp

X,U=sp.symbols('x u',real=True)


class Parser:
    def __init__(self,text):
        text=text.replace('\u2061','').replace(r'\operatorname{ln}',r'\ln')
        text=re.sub(r'(?<![A-Za-z\\])ln',lambda _:r'\ln',text)
        for command in (r'\left',r'\right',r'\,',r'\!',r'\quad',r'\qquad'):
            text=text.replace(command,'')
        text=text.replace(r'\cdot','*').replace(r'\times','*')
        self.tokens=[];self.i=0;pos=0
        while pos<len(text):
            if text[pos].isspace():pos+=1;continue
            m=re.match(r'\\(?:frac|ln)|\d+|[xu{}()+\-*/^]',text[pos:])
            if not m:raise ValueError('Unsupported displayed notation: '+repr(text[pos:]))
            self.tokens.append(m.group());pos+=len(m.group())

    def peek(self):return self.tokens[self.i] if self.i<len(self.tokens) else None
    def take(self,expected=None):
        v=self.peek()
        if v is None or expected is not None and expected!=v:raise ValueError(('Expected',expected,v))
        self.i+=1;return v
    def expression(self):
        v=self.product()
        while self.peek() in ('+','-'):
            op=self.take();w=self.product();v=v+w if op=='+' else v-w
        return v
    def product(self):
        v=self.unary()
        while True:
            t=self.peek()
            if t in ('*','/'):
                op=self.take();w=self.unary();v=v*w if op=='*' else v/w
            elif t is not None and (t.isdigit() or t in ('x','u','{','(',r'\frac',r'\ln')):v*=self.unary()
            else:return v
    def unary(self):
        if self.peek() in ('+','-'):
            op=self.take();v=self.unary();return -v if op=='-' else v
        v=self.atom()
        if self.peek()=='^':self.take();v=v**self.unary()
        return v
    def group(self):
        t=self.take()
        if t not in ('{','('):raise ValueError('A group is required')
        v=self.expression();self.take('}' if t=='{' else ')');return v
    def atom(self):
        t=self.peek()
        if t in ('{','('):return self.group()
        t=self.take()
        if t.isdigit():return sp.Integer(t)
        if t in ('x','u'):return X if t=='x' else U
        if t==r'\frac':return self.group()/self.group()
        if t==r'\ln':
            # Both source bare ln4 and grouped SymPy ln{(4)} occur.
            return sp.log(self.group() if self.peek() in ('{','(') else self.atom())
        raise ValueError('Unsupported atom '+t)


def expression(text):
    p=Parser(text);value=p.expression()
    if p.peek() is not None:raise ValueError('Unconsumed mathematical tokens')
    return value


def equal(a,b):
    return sp.simplify(sp.expand_log(a-b,force=True))==0


def prompt_object(prompt):
    blocks=re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',prompt,re.S)
    definition=next(b for b in blocks if re.match(r'(?:f\(x\)|y)\s*=',b))
    name='f' if definition.startswith('f') else 'y'
    f=expression(definition.split('=',1)[1].rstrip(' ,.;'))
    powers=[p for p in f.atoms(sp.Pow) if p.exp.has(X) and p.base.is_Integer]
    if len(powers)!=1:raise AssertionError('Expected exactly one displayed base power')
    b,u=powers[0].base,powers[0].exp;c=sp.cancel(f/b**u)
    point=None
    if 'slope' in prompt:
        at=re.search(r'point where \$x=(.*?)\$',prompt)
        if not at:raise AssertionError('Missing point')
        point=expression(at[1].rstrip(' .'))
    fragment=bool(re.search(r'\{\{field-1\}\}\$\\cdot',prompt))
    return {'f':f,'name':name,'base':b,'inner':u,'scale':c,'point':point,'fragment':fragment}
