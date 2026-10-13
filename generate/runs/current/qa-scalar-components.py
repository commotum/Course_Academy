"""Root actual vectors/request, full banks, every formal and numeric projection row."""
import sys,re,json,hashlib,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(file,name):
 z=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'spatial-jacobian-readback.py','scalar')
n=dict(records=0,choices=0,projection_rows=0,combination_rows=0,component_inputs=0,formal_rows=0,complete_method_banks=0,source_prompts=0,source_values=0,source_solutions=0,source_refs=0)
def check(rec):
 q=rec['question'];meta=rec['generation'];text=q[':question/problem'];names=re.findall(r'\$([a-z])\s*=',text);vectors=re.findall('⟨([^⟩]+)⟩',text);assert len(names)==len(vectors)==2;A,B=names;a,b=[tuple(p.scalar(x) for x in z.split(',')) for z in vectors];assert len(a)==len(b)==3
 D=s.expand(sum(x*y for x,y in zip(a,b)));A2=sum(x*x for x in a);B2=sum(x*x for x in b);an,bn=s.sqrt(A2),s.sqrt(B2);P=D/bn;Q=D/an
 request=text.split('Find',1)[1];request=re.sub(r'(?<!text\{)comp_\{([a-z])\}\s*([a-z])',lambda m:r'{\text{comp}}_{'+m[1]+r'}\,'+m[2],request)
 if 'scalar projection' in request:op='single';assert f'of ${A}$ onto ${B}' in request;correct=P
 else:
  one=r'{\text{comp}}_{'+B+r'}\,'+A;two=r'{\text{comp}}_{'+A+r'}\,'+B
  assert one in request and two in request;sign=request[request.index(one)+len(one):request.index(two)].strip();assert sign in ('+','-');op='sum' if sign=='+' else 'difference';correct=P+Q if op=='sum' else P-Q
 f=q[':question/answer-fields'][0];values=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];assert len(values)==(1 if f[':answer-field/type'].endswith('/blank') else 5);assert all(not p.same(x,y) for i,x in enumerate(values) for y in values[:i]);hits=[i for i,z in enumerate(values) if p.same(z,correct)];assert len(hits)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][hits[0]][':answer/id']==f[':answer-field/correct'][1]
 else:assert meta['evidence_only'] and not meta['eligible_for_learning']
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in text
 if meta['eligible_for_learning'] and len(values)==5:
  if op=='single':want=[P,Q,D/B2,(D-a[0]*b[0])/bn,-P]
  else:sgn=1 if op=='sum' else -1;want=[correct,P-sgn*Q,P,P+sgn*D/A2,-correct]
  assert all(sum(p.same(x,y) for y in want)==1 for x in values);n['complete_method_banks']+=1
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==(1 if op=='single' else 3)
  for i,block in enumerate(blocks):
   expected=(P,Q,correct)[i];rows=re.findall(r' & =(.*?)(?= \\\\  & =|$)',block,re.S);assert len(rows)>=2
   for raw in rows:
    raw=raw.strip().rstrip('.')
    for name,vec,norm in ((A,a,an),(B,b,bn)):
     for coord,value in zip('xyz',vec):
      token='{'+name+'}_{'+coord+'}'
      if token in raw:n['component_inputs']+=raw.count(token);raw=raw.replace(token,'('+s.latex(value)+')')
     raw=raw.replace('|\\,'+name+'\\,|','('+s.latex(norm)+')')
    for first,second in ((A,B),(B,A)):
     token=first+r'\cdot '+second
     if token in raw:n['formal_rows']+=1;raw=raw.replace(token,'('+s.latex(D)+')')
    assert p.same(p.scalar(raw),expected),(meta['template'],i,raw,expected)
    n['projection_rows' if i<2 else 'combination_rows']+=1
 if meta['eligible_for_learning'] and q[':question/difficulty'].endswith('hard'):assert D.is_Rational is False and A2!=B2 and not an.is_Integer and not bn.is_Integer and all(x*y!=0 for x,y in zip(a,b))
 n['records']+=1;n['choices']+=len(values)
if __name__=='__main__':
 kp=17592186105917;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));old={q[':question/math-academy-id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(rec);q=rec['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  if ':answer-field/correct' in of:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'];n['source_refs']+=1
  n['source_prompts']+=1;n['source_values']+=len(f[':answer-field/choices']);n['source_solutions']+=int(':question/worked-solution' in o)
 for item in json.load(open(D/'review.json')):check(item.get('record',item))
 for level in ('easy','moderate','hard'):
  for seed in range(12):check(g.generate(level,seed=90000+seed))
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
