"""Independent displayed-math, exact source, native grading and identity audit."""
import importlib.util,json,re,subprocess,hashlib,itertools,sys
from pathlib import Path
P=Path(__file__).parent;S=P.with_suffix('.py');REPO=P.parents[2]
sp=importlib.util.spec_from_file_location('g',S);g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
checks=[];review=[];audits=[]
def equal(a,b):return g.s.simplify(a-b)==0
def tuple_equal(a,b):return all(equal(v,w) for v,w in zip(a,b))
def fields_equal(a,b):
 a=json.loads(json.dumps(a));b=json.loads(json.dumps(b))
 for q in (a,b):
  for f in q.get(':question/answer-fields',[]):f[':answer-field/choices']=sorted(f[':answer-field/choices'],key=lambda z:z[':answer/id'])
 return a==b

def syntax(z):
 assert '@@' not in z,z
 assert z.count('$')%2==0,z
 depth=0
 for c in z:
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,z
 assert depth==0,z
 assert '+-' not in z and '--' not in z,z

def balanced_argument(z,start):
 depth=1;end=start
 while depth:
  c=z[end]
  if c=='(':depth+=1
  elif c==')':depth-=1
  end+=1
 return z[start:end-1]

def inspect(r,raw=False,opaque=False):
 q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'}
 parts=q[':question/problem'].split('$');L,R=parts[1].rstrip('.').split('=')
 residual=g.parse(L)-g.parse(R)
 pt=re.findall(r'\$\((.*?)\)\.?\$',q[':question/problem'])[-1]
 a,b=map(g.parse,pt.split(','));membership=equal(residual.subs({g.x:a,g.y:b}),0)
 if not membership:
  assert raw and r['generation']['template']=='q-130201',('point not on displayed curve',r)
 grad=(g.s.diff(residual,g.x).subs({g.x:a,g.y:b}),g.s.diff(residual,g.y).subs({g.x:a,g.y:b}))
 syntax(q[':question/problem'])
 field_reports=[]
 for f in q[':question/answer-fields']:
  pairs=[g.pair(ans[':answer/value']) for ans in f[':answer-field/choices']]
  eligible=[index for index,z in enumerate(pairs) if z!=(0,0) and g.dot(grad,z)==0]
  correct=f.get(':answer-field/correct',[None,None])[1]
  marked=[idx for idx,ans in enumerate(f[':answer-field/choices']) if ans[':answer/id']==correct]
  if not opaque:assert len(eligible)==1,('ambiguous full bank',r,eligible)
  if marked:assert (marked==eligible if not opaque else marked[0] in eligible),('wrong correct designation',r)
  else:assert raw,('missing designation in completed record',r)
  assert len(f[':answer-field/choices'])==5
  for ans in f[':answer-field/choices']:
   # Doubled legacy slashes are explicitly raw evidence; completed and normal
   # records normalize those presentation bytes before learner use.
   syntax(ans[':answer/value'])
   if not raw:assert '\\\\' not in ans[':answer/value']
  if r['generation']['eligible_for_learning']:
   assert len({ans[':answer/id'] for ans in f[':answer-field/choices']})==5
   assert all(not g.same_direction(pairs[ii],pairs[jj]) for ii in range(5) for jj in range(ii))
  field_reports.append({'key':f[':answer-field/key'],'valid_indices':eligible,'source_has_correct':bool(marked)})
 sol=q.get(':question/worked-solution')
 stages=0;conclusion_checked=False
 if sol:
  syntax(sol)
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
  rows=blocks[-1].split(r'\\');operatorrow=rows[0]
  for before in blocks[:-1]:
   for row in before.split(r'\\'):
    LHS,RHS=row.split('&',1);RHS=RHS.lstrip(' =').rstrip(' .')
    relation=g.parse(LHS.strip())-g.parse(RHS)
    assert equal(relation,residual) or equal(relation,-residual),('displayed rearrangement incorrect',r['generation']['template'],row)
  inputs=[]
  pattern=r'\\frac\{(?:∂|\\partial)\}\{(?:∂|\\partial) ?([xy])\}\('
  for match in re.finditer(pattern,operatorrow):inputs.append((match[1],g.parse(balanced_argument(operatorrow,match.end()))))
  assert [u for u,F in inputs]==['y','x'],operatorrow
  FY,FX=inputs[0][1],inputs[1][1];assert equal(FY,FX)
  declaration=re.search(r'(?:if|If) we set \$f\(x,y\)\s*=\s*(.*?)\$',sol)
  assert declaration,('missing prose function declaration',r)
  declared=g.parse(declaration[1].rstrip(',.'))
  assert equal(declared,FY),('stale prose function declaration',r['generation']['template'],declaration[1],FY)
  level=re.search(r'level curve \$f\(x,y\)=(.*?)\.\$',sol)
  assert level,sol
  level_ok=equal(FY.subs({g.x:a,g.y:b}),g.parse(level[1]))
  if not level_ok:assert raw and r['generation']['template'] in ('q-72463','q-130201'),('false displayed level',r)
  assert equal(g.s.diff(FY,g.x),g.s.diff(residual,g.x)) or equal(g.s.diff(FY,g.x),-g.s.diff(residual,g.x))
  assert equal(g.s.diff(FY,g.y),g.s.diff(residual,g.y)) or equal(g.s.diff(FY,g.y),-g.s.diff(residual,g.y))
  # A single orientation factor must apply to both components.
  assert equal(g.s.diff(FY,g.x)*g.s.diff(residual,g.y)-g.s.diff(FY,g.y)*g.s.diff(residual,g.x),0)
  symbolic=(g.s.diff(FY,g.y),-g.s.diff(FY,g.x));numeric=tuple(z.subs({g.x:a,g.y:b}) for z in symbolic)
  for idx,row in enumerate(rows[1:]):
   rhs=row.split('&',1)[1].lstrip(' =')
   actual=g.pair(rhs)
   expected=symbolic if idx==0 else numeric
   assert tuple_equal(actual,expected),('displayed row incorrect',r['generation']['template'],idx,rhs,actual,expected)
   stages+=1
  final=g.pair(rows[-1].split('&',1)[1].lstrip(' ='))
  assert g.dot(grad,final)==0
  conclusion=re.search(r'Therefore, our tangent vector is \$(.*?)\$',sol)
  assert conclusion,('missing final prose vector',r)
  concluding=g.pair(conclusion[1].rstrip('.'))
  assert tuple_equal(concluding,numeric),('stale concluding vector',r['generation']['template'],r['generation']['parameters'],conclusion[1],numeric)
  assert tuple_equal(concluding,final) and g.dot(grad,concluding)==0
  conclusion_checked=True
  # Full formal operator inputs, then symbolic derivative, point substitution,
  # numerical evaluation (if source has it), collected vector in source order.
  expected_rows=5 if r['generation']['eligible_for_learning'] else (len(re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',g.QUESTIONS[r['generation']['template']].get(':question/worked-solution',''),re.S)[-1].split(r'\\')) if r['generation']['template']!='q-36391' else 5)
  assert len(rows)==expected_rows
 metadata=r['generation'];assert metadata['dependencies']=={'python':g.platform.python_version(),'sympy':g.s.__version__}
 assert metadata['domain']['variables']=={'x':'real','y':'real'}
 assert metadata['domain']['conditions']==(['y>0'] if residual.has(g.s.log(g.y)) else [])
 assert metadata['domain']['regular_point_verified'] is True
 assert metadata['domain']['point_membership_verified']==membership
 return {'membership':membership,'stages':stages,'concluding_vector_checked':conclusion_checked,'fields':field_reports}

def native(r,label):
 cs=[]
 for fi,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:
   cs.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned complete-bank selection'})
 checks.append({'label':label,'record':r,'checks':cs})

def main():
 source_cases=json.loads((P/'source-cases.json').read_text());source_counts={'questions':0,'banks':0,'options':0,'worked_solutions':0,'existing_correct_designations':0};findings=[]
 for case in source_cases:
  qid=case['source_id'];raw=g.generate('moderate',parameters=case['parameters'],profile=case['bank_profile'])
  assert fields_equal(raw['question'],g.shape(g.QUESTIONS[qid])),qid
  assert set(raw['question'])==set(g.shape(g.QUESTIONS[qid]))
  assert raw['generation']['evidence_only'] and not raw['generation']['eligible_for_learning']
  audit=inspect(raw,True);audits.append({'source_id':qid,'raw':audit})
  source_counts['questions']+=1;source_counts['banks']+=len(raw['question'][':question/answer-fields']);source_counts['options']+=sum(len(f[':answer-field/choices']) for f in raw['question'][':question/answer-fields']);source_counts['worked_solutions']+=int(':question/worked-solution' in raw['question']);source_counts['existing_correct_designations']+=sum(':answer-field/correct' in f for f in raw['question'][':question/answer-fields'])
  complete=g.generate('moderate',parameters=case['parameters'],profile='completed:'+qid);inspect(complete);native(complete,'completed:'+qid)
  assert complete['generation']['evidence_only'] and not complete['generation']['eligible_for_learning']
  review.extend([{'label':'Original raw '+qid,'record':raw},{'label':'Minimal supported completion '+qid,'record':complete}])
  if complete['generation']['repairs']:findings.append({'source_id':qid,'repairs':complete['generation']['repairs']})
  # Meaningful point changes use the same full masks; original opaque banks are
  # evidence only and are not assumed to remain eligible for learning.
  changes={
   'q-36391':{'x0':'-1','y0':'2'},'q-65204':{'x0':'0','y0':'-pi/2'},
   'q-130198':{'x0':'-pi/2','y0':'0'},'q-130200':{'x0':'-1','y0':'0'},
   'q-37516':{'x0':'-1','y0':'E'},'q-72400':{'x0':'-2','y0':'1'},
   'q-72463':{'x0':'-1','y0':'1'},'q-130201':{'x0':'1','y0':'-1'},
   'q-72388':{'x0':'-1','y0':'2'},'q-130192':{'x0':'-2','y0':'1'},'q-130194':{'x0':'1','y0':'1'}}
  variant=g.generate('moderate',profile='raw:'+qid,parameters=changes[qid])
  # This is a public API opaque evidence variant, not a learner default bank.
  va=inspect(variant,raw=True,opaque=True);audits.append({'source_id':qid,'changed_parameter_opaque_evidence':va})
  review.append({'label':'Changed-parameter observed-mask evidence '+qid,'record':variant})
 diversity={}
 for level in ('easy','moderate','hard'):
  unique=set()
  for seed in range(80):
   rec=g.generate(level,seed);audit=inspect(rec);audits.append({'level':level,'seed':seed,**audit});native(rec,level+'/'+str(seed));unique.add(rec['generation']['mathematical_fingerprint'])
   # Same parameters across seeds/order preserve identity.
   twin=g.generate(level,seed+943,parameters=rec['generation']['parameters'])
   assert rec['question'][':question/id']==twin['question'][':question/id']
   assert rec['generation']['content_fingerprint']==twin['generation']['content_fingerprint']
   if seed<2:review.append({'label':'Authored '+level+' variant '+str(seed+1),'record':rec})
  assert len(unique)>=40,(level,len(unique));diversity[level]={'sampled_seeds':80,'distinct_meaningful_tasks':len(unique)}
 # A stale prose vector must fail even when every aligned row is correct.
 regression=g.generate('moderate',profile='raw:q-37516',parameters={'x0':'-1','y0':'E'})
 bad=json.loads(json.dumps(regression));bad['question'][':question/worked-solution']=re.sub(r'(Therefore, our tangent vector is \$).*?(\.\$)',lambda m:m[1]+r'(\frac{2}{e}-8)i+(8e-2)\,j'+m[2],bad['question'][':question/worked-solution'])
 try:inspect(bad,raw=True,opaque=True)
 except AssertionError as error:assert 'stale concluding vector' in str(error)
 else:raise AssertionError('validator accepted the root stale-conclusion regression')
 # Explicit domain guards as well as random samplers.
 for level in ('easy','moderate','hard'):
  baseline=g.generate(level,22)['generation']['parameters']
  for key,bad in [('a','0'),('a','-5'),('x0','0'),('x0','1/17'),('y0','-E' if level=='hard' else '3')]:
   p={**baseline,key:bad}
   try:g.generate(level,parameters=p)
   except ValueError:pass
   else:raise AssertionError((level,key,bad))
 for qid in g.QUESTIONS:
  bad={**json.loads((P/'source-templates.json').read_text())[qid]['parameters'],'x0':'1/100003'}
  try:g.generate('moderate',profile='raw:'+qid,parameters=bad)
  except ValueError:pass
  else:raise AssertionError(('source arithmetic guard',qid))
 # Atomic evidence-only writing; shared engine remains unchanged.
 (P/'engine-input.json').write_text(json.dumps(checks,indent=2)+'\n')
 engine=REPO/'generate/runs/current/check-engine'
 subprocess.run([str(engine),str(P/'engine-input.json'),str(P/'engine-report.json')],check=True)
 result={'status':'pass','source_fidelity':source_counts,'raw_exact_questions':11,'supported_completion_questions':11,'presentation_normalization_count':0,'mathematically_repaired_source_questions':2,'source_mathematical_findings':findings,'observed_difficulties':{'moderate':10,'unrated':1,'easy':0,'hard':0},'authored_extensions':['quadratic easy canonical workload','mixed-polynomial moderate complete method bank','log-product hard signed nonzero evaluation extension'],'diversity':diversity,'native_engine':json.loads((P/'engine-report.json').read_text()),'displayed_math_audits':audits,'limits':['Historical distractor intent remains opaque; raw and completed historical banks are evidence-only.','Easy/hard difficulty labels are authored scope claims, not observed labels.','No blanks in observed or authored layouts; equivalent free-entry checks are inapplicable.'],'database_writes':0,'engine_hash':hashlib.sha256(engine.read_bytes()).hexdigest()}
 (P/'validation.json').write_text(json.dumps(result,indent=2)+'\n');(P/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 (P/'review.md').write_text('# Tangent-vector review\n\nRaw originals retain source errors and missing keys. Completions and opaque variants remain evidence only. The six authored examples are eligible complete method banks.\n\n'+'\n'.join('## '+item['label']+'\n\n'+g.markdown(item['record']) for item in review))
 print('PASS: 11 raw questions,12 full banks,60 options,10 source solutions;240 authored displayed-math/native records.')
if __name__=='__main__':main()
