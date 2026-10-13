#!/usr/bin/env python3
"""Independent displayed-math, full source fidelity, scope and native QA."""
import importlib.util,json,re,sys,hashlib,subprocess,itertools
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
P=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('cosecant_generator',P.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,)
x=sp.Symbol('z',real=True)

def parse(s):
 s=s.strip().rstrip('.,').replace('⁡','').replace('π','pi').replace(r'\pi','pi').replace(r'\cdot','*').replace(r'\left','').replace(r'\right','').replace('−','-')
 s=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',s)
 while r'\frac' in s or r'\dfrac' in s:
  newer=re.sub(r'\\d?frac\{([^{}]+)\}\{([^{}]+)\}',lambda m:'(('+m[1]+')/('+m[2]+'))',s)
  if newer==s:raise AssertionError('unsupported fraction '+s)
  s=newer
 s=re.sub(r'\\sqrt\{([^{}]+)\}',r'sqrt(\1)',s)
 return sp.simplify(parse_expr(s,local_dict={'pi':sp.pi,'sqrt':sp.sqrt,'z':x},transformations=TRANS))

def read_prompt(q):
 pieces=re.findall(r'(?<!\$)\$(?!\$)(.*?)\$(?!\$)',q[':question/problem'])
 assert len(pieces)==2,pieces
 first=re.sub(r'\\operatorname\{csc\}⁡|\\csc\s*','CS',pieces[0].replace(r'\theta','theta')).strip().rstrip(',')
 m=re.fullmatch(r'CS([a-z]+)\s*=\s*(.*)',first);assert m,first
 variable=m[1];v=parse(m[2]);assert abs(v)>1
 request=pieces[1].rstrip('=').strip()
 return variable,v,request

def evaluate(s,variable,v):
 s=s.rstrip('.,').replace(r'\theta','theta').replace(r'\operatorname{csc}⁡','CS').replace(r'\csc','CS')
 def replace(m):
  arg=m[1];a=parse(re.sub(r'(?<![A-Za-z\\])'+re.escape(variable)+r'(?![A-Za-z])','z',arg));coef=sp.expand(a).coeff(x);shift=sp.simplify((a-coef*x)/(2*sp.pi))
  assert coef in (-1,1) and shift.is_Integer,('not signed whole-period angle',arg,a)
  return '('+str(coef*v)+')'
 s=re.sub(r'CS\s*\(([^()]*)\)',replace,s)
 s=re.sub(r'CS\s*'+re.escape(variable)+r'\b','('+str(v)+')',s)
 assert 'CS' not in s,s
 return parse(s)

def check_format(q):
 for s in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:
  assert s.count('$$')%2==0
  without=s.replace('$$','');assert without.count('$')%2==0
  depth=0
  for c in s:
   if c=='{':depth+=1
   if c=='}':depth-=1
   assert depth>=0
  assert depth==0
  assert '--' not in s and '+-' not in s

def displayed_math(r):
 q=r['question'];variable,v,request=read_prompt(q);answer=evaluate(request,variable,v)
 f=q[':question/answer-fields'][0];values=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(values)==5 and len(set(values))==5
 assert sum(sp.simplify(z-answer)==0 for z in values)==1
 if ':answer-field/correct' in f:
  chosen=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert parse(chosen[':answer/value'])==answer
 sol=q.get(':question/worked-solution')
 if sol:
  calc=sol.split("Let's now evaluate our expression:")[-1] if "Let's now evaluate our expression:" in sol else sol.split('Therefore,')[-1]
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',calc,re.S)
  level=r['generation']['template'];expected=3 if level.startswith('hard') else 2 if r['generation']['parameters']['n']!='0' else 1
  assert len(blocks)==expected,(level,len(blocks),expected)
  for block in blocks:
   rows=block.split(r'\\');left=None
   for row in rows:
    lhs,rhs=row.split('&');rhs=rhs.strip();assert rhs.startswith('=');rhs=rhs[1:]
    if lhs.strip():left=evaluate(lhs.strip(),variable,v)
    assert sp.simplify(evaluate(rhs,variable,v)-left)==0,(row,left)
  if not level.startswith('hard') and r['generation']['parameters']['n']!='0':
   conclusion=re.search(r'Therefore, \$(.*?)\$',calc)[1];left,right=conclusion.split('=');assert evaluate(left,variable,v)==parse(right)
  # Hard arithmetic row structurally distinguishes substitution from evaluated
  # product and collected result even if a CAS would simplify all three.
  if level.startswith('hard'):
   last=blocks[-1].split(r'\\');assert len(last)==3
   assert '(' in last[0] and '(' not in last[1] and '(' not in last[2]
 check_format(q)
 return answer

def main():
 stats={'source_questions':len(g.CASES),'complete_banks':0,'choice_values':0,'correct_designations':0,'worked_solutions':0,'raw_attribute_presence':0,'raw_exact_strings':0,'normal_source_stage_fidelity':0}
 originals=[];review=[];native=[];coverage=set();fingerprints={l:set() for l in ('easy','moderate','hard')}
 for sid,t,p in g.CASES:
  level=g.TEMPLATES[t];r=g.generate(level,template=t,parameters=p,profile='raw_'+sid);q=r['question'];source=g.QUESTIONS[sid]
  displayed_math(r)
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):
   assert (key in q)==(key in source),(sid,key)
  f=q[':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
  assert (':answer-field/correct' in f)==(':answer-field/correct' in sf)
  stats['raw_attribute_presence']+=1
  assert q[':question/problem']==source[':question/problem'],(sid,q[':question/problem'],source[':question/problem'])
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices']),(sid,'literal bank')
  stats['complete_banks']+=1;stats['choice_values']+=len(f[':answer-field/choices'])
  if ':answer-field/correct' in sf:
   correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert parse(correct[':answer/value'])==parse(sf[':answer-field/correct'][':answer/value']);stats['correct_designations']+=1
  if ':question/worked-solution' in source:
   assert q[':question/worked-solution']==source[':question/worked-solution'],(sid,'solution sequence/string')
   stats['worked_solutions']+=1
   normal=g.generate(level,template=t,parameters=p)
   assert normal['question'][':question/worked-solution']==source[':question/worked-solution']
   stats['normal_source_stage_fidelity']+=1
  stats['raw_exact_strings']+=1;originals.append({'source_id':sid,'raw_replay':r})
  # Original raw missing correct refs cannot be graded as if observed complete.
  if ':answer-field/correct' in f:add_native(native,r,'raw '+sid)
  # Each bank/profile has two generated, publicly parameterized evidence variants.
  for seed in (211,212):
   variant=g.generate(level,seed=seed,template=t,profile='raw_'+sid);displayed_math(variant);review.append(variant)
   normal_variant=g.generate(level,seed=seed,template=t);displayed_math(normal_variant);review.append(normal_variant)
 for level in fingerprints:
  for seed in range(120):
   r=g.generate(level,seed);displayed_math(r);coverage.add((r['generation']['template'],r['generation']['profile']));fingerprints[level].add(r['generation']['mathematical_fingerprint']);add_native(native,r,level+' '+str(seed))
   if seed<4:review.append(r)
   p=r['generation']['parameters'];t=r['generation']['template'];p2=dict(p)
   # Aliased whole-period shifts must share task identity, while presentation IDs differ.
   if level!='easy':
    p2['n']='1' if p['n']!='1' else '2';other=g.generate(level,template=t,parameters=p2)
    assert other['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
   repeat=g.generate(level,999,template=t,parameters=p,profile=r['generation']['profile'])
   assert repeat['question'][':question/id']==r['question'][':question/id']
   assert r['question'][':question/id']==g.uid(r['generation']['content_fingerprint'])
   assert set(repeat['knowledge_point'])=={'db_id','id','title'}
 for bad in [dict(v='0'),dict(v='1'),dict(v='2',n=1),dict(v='sqrt(17)'),dict(v='sqrt(8)'),dict(v='19/6')]:
  try:g.generate('easy',parameters=bad)
  except ValueError:pass
  else:raise AssertionError(('scope guard failed',bad))
 for level,p in [('moderate',dict(v='3',n=0)),('hard',dict(v='3',n=2,a=1,b=4)),('hard',dict(v='3',n=2,a=-7,b=4)),('hard',dict(v='sqrt(5)',n=2,a=3,b=4))]:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('level boundary admitted')
 for t in ('hard_integer','hard_rational'):
  p=dict(v='-5' if t.endswith('integer') else '-17/6',n=-12,a=-6,b=-9)
  displayed_math(g.generate('hard',template=t,parameters=p))
 assert coverage=={(t,g.profile_for(t)) for t in g.TEMPLATES if not t.startswith('legacy')}
 # Every public named-angle alias must render a single mathematical variable.
 alias_checks=0
 for level,template,p in [('easy','easy_integer',{'v':'3','n':0,'a':1,'b':0}),('moderate','moderate_periodic',{'v':'3','n':2,'a':1,'b':0}),('hard','hard_integer',{'v':'3','n':-2,'a':2,'b':1})]:
  for var in ('a','x','t','theta'):
   r=g.generate(level,template=template,parameters={**p,'variable':var})
   displayed_math(r)
   if var=='theta':
    assert r'\theta' in r['question'][':question/problem']
    assert 'theta' not in r['question'][':question/problem'].replace(r'\theta','')
    assert 'theta' not in r['question'][':question/worked-solution'].replace(r'\theta','')
   add_native(native,r,'named variable '+var+' '+level)
   alias_checks+=1
 stats['public_named_variable_checks']=alias_checks
 # Enumerate meaningful scalar values; shifts and variable letters do not inflate counts.
 values=set([sp.Integer(i)*sign for i in range(2,13) for sign in (-1,1)])
 values|={sp.Rational(n,d)*sign for d in range(2,7) for n in range(d+1,18) if sp.Rational(n,d).q!=1 for sign in (-1,1)}
 radicals={sp.sqrt(n)*sign for n in (2,3,5,6,7,10,11,13) for sign in (-1,1)}
 easy=len(values|radicals);moderate=easy
 hard=0
 for v,a,b in itertools.product(values,range(2,7),list(range(-9,0))+list(range(1,10))):
  try:g.bank('outer_operations',{'v':v,'a':sp.Integer(a),'b':sp.Integer(b),'n':sp.Integer(1)})
  except ValueError:continue
  hard+=1
 stats.update({'normal_instances_checked':360,'native_records':len(native),'native_checks':sum(len(n['checks']) for n in native),'coverage':[list(x) for x in sorted(coverage)],'sample_distinct_mathematical_tasks':{l:len(v) for l,v in fingerprints.items()},'enumerated_sampler_tasks':{'easy':easy,'moderate':moderate,'hard':hard},'missing_observed_correct_refs':2,'missing_observed_difficulty':2,'missing_observed_solutions':2,'authored_moderate':True,'plots':'unchanged inspected source raster','python':sys.version.split()[0],'sympy':sp.__version__})
 (P/'native-input.json').write_text(json.dumps(native,ensure_ascii=False,indent=2))
 engine=P.parents[1]/'runs/current/check-engine';result=subprocess.run([str(engine),str(P/'native-input.json'),str(P/'native-report.json')],capture_output=True,text=True)
 assert result.returncode==0,(result.stdout,result.stderr)
 stats['native_engine_sha256']=hashlib.sha256(engine.read_bytes()).hexdigest();stats['native_exit_code']=result.returncode
 stats['limitations']=['Two raw captures lack observed correct refs/difficulty/solution; inferred normal answers are not observed designations.','Hard historical numeric banks and rational subtract-unit bank have unresolved error intent and remain evidence-only.','Radio fields have no typed equivalent-entry interface; blank equivalents are inapplicable.','Whole-period shifts and variable-letter aliases are excluded from mathematical variety counts.']
 stats['passed']=True
 (P/'validation.json').write_text(json.dumps(stats,indent=2));(P/'review.json').write_text(json.dumps({'originals':originals,'generated':review},ensure_ascii=False,indent=2))
 lines=['# Cosecant oddness review','Original raw evidence retains missing attributes. Generated evidence profiles are not eligible for learning. Normal variants retain source-shaped solutions with authored method banks.']
 for entry in originals:
  lines+=['\n## Original '+entry['source_id'],g.markdown(entry['raw_replay'])]
 for i,r in enumerate(review):lines+=['\n## Generated '+str(i+1)+' — '+r['generation']['template']+' / '+r['generation']['profile']+(' (evidence only)' if r['generation']['evidence_only'] else ' (normal)'),g.markdown(r)]
 (P/'review.md').write_text('\n\n'.join(lines));print(json.dumps(stats,indent=2))

def add_native(out,r,label):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 out.append({'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'actual radio ID grading, independently verified displayed scalar'} for a in f[':answer-field/choices']]})
if __name__=='__main__':main()
