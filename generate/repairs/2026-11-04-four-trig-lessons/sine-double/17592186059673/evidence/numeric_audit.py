"""Independent numeric witnesses for visible questions and all radio choices.

This reads displayed TeX through the capture AST, not generator metadata or
answer recipes. Equality at sample points is a check, not a symbolic proof.
"""
import collections,json,math,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[5];sys.path.insert(0,str(ROOT))
from scripts.question_capture.math_notation import Parser,tokens
from scripts.question_capture.math_format import MATH,normalize_function_operators
FUN={'sin':math.sin,'cos':math.cos,'tan':math.tan,'cot':lambda x:1/math.tan(x),'sec':lambda x:1/math.cos(x),'csc':lambda x:1/math.sin(x)}
class Numeric:
    def __init__(self,nodes,bindings):self.nodes=nodes;self.i=0;self.bindings=bindings
    def peek(self):return self.nodes[self.i] if self.i<len(self.nodes) else None
    def take(self):n=self.peek();self.i+=1;return n
    def evaluate(self):
        result=self.sum()
        if self.i!=len(self.nodes):raise ValueError('unconsumed '+str(self.peek()))
        return result
    def sub(self,nodes):return Numeric(nodes,self.bindings).evaluate()
    def sum(self):
        v=self.product()
        while self.peek() in [('char','+'),('char','-')]:
            op=self.take()[1];w=self.product();v=v+w if op=='+' else v-w
        return v
    def product(self):
        v=self.unary()
        while self.peek() is not None and self.peek() not in [('char','+'),('char','-')]:
            if self.peek() in [('char','/'),('command','div')]:self.take();v/=self.unary()
            elif self.peek() in [('command','cdot'),('command','times'),('char','·')]:self.take();v*=self.unary()
            else:v*=self.unary()
        return v
    def unary(self):
        if self.peek() in [('char','+'),('char','-')]:return (-1 if self.take()[1]=='-' else 1)*self.unary()
        return self.atom(self.take())
    def atom(self,n):
        if n is None:raise ValueError('missing atom')
        kind=n[0]
        if kind=='char':
            if re.fullmatch(r'\d+(?:\.\d+)?',n[1]):return float(n[1])
            if n[1] in self.bindings:return self.bindings[n[1]]
        elif kind=='command':
            if n[1]=='pi':return math.pi
            if n[1] in self.bindings:return self.bindings[n[1]]
        elif kind=='fence':return self.sub(n[2])
        elif kind=='group':return self.sub(n[1])
        elif kind=='frac':return self.sub(n[1])/self.sub(n[2])
        elif kind=='root':return self.sub(n[2])**(1/(self.sub(n[1]) if n[1] else 2))
        elif kind=='operator' and n[1] in FUN:return FUN[n[1]](self.function_argument())
        elif kind=='script':
            if n[1][0]=='operator' and n[1][1] in FUN:v=FUN[n[1][1]](self.function_argument())
            else:v=self.atom(n[1])
            if n[2]:raise ValueError('subscript')
            if n[3] in [(('command','circ'),),(('char','∘'),),(('char','°'),)]:return v*math.pi/180
            return v**self.sub(n[3]) if n[3] else v
        raise ValueError('unsupported atom '+str(n))
    def function_argument(self):
        first=self.peek();v=self.unary();following=self.peek()
        if first and (first[0]=='frac' or first[0]=='char' and first[1].replace('.','').isdigit()):
            if following and (following[0]=='char' and following[1] in self.bindings or following==('command','pi')):v*=self.unary()
            elif following==('command','cdot'):self.take();v*=self.unary()
        return v

def nodes(tex):
    tex=tex.strip().strip('$').strip().rstrip('.,;?').split('=')[0]
    tex=re.sub(r'\\(?:begin|end)\{aligned\}','',tex).replace(r'\\','').replace('&','')
    # Audit the intended function in legacy source spelling, while retaining
    # those missing operator wrappers as a separate formatting finding.
    tex=re.sub(r'\{(cos|sin)\}(?=\s*\^)',lambda m:'\\'+m[1],tex)
    tex=normalize_function_operators(tex)
    return Parser(tokens(tex)).sequence()

def field_key(f):
    ref=f.get(':answer-field/correct')
    if not ref:return None
    if isinstance(ref,dict) and ':answer/value' in ref:return ref[':answer/value']
    ident=ref[1] if isinstance(ref,list) else ref.get(':answer/id')
    return next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==ident)

def target(q):
    for match in MATH.finditer(q[':question/problem']):
        s=match[0]
        if re.search(r'\\(?:sin|cos|tan|cot|sec|csc|operatorname)|\b(?:sin|cos|tan|cot|sec|csc)\b',s):return s
    raise ValueError('No expression')

def key_expression(q,keys):
    if len(keys)==1:return next(iter(keys.values()))
    text=q[':question/problem'];first=re.search(r'\{\{[^{}]+\}\}',text)
    if not first:raise ValueError('Multiple fields without placeholders')
    if re.search(r'A=\$?\s*\{\{field-1\}\}',text):return '('+keys['field-1']+r')\sin x+('+keys['field-2']+r')\cos x'
    tail=text[first.start():]
    for key,value in keys.items():tail=tail.replace('{{'+key+'}}','('+value+')')
    return tail.replace('$','').strip()

def audit(q,label,kid):
    fields=q.get(':question/answer-fields',[]);keys={f[':answer-field/key']:field_key(f) for f in fields}
    if not fields or any(v is None for v in keys.values()):return {'label':label,'kp':kid,'status':'no_response_key'}
    try:
        left=nodes(target(q));right=nodes(key_expression(q,keys));points=[]
        for value in [.371,.823,1.197]:
            bindings={n:value for n in ('x','t','w','theta')};a=Numeric(left,bindings).evaluate();b=Numeric(right,bindings).evaluate();points.append((a,b))
        matched=all(abs(a-b)<1e-8*max(1,abs(a),abs(b)) for a,b in points)
        errors=[]
        for f in fields:
            kind=f[':answer-field/type'];kind=kind.get(':db/ident') if isinstance(kind,dict) else kind
            if not kind.endswith(('/radio','/select')):continue
            selected=field_key(f);equivalents=[]
            for a in f[':answer-field/choices']:
                if a[':answer/value']==selected:continue
                alternative=nodes(a[':answer/value'])
                same=all(abs(Numeric(alternative,{n:v for n in ('x','t','w','theta')}).evaluate()-b)<1e-8*max(1,abs(b)) for v,(original,b) in zip([.371,.823,1.197],points))
                if same:equivalents.append(a[':answer/value'])
            if equivalents:errors.append({'field':f[':answer-field/key'],'equivalent_wrong_choices':equivalents})
        return {'label':label,'kp':kid,'status':'match' if matched else 'mismatch','points':points,'choice_ambiguities':errors}
    except Exception as e:return {'label':label,'kp':kid,'status':'unparsed','error':str(e)}

def main():
    results=[]
    for kid,k in json.loads((H/'kps.json').read_text()).items():
        for q in k[':knowledge-point/questions']+[k[':knowledge-point/canonical-example']]:results.append(audit(q,str(q[':db/id']),kid))
        for path in sorted((H/'kps'/kid/'samples').glob('*.json')):
            for i,r in enumerate(json.loads(path.read_text())):results.append(audit(r['question'],path.stem+'/'+str(i),kid))
    (H/'numeric-results.json').write_text(json.dumps(results,indent=2)+'\n')
    counts=collections.Counter(r['status'] for r in results);findings=[r for r in results if r['status'] in ('mismatch','unparsed') or r.get('choice_ambiguities')]
    (H/'numeric-findings.json').write_text(json.dumps(findings,indent=2)+'\n');print(json.dumps({'counts':dict(counts),'findings':len(findings)}));
    for r in findings:print(json.dumps(r)[:900])

if __name__=='__main__':main()
