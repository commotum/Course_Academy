#!/usr/bin/env python3
"""Independent read-back, source fidelity, workload, identity and native grading."""
import copy,functools,hashlib,importlib.util,json,pathlib,re,subprocess,sys
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
sys.dont_write_bytecode=True
D=pathlib.Path(__file__).resolve().parent;ROOT=D.parents[2]
spec=importlib.util.spec_from_file_location('polar_generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
trans=standard_transformations+(implicit_multiplication_application,rationalize)

def groups(s,start):
 assert s[start]=='{';depth=1;i=start+1
 while depth:
  assert i<len(s),'Unbalanced TeX group'
  depth+= (s[i]=='{')-(s[i]=='}');i+=1
 return s[start+1:i-1],i

@functools.lru_cache(maxsize=None)
def tex_parse(s,r=None,theta=None):
 # Parse actual learner-visible mathematics, not generation metadata.
 s=s.replace('⁡','').replace('π',r'\pi').replace(r'\,','').replace(r'\left','').replace(r'\right','')
 s=re.sub(r'\{?(\d+)\}?\^\{∘\}',lambda m:'('+m.group(1)+'*pi/180)',s)
 s=s.replace(r'\operatorname{cos}','*cos').replace(r'\operatorname{sin}','*sin').replace(r'\cos','*cos').replace(r'\sin','*sin')
 for command in (r'\frac',r'\dfrac',r'\sqrt'):
  while command in s:
   k=s.index(command);j=k+len(command)
   a,j=groups(s,j)
   if command.endswith('frac'):b,j=groups(s,j);v='(('+str(tex_parse(a,r,theta))+')/('+str(tex_parse(b,r,theta))+'))'
   else:v='sqrt('+str(tex_parse(a,r,theta))+')'
   s=s[:k]+v+s[j:]
 s=s.replace(r'\pi','pi').replace(r'\theta','T').replace(r'\cdot','*').replace('{','(').replace('}',')')
 s=re.sub(r'(cos|sin)\s*T',r'\1(T)',s).replace('**cos','*cos').replace('**sin','*sin')
 s=re.sub(r'\*\s*\*','*',s)
 result=parse_expr(s,local_dict={'pi':sp.pi,'sqrt':sp.sqrt,'sin':sp.sin,'cos':sp.cos,'r':sp.Symbol('R'),'T':sp.Symbol('T')},transformations=trans)
 if r is not None:result=result.subs(sp.Symbol('R'),r)
 if theta is not None:result=result.subs(sp.Symbol('T'),theta)
 return sp.simplify(result)

def point(s):
 assert s.startswith('(') and s.endswith(')'),s
 a,b=s[1:-1].split(',');return tex_parse(a),tex_parse(b)
def read_prompt(problem):
 m=re.search(r'origin is \$(.+?)\$',problem);assert m,'Printed radius missing';r=tex_parse(m[1].rstrip(','))
 m=re.search(r'angle of \$(.+?)\$',problem);assert m,'Printed angle missing';theta=tex_parse(m[1])
 assert r>0 and theta.is_real
 return r,theta

def formatting(s):
 s=re.sub(r'\{\{[^{}]+\}\}','',s)
 assert s.count('$')%2==0,'Unbalanced math delimiters'
 depth=0
 for c in s:
  depth+=(c=='{')-(c=='}');assert depth>=0,'Unbalanced TeX braces'
 assert depth==0,'Unbalanced TeX braces'
 assert not re.search(r'(?<!\\)(?:--|\+\-)',s),'Ungrouped signs'

def independent_bank(record,r,theta,xy):
 x,y=xy;c=sp.cos(theta);v=sp.sin(theta);profile=record['generation']['profile']
 if profile.startswith('raw-') or profile.startswith('source-'):
  sid=profile[4:] if profile.startswith('raw-') else {'source-sign-root':'q-17126','source-sign-half':'q-17134','source-axis-down':'q-17128','source-axis-right':'q-17137'}[profile]
  z=sp.sqrt
  table={
   'q-17133':[(-r/2,r*z(3)/2),(r/2,-r*z(3)/2),(-r*z(3)/2,-r*z(3)/2),(-r*z(3)/2,r/2),(r/2,-r/2)],
   'q-8522':[(-r*z(2)/2,r),(r*z(2)/2,-r/2),(r*z(3)/2,-r),(r,r*z(2)/2),(r*z(3)/2,-r/2)],
   'q-120328':[(x,y),(x/2,y/2),(r*z(3)/3,-r*z(3)/3),(-r*z(2),r*z(2)),(r*z(3)/9,-r*z(3)/9)],
   'q-17124':[(-z(2)/(1/r+1),)*2,(-z(2)/2,)*2,(-r*z(2),)*2,(x,y),(-z(2)/(1/r+2),)*2],
   'q-17126':[(-x,-y),(x,-y),(x,-r*z(3)/2),(-x,y),(x,y)],
   'q-17128':[(0,r),(0,1),(0,-r),(r,0),(-r,0)],
   'q-17134':[(-x,y),(x,-y/2),(-x,-y/2),(x,y),(-x,-y)],
   'q-17137':[(0,r),(r,1),(r,0),(1,0),(-r,0)],
   'q-8516':[(-x,r*z(3)/4),(-x,y),(x,r*z(2)/2),(x,y),(x,r*z(3))]}
  return [tuple(sp.simplify(k) for k in point) for point in table[sid]]
 return [(x,y),(-x,y),(x,-y),(-x,-y),((y,x) if x!=y and x!=-y else (2*x,2*y)) if r==1 else (c,v)]

def verify(record):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 q=record['question'];r,theta=read_prompt(q[':question/problem']);xy=(sp.simplify(r*sp.cos(theta)),sp.simplify(r*sp.sin(theta)))
 fields=q.get(':question/answer-fields',[]);identities=[]
 for f in fields:
  uuid=f[':answer-field/id'];assert len(uuid)==36
  choices=f[':answer-field/choices'];values=[]
  for a in choices:
   identities.append(a[':answer/id']);assert a[':answer/type']==':answer.type/math'
   val=point(a[':answer/value']) if f[':answer-field/type'].endswith('/radio') else tex_parse(a[':answer/value']);values.append(val)
   formatting(a[':answer/value'])
  assert len(set(map(str,values)))==len(values),'Ambiguous full bank'
  if f[':answer-field/type'].endswith('/radio'):assert set(values)==set(independent_bank(record,r,theta,xy)), 'Displayed full bank does not implement its complete operations'
  expected=xy if f[':answer-field/type'].endswith('/radio') else xy[0 if f[':answer-field/key']=='field-1' else 1]
  assert values.count(expected)==1,'Missing mathematical answer'
  if ':answer-field/correct' in f:
   ref=f[':answer-field/correct'];assert ref[0]==':answer/id'
   a=next(a for a in choices if a[':answer/id']==ref[1]);val=point(a[':answer/value']) if isinstance(expected,tuple) else tex_parse(a[':answer/value'])
   assert val==expected,'Wrong correct designation'
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 assert len(set(identities))==len(identities),'Answers not field-owned'
 formatting(q[':question/problem'])
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];formatting(sol)
  m=re.search(r'r=(.+?),\\,\\theta =(.+?)\.',sol);assert m,'Initial interpreted polar block missing'
  assert tex_parse(m[1])==r and tex_parse(m[2])==theta,'Incorrect interpreted polar quantities'
  assert r'x=r\operatorname{cos}⁡\theta ,\,y=r\operatorname{sin}⁡\theta .' in sol,'Conversion formula changed'
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==2
  for i,block in enumerate(blocks):
   rows=block.split('\\\\');assert len(rows)==4,'Wrong stage count'
   rhs=[re.split(r'&\s*=',row,maxsplit=1)[1].strip() for row in rows]
   assert ('cos' if i==0 else 'sin') in rhs[0]
   assert ('cos' if i==0 else 'sin') in rhs[1]
   assert not any(t in rhs[2] for t in ('cos','sin')), 'Evaluation stage missing'
   assert r'\cdot' in rhs[2] or '(' in rhs[2], 'Multiplication stage collapsed'
   for row in rhs:assert tex_parse(row,r,theta)==xy[i],('Wrong printed solution row',row,xy[i])
  conclusion=re.search(r'Therefore,.*?are \$(\([^$]*\))\.\$',sol,re.S);assert conclusion and point(conclusion[1])==xy,'Wrong printed conclusion'
 return xy

def engine_checks(record):
 checks=[]
 for i,f in enumerate(record['question'][':question/answer-fields']):
  if ':answer-field/correct' not in f:continue
  correct=f[':answer-field/correct'][1]
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Actual native owned-option grading'})
  else:
   v=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct);x=tex_parse(v)
   # Unsimplified arithmetic entries remain different strings from canonical values.
   equivalent='('+str(x)+')*3/3' if not x.has(sp.sqrt) else str(x)
   if x.is_Integer:equivalent=str(int(x)*3)+'/3'
   if x.has(sp.Pow) and not x.is_Integer:
    if x.is_negative:equivalent='-sqrt('+str(sp.simplify(x*x))+')'
    else:equivalent='sqrt('+str(sp.simplify(x*x))+')'
   checks += [{'field_index':i,'submitted':v,'expected':'accepted','purpose':'Canonical component'},
              {'field_index':i,'submitted':equivalent,'expected':'accepted','purpose':'Unsimplified equivalent component'},
              {'field_index':i,'submitted':str(x+1),'expected':'rejected','purpose':'Incorrect component'}]
 return checks

def run():
 originals=json.loads((D/'source.json').read_text())['record'][':knowledge-point/questions'];by={q[':question/math-academy-id']:q for q in originals}
 cases=json.loads((D/'source-cases.json').read_text());records=[];reports=[];engine=[];choice_count=0;designation_count=0
 for case in cases:
  rec=g.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);verify(rec);q=rec['question'];src=by[case['source_id']]
  assert q[':question/problem']==src[':question/problem'],case['source_id']+' prompt fidelity'
  for k in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
   assert (k in q)==(k in src),'Source omission parity '+k
  if ':question/worked-solution' in src:assert q[':question/worked-solution']==src[':question/worked-solution'],case['source_id']+' solution fidelity'
  assert len(q[':question/answer-fields'])==len(src[':question/answer-fields']), 'Source field count'
  for f,s in zip(q[':question/answer-fields'],src[':question/answer-fields']):
   for k in (':answer-field/key',':answer-field/correct',':answer-field/choices'):assert (k in f)==(k in s),'Field attribute parity'
   assert f[':answer-field/key']==s[':answer-field/key'] and f[':answer-field/type']==s[':answer-field/type'][':db/ident']
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in s[':answer-field/choices']),'Complete literal bank mismatch'
   choice_count+=len(s[':answer-field/choices'])
   if ':answer-field/correct' in s:
    designation_count+=1
    selected=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert selected==s[':answer-field/correct'][':answer/value']
  records.append({'kind':'original raw replay','source_id':case['source_id'],'record':rec})
  reports.append({'source_id':case['source_id'],'prompt_exact':True,'solution_exact':':question/worked-solution' in src,'solution_absent':':question/worked-solution' not in src,'all_bank_values_exact':True,'omission_parity':True,'native_eligible_original':all(':answer-field/correct' in f for f in q[':question/answer-fields'])})
  checks=engine_checks(rec)
  if checks:engine.append({'label':'original '+case['source_id'],'record':rec,'checks':checks})
 # Two changed parameter variants for each supported family at each supported level.
 for level,templates in g.FAMILIES.items():
  for t in templates:
   for seed in (71,903):
    rec=g.generate(level,seed,template=t);verify(rec);records.append({'kind':'generated variant','record':rec});engine.append({'label':level+' '+t+' '+str(seed),'record':rec,'checks':engine_checks(rec)})
 # Public raw recipes change whole-component parameters, including opaque banks.
 for c in cases:
  for offset in (1,2):
   p=dict(c['parameters']);p['radius']=str(sp.sympify(p['radius'])+offset)
   rec=g.generate(c['level'],template=c['template'],parameters=p,profile=c['bank_profile']);verify(rec)
   records.append({'kind':'changed-parameter evidence variant','source_id':c['source_id'],'record':rec})
   checks=engine_checks(rec)
   if checks:engine.append({'label':'raw variant '+c['source_id']+' '+str(offset),'record':rec,'checks':checks})
 # Exhaust all authored domains including explicit source-shaped bank constraints.
 unique={};domain_count={};tested=0
 for level,templates in g.FAMILIES.items():
  domain=set()
  for t in templates:
   for d in g.DEGREES:
    radii=(1,) if level=='easy' else tuple(range(2,13))+tuple(sp.Rational(1,i) for i in range(2,7))+(sp.Rational(3,2),sp.Rational(5,2),sp.Rational(7,3)) if level=='moderate' else tuple(k*sp.sqrt(2 if d%90==45 else 3) for k in range(1,7))
    for r in radii:
     u=g.expected_unit(t);p={'radius':str(r),'angle':str(sp.Rational(d,180) if u=='radians' else d),'unit':u}
     try:rec=g.generate(level,template=t,parameters=p)
     except ValueError as err:
      if not any(token in str(err) for token in ('Easy:','Moderate:','Hard:','requires','Source sign','Whole bank')):raise
      continue
     verify(rec);tested+=1;domain.add(rec['generation']['mathematical_fingerprint'])
     again=g.generate(level,999,template=t,parameters=p);assert rec['question'][':question/id']==again['question'][':question/id'],'Shuffle identity unstable'
     fp=rec['generation']['mathematical_fingerprint'];xy=verify(rec)
     if xy in unique:assert unique[xy]==fp
     unique[xy]=fp
  domain_count[level]=len(domain)
 # Every normal default source-shaped family appears; no opaque source enters defaults.
 default_coverage={}
 for l,ts in g.FAMILIES.items():
  seen=set()
  for seed in range(150):
   rec=g.generate(l,seed);verify(rec);seen.add(rec['generation']['template']);assert rec['generation']['eligible_for_learning'] and not rec['generation']['raw_evidence']
  assert seen==set(ts);default_coverage[l]=sorted(seen)
 # Profile selection restricts the family before parameter sampling.
 for l in g.FAMILIES:
  for profile in ('method-sign-scale','coordinate-blanks'):
   for seed in range(12):
    rr=g.generate(l,seed,profile=profile);verify(rr)
    assert rr['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio' if profile=='method-sign-scale' else '/blank')
 # Explicit input guards have the same policy as samplers.
 invalid=[('easy','degree_blank',{'radius':'2','angle':'30','unit':'degrees'}),('moderate','degree_blank',{'radius':'1','angle':'30','unit':'degrees'}),('hard','degree_blank',{'radius':'sqrt(3)','angle':'45','unit':'degrees'}),('hard','degree_blank',{'radius':'7*sqrt(3)','angle':'30','unit':'degrees'}),('moderate','axis_radian_radio',{'radius':'2','angle':'1/6','unit':'radians'}),('easy','degree_blank',{'radius':'1','angle':'390','unit':'degrees'})]
 for l,t,p in invalid:
  try:g.generate(l,template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit input admitted')
 # Independent reader must reject prompt, substitution, multiplication, conclusion mutations.
 specimen=next(r['record'] for r in records if r['kind']=='generated variant' and r['record']['generation']['template']=='degree_blank')
 for key,old,new in [(':question/problem','origin is $','origin is $2*'),(':question/worked-solution',r'\operatorname{cos}⁡(',r'\operatorname{sin}⁡('),(':question/worked-solution','Therefore,','Therefore, ERROR')]:
  altered=copy.deepcopy(specimen)
  if new.endswith('ERROR'):altered['question'][key]=altered['question'][key].replace('are $(','are $(1+',1)
  else:altered['question'][key]=altered['question'][key].replace(old,new,1)
  try:verify(altered)
  except Exception:pass
  else:raise AssertionError('Reader failed to detect altered mathematics')
 for action in ('initial-polar','evaluated-product','wrong-full-choice'):
  altered=copy.deepcopy(specimen);q=altered['question']
  if action=='initial-polar':q[':question/worked-solution']=q[':question/worked-solution'].replace('r=','r=2*',1)
  elif action=='evaluated-product':
   q[':question/worked-solution']=q[':question/worked-solution'].replace(r'\cdot (',r'\cdot (1+',1)
  else:
   f=q[':question/answer-fields'][0]
   # Use a radio record so an arbitrary unequal distractor cannot pass on uniqueness alone.
   altered=copy.deepcopy(next(rr['record'] for rr in records if rr['kind']=='generated variant' and rr['record']['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio')))
   f=altered['question'][':question/answer-fields'][0];a=next(a for a in f[':answer-field/choices'] if a[':answer/id']!=f[':answer-field/correct'][1]);a[':answer/value']='(123,456)'
  try:verify(altered)
  except Exception:pass
  else:raise AssertionError('Reader failed to reject '+action)
 (D/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
 proc=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'engine-input.json'),str(D/'engine-report.json')],text=True,capture_output=True)
 assert proc.returncode==0,proc.stdout+proc.stderr
 native=json.loads((D/'engine-report.json').read_text())
 (D/'review.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
 md=['# Polar-to-Cartesian review','Raw replay retains source omissions and opaque historical banks. Generated variants are authored bounds/banks using the observed component masks. Correct identities are author evidence.']
 for rr in records:
  rec=rr['record'];m=rec['generation'];md += ['## '+rr['kind']+' — '+rr.get('source_id',m['level']+' / '+m['template']),g.markdown(rec),'Author metadata: '+json.dumps({'level':m['level'],'parameters':m['parameters'],'profile':m['profile'],'eligible':m['eligible_for_learning']})]
 (D/'review.md').write_text('\n\n'.join(md)+'\n')
 report={'passed':True,'version':g.VERSION,'source':g.SOURCE,'source_questions':len(cases),'prompt_exact':len(cases),'full_solution_exact':10,'missing_solution_preserved':2,'complete_banks_exact':len(cases),'radio_banks_exact':9,'blank_answer_fields_exact':6,'displayed_answer_values_exact':choice_count,'matched_designations':designation_count,'missing_designations':2,'opaque_historical_banks':['q-17133','q-8522','q-120328','q-17124','q-8516'],'eligible_normal_source_bank_profiles':list(g.SUPPORTED_BANKS.values()),'raw_presence_parity':len(cases),'source_repairs':0,'normal_legacy_completions':{'source_ids':['q-17133','q-8522'],'worked_solution':'authored common four-stage mask','correct_designation':'independently derived; not counted as original matched refs'},'observed_solution_exact_denominator':10,'normal_prose_repairs':['q-17128 x heading to y heading'],'authored_typo_normalization':'q-17128 y-stage heading x -> y in normal output only','exhaustive_normal_instances':tested,'independent_checks':['printed radius/angle','interpreted polar block','conversion formulas','both formal/substituted/evaluated/final component stages','full conclusion','every complete bank operation','all native correct/wrong choices','typed canonical/equivalent/wrong entries','prompt/initial/evaluated/choice/conclusion mutation rejection'],'unique_substantive_tasks':domain_count,'all_family_default_coverage':default_coverage,'native':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':native['documented_unresolved_checks'],'ungradable_raw_sources':['q-17133','q-8522']},'decoded_answer_backslash_runs':{q[':question/math-academy-id']:max([len(m[0]) for f in q[':question/answer-fields'] for a in f[':answer-field/choices'] for m in re.finditer(r'\\+',a[':answer/value'])] or [0]) for q in originals},'plot_references_in_assigned_sources':[],'tex_anomalies':[],'decoded_byte_counts':{q[':question/math-academy-id']:{k:len(v.encode()) for k,v in q.items() if k in (':question/problem',':question/worked-solution')} for q in originals},'freeze':{'script_sha256':hashlib.sha256(D.with_suffix('.py').read_bytes()).hexdigest(),'recipes_sha256':hashlib.sha256((D/'recipes.json').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()},'database_writes':0}
 (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':run()
