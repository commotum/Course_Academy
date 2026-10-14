"""Independently read rendered givens, infer theorem facts and grade every option."""
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('imt',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
STATEMENT=re.compile(r'(?:\*\*(III|II|I)\.\*\*|(?<![A-Z])(III|II|I)\.)\s*([^\n]+)')

def save(name,value):(HERE/name).write_text(json.dumps(value,indent=2)+'\n')
def statements(text):return [(m[0] or m[1],m[2]) for m in STATEMENT.findall(text)]
def plain(s):
 return re.sub(r'[\s${}]','',s.replace(r'\text','').replace(r'\textrm','').replace(r'\ne','!=').replace('\\',''))
def column(text):
 return [sp.sympify(re.sub(r'(\d)(x)',r'\1*\2',re.sub(r'\{x\}_\{([12])\}',r'x\1',row.strip()))) for row in text.split(r'\\')]
def facts(prompt):
 n=int(re.search(r'(\d+)\s*\\times\s*(\d+)',prompt)[1]);head=STATEMENT.split(prompt)[0]
 matrix=g.MATRIX.findall(head)
 if matrix:
  vals=column(matrix[0]);assert len(vals)==n
  if any(v.free_symbols for v in vals):
   xs=sorted(set().union(*(v.free_symbols for v in vals)),key=str)
   a=sp.Matrix([[v.coeff(x) for x in xs] for v in vals]);k=a.rank();assert k==len(xs)
   assert all(v==sum(a[i,j]*x for j,x in enumerate(xs)) for i,v in enumerate(vals))
   return n,False,n-k,k,a
  a=sp.Matrix(vals);assert a.rank()==1
  return n,False,None,None,a
 if 'det(A)' in head:
  d=int(re.search(r'det\(A\)=(-?\d+)',head)[1]);inv=d!=0
  return n,inv,n if inv else None,0 if inv else None,None
 assert re.search(r'\\text\{rank\}\(A\)='+str(n),head)
 return n,True,n,0,None

def truth(s,n,inv,rank,nullity):
 s=plain(s)
 if s=='Aisinvertible':return inv
 if s=='Aisnotinvertible':return not inv
 if s.startswith('Ahas'):
  k=int(re.search(r'Ahas(\d+)pivotcolumns',s)[1]);assert rank is not None;return rank==k
 m=re.fullmatch(r'(?:Null|Col)\(A\)(=|!=)(.*)',s)
 if m:
  isnull=s.startswith('Null');op,rhs=m.groups()
  if rhs=='0':eq=inv if isnull else rank==0 if rank is not None else False
  else:assert rhs=='R^'+str(n) and not isnull;eq=inv
  return eq if op=='=' else not eq
 m=re.fullmatch(r'(rank|dim\(Null|dim\(Col|nullity)\(A\)\)?(=|!=|<)(\d+)',s)
 assert m,s
 kind,op,rhs=m.groups();rhs=int(rhs)
 actual=rank if kind in ('rank','dim(Col') else nullity
 if actual is not None:return {'=':actual==rhs,'!=':actual!=rhs,'<':actual<rhs}[op]
 # Only consequences that are determined by singularity are accepted.
 if kind in ('rank','dim(Col'):
  assert rhs==n;return {'=':False,'!=':True,'<':True}[op]
 assert rhs==0;return {'=':False,'!=':True,'<':False}[op]

def subset(mask):
 labels=[k for k,v in mask if v]
 return 'none' if not labels else ' and '.join(labels)+' only'

def check(r):
 q=r['question'];meta=r['generation'];p=meta['parameters'];t=meta['template']
 assert r==g.generate('moderate',meta['seed'],t,p,meta['replay'])
 assert q[':question/difficulty']==':question.difficulty/moderate'
 n,inv,rank,k,a=facts(q[':question/problem'])
 claims=statements(q[':question/problem']);assert [x[0] for x in claims]==['I','II','III']
 mask=[(key,truth(s,n,inv,rank,k)) for key,s in claims]
 solution=q[':question/worked-solution']
 assert 'Since $A$ is a $'+str(n)+r'\times '+str(n)+'$ matrix' in solution
 judgments=re.findall(r'Statement (III|II|I) is (true|false)',solution)
 assert judgments==[(key,str(b).lower()) for key,b in mask]
 assert subset(mask) in solution
 if a is not None and '{x}' in q[':question/problem']:
  bases=[sp.Matrix(column(text)) for text in g.MATRIX.findall(solution)]
  assert len(bases)==a.cols and sp.Matrix.hstack(*bases)==a
  assert re.search(r'\\text\{dim\(Null\}\(A\)\)='+str(k),solution)
 if 'det(A)' in q[':question/problem']:
  det=int(re.search(r'det\(A\)=(-?\d+)',q[':question/problem'])[1])
  assert 'det(A)='+str(det) in solution
 fs=q[':question/answer-fields'];kind=fs[0][':answer-field/type']
 uuids={q[':question/id']}
 if kind.endswith('/checkbox'):
  assert [f[':answer-field/key'] for f in fs]==['I','II','III']
  correct={key:str(b).lower() for key,b in mask}
 else:
  assert kind.endswith('/radio') and len(fs)==1
  correct={'selection':subset(mask)}
 for f in fs:
  assert f[':answer-field/id'] not in uuids;uuids.add(f[':answer-field/id'])
  answers=f[':answer-field/choices'];values=[a[':answer/value'] for a in answers]
  assert len(values)==len(set(values))
  if kind.endswith('/checkbox'):assert sorted(values)==['false','true']
  else:assert len(values)==5
  for a in answers:assert a[':answer/id'] not in uuids;uuids.add(a[':answer/id'])
  answer=next(a for a in answers if a[':answer/id']==f[':answer-field/correct'][1])
  assert answer[':answer/value']==correct[f[':answer-field/key']]
 assert g.fingerprint(q)==meta['mathematical_fingerprint']
 return r

def native(label,r):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  checks.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete field-owned radio or checkbox bank'} for a in f[':answer-field/choices'])
 return {'label':label,'record':r,'checks':checks}

def main():
 replays=[];samples=[];inputs=[];mapping=[];coverage={};reviews=[]
 for t in g.TEMPLATES:
  q=g.SOURCES[t];r=check(g.generate('moderate',0,t,g.original(t),True));rq=r['question']
  assert rq[':question/problem']==q[':question/problem'] and rq[':question/worked-solution']==q[':question/worked-solution']
  total=0;incorrect=0
  for sf,gf in zip(q[':question/answer-fields'],rq[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in sf[':answer-field/choices'])==sorted(a[':answer/value'] for a in gf[':answer-field/choices'])
   for sa in sf[':answer-field/choices']:
    ga=[a for a in gf[':answer-field/choices'] if a[':answer/value']==sa[':answer/value']];assert len(ga)==1
    yes=sa[':answer/id']==sf[':answer-field/correct'][':answer/id'];assert yes==(ga[0][':answer/id']==gf[':answer-field/correct'][1])
    mapping.append({'source':t,'field':sf[':answer-field/key'],'source_answer_id':sa[':answer/id'],'value':sa[':answer/value'],'recipe':'literal Boolean' if gf[':answer-field/type'].endswith('/checkbox') else 'literal statement subset','profile':t,'complete_value_reproduced':True,'correct':yes});total+=1;incorrect+=not yes
  replays.append({'source':t,'source_db_id':q[':db/id'],'complete_bank_match':True,'matched_choices':total,'total_choices':total,'matched_distractors':incorrect,'total_distractors':incorrect,'exact_prompt':True,'exact_solution':True})
  inputs.append(native('source-'+t,r));coverage[t]={'n':set(),'det':set(),'coefficient_values':set(),'sign_patterns':set(),'semantic_fingerprints':set()}
  reviews.append('## Source '+t+'\n\n'+g.markdown(r))
  for seed in range(80):
   r=check(g.generate('moderate',seed,t));p=r['generation']['parameters']
   assert r['question']==g.generate('moderate',seed+999,t,p)['question']
   samples.append(r);inputs.append(native(t+'-'+str(seed),r));c=coverage[t]
   c['n'].add(p['n']);c['semantic_fingerprints'].add(g.fingerprint(r['question']))
   if 'det' in p:c['det'].add(p['det'])
   if 'matrix' in p:
    c['coefficient_values'].update(v for row in p['matrix'] for v in row)
    c['sign_patterns'].add(tuple(sp.sign(v) for row in p['matrix'] for v in row))
  reviews.append('## Variant '+t+'\n\n'+g.markdown(samples[-1]))
  kind,n,k=g.SPEC[t]
  c=coverage[t]
  if kind in ('det','rank'):assert c['n']==set(range(3,8))
  if kind=='det':assert c['det']==({0} if g.original(t)['det']==0 else {-4,-3,-2,-1,1,2,3,4})
  if kind in ('vector','nullspace'):assert {-4,-3,-2,-1,1,2,3,4}<=c['coefficient_values'] and len(c['sign_patterns'])>1
 # Changed given direction with all other data fixed: different prompt/key evidence.
 # Truth remains a singularity consequence; the solution must not assert exact rank.
 p=g.original('q-34929');r0=check(g.generate('moderate',0,'q-34929',p));p['matrix']=[[0],[1],[0],[0]];r1=check(g.generate('moderate',0,'q-34929',p));assert g.fingerprint(r0['question'])!=g.fingerprint(r1['question'])
 inputs.extend([native('changed-given-original',r0),native('changed-given-new',r1)])
 # Positive scalar multiple, determinant magnitude, seed and choice order cannot add tasks.
 p=g.original('q-139977');a=check(g.generate('moderate',0,'q-139977',p));p['matrix']=[[2*v for v in row] for row in p['matrix']];b=check(g.generate('moderate',1,'q-139977',p));assert g.fingerprint(a['question'])==g.fingerprint(b['question'])
 p=g.original('q-141200');a=check(g.generate('moderate',0,'q-141200',p));p['det']=4;b=check(g.generate('moderate',1,'q-141200',p));assert g.fingerprint(a['question'])==g.fingerprint(b['question'])
 for level in ('easy','hard'):
  try:g.batch(level,5,0)
  except ValueError:pass
  else:raise AssertionError('Unsupported band accepted')
 for t in g.TEMPLATES:
  if g.SPEC[t][0] in ('vector','nullspace'):
   p=g.original(t);p['matrix']=[[0]*len(row) for row in p['matrix']]
   try:g.generate('moderate',0,t,p)
   except AssertionError:pass
   else:raise AssertionError('zero/dependent given accepted')
 save('source-choice-mapping.json',mapping);save('source-replay.json',{'passed':True,'basis':g.S['basis'],'profiles':replays,'complete_banks_matched':len(replays),'complete_banks_total':len(replays),'matched_choices':sum(x['matched_choices'] for x in replays),'matched_distractors':sum(x['matched_distractors'] for x in replays),'missing_or_extra_options':[],'excluded_sources':g.EXCLUDED})
 save('native-input.json',inputs);subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 save('previews.json',samples[:24]);(HERE/'review.md').write_text('\n\n'.join(reviews)+'\n')
 cov={t:{k:len(v) if k in ('sign_patterns','semantic_fingerprints') else sorted(v) for k,v in c.items()} for t,c in coverage.items()}
 save('validation.json',{'passed':True,'supported_levels':['moderate'],'unsupported_levels':['easy','hard'],'sample_count':len(samples),'source_templates':len(replays),'source_fidelity':'Exact prompts, solutions, field layouts and all complete banks of 12 supported sources; two explicit exclusions','mathematics':'Independent parsing of rendered givens and all claims, exact SymPy rank, independent theorem truth keys and rendered solution judgments','actual_grading':'All options of every field through learning::grade_field; unresolved count zero','coverage':cov,'changed_given_checked':True,'duplicate_scalar_and_determinant_magnitude_rejected':True,'assets':[],'hashes':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json')}})
 print('Validated 12 complete source banks, 960 sampled moderate instances and duplicate/domain boundaries.')
if __name__=='__main__':main()
