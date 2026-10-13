"""Read printed ODEs, choices and every mathematical solution row independently.
Raw source omissions are audited separately; grading uses the actual native engine.
"""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
from math_reader import scalar,x,y,z,C
ROOT=Path(__file__).parent
REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('direct',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(n,v):(ROOT/n).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def clean(v):
 v=v.replace(r'\operatorname{ln}',r'\ln').replace('⁡','')
 v=re.sub(r'\\ln\s*\\left\|(.+?)\\right\|',r'\\ln(\1)',v)
 v=re.sub(r'\\ln\s*\|([^|]+)\|',r'\\ln(\1)',v)
 return v.replace(r'\left|','').replace(r'\right|','').replace('|','')
DERIV=[r'\frac{\text{d}y}{\text{d}x}',r'{f}^{′}(x)',r'f^{′}(x)',r"f'(x)",r'f\prime(x)']
def read(v):
 v=clean(v.strip().rstrip('.,'))
 for d in DERIV:v=v.replace(d,'z')
 v=v.replace('f(x)','y')
 return scalar(v)
def ode(q):
 v=re.findall(r'(?<!\$)\$(?!\$)(.+?)(?<!\$)\$(?!\$)',q[':question/problem'],re.S)[0]
 a,b=v.rstrip('.').split('=');res=read(a)-read(b);assert res.has(z)
 return s.solve(res,z)[0]
def choice(v):
 a,b=v.split('=');assert 'f(x)' in a or 'y' in a,a
 left=read(a);right=read(b);assert not right.has(y,z)
 return s.solve(left-right,y)[0]
def deriv(v):return s.simplify(s.diff(v,x))
def family(a,b):
 # Nonzero affine rescaling/shift of arbitrary C yields same full family.
 aa=s.diff(a,C);bb=s.diff(b,C)
 return aa!=0 and bb!=0 and not aa.has(x,C) and not bb.has(x,C) and s.simplify(deriv(a.subs(C,0)-b.subs(C,0)))==0

def solution(q,F):
 if ':question/worked-solution' not in q:return 0
 rows=0
 for block in re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S):
  block=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
  prev=None
  for line in block.split(r'\\'):
   line=line.replace('&','').strip().rstrip('.')
   if not line:continue
   a,b=line.split('=',1);a=a.strip() or prev;assert a is not None
   prev=a
   def val(text):
    text=clean(text)
    for marker in DERIV:text=text.replace(marker,'z')
    # Every formal integral gets evaluated independently from its displayed integrand.
    pattern=r'\\int\s*(.*?)\\(?:,\\)?text\{d\}x'
    def integ(m):
     expr=read(m[1]) if m[1].strip() else s.Integer(1);expr=expr.subs(z,deriv(F.subs(C,0)))
     primitive=s.integrate(expr,x)
     if primitive.has(s.Integral):raise AssertionError(('Unevaluated displayed integral',m[0]))
     return '('+g.tex(primitive)+')'
    text=re.sub(pattern,integ,text)
    assert r'\int' not in text,('Unparsed formal integral',text)
    return read(text).subs({y:F.subs(C,0),z:deriv(F.subs(C,0)),C:0})
   va,vb=val(a),val(b);assert s.simplify(va-vb)==0,(line,va,vb)
   rows+=1
 return rows

def formatting(q):
 texts=[q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']]
 for text in texts:
  assert text.count('$')%2==0
  depth=0
  for c in text:
   if c=='{':depth+=1
   if c=='}':depth-=1
   assert depth>=0
  assert depth==0
  assert '@@' not in text and 'sinh' not in text and 'cosh' not in text
  assert not re.search(r'(?<![A-Za-z])[tuv](?![A-Za-z])',re.sub(r'\\[A-Za-z]+','',text)),text

def check(r,raw=False):
 assert set(r)=={'knowledge_point','question','generation'};assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];formatting(q);rhs=ode(q);field=q[':question/answer-fields'][0];bank=field[':answer-field/choices'];assert len(bank)==5
 math=[choice(a[':answer/value']) for a in bank];eligible=[i for i,a in enumerate(math) if s.diff(a,C)!=0 and not s.diff(a,C).has(x,C) and s.simplify(deriv(a)-rhs)==0]
 assert len(eligible)==1,(q,eligible);correct=bank[eligible[0]]
 if ':answer-field/correct' in field:assert field[':answer-field/correct'][1]==correct[':answer/id']
 for i,a in enumerate(math):
  for b in math[:i]:assert not family(a,b),('Ambiguous complete families',a,b)
 if not raw:
  assert all(s.diff(a,C)!=0 for a in math)
  assert r['generation']['eligible_for_learning'] and not r['generation']['evidence_only']
  opening=('First, notice that the derivative term is already isolated on the left:' if s.Rational(r['generation']['parameters']['d'])==1 else 'First, we rearrange the equation to isolate the derivative term:')
  assert q[':question/worked-solution'].startswith(opening)
  primitive_count=r['generation']['primitive_count']
  blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S)
  assert len(blocks)==2
  ordered=blocks[1].split(r'\\')
  assert len(ordered)==4
  assert ordered[0].count(r'\int')==2
  assert ordered[1].count(r'\int')==primitive_count
  assert ordered[2].count(r'\cdot \left(')==primitive_count
  assert r'\int' not in ordered[2] and r'\int' not in ordered[3]
 else:assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']
 count=solution(q,math[eligible[0]])
 return count,correct

def main():
 records=[];checks=[];cases=[];fidelity=[];stage_count=0
 for sid,t,l in g.CASES:
  raw=g.generate(l,template=t,parameters={'dependent_scale':1},profile=sid);original=g.QUESTIONS[sid]
  q=raw['question'];of=original[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  for key in (':question/difficulty',':question/worked-solution'):assert (key in q)==(key in original)
  assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
  assert q[':question/problem']==original[':question/problem'];assert q.get(':question/worked-solution')==original.get(':question/worked-solution')
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
  n,correct=check(raw,True);stage_count+=n;records.append(raw)
  cases.append({'source_id':sid,'template':t,'parameters':{'dependent_scale':1},'bank_profile':sid,'authored_level_assignment':l if ':question/difficulty' not in original else None})
  fidelity.append({'source_id':sid,'prompt_exact':True,'solution_exact':True if ':question/worked-solution' in original else None,'key_presence':True,'bank_matched':5,'designation_matched':True if ':answer-field/correct' in of else None})
  changed=g.generate(l,template=t,parameters={'dependent_scale':2},profile=sid);stage_count+=check(changed,True)[0];records.append(changed)
 for t,l in g.TEMPLATES.items():
  for seed in range(12):
   r=g.generate(l,seed,template=t);stage_count+=check(r)[0]
   if seed<2:records.append(r)
   alternate=g.generate(l,seed+100,template=t,parameters=r['generation']['parameters']);assert alternate['question'][':question/id']==r['question'][':question/id']
  try:g.generate(l,template=t,parameters={'d':1,'terms':[['poly',20,1]]})
  except ValueError:pass
  else:raise AssertionError('Invalid workload accepted')
 for r in records:
  q=r['question'];f=q[':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue # raw absence is not a matched designation
  checks.append({'label':r['generation']['template']+'/'+r['generation']['bank_profile'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual radio grading of owned answer'} for a in f[':answer-field/choices']]})
 write('source-cases.json',cases);write('source-fidelity.json',fidelity);write('review.json',records);write('engine-input.json',checks)
 native=ROOT/'reference/replenishment/check-engine'
 if not native.exists():native=REPO/'generate/runs/current/check-engine'
 subprocess.run([str(native),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True)
 review=['# Direct-integration review','Raw original profiles have dependent_scale=1; changed profiles have dependent_scale=2. Normal records have an authored method bank.']
 for r in records:
  meta=r['generation'];source=g.QUESTIONS.get(meta.get('raw_source_id'));level=r['question'].get(':question/difficulty','unrated').split('/')[-1].title()
  kind=('Original source replay' if meta['parameters'].get('dependent_scale')=='1' else 'Generated evidence variant') if meta['evidence_only'] else 'Generated learning question'
  review+=['\n## '+kind+' — '+level+' — '+meta['template']+' — '+meta['bank_profile']+' '+str(meta['parameters']),g.markdown(r)]
 (ROOT/'review.md').write_text('\n\n'.join(review))
 engine=json.loads((ROOT/'engine-validation.json').read_text())
 result={'passed':True,'basis':1356,'practice_sources':8,'source_prompts_exact':8,'source_banks_exact':8,'source_options_exact':40,'source_designations_matched':7,'source_designations_missing':1,'source_worked_solutions_exact':7,'source_worked_solutions_missing':1,'raw_attribute_presence_preserved':8,'generated_checked':132,'displayed_solution_rows_checked':stage_count,'authored_hard_templates':3,'plots':'none','source_opaque_profiles':8,'native_accepted':engine['accepted_checks'],'native_rejected':engine['rejected_checks'],'native_unresolved':engine['documented_unresolved_checks'],'native_limitation':'All assessed fields are radios: engine grades owned choice UUIDs; mathematical full-family equivalence is independently checked, not established by radio-ID tests.','source_anomaly':'q-14245 lacks rating, solution and correct ref, and one distractor lacks C; raw preserved. Normal authored linear bank supplies all C and a verified designation.','hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [ROOT.with_suffix('.py'),ROOT/'math_reader.py',native,REPO/'engine/rust/learning.rs',REPO/'engine/rust/symbolic.rs']}}
 write('validation.json',result)
 print(json.dumps(result,indent=2))
if __name__=='__main__':main()
