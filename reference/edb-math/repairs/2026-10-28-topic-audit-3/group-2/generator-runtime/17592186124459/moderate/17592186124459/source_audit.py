"""Validate current captured sources; keep the frozen generator replay unchanged."""
import json,re,sys
from pathlib import Path
import sympy as s
import validate as v
HERE=Path(__file__).parent

def scalar(t):
    t=t.replace(r'\sqrt',r' \sqrt')
    t=re.sub(r'\{sec\}\^\{2\}⁡\(([^()]*)\)',r' sec(\1)^2',t)
    for op in ('tan','sec'):
        t=t.replace(r'\operatorname{'+op+'}', ' '+op+' ').replace('{'+op+'}',' '+op+' ')
    # Source LaTeX uses bare trig arguments and juxtaposition. Give each
    # familiar single-token argument parentheses before implicit multiplication.
    for op in ('sin','cos'):
        t=t.replace(r'\operatorname{'+op+'}⁡', '\\'+op).replace(r'\operatorname{'+op+'}', '\\'+op)
        t=re.sub(r'\\'+op+r'\s*(\\pi|[xyz]|[01])(?![A-Za-z])',lambda m:' '+op+'('+m[1]+') ',t)
    return v.math(t)

def vector(t):
    t=t.strip();sign=1
    if t.startswith('-⟨'):sign=-1;t=t[1:]
    if t.startswith('⟨'):return [sign*scalar(e) for e in t[1:t.index('⟩')].replace(r'\,','').split(',')]
    e=s.expand(scalar(t));return [e.coeff(i) for i in v.ivs[:2]]
def formal_args(t):
    out=[]
    for m in re.finditer(r'\\frac\{∂\}\{∂([xyz])\}\(',t):
        i=m.end();start=i;depth=1
        while depth:depth+=(t[i]=='(')-(t[i]==')');i+=1
        out.append((m[1],scalar(t[start:i-1])))
    return out

def audit(q):
    errors=[];text=q[':question/problem'];sol=q.get(':question/worked-solution','')
    if any('\\\\' in a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f.get(':answer-field/choices',[])):errors.append('double-escaped LaTeX commands in current answer values')
    F=scalar(re.search(r'[fg]\(x,\s*y(?:,\s*z)?\)\s*=([^$]+)',text)[1])
    P=[scalar(e) for e in re.search(r'point \$\(([^)]+)\)',text)[1].split(',')];vs=(v.x,v.y,v.z)[:len(P)]
    d=[s.diff(F,x) for x in vs];g=[s.simplify(e.subs(dict(zip(vs,P)))) for e in d];sign=-1 if 'decrease most rapidly' in text else 1;target=[sign*e for e in g]
    f=q[':question/answer-fields'][0];values=[vector(a[':answer/value'].replace('\\\\','\\')) for a in f[':answer-field/choices']]
    matches=[v.parallel(a,target) for a in values]
    if sum(matches)!=1:errors.append('ambiguous direction bank')
    correct=f.get(':answer-field/correct',{}).get(':answer/id')
    if not correct or any(ok!=(str(a[':answer/id'])==str(correct)) for a,ok in zip(f[':answer-field/choices'],matches)):errors.append('missing or incorrect answer designation')
    for i,a in enumerate(values):
        if any(v.parallel(a,b) for b in values[:i]):errors.append('duplicate direction choices');break
    if not sol:errors.append('absent worked solution')
    else:
        blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
        rows=blocks[0].split(r'\\')
        args=formal_args(rows[0])
        if any(not v.equal(e,F) for var,e in args):errors.append('held-partial operand differs from prompt')
        if not v.veq(vector(rows[1].split(' & =')[1]),[sign*e for e in d]):errors.append('symbolic partial row differs from gradient')
        for row in rows[2:]:
            if not v.veq(vector(row.split(' & =')[1]),target):errors.append('substitution row differs from evaluated gradient');break
        final=re.search(r'Therefore,.*?direction of \$(.*?)\.\$',sol,re.S)
        if not final or not v.veq(vector(final[1]),target):errors.append('conclusion differs from target')
        label=re.search(r'evaluate it at the point \$(.*?)[:?]',sol)
        if label and label[1].rstrip('$')!=re.search(r'point \$\(([^)]+)\)',text)[0].split('$')[1]:errors.append('evaluation prose has stale point')
        labels=re.findall(r'∇[fg](\([^xyz)]*\))\s*&',blocks[0]);p='('+','.join(str(e) for e in P)+')'
        # Rendered fractions/pi are checked through the actual substituted row.
        for label in labels:
            pp=[scalar(e) for e in label[1:-1].split(',')]
            if not v.veq(pp,P):errors.append('evaluation row has stale point')
    # Content distinctness is the direction criterion, with dimensionality and
    # held-partial function backbone recorded separately for source families.
    first=next(e for e in target if e!=0)
    signature=[str(s.simplify(e/s.Abs(first))) for e in target]
    return {'id':q[':db/id'],'math_academy_id':q.get(':question/math-academy-id'),'level':str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1],'field_type':str(f[':answer-field/type'][':db/ident']),'choice_count':len(values),'plot':'none','function':str(F),'point':list(map(str,P)),'direction':signature,'errors':sorted(set(errors)),'validated':not errors}
if __name__=='__main__':
    kp=json.loads((HERE/'reference/initial/kp.json').read_text());rows=[]
    for q in kp[':knowledge-point/questions']:
        try:r=audit(q)
        except Exception as e:r={'id':q[':db/id'],'validated':False,'errors':[repr(e)]}
        rows.append(r)
    (HERE/'reference/initial/source-audit.json').write_text(json.dumps(rows,indent=2));print(json.dumps(rows,indent=2))
