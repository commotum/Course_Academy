"""Independent strict recursive TeX reader for displayed elementary mathematics.

This parser does not use generation metadata or the generator's expressions.
It preserves Derivative nodes and ordinary arithmetic operations until checks.
Unknown commands, trailing tokens, and malformed groups fail closed.
"""
import re
import sympy as S
SYMBOLS={k:S.Symbol(k,real=True) for k in ('x','y','u','v')}
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
    def __init__(self,s):
        self.source=s;self.tokens=re.findall(r'\\[A-Za-z]+|D[xyuv]|\d+(?:\.\d+)?|[A-Za-z]|[^\s]',normalized(s));self.i=0
    def peek(self):return self.tokens[self.i] if self.i<len(self.tokens) else None
    def take(self):
        t=self.peek()
        if t is None:raise ValueError('Unexpected end: '+self.source)
        self.i+=1;return t
    def group(self):
        opening=self.take()
        if opening not in ('{','('):raise ValueError('Expected group')
        closing='}' if opening=='{' else ')';val=self.sum()
        if self.take()!=closing:raise ValueError('Mismatched group')
        return val
    def atom(self):
        t=self.peek()
        if t in ('{','('):return self.group()
        t=self.take()
        if re.fullmatch(r'\d+(?:\.\d+)?',t):return S.Rational(t)
        if t in SYMBOLS:return SYMBOLS[t]
        if t=='e':return S.E
        if t==r'\pi':return S.pi
        if t==r'\frac':return self.argument()/self.argument()
        if t==r'\sqrt':return S.sqrt(self.argument())
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
        while self.peek() not in (None,'+','-',')','}',',','=','&'):
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

def parse(s):return Parser(s).parse()
def equivalent(a,b):
    difference=(a-b).doit()
    return S.simplify(S.trigsimp(difference))==0

def point_parts(s):
    depth=0
    for i,c in enumerate(s):
        if c in '{(':depth+=1
        elif c in '})':depth-=1
        elif c==',' and depth==0:return parse(s[:i]),parse(s[i+1:])
    raise ValueError('Point needs exactly two ordered coordinates: '+s)
def prompt(problem):
    math=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$',problem,re.S)
    if len(math)!=2 and len(math)!=3:raise ValueError('Unexpected prompt math layout')
    formula=math[0].split('=',1)[1].rstrip(',')
    fun=parse(formula)
    ask=math[1].rstrip('.,')
    mt=re.search(r'(?:∂|\\partial)\s*([xy])',ask)
    if not mt:mt=re.search(r'(?:\{f\}|f)_\{?([xy])\}?',ask)
    if not mt:raise ValueError('Requested derivative target absent')
    target=SYMBOLS[mt[1]]
    pointtext=math[2].rstrip('.') if len(math)==3 else ask[ask.index('('):]
    if not pointtext.startswith('(') or not pointtext.endswith(')'):raise ValueError('Point tuple malformed: '+pointtext)
    X,Y=point_parts(pointtext[1:-1]);return fun,target,{SYMBOLS['x']:X,SYMBOLS['y']:Y}
def rows(solution):
    groups=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S)
    out=[]
    for group in groups:
        result=[]
        for row in re.split(r'\\\\',group):
            if '&' not in row:raise ValueError('Missing solution alignment')
            rhs=row.split('&',1)[1].strip()
            if not rhs.startswith('='):raise ValueError('Missing solution equality')
            result.append((rhs[1:].strip(),parse(rhs[1:].strip())))
        out.append(result)
    return out
