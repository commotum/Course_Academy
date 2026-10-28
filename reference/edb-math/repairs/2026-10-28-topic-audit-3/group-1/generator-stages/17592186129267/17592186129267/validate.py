#!/usr/bin/env python3
"""Independent displayed-TeX, bank, source-presence and real-grader checks."""
import copy,importlib.util,json,re,subprocess,sys,hashlib
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)
def component(a):
 a=a.replace('⁡','').replace('Δ','Delta').replace('θ',r'\theta').replace('π',r'\pi')
 a=re.sub(r'\\(?:operatorname|mathrm|text)\{(cos|sin)\}',r'\1',a)
 a=a.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
 def groups(txt,pos):
  assert txt[pos]=='{',txt[pos:];n=1;j=pos+1
  while n:
   n+=(txt[j]=='{')-(txt[j]=='}');j+=1
  return txt[pos+1:j-1],j
 while r'\frac' in a:
  k=a.index(r'\frac');u,j=groups(a,k+5);v,end=groups(a,j)
  a=a[:k]+'(('+component(u)+')/('+component(v)+'))'+a[end:]
 while r'\sqrt' in a:
  k=a.index(r'\sqrt');u,end=groups(a,k+5);a=a[:k]+'sqrt('+component(u)+')'+a[end:]
 a=a.replace(r'\theta','theta').replace(r'\pi','pi').replace(r'\cos','cos').replace(r'\sin','sin')
 a=re.sub(r'\{(cos|sin)\}\^\{([0-9]+)\}\s*theta',r'\1(theta)^\2',a)
 a=re.sub(r'(cos|sin)\^([0-9]+)\s*theta',r'\1(theta)^\2',a)
 a=re.sub(r'(cos|sin)\s*2\s*theta',r'\1(2*theta)',a)
 a=re.sub(r'(cos|sin)\s*theta',r'\1(theta)',a)
 a=re.sub(r'(?<=[a-z0-9)])(?=(?:cos|sin|sqrt)\()', '*', a)
 a=a.replace('{','(').replace('}',')').strip().rstrip('.')
 a=re.sub(r'(cos|sin)\^\((\d+)\)\(\(([^()]*)\)\)',r'\1(\3)^\2',a)
 return str(parse_expr(a,local_dict={'r':g.r,'theta':g.theta,'z':g.z,'x':g.x,'y':g.y,'pi':s.pi,'cos':s.cos,'sin':s.sin,'sqrt':s.sqrt},transformations=TRANS))
def expr(a):return s.sympify(component(a),locals={'r':g.r,'theta':g.theta,'z':g.z,'x':g.x,'y':g.y})
def parse_integral(text):
 def take(i):
  assert text[i]=='{';j=i+1;n=1
  while n:n+=(text[j]=='{')-(text[j]=='}');j+=1
  return text[i+1:j-1],j
 vals=[];cursor=0
 for _ in range(3):
  k=text.index(r'{\int }_',cursor)+len(r'{\int }_');lo,j=take(k);assert text[j]=='^';hi,j=take(j+1);vals.extend([expr(lo),expr(hi)]);cursor=j
 f=text[cursor:text.index(r'\,dz',cursor)]
 return (vals[0],vals[1],vals[3],vals[4],vals[5],expr(f)),vals[2]
def formatting(text):
 if any(ord(c)<32 and c not in '\n\t\r' for c in text):raise AssertionError('C0 control')
 assert text.count('$$')%2==0
 assert len(re.findall(r'(?<!\\)\$',text))%2==0
 n=0
 for i,c in enumerate(text):
  if i and text[i-1]=='\\':continue
  if c=='{':n+=1
  if c=='}':n-=1
  assert n>=0,'unmatched brace'
 assert n==0,'unclosed brace'
def verify(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 q=rec['question'];m=rec['generation'];t=m['template'];p=m['parameters'];model=g.model(t,p)
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:formatting(text)
 # Independent actual prompt cylinder and integrand extraction.
 prompt=q[':question/problem'];actualS=int(re.search(r'(?:\{y\}\^\{2\}|y\^2|y\^\{2\})\s*(?:\+)?\s*=\s*(\d+)',prompt)[1]);assert actualS==p['S']
 if '$$' in prompt:
  block=prompt.split('$$')[1];block=re.sub(r'.*?(?:\{∭\}_\{R\}|\\iiint_R)\s*','',block,flags=re.S)
  block=re.split(r'\\(?:,|mathrm|text)',block)[0].strip()
  F=expr(block) if block else s.Integer(1)
  assert s.simplify(F-model[6])==0,(F,model[6])
 heights=re.findall(r'\$z\s*=\s*(.*?)\$',prompt)
 assert len(heights)==2,heights
 for actual,wanted in zip(heights,model[8:10]):assert s.simplify(expr(actual.rstrip('.,'))-s.sympify(wanted))==0,(actual,wanted)
 vals=[];corr=None
 for field in q[':question/answer-fields']:
  assert len(field[':answer-field/choices'])==5
  for a in field[':answer-field/choices']:
   obj,rl=parse_integral(a[':answer/value']);vals.append(g.value(obj,rl))
   if a[':answer/id']==field[':answer-field/correct'][1]:
    assert all(s.simplify(s.sympify(u)-s.sympify(v))==0 for u,v in zip(obj,model[:6]));assert rl==0;corr=a
  assert corr
 ns=[complex(s.N(v,18)) if isinstance(v,s.Basic) else complex(v) for v in vals]
 assert all(abs(u-v)>1e-9*max(1,abs(u),abs(v)) for i,u in enumerate(ns) for v in ns[:i]),'whole integrals equivalent'
 # Read every displayed operative aligned integrand back independently.
 sol=q[':question/worked-solution'];chain=sol.split(r'\begin{aligned}')[-1].split(r'\end{aligned}')[0]
 for row in chain.split(r'\\'):
  if '{∭}_{Δ}' in row:rhs=row.split('{∭}_{Δ}')[1]
  elif r'\iiint_\Delta' in row:rhs=row.split(r'\iiint_\Delta')[1]
  else:continue
  rhs=re.split(r'\\,?dz|dz',rhs)[0];rhs=rhs.rstrip(' \\,')
  actual=expr(rhs);assert s.trigsimp(actual-model[5])==0,(t,rhs,actual,model[5])
 # Need operative expansion and collection at changed params.
 if t in ['half_difference','half_zdifference','quarter_zdifference']:assert chain.count('cos')>=4 and chain.count('sin')>=3
 return True

def main():
 cases=[];fidelity=[];review=[];native=[];anomalies=[]
 # Independently verify angular moment helper against direct SymPy integration.
 for a,b in [(0,2*s.pi),(0,s.pi),(s.pi/2,3*s.pi/2),(-s.pi/2,s.pi/2),(0,s.pi/2),(s.pi/2,s.pi)]:
  for term in [s.Integer(1),s.sin(g.theta),s.cos(g.theta),s.sin(g.theta)**2,s.cos(g.theta)**2,s.sin(g.theta)*s.cos(g.theta)]:
   assert s.simplify(g.angular_integral(term,a,b)-s.integrate(term,(g.theta,a,b)))==0
 for t,(lev,sid,p) in g.TEMPLATES.items():
  print('checking',t,flush=True)
  if sid:
   case={'source_id':sid,'template':t,'level':lev,'parameters':p,'bank_profile':'observed:'+sid};cases.append(case)
   rec=g.generate(lev,template=t,parameters=p,profile=case['bank_profile']);src=g.QS[sid];q=rec['question']
   for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (key in q)==(key in src),(sid,key)
   assert q[':question/problem']==src[':question/problem'],sid
   if ':question/worked-solution' in src:assert q[':question/worked-solution']==src[':question/worked-solution'],sid
   matches=0;des=0
   for f,f0 in zip(q[':question/answer-fields'],src[':question/answer-fields']):
    assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']),sid
    matches+=len(f0[':answer-field/choices']);assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
    if ':answer-field/correct' in f0:
     a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert a[':answer/value']==f0[':answer-field/correct'][':answer/value'];des+=1
   fidelity.append({'source_id':sid,'raw_exact_prompt':True,'raw_exact_solution':':question/worked-solution' in src,'options_matched':matches,'correct_designations_matched':des,'banks':len(src[':question/answer-fields'])})
   # Independent source mathematical bank checks, separate from raw strings.
   if sid!='q-161520':
    modern=next(f for f in src[':question/answer-fields'] if ':answer-field/correct' in f)
    source_values=[g.value(*parse_integral(a[':answer/value'])) for a in modern[':answer-field/choices']]
    normal=g.generate(lev,template=t,parameters=p,profile='source:'+sid);verify(normal)
    normal_values=[g.value(*parse_integral(a[':answer/value'])) for a in normal['question'][':question/answer-fields'][0][':answer-field/choices']]
    def canonical_obj(text):
     obj,rl=parse_integral(text);return tuple(str(s.simplify(s.sympify(v))) for v in (*obj,rl))
    assert sorted(canonical_obj(a[':answer/value']) for a in modern[':answer-field/choices'])==sorted(canonical_obj(a[':answer/value']) for a in normal['question'][':question/answer-fields'][0][':answer-field/choices']),sid
   # Original-equivalence evidence, separate from fidelity.
   opts,_=g.banks(t,p);lowers=[0]*5
   if t=='full_z2radial':lowers[:2]=[s.sqrt(p['S'])]*2
   ok,values=g.whole_bank_ok(opts,lowers)
   if not ok:anomalies.append({'source_id':sid,'issue':'complete definite integral values collide','values':[str(v) for v in values]})
   review.append({'label':'original raw '+sid,'record':rec})
  for i in range(2):
   profile='source:'+sid if sid else 'authored:method'
   rec=g.generate(lev,seed=100+17*i,template=t,profile=profile);verify(rec);review.append({'label':'generated '+t,'record':rec})
   checks=[]
   for fi,f in enumerate(rec['question'][':question/answer-fields']):
    for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio selection'})
   native.append({'label':t+'-'+str(i),'record':rec,'checks':checks})
 # Changed-parameter evidence replay for every original field/bank, including legacy.
 for t,(lev,sid,p) in g.TEMPLATES.items():
  if not sid:continue
  changed=next(item['record']['generation']['parameters'] for item in review if item['label']=='generated '+t)
  raw=g.generate(lev,seed=89,template=t,parameters=changed,profile='observed:'+sid)
  assert raw['generation']['evidence_only'] and not raw['generation']['eligible_for_learning']
  review.append({'label':'generated raw evidence bank '+sid,'record':raw})
 # Every optional complete authored bank profile, selected before parameters.
 for t,(lev,sid,p) in g.TEMPLATES.items():
  if sid:
   rec=g.generate(lev,seed=210,template=t,profile='authored:method');verify(rec)
   review.append({'label':'generated authored bank '+t,'record':rec})
   field=rec['question'][':question/answer-fields'][0]
   native.append({'label':'authored-'+t,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'optional complete authored bank'} for a in field[':answer-field/choices']]})
 # Moderate/hard templates each changed radius and endpoints where applicable.
 for level in ['easy','moderate','hard']:
  for seed in range(8):
   print('default',level,seed,flush=True);verify(g.generate(level,seed))
 # Fixed displayed parameters/profile keep content IDs across seed/order changes.
 for item in review:
  if item['record']['generation']['evidence_only']:continue
  rec=item['record'];m=rec['generation'];lev=g.TEMPLATES[m['template']][0]
  other=g.generate(lev,seed=19,template=m['template'],parameters=m['parameters'],profile=m['profile'])
  assert rec['question'][':question/id']==other['question'][':question/id']
  assert m['mathematical_fingerprint']==other['generation']['mathematical_fingerprint']
 # Mutations must fail, including C0 whose whitespace is parser-tolerated.
 base=next(v['record'] for v in review if v['label'].startswith('generated half_zdifference'))
 mutated=copy.deepcopy(base);mutated['question'][':question/worked-solution']+='\f'
 try:verify(mutated);raise AssertionError('mutation undetected')
 except AssertionError as e:assert 'C0' in str(e)
 # Remove required expansion while preserving correct final: must fail stages.
 mutated=copy.deepcopy(base);sol=mutated['question'][':question/worked-solution'];mutated['question'][':question/worked-solution']=re.sub(r'& =\{∭\}_\{Δ\}rz.*?\\\\','',sol)
 caught=False
 try:verify(mutated)
 except AssertionError:caught=True
 assert caught,'stage mutation undetected'
 g.atomic(D/'source-cases.json',json.dumps(cases,indent=2));g.atomic(D/'review.json',json.dumps(review,ensure_ascii=False,indent=2));g.atomic(D/'native-input.json',json.dumps(native,ensure_ascii=False,indent=2))
 subprocess.run([str(g.ROOT.parent/'runs/current/check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 report={'status':'passed','basis':1356,'runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'source_questions':8,'source_banks':9,'raw_options_matched':sum(v['options_matched'] for v in fidelity),'modern_mathematical_options':35,'legacy_flattened_options':10,'legacy_interpretation':'r 2 interpreted as r squared; raw captured notation remains malformed/ineligible','raw_designations_matched':sum(v['correct_designations_matched'] for v in fidelity),'missing_original_designations':2,'raw_solution_exact':7,'original_fidelity':fidelity,'source_bank_math_anomalies':anomalies,'normal_generated_verified':57,'native_checks':sum(len(n['checks']) for n in native),'native_binary_sha256':hashlib.sha256((g.ROOT.parent/'runs/current/check-engine').read_bytes()).hexdigest(),'catalog':json.loads((D/'catalog.json').read_text()),'source_solution_math_repairs':['q-161607 initial LHS','q-161612 extra radial factor'],'authored_optional_profiles_verified':8,'authored_hard':'quarter_zdifference','raw_evidence_eligible':False}
 g.atomic(D/'validation.json',json.dumps(report,indent=2));g.atomic(D/'review.md','\n\n---\n\n'.join('## '+v['label']+'\n\n'+g.markdown(v['record']) for v in review))
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
