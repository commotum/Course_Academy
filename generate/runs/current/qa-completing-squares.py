"""Root readback of displayed polynomials, complete banks and operative stages."""
import sys,json,re,hashlib,importlib.util
from pathlib import Path
import sympy as s
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
def load(path,name):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);sys.modules[name]=m;spec.loader.exec_module(m);return m
p=load(R/'vector-math-parser.py','square_parent_math');p.locals_['a']=s.Symbol('a',real=True)
def math(raw):
 raw=re.sub(r'\\text\{[^{}]*\}','',raw).strip().rstrip('.,').replace('&','');raw=re.sub(r'\\underbrace(?=\{)','',raw)
 raw=raw.replace('{)}',')').replace('{(}','(').replace('_{⏟}','');raw=re.sub(r'(?<![A-Za-z\\])a','u',raw);return p.scalar(raw)
def raw(g,K,D):
 old={q[':question/math-academy-id']:q for q in json.loads((R/f'sources/{K}.json').read_text())['record'][':knowledge-point/questions']};C=dict(prompts=0,solutions=0,fields=0,values=0,keys=0,missing_keys=0,missing_banks=0,missing_ratings=0)
 for case in json.loads((D/'source-cases.json').read_text()):
  o=old[case['source_id']];lev=o.get(':question/difficulty',{}).get(':db/ident','').split('/')[-1] or case.get('level',case.get('difficulty','easy'));q=g.generate(lev,template=case['template'],parameters=case['parameters'],profile=case.get('profile',case.get('bank_profile')))['question']
  for k in (':question/problem',':question/worked-solution',':question/answer-fields',':question/difficulty'):assert (k in o)==(k in q)
  assert q[':question/problem']==o[':question/problem'];C['prompts']+=1
  if ':question/worked-solution' in o:assert q[':question/worked-solution']==o[':question/worked-solution'];C['solutions']+=1
  if ':question/difficulty' not in o:C['missing_ratings']+=1
  assert len(q.get(':question/answer-fields',[]))==len(o.get(':question/answer-fields',[]))
  for f,f0 in zip(q.get(':question/answer-fields',[]),o.get(':question/answer-fields',[])):
   assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident'];C['fields']+=1
   for k in (':answer-field/choices',':answer-field/correct'):assert (k in f)==(k in f0)
   assert sorted(a[':answer/value'] for a in f.get(':answer-field/choices',[]))==sorted(a[':answer/value'] for a in f0.get(':answer-field/choices',[]));C['values']+=len(f0.get(':answer-field/choices',[]))
   if ':answer-field/choices' not in f0:C['missing_banks']+=1
   if ':answer-field/correct' in f0:assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==f0[':answer-field/correct'][':answer/value'];C['keys']+=1
   else:C['missing_keys']+=1
 return C
def check(rec,K,C):
 q=rec['question'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];body=re.search(r'\$([^$]*\^\{2\}[^$]*)\$',prompt)[1];body=body.split('=')[0].strip();pol=math(body);vs=list(pol.free_symbols);assert len(vs)==1;v=vs[0];leading=s.expand(pol).coeff(v,2);linear=s.expand(pol).coeff(v);constant=s.expand(pol).coeff(v,0);b=s.sqrt(leading);shift=linear/(2*b);outer=constant-shift**2;expected=(b*v+shift)**2+outer;assert s.expand(expected-pol)==0
 general=K in (17592186068875,17592186068876);minus_convention=K==17592186068876 and '-p' in prompt;paramshift=-shift if minus_convention else shift
 if general:assert leading==1 and (linear>0)==(K==17592186068875);inner=pol
 else:
  assert (linear>0)==(K==17592186068873);inner=pol-outer
 blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==(4 if general else 3)
 if general:
  assert all(x in sol for x in ('First, we rewrite the coefficient of the linear term as a product with $2$ as a factor:','We *add* and *then subtract*','The first three terms form a perfect square','Finally, evaluating the last'))
  for block in blocks:assert s.expand(math(block)-pol)==0,(block,pol);C['operative_stages']+=1
  assert (r'\underbrace' in blocks[1] or '⏟' in blocks[1]) and len(re.findall(r'\^\{2\}',blocks[1]))==3 and blocks[2].count('^{2}')==2
  for name,num in re.findall(r'\$(p|q)=([^$]+)\$',sol):assert math(num)==(paramshift if name=='p' else outer);C['conclusions']+=1
 else:
  a=p.locals_['a'];left,right=blocks[0].split('=');assert s.expand(math(left)-math(right))==0;C['formal_identity']+=1
  for bi,block in enumerate(blocks[1:]):
   rows=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(chr(92)*2)
   actual=[row.replace('&','').replace('=','').strip().rstrip(' .') for row in rows];actual=[a for a in actual if a]
   assert len(actual)>= (3 if bi==0 else 2)
   for row in actual:assert s.expand(math(row)-(inner if bi==0 else pol))==0,(row,pol);C['operative_stages']+=1
   if bi==0:assert r'\cdot' in block
  assert 'First, we recall the following formula:' in sol and 'Notice that we have a perfect square in the parentheses that we can factor as follows:' in sol and 'Therefore, we obtain' in sol
 fields=q[':question/answer-fields'];correct={}
 for f in fields:
  ref=f[':answer-field/correct'][1];val=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==ref);correct[f[':answer-field/key']]=val
  if f[':answer-field/type'].endswith('/radio'):
   values=[]
   for a in f[':answer-field/choices']:
    text=a[':answer/value']
    if text.startswith('p='):
     aa,bb=re.sub(r'\\text\{[^{}]*\}','',text).replace(r'\,','').split(',');values.append((math(aa[2:]),math(bb[2:])))
    else:values.append(s.expand(math(text)))
   assert len(values)==5 and len(set(values))==5
   if general:
    tuples=[(shift,outer),(shift,constant),(shift,constant-shift),(shift,constant+shift**2),(2*shift,constant-4*shift**2)]
    if K==17592186068876:tuples=[(shift,outer),(-shift,outer),(shift,constant),(shift,constant+shift),(2*shift,constant-4*shift**2)]
    bank=[((-h if minus_convention else h),k) for h,k in tuples] if isinstance(values[0],tuple) else [s.expand((v+h)**2+k) for h,k in tuples]
   elif K==17592186068873:bank=[s.expand((v+h)**2+outer) for h in (shift,-shift,2*shift,shift/2,-2*shift)]
   else:
    aa=-shift;name=rec['generation']['profile']
    if name=='scaled_method':pairs=[(b,-aa),(b,aa),(b,-2*aa),(1,-aa),(b*b,-aa)]
    elif name=='half_coefficient':pairs=[(b,-aa),(b,aa),(b,-2*aa),(b,-aa/2),(b,2*aa)]
    elif name=='square_constant':pairs=[(b,-aa),(b,aa),(b,-aa*aa),(b,-2*aa),(b,2*aa)]
    elif name=='both_constant_signs':pairs=[(b,-aa),(b,aa),(b,-aa*aa),(b,-2*aa),(b,aa*aa)]
    else:raise AssertionError(('Unexpected normal bank',name))
    bank=[s.expand((bb*v+h)**2+outer) for bb,h in pairs]
   assert set(values)==set(bank),('Displayed wrong operations',values,bank)
   wanted=(paramshift,outer) if isinstance(values[0],tuple) else s.expand(pol);assert values.count(wanted)==1;assert values[next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==ref)]==wanted;C['whole_banks']+=1
  else:assert '{{'+f[':answer-field/key']+'}}' in prompt
  C['choices']+=len(f[':answer-field/choices'])
 if len(fields)==2:
  one,two=[math(correct[f[':answer-field/key']]) for f in fields]
  if general and '$p' in prompt:assert one==paramshift and two==outer
  else:assert one==b*v+shift and two==abs(outer)
  C['blank_fragments']+=2
 if q[':question/difficulty'].endswith('/hard'):
  if K==17592186068875:assert 12<=shift<=15 and 1<=abs(outer)<=25
  elif K==17592186068876:assert constant<0 and -shift>=3
  elif K==17592186068873:assert 11<=shift<=15 and outer<0
  else:assert b>1 and shift<0
  C['hard_guards']+=1
 C['records']+=1
if __name__=='__main__':
 K=int(sys.argv[1]);D=ROOT/f'generate/scratch/{K}';g=load(D.with_suffix('.py'),'root_square_gen');source=raw(g,K,D);records=json.loads((R/f'qa/{K}-sampled.json').read_text());C={k:0 for k in ('records','formal_identity','operative_stages','conclusions','whole_banks','choices','blank_fragments','hard_guards')}
 if K==17592186068876:
  for lev,fams in g.TEMPLATES.items():
   for fam in fams:records.append(g.generate(lev,template=fam,seed=643))
 elif hasattr(g,'CONFIG'):
  for fam,cfg in g.CONFIG.items():records.append(g.generate(cfg[0],template=fam,seed=643))
 else:
  for level in ('easy','moderate','hard'):
   for fam in g.TEMPLATES:
    if (level=='hard')==fam.endswith('_scaled'):records.append(g.generate(level,template=fam,seed=643))
 for z in records:check(z,K,C)
 out=dict(status='passed',source=source,readback=C,script_sha256=hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest());(R/f'qa/{K}-root-readback.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
