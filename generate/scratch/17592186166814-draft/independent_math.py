"""Independent exact slope transcription for validation, never learner generation.

These are separately transcribed mathematical equations, not original answer-ID
or value tables. All coefficient/exponent slots are evaluated from the instance.
"""
import sympy as s
X,Y=s.symbols('x y',real=True)

def slopes(meta,level):
    p=meta['parameters'];t=meta['template']
    if t=='authored_triplet':
        rows=[]
        for kind in p['kinds']:
            family,role=kind.split(':');z=Y if level=='hard' or role=='y' else X
            f={'power':lambda:z**p['n'],'exp':lambda:s.exp(z),'sqrt':lambda:s.sqrt(z),'log':lambda:s.log(z),'sin':lambda:s.sin(z),'cos':lambda:s.cos(z)}[family]()
            if level=='easy':rows.append(f)
            elif level=='moderate':rows.append((p['a']*f-p['b'])/(Y if role=='y' else X))
            else:rows.append((X+(p['a'] if role=='y' else p['c']))*(f+p['b'])/(X+p['a']))
        return rows
    a=lambda n:s.Integer(p['n'+str(n)])
    recipes={
      'q-95984':lambda:[s.exp(Y),a(3)*Y,(X*Y+s.sqrt(X))/a(2)],
      'q-96387':lambda:[s.exp(X),a(3)/Y,a(2)*(X*Y+s.exp(X))],
      'q-118863':lambda:[a(8)*s.exp(Y)+a(2),(s.cos(Y)-a(3))/Y,(s.exp(Y)+a(8))/X],
      'q-96702':lambda:[s.exp(Y)+X,(s.sqrt(Y)+a(2))/Y,(a(5)*Y+X/Y)/a(4)],
      'q-96703':lambda:[(a(2)+a(3)*Y**a(3))/X,a(7)*Y**a(2)+1/Y,s.log(Y)],
      'q-96705':lambda:[a(3)*Y**a(3)*s.exp(-Y),s.log(Y)+a(2)*X,Y/(a(5)*X**2)],
      'q-96712':lambda:[1-s.sqrt(Y),s.tan(Y)+s.exp(a(2)),(a(4)*Y+1)/(X*Y)],
      'q-118858':lambda:[-s.exp(-a(2)*Y),a(2)-s.sqrt(X*Y),s.log(Y)],
      'q-118859':lambda:[a(3)*X**a(2)+1,s.exp(a(3)*Y)-a(6)*Y,s.log(a(2)*X**a(2)+1)],
      'q-118868':lambda:[(a(8)-a(6)*X*Y**a(2))/X**a(2),a(3)*Y**a(2)-1/X,s.atan(Y**a(2)+a(2))],
      'q-118869':lambda:[-Y/(s.atan(Y)+a(2)*s.pi),X**a(2)-Y**a(2),s.sin(X)],
      'q-118870':lambda:[s.exp(a(3)-Y)-a(2),(1-s.cos(Y))/Y,s.tan(X+Y)],
      'q-96711':lambda:[s.sin(Y/X),X**a(2)*Y+s.exp(X),a(3)/Y**a(2)+1],
      'q-96713':lambda:[-s.sqrt(Y)*s.exp(Y),Y**a(3)+a(2)*s.exp(X),a(2)/Y**a(3)+a(3)*s.sqrt(Y)],
      'q-96715':lambda:[s.sqrt(X**a(2)+s.sin(Y)),s.sec(s.sqrt(a(2)*Y)),Y**a(3)+a(3)*s.sqrt(Y)],
    }
    return recipes[t]()
