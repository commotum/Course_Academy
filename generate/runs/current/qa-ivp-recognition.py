"""Root printed ODE order, initial-condition chains, prose and Boolean response."""
import sys,re,json,itertools,importlib.util
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','reader');x,y=p.x,p.y;Ds={1:p.u,2:p.v,3:p.z}
def translate(raw):
 for sign,n in [('‴',3),("'''",3),('″',2),("''",2),('′',1),("'",1)]:raw=raw.replace('{y}^{'+sign+'}',str(Ds[n]))
 for cmd in ('frac','dfrac'):
  raw=raw.replace('\\'+cmd+'{dy}{dx}',str(Ds[1]))
  for n in (2,3):raw=raw.replace('\\'+cmd+'{d^'+str(n)+'y}{dx^'+str(n)+'}',str(Ds[n]))
 return raw
def residual(raw):
 a,b=raw.split('=');return s.expand(p.scalar(translate(a))-p.scalar(translate(b)))
def conditions(raw):
 if not raw:return []
 results=[]
 for part in translate(raw).strip().rstrip('.,').split(r',\,'):
  chain=part.split('=');value=p.scalar(chain[-1].strip().rstrip('.,'));assert not value.free_symbols
  for term in chain[:-1]:
   m=re.fullmatch(r'([yuvz])\((.*?)\)',term);assert m,(raw,term);point=p.scalar(m[2]);assert not point.free_symbols;results.append((m[1],point,value))
 return results
def system(raw):
 bits=raw.split(r',\,',1);F=residual(bits[0]);order=max(n for n,d in Ds.items() if F.has(d));ct=conditions(bits[1]) if len(bits)>1 else [];truth=order==1 and any(z[0]=='y' for z in ct);return F,order,ct,truth
n=dict(records=0,systems=0,choices=0,prose_equations=0,prose_conditions=0,classification_sentences=0,conclusions=0,normal_defined_points=0,known_raw_domain_issues=0,source_prompts=0,source_solutions=0,source_values=0,source_refs=0)
def check(rec):
 q=rec['question'];g=rec['generation'];parts=re.findall(r'- \*\*(?:I|II|III)\.\*\* \$(.*?)\$',q[':question/problem']);assert len(parts)==3;blocks=q[':question/worked-solution'].split('- System ')[1:];assert len(blocks)==3;selected=[]
 for roman,raw,block,f in zip(('I','II','III'),parts,blocks,q[':question/answer-fields']):
  F,order,ct,truth=system(raw);assert block.startswith(roman+' ');assert ('is a first-order initial value problem' in block)==truth;assert f[':answer-field/key']==roman and f[':answer-field/type'].endswith('/checkbox');choices=f[':answer-field/choices'];assert {a[':answer/value'] for a in choices}=={'false','true'}
  correct=next(a[':answer/value'] for a in choices if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==str(truth).lower()
  if truth:selected.append(roman)
  if order>1:assert ('second' if order==2 else 'third')+'*-order' in block or ('second' if order==2 else 'third')+'-order' in block
  elif not ct:assert 'no initial condition' in block
  printed_ct=[]
  for span in re.findall(r'\$(.*?)\$',block):
   if any(z in span for z in ('′','″','‴',"'",r'\dfrac')) and '(' not in translate(span) and span.startswith('y('):pass
   if any(z in span for z in ('′','″','‴',"'",r'\dfrac')) and not re.match(r'y\(',span) and not re.match(r'\{y\}\^\{[^}]+\}\(',span):
    assert s.simplify(residual(span.rstrip('.,'))-F)==0;n['prose_equations']+=1
   elif '=' in span and '(' in span:
    parsed=conditions(span);printed_ct.extend(parsed);n['prose_conditions']+=len(parsed)
  if ct:assert sorted(printed_ct,key=str)==sorted(ct,key=str),(raw,block,ct,printed_ct)
  for name,point,value in ct:
   if name!='y':continue
   at=F.subs({x:point,y:value});defined=not at.has(s.zoo,s.nan,s.oo,-s.oo,s.I)
   if not defined:assert g['evidence_only'] and g['template']=='source_q-96987';n['known_raw_domain_issues']+=1
   elif not g['evidence_only']:n['normal_defined_points']+=1
  n['systems']+=1;n['choices']+=2;n['classification_sentences']+=1
 assert q[':question/worked-solution'].endswith('"'+' and '.join(selected)+' only."');n['conclusions']+=1;n['records']+=1
if __name__=='__main__':
 kp=17592186166815;D=R.parents[2]/'generate/scratch'/str(kp);g=load(D.with_suffix('.py'),'generator');src=json.load(open(D/'source.json'));assert src==json.load(open(R/'sources'/f'{kp}.json'));olds={q[':question/id']:q for q in src['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  rec=g.generate(c['level'],parameters=c['parameters'],template=c['template'],profile=c['bank_profile']);check(rec);q=rec['question'];o=olds[c['source_id']]
  for attr in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (attr in q)==(attr in o)
  assert q[':question/problem']==o[':question/problem'] and q[':question/worked-solution']==o[':question/worked-solution'] and q[':question/difficulty']==o[':question/difficulty'][':db/ident']
  for f,of in zip(q[':question/answer-fields'],o[':question/answer-fields']):
   assert f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert correct==of[':answer-field/correct'][':answer/value'];n['source_values']+=2;n['source_refs']+=1
  n['source_prompts']+=1;n['source_solutions']+=1
 for rec in json.load(open(D/'review.json')):check(rec.get('record',rec))
 for level in ('easy','moderate','hard'):
  for seed in range(30):check(g.generate(level,seed=310000+seed))
  families={tuple(sorted(p['kinds'])) for p in (g.generate(level,seed=i)['generation']['parameters'] for i in range(1000))};assert len(families)==(9 if level=='easy' else 12)
 (R/'qa'/f'{kp}-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
