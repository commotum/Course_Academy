"""Independent parser for every printed exponential ODE/formal derivative row.

Reads displayed strings, not generation component ASTs. Fails closed on any
unrecognized token; exact derivatives are taken on the printed operator input.
"""
import re
import sympy as sp
X=sp.Symbol('x',real=True)
A,ALPHA,BETA,Y,D=sp.symbols('A alpha beta y yd',real=True)
class Parser:
    def __init__(self,text,context=None):
        self.context=context or {}
        text=text.strip().rstrip('.,')
        for old,new in [('{y}_{c}','yc'),('{y}_{p}','yp'),('y_{c}','yc'),('y_{p}','yp'),('{y}','y'),('^{′}',"'"),('′',"'"),(r'\alpha','alpha'),(r'\beta','beta'),(r'\cdot','*'),(r'\left',''),(r'\right','')]:text=text.replace(old,new)
        text=re.sub(r'\b(yc|yp|y)\(x\)',r'\1',text)
        self.tokens=[];position=0
        while position<len(text):
            if text[position].isspace():position+=1;continue
            match=re.match(r'\\frac\b|alpha|beta|yc|yp|[0-9]+|[xyeA{}()+\-*/^\']',text[position:])
            if not match:raise ValueError('Unsupported printed math: '+repr(text[position:]))
            self.tokens.append(match[0]);position+=len(match[0])
        self.index=0
    def peek(self):return self.tokens[self.index] if self.index<len(self.tokens) else None
    def take(self,wanted=None):
        token=self.peek()
        if token is None or wanted is not None and token!=wanted:raise ValueError((wanted,token))
        self.index+=1;return token
    def expression(self):
        v=self.product()
        while self.peek() in ('+','-'):
            op=self.take();t=self.product();v=v+t if op=='+' else v-t
        return v
    def product(self):
        v=self.unary()
        while True:
            token=self.peek()
            if token in ('*','/'):
                op=self.take();t=self.unary();v=v*t if op=='*' else v/t
            elif token is not None and (token.isdigit() or token in ['alpha','beta','yc','yp','x','y','e','A','{','(',r'\frac']):v*=self.unary()
            else:return v
    def unary(self):
        if self.peek() in ['+','-']:
            op=self.take();v=self.unary();return v if op=='+' else -v
        v=self.atom()
        if self.peek()=='^':self.take();v=v**self.unary()
        while self.peek()=="'":
            self.take();v=self.context.get('yd',D) if v==Y else sp.diff(v,X)
        return v
    def group(self):
        opening=self.take();assert opening in ['{','(']
        v=self.expression();self.take('}' if opening=='{' else ')');return v
    def atom(self):
        if self.peek() in ['{','(']:return self.group()
        t=self.take()
        if t.isdigit():return sp.Integer(t)
        if t==r'\frac':return self.group()/self.group()
        value={'x':X,'A':A,'alpha':ALPHA,'beta':BETA,'e':sp.E,'y':Y}.get(t)
        if t in self.context:return self.context[t]
        if value is None:raise ValueError('Unbound printed symbol '+t)
        return value

def expression(t,context=None):
    p=Parser(t,context);v=p.expression()
    if p.peek() is not None:raise ValueError('Unconsumed tokens '+repr(p.tokens[p.index:]))
    return v

def math_spans(s):return re.findall(r'\$\$[\s\S]*?\$\$|(?<!\$)\$(?!\$)[^$]*?\$',s)
def inner(s):return s[2:-2] if s.startswith('$$') else s[1:-1]
def eq_sides(s,context=None):return [expression(t.replace('&',''),context) for t in s.split('=')]
def family_equivalent(f,g,a):
    """Complete affine A-family equivalence under nonzero rescaling+shift."""
    ef=sp.diff(f,A);eg=sp.diff(g,A)
    if ef==0 or eg==0 or sp.diff(f,A,2)!=0 or sp.diff(g,A,2)!=0:return False
    ratio=sp.simplify(ef/eg)
    shift=sp.simplify((f.subs(A,0)-g.subs(A,0))/sp.exp(a*X))
    return not ratio.free_symbols and ratio.is_zero is False and not shift.free_symbols

def audit(record):
    q=record['question'];p=record['generation']['parameters'];template=record['generation']['template']
    prompt=math_spans(q[':question/problem']);ode=inner(prompt[0]).strip().rstrip('.')
    lhs,rhs=eq_sides(ode)
    assert sp.diff(lhs,D)==1 and sp.diff(lhs,Y,D)==0
    a=-sp.diff(lhs,Y)
    assert not a.free_symbols and sp.simplify(lhs-(D-a*Y))==0
    assert rhs.free_symbols <= {X}
    yc=eq_sides(inner(prompt[1]),{'yc':Y})[1]
    assert sp.simplify(sp.diff(yc,X)-a*yc)==0 and yc.has(A)
    f=q[':question/answer-fields'][0]
    expected=A*sp.exp(a*X)+sp.exp(a*X)*sp.integrate(sp.exp(-a*X)*rhs,X)
    for answer in f.get(':answer-field/choices',[]):
        value=expression(answer[':answer/value'])
        assert family_equivalent(value,expected,a),answer
        assert sp.simplify(sp.diff(value,X)-a*value-rhs)==0
    assert a==p['a']
    stated=sp.Integer(p['b'])*sp.exp(p['k']*X)
    if template=='mixed':stated=sp.Integer(p['b'])*sp.exp(p['a']*X)+sp.Integer(p['c'])*sp.exp(p['k']*X)
    assert sp.simplify(rhs-stated)==0,'Printed ODE differs from declared parameters'
    solution=q.get(':question/worked-solution')
    if solution is None:return {'equations':0,'derivative_rows':0,'raw_missing':True}
    blocks=[inner(t) for t in math_spans(solution) if t.startswith('$$')]
    assert len(blocks)==(10 if template=='mixed' else 8), 'missing/extra mathematical stage'
    assert len(blocks[4].split(r'\\'))==(4 if template=='resonant' else 3), 'substitution stage sequence'
    prose_forcing=re.search(r'right-hand side is \$([^$]+)\$',solution)
    assert prose_forcing is not None
    assert sp.simplify(expression(prose_forcing[1])-rhs)==0,'stale forcing in worked-solution prose'
    resonance_match=re.search(r'and \$([^$]+)\$ is (not )?a term in the complementary solution',solution)
    assert resonance_match is not None
    compared=expression(resonance_match[1])
    exponent_matches=sp.simplify(compared-sp.exp(a*X))==0
    assert exponent_matches==(resonance_match[2] is None), 'false resonance statement'
    if template=='mixed':
        other=re.search(r'while \$([^$]+)\$ is not',solution)
        assert other is not None and sp.simplify(expression(other[1])-sp.exp(a*X))!=0
    # Trial is found from actual printed yp equation before derivative stage.
    trial_block=blocks[2];trial=expression(trial_block.split('=',1)[1])
    # Independent coefficient extraction via substitution samples remains exact:
    # residual coefficients of distinct exponentials can be isolated algebraically.
    if template=='nonresonant':coeffs={ALPHA:sp.simplify(rhs/(sp.diff(trial,X)-a*trial)*ALPHA)}
    elif template=='resonant':coeffs={ALPHA:sp.simplify(rhs/(sp.diff(trial,X)-a*trial)*ALPHA)}
    else:
        ua=sp.diff(trial,ALPHA);ub=sp.diff(trial,BETA)
        la=sp.diff(ua,X)-a*ua;lb=sp.diff(ub,X)-a*ub
        r1,r2=rhs.subs(X,0),rhs.subs(X,1)
        coeffs=sp.solve([ALPHA*la.subs(X,0)+BETA*lb.subs(X,0)-r1,ALPHA*la.subs(X,1)+BETA*lb.subs(X,1)-r2],[ALPHA,BETA])
    assert coeffs and all(not v.free_symbols for v in coeffs.values())
    yp=trial.subs(coeffs);assert sp.simplify(sp.diff(yp,X)-a*yp-rhs)==0
    context={'yc':yc,'yp':trial,'y':yc+yp,'yd':sp.diff(yc+yp,X)}
    count=0;derivative_rows=0
    for block_index,block in enumerate(blocks):
        block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip()
        previous=None
        for row in block.split(r'\\'):
            row=row.strip().rstrip('.,')
            if not row:continue
            for segment in row.split(r'\quad \text{and} \quad'):
                sides=segment.split('=')
                assert len(sides)>1,(block_index,segment)
                if not sides[0].replace('&','').strip():
                    assert previous is not None; sides[0]=previous
                previous=sides[0].replace('&','').strip()
                values=[expression(t.replace('&',''),context) for t in sides]
                if block_index==3:
                    # Every formal derivative and product-rule row holds for arbitrary
                    # trial coefficients, prior to their determination.
                    assert all(sp.simplify(v-values[0])==0 for v in values[1:]),segment
                    derivative_rows+=1
                else:
                    assert all(sp.simplify((v-values[0]).subs(coeffs))==0 for v in values[1:]),(segment,values,coeffs)
                count+=len(values)-1
    expected_derivatives=4 if template in ['resonant','mixed'] else 1
    assert derivative_rows==expected_derivatives
    # Check actual formal-operator structure, not only equivalent reduced rows.
    if template in ['resonant','mixed']:
        derivative=blocks[3]
        assert derivative.count('^{′}')==(4 if template=='mixed' else 3)
        assert len(derivative.split(r'\\'))==4
    return {'equations':count,'derivative_rows':derivative_rows,'forcing':str(rhs),'homogeneous_exponent':str(a)}
