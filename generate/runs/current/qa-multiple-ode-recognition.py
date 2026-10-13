"""Root actual three functions, complete subset banks and all printed stages."""
import importlib.util,json,re,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
R=Path(__file__).resolve().parent;D=R.parents[2]/'generate/scratch/17592186100959'
def load(path,name):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
p=load(R/'ode-scalar-parser.py','p');g=load(D.with_suffix('.py'),'g');x=s.Symbol('x',positive=True);y=p.y
n=dict(records=0,choices=0,whole_subset_banks=0,printed_derivatives=0,printed_comparisons=0,source_prompts=0,source_solutions=0,source_values=0,source_designations=0)
def scalar(t):
 t=t.strip().replace(r'\,✓','').replace(r'\,\times','').replace(r'\times','').replace('✓','').strip().rstrip('.,')
 return p.scalar(t).subs(p.x,x)
def equal(a,b):return s.simplify(s.trigsimp(s.expand_log(a-b,force=True)))==0
def subsets(t):return frozenset(re.findall(r'\b(?:III|II|I)\b',t))
def check(r):
 q=r['question'];m=r['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution'];eq=re.findall(r'\$\$(.*?)\$\$',prompt,re.S)[0];rhs=scalar(eq.split('=',1)[1].split(',')[0]);fs=[scalar(t) for t in re.findall(r'- \$y=(.*?)\$',prompt)];assert len(fs)==3;flags=[equal(s.diff(f,x),rhs.subs(y,f)) for f in fs];good=frozenset(z for z,ok in zip(('I','II','III'),flags) if ok)
 bank=q[':question/answer-fields'][0];vs=[subsets(a[':answer/value']) for a in bank[':answer-field/choices']];assert len(vs)==5 and len(set(vs))==5 and vs.count(good)==1;correct=next(a[':answer/value'] for a in bank[':answer-field/choices'] if a[':answer/id']==bank[':answer-field/correct'][1]);assert subsets(correct)==good;assert 'correct answer is "'+correct+'."' in sol
 if not m['evidence_only']:
  assert 'stated domain' in sol
  if any(f.has(s.log) for f in fs):assert 'x>0' in prompt
 blocks=re.findall(r'\$\$\s*\\begin\{aligned\}(.*?)\\end\{aligned\}\s*\$\$',sol,re.S);assert len(blocks)==3
 prose=re.findall(r'Differentiating \$y=(.*?)\$.*?get \$.*?=(.*?)\$',sol,re.S);assert len(prose)==3
 for index,(f,b,pr) in enumerate(zip(fs,blocks,prose)):
  df=s.diff(f,x);sub=rhs.subs(y,f);res=df-sub;assert equal(scalar(pr[0]),f) and equal(scalar(pr[1]),df);n['printed_derivatives']+=1
  rows=b.split(r'\\')
  for j,row in enumerate(rows):
   left,right=row.split('&',1);right=right.strip();relation=re.match(r'(\\overset\{\?\}\{=\}|\\not\\equiv|\\ne|=)(.*)',right,re.S);assert relation,row;op,rt=relation.groups()
   if j==0:assert equal(scalar(rt),rhs);continue
   a,v=scalar(left),scalar(rt)
   if j==1:assert equal(a,df) and equal(v,sub)
   elif equal(a,df) and equal(v,sub):pass
   else:
    rr=s.simplify(s.trigsimp(s.expand_log(a-v,force=True)))
    if flags[index]:assert equal(rr,0)
    else:
     assert not equal(rr,0);ratio=s.simplify(s.trigsimp(s.expand_log(rr/res,force=True)));assert ratio!=0 and not ratio.has(s.zoo,s.nan),(row,res,ratio)
     # Reduced source comparisons may multiply/divide by a domain-nonzero
     # x power/exponential; retain nonidentity rather than assert false '='.
   if op=='=' and not m['evidence_only']:assert flags[index] and equal(a,v)
   n['printed_comparisons']+=1
 n['records']+=1;n['choices']+=5;n['whole_subset_banks']+=1
if __name__=='__main__':
 old={q[':question/math-academy-id']:q for q in json.load(open(D/'source.json'))['record'][':knowledge-point/questions']}
 assert json.load(open(D/'source.json'))==json.load(open(R/'sources/17592186100959.json'))
 for c in json.load(open(D/'source-cases.json')):
  r=g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters=c['parameters']);check(r);o=old[c['source_id']];q=r['question'];assert q[':question/problem']==o[':question/problem'];assert q[':question/worked-solution']==o[':question/worked-solution'];n['source_prompts']+=1;n['source_solutions']+=1
  f=q[':question/answer-fields'][0];of=o[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices']);a=next(a[':answer/value'] for a in of[':answer-field/choices'] if a[':answer/id']==of[':answer-field/correct'][':answer/id']);b=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert a==b;n['source_values']+=5;n['source_designations']+=1
  for k in (2,-3):check(g.generate(c['level'],template=c['template'],profile=c['bank_profile'],parameters={'scale':k}))
 for level,templates in g.FAMILIES.items():
  for template in templates:
   for seed in range(9):
    r=g.generate(level,template=template,seed=18000+seed);check(r);z=g.generate(level,template=template,seed=19000+seed,parameters=r['generation']['parameters']);assert r['question'][':question/id']==z['question'][':question/id']
 for r in json.load(open(D/'review.json')):check(r.get('record',r))
 (R/'qa/17592186100959-independent.json').write_text(json.dumps(n,indent=2)+'\n');print(n)
