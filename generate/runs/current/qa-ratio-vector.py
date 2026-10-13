"""Independent readback of internal ratios, complete banks and vector stages."""
import importlib.util,json,re,math
from pathlib import Path
R=Path(__file__).resolve().parent;K=17592186096653;D=R.parents[2]/f'generate/scratch/{K}'
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
p=module('ratio_parent_scalar',R/'ode-scalar-parser.py');g=module('ratio_review_generator',D.with_suffix('.py'));s=p.s
counts=dict(instances=0,complete_values=0,vector_stages=0,source_fields=0,source_values=0,source_solutions=0,source_prompts=0,existing_refs=0,missing_refs=0,raw_reversed_question_instances=0,plots=0)
def layout(prompt):
 m=re.search(r'([A-Z])([A-Z]):\s*\2([A-Z])\s*=\s*(\d+):\s*(\d+)',prompt);assert m,prompt
 A,X,B,r,t=m.groups();r,t=int(r),int(t);defs=dict(re.findall(r'\{O([A-Z])\}\s*=\s*([a-z])',prompt))
 defs.update(re.findall(r'O([A-Z])\^\(→\)\s*=\s*([a-z])',prompt));assert A in defs and B in defs
 a,b=s.Rational(t,r+t),s.Rational(r,r+t)
 points={'O':0,A:p.i,B:p.j,X:a*p.i+b*p.j};basis={defs[A]:p.i,defs[B]:p.j}
 return points,basis,(a,b),(A,B,X,r,t)
def scalar(raw,basis):
 # Protect TeX commands while replacing the actual printed basis names.
 pieces=re.split(r'(\\[A-Za-z]+)',raw);raw=''.join(x if x.startswith('\\') else re.sub('[a-z]',lambda m:str(basis[m[0]]) if m[0] in basis else m[0],x) for x in pieces)
 return p.scalar(raw)
def vector(raw,points,basis):
 saved=[]
 def hold(m):
  saved.append(points[m[1][1]]-points[m[1][0]]);return 'ZZ'+str(len(saved)-1)+'ZZ'
 raw=re.sub(r'\\overset\{\\to\s*\}\{([A-Z]{2})\}',hold,raw)
 raw=re.sub(r'([A-Z]{2})\^\(→\)',hold,raw)
 pieces=re.split(r'(\\[A-Za-z]+)',raw);raw=''.join(x if x.startswith('\\') else re.sub('[a-z]',lambda m:str(basis[m[0]]) if m[0] in basis else m[0],x) for x in pieces)
 for n,value in enumerate(saved):raw=raw.replace('ZZ'+str(n)+'ZZ','('+str(value)+')')
 return p.scalar(raw)
def same(a,b):return s.expand(a-b)==0
def val(raw,points,basis):
 parts=raw.strip().strip('$').split('=');assert len(parts)==2,raw
 lhs,rhs=[vector(x,points,basis) for x in parts];return s.expand(rhs-lhs)
def stages(text,points,basis):
 n=0
 for block in re.findall(r'\$\$(.*?)\$\$|(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',text,re.S):
  raw=next(x for x in block if x);raw=re.sub(r'\\(?:begin|end)\{aligned\}','',raw);carry=None
  for row in raw.split(r'\\'):
   row=row.replace('&','').strip().rstrip('.,')
   if '=' not in row:continue
   parts=row.split('=')
   if not parts[0].strip():assert carry is not None;parts[0]=carry
   else:carry=parts[0]
   if not ('overset' in ''.join(parts) or '^(→)' in ''.join(parts)):continue
   vals=[vector(x,points,basis) for x in parts]
   assert all(same(vals[0],x) for x in vals[1:]),(row,vals)
   n+=len(vals)-1
 return n
def check(record):
 q=record['question'];meta=record['generation'];prompt=q[':question/problem'];pts,bs,(a,b),(A,B,X,r,t)=layout(prompt)
 image=Path(re.search(r'!\[\]\((.*?)\)',prompt)[1]);assert image.is_file();side=json.loads(Path(str(image)+'.json').read_text());assert side['ratio']==[r,t]
 assert (side['parameters']['A'],side['parameters']['B'],side['parameters']['X'])==(A,B,X)
 for k in ('u','v'):assert side['parameters'][k] in bs
 O,AA,BB,XX=[s.Matrix(side[n]) for n in ('O','A','B','X')]
 want=AA+float(b)*(BB-AA);assert max(abs(float(z)) for z in XX-want)<1e-12 and 0<float(b)<1
 assert abs(float(s.det(s.Matrix.hstack(AA-O,BB-O))))>1e-9;counts['plots']+=1
 fields=q[':question/answer-fields'];raw_wrong=meta['raw_wrong_blank_key'];correctvals=[]
 for f in fields:
  if f[':answer-field/type'].endswith('/radio'):
   vals=[val(z[':answer/value'],pts,bs) for z in f[':answer-field/choices']];good=[v==0 for v in vals];assert sum(good)==1 and len(set(vals))==len(vals)
  else:
   tail=prompt.split('{{'+f[':answer-field/key']+'}}',1)[1];name=re.search(r'\$\s*([a-z])',tail)[1];expected=a if bs[name]==p.i else b
   vals=[p.scalar(z[':answer/value']) for z in f[':answer-field/choices']];good=[same(v,expected) for v in vals]
   assert all(not z for z in good) if raw_wrong else all(good)
  correct=next(i for i,z in enumerate(f[':answer-field/choices']) if z[':answer/id']==f[':answer-field/correct'][1]);assert good[correct]!=raw_wrong
  counts['complete_values']+=len(vals)
 counts['raw_reversed_question_instances']+=int(raw_wrong);n=stages(q[':question/worked-solution'],pts,bs);assert n>=8,(meta,n);counts['vector_stages']+=n;counts['instances']+=1
 if not meta['observed'] and q[':question/difficulty'].endswith('/hard'):assert min(r,t)>=5 and r+t>=19 and math.gcd(r,t)==1
 return q,pts,bs
def normalized_images(text):return re.sub(r'!\[\]\(.*?\)','![](ASSET)',text)
sources={q[':question/math-academy-id']:q for q in json.loads((R/'sources'/f'{K}.json').read_text())['record'][':knowledge-point/questions']}
def source_bank(old,q,pts,bs,indexmap=None):
 for oi,ni in indexmap or [(i,i) for i in range(len(q[':question/answer-fields']))]:
  of=old[':question/answer-fields'][oi];nf=q[':question/answer-fields'][ni];read=(lambda z:val(z,pts,bs)) if nf[':answer-field/type'].endswith('/radio') else p.scalar
  remaining=[read(z[':answer/value']) for z in nf[':answer-field/choices']]
  for z in of[':answer-field/choices']:
   v=read(z[':answer/value']);i=next(i for i,w in enumerate(remaining) if same(v,w));remaining.pop(i)
  assert not remaining
  if of.get(':answer-field/correct'):
   actual=read(next(z[':answer/value'] for z in nf[':answer-field/choices'] if z[':answer/id']==nf[':answer-field/correct'][1]));assert same(actual,read(of[':answer-field/correct'][':answer/value']));counts['existing_refs']+=1
  else:counts['missing_refs']+=1
  counts['source_fields']+=1;counts['source_values']+=len(of[':answer-field/choices'])
for c in json.loads((D/'source-cases.json').read_text()):
 old=sources[c['source_id']];record=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);q,pts,bs=check(record)
 assert normalized_images(q[':question/problem'])==normalized_images(old[':question/problem']);counts['source_prompts']+=1
 if old.get(':question/worked-solution'):assert normalized_images(q[':question/worked-solution'])==normalized_images(old[':question/worked-solution']);counts['source_solutions']+=1
 source_bank(old,q,pts,bs,[(1,0)] if c['source_id']=='q-12212' else None)
 if c['source_id'] in g.REVERSED:check(g.generate(c['level'],parameters=c['parameters'],profile=c['source_id']+'-repaired'))
c=next(c for c in json.loads((D/'source-cases.json').read_text()) if c['source_id']=='q-12212');q,pts,bs=check(g.generate('moderate',parameters=c['parameters'],profile='q-12212-legacy'));source_bank(sources['q-12212'],q,pts,bs,[(0,0)])
for r in json.loads((D/'review.json').read_text()):check(r.get('record',r))
for r in json.loads((R/'qa'/f'{K}-sampled.json').read_text()):check(r)
for ratio in ((10,10),(20,10),(5,6)):
 try:g.generate('hard',template='coefficients',parameters=dict(A='A',B='B',X='T',u='a',v='b',r=ratio[0],s=ratio[1]))
 except ValueError:pass
 else:raise AssertionError('Reduced workload guard failed')
aa=g.generate('moderate',template='coefficients',parameters=dict(A='A',B='B',X='T',u='a',v='b',r=3,s=5));bb=g.generate('moderate',template='coefficients',parameters=dict(A='A',B='B',X='T',u='a',v='b',r=6,s=10));assert aa['generation']['mathematical_fingerprint']==bb['generation']['mathematical_fingerprint']
counts['database_writes']=0;(R/'qa'/f'{K}-independent.json').write_text(json.dumps(counts,indent=2)+'\n');print(counts)
