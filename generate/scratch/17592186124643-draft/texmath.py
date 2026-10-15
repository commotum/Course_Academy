"""Independent strict recursive TeX reader for displayed elementary mathematics.

This parser does not use generation metadata or the generator's expressions.
It preserves Derivative nodes and ordinary arithmetic operations until checks.
Unknown commands, trailing tokens, and malformed groups fail closed.
"""
import re
import sympy as S
SYMBOLS={k:S.Symbol(k,real=True) for k in ('x','y','u','v','h')}
FUNCS={'sin':S.sin,'cos':S.cos,'tan':S.tan,'cot':S.cot,'sec':S.sec,'csc':S.csc,'ln':S.log,'log':S.log,'exp':S.exp}
def normalized(s):
    s=s.replace('⁡','').replace('π',r'\pi ').replace(r'\partial','∂')
    s=re.sub(r'\\operatorname\{(sin|cos|tan|cot|sec|csc|ln|log)\}',lambda m:'\\'+m[1]+' ',s)
    s=re.sub(r'\{(csc|sec|cot|sin|cos|tan)\}',lambda m:'\\'+m[1]+' ',s)
    s=re.sub(r'\\(?:d?frac)\{∂\}\{∂([xyuv])\}',lambda m:' D'+m[1]+' ',s)
    s=s.replace(r'\left','').replace(r'\right','').replace(r'\,',' ').replace(r'\!',' ').replace(r'\;',' ')
    s=s.replace(r'\cdot','*').replace(r'\times','*').replace(r'\dfrac',r'\frac')
    return s.strip()
class Parser:
    def __init__(self,s,fun=None):
        self.fun=fun;self.source=s;self.tokens=re.findall(r'\\[A-Za-z]+|D[xyuv]|\d+(?:\.\d+)?|[A-Za-z]|[^\s]',normalized(s));self.i=0
    def peek(self):return self.tokens[self.i] if self.i<len(self.tokens) else None
    def take(self):
        t=self.peek()
        if t is None:raise ValueError('Unexpected end: '+self.source)
        self.i+=1;return t
    def group(self):
        opening=self.take()
        if opening not in ('{','(','['):raise ValueError('Expected group')
        closing={'{':'}','(':')','[':']'}[opening];val=self.sum()
        if self.take()!=closing:raise ValueError('Mismatched group')
        return val
    def atom(self):
        t=self.peek()
        if t in ('{','(','['):return self.group()
        t=self.take()
        if re.fullmatch(r'\d+(?:\.\d+)?',t):return S.Rational(t)
        if t in SYMBOLS:return SYMBOLS[t]
        if t=='e':return S.E
        if t==r'\pi':return S.pi
        if t==r'\frac':return self.argument()/self.argument()
        if t==r'\sqrt':
            degree=2
            if self.peek()=='[':degree=self.group()
            return self.argument()**(1/S.sympify(degree))
        if t=='f':
            if self.fun is None:raise ValueError('Unbound f')
            if self.take()!='(':raise ValueError('Function needs argument pair')
            X=self.sum()
            if self.take()!=',':raise ValueError('Function needs two coordinates')
            Y=self.sum()
            if self.take()!=')':raise ValueError('Unclosed function')
            return self.fun.subs({SYMBOLS['x']:X,SYMBOLS['y']:Y},simultaneous=True)
        if t.startswith('D') and len(t)==2:return S.Derivative(self.argument(),SYMBOLS[t[1]],evaluate=False)
        if t.startswith('\\') and t[1:] in FUNCS:
            power=None
            if self.peek()=='^':self.take();power=self.argument()
            numeric_argument=bool(self.peek() and re.fullmatch(r'\d+(?:\.\d+)?',self.peek()))
            argument=self.argument()
            if numeric_argument and self.peek() in (r'\pi','x','y','u','v'):
                argument=argument*self.power()
            val=FUNCS[t[1:]](argument)
            return val if power is None else val**power
        raise ValueError('Unknown token '+repr(t)+' in '+self.source)
    def argument(self):
        return self.group() if self.peek() in ('{','(') else self.power()
    def power(self):
        val=self.atom()
        if self.peek()=='^':self.take();val=val**self.argument()
        return val
    def unary(self):
        if self.peek()=='+':self.take();return self.unary()
        if self.peek()=='-':self.take();return -self.unary()
        return self.power()
    def product(self):
        val=self.unary()
        while self.peek() not in (None,'+','-',')','}',']',',','=','&'):
            token=self.peek()
            if token=='*':self.take();val=val*self.unary()
            elif token=='/':self.take();val=val/self.unary()
            else:val=val*self.unary()
        return val
    def sum(self):
        val=self.product()
        while self.peek() in ('+','-'):
            sign=self.take();other=self.product();val=val+other if sign=='+' else val-other
        return val
    def parse(self):
        val=self.sum()
        if self.peek() is not None:raise ValueError('Trailing token '+repr(self.peek())+' in '+self.source)
        return val

def parse(s,fun=None):return Parser(s,fun).parse()
def equivalent(a,b):
    difference=(a-b).doit()
    return S.simplify(S.trigsimp(difference))==0


def quotient(text,fun=None):
    source=text.strip().rstrip('.')
    match=re.match(r'^(?:\{lim\}|\\lim)_\{h\s*\\to\s*0\}|^lim_\(h\s*→\s*0\)',source)
    if not match:raise ValueError('Missing h -> 0 limit: '+text)
    body=source[match.end():]
    if not re.search(r'\\(?:d?frac)\{(?:1|.*)\}\{h\}|/\(h\)',body):
        raise ValueError('Missing increment denominator: '+text)
    return parse(body,fun)

def prompt(problem):
    math=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$',problem,re.S)
    formula=math[0].split('=',1)[1].rstrip(',')
    fun=parse(formula)
    target=re.search(r'(?:∂|\\partial)\s*([xy])',math[1])
    if target:target=target[1];point=None
    else:
        mt=re.fullmatch(r'f_([xy])\((-?\d+),(-?\d+)\)',math[1]);assert mt,'Unrecognized target point'
        target=mt[1];point=(S.Integer(mt[2]),S.Integer(mt[3]))
    return fun,SYMBOLS[target],point

def witness_unequal(a,b):
    # A nonzero value at one common finite-domain point disproves equality.
    # Positive test points avoid all observed log/root/denominator boundaries.
    for X,Y,H in [(2,3,S.Rational(1,5)),(3,2,S.Rational(1,7)),(4,5,S.Rational(1,3))]:
        v=(a-b).subs({SYMBOLS['x']:X,SYMBOLS['y']:Y,SYMBOLS['h']:H})
        if v.is_zero is False:return True
        z=complex(v.evalf(40))
        if abs(z)>1e-20:return True
    return False
