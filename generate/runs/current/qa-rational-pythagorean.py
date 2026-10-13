"""Root actual rational banks, source stages and original denominator domain."""
import importlib.util,json,re,sys
from pathlib import Path
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186059642'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'rational-trig-readback.py','p');g=load(D.with_suffix('.py'),'g')
n=dict(records=0,choices=0,whole_banks=0,printed_equalities=0,denominator_zero_checks=0,source_prompts=0,source_values=0,source_solutions=0,source_designations=0)
def scalar(t):return p.scalar(t.strip().rstrip('.,'))
def check(r):
 q=r['question'];m=r['generation'];tex=q[':question/problem'].split('$')[1].rstrip('.=');truth=scalar(tex);f=q[':question/answer-fields'][0];vs=[scalar(a[':answer/value']) for a in f[':answer-field/choices']];assert len(vs)==5 and all(not p.equal(a,b) for i,a in enumerate(vs) for b in vs[:i]);good=[i for i,v in enumerate(vs) if p.equal(v,truth)];assert len(good)==1
 if ':answer-field/correct' in f:assert f[':answer-field/choices'][good[0]][':answer/id']==f[':answer-field/correct'][1]
 assert m['eligible_for_learning']==(not m['evidence_only'])
 ds=p.denominators(tex);assert ds
 for S,C in ((0,1),(1,0),(0,-1),(-1,0)):
  zero=any(d.subs({p.S:S,p.C:C})==0 for d in ds);declared=any(scalar(z.split(' !=')[0]).subs({p.S:S,p.C:C})==0 for z in m['domain']);assert zero==declared,(tex,m['domain'],S,C);n['denominator_zero_checks']+=1
 sol=q.get(':question/worked-solution')
 if sol:
  blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==3
  if not m['evidence_only']:
   fact=scalar(blocks[0].split('=',1)[1]);wrong_identity=fact.subs(p.S**2+p.C**2,2)
   if wrong_identity==fact:wrong_identity=p.s.factor(fact).subs(p.S**2+p.C**2,2)
   assert not p.equal(wrong_identity,truth),(m['template'],fact,blocks[0])
   ct=next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==f[':answer-field/correct'][1]);recip=re.sub(r'(?<![A-Za-z])(sin|cos|tan|cot|sec|csc)(?![A-Za-z])',lambda z:{'sin':'csc','cos':'sec','tan':'cot','cot':'tan','sec':'cos','csc':'sin'}[z[1]],ct)
   if '+' in ct:
    F=wrong_identity-truth;residual=truth-F;expected=[truth,residual-F,wrong_identity,scalar(recip),F+m['parameters']['k']]
   else:expected=[truth,-truth,wrong_identity,scalar(recip),truth*(p.C if m['parameters']['mirror'] else p.S)]
   assert all(sum(p.equal(z,v) for v in vs)==1 for z in expected),'Complete operation bank differs from actual identity stage'
  for b in blocks:
   last=None
   for row in b.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\'):
    for t in row.replace('&','').split('='):
     if not t.strip():continue
     value=scalar(t);assert p.equal(value,truth),(row,truth)
     if last is not None:assert p.equal(last,value);n['printed_equalities']+=1
     last=value
  for inline in re.findall(r'(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)',re.sub(r'\$\$.*?\$\$','',sol,flags=re.S),re.S):
   if '=' in inline:
    a,b=inline.split('=');assert p.equal(scalar(a),scalar(b));n['printed_equalities']+=1
 n['records']+=1;n['choices']+=5;n['whole_banks']+=1
if __name__=='__main__':
 assert json.load(open(D/'source.json'))==json.load(open(R/'sources/17592186059642.json'));old={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
 for c in json.load(open(D/'source-cases.json')):
  r=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(r);q=r['question'];o=old[c['source_id']]
  for key in (':question/problem',':question/worked-solution',':question/difficulty'):
   assert (key in q)==(key in o)
   if key in o:assert q[key]==(o[key][':db/ident'] if key.endswith('difficulty') else o[key])
  of=o[':question/answer-fields'][0];f=q[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices']);assert (':answer-field/correct' in of)==(':answer-field/correct' in f)
  if ':answer-field/correct' in of:
   ov=next(a[':answer/value'] for a in of[':answer-field/choices'] if a[':answer/id']==of[':answer-field/correct'][':answer/id']);gv=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert ov==gv;n['source_designations']+=1
  n['source_prompts']+=1;n['source_values']+=5;n['source_solutions']+=int(':question/worked-solution' in o)
 for template,entry in g.TEMPLATES.items():
  for mirror in (False,True):
   for k in (1,3,12):
    r=g.generate(entry['level'],template=template,parameters={'angle':r'\phi','k':k,'mirror':mirror});check(r);z=g.generate(entry['level'],seed=42,template=template,parameters=r['generation']['parameters']);assert r['question'][':question/id']==z['question'][':question/id']
 for r in json.load(open(D/'review.json')):check(r.get('record',r))
 for k in (0,-1,13):
  try:g.generate('easy',parameters={'angle':'x','k':k,'mirror':False})
  except ValueError:pass
  else:raise AssertionError('Workload guard bypassed')
 (R/'qa/17592186059642-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
