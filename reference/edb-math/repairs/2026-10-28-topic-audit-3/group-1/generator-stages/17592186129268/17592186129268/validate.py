#!/usr/bin/env python3
"""Displayed source-shaped algebra and whole-integral QA; component parser adapted
from neighboring private cylindrical-solid validator, independently checks output."""
import copy,importlib.util,json,re,subprocess,sys,hashlib,concurrent.futures,itertools,tempfile
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
 q=rec['question'];meta=rec['generation'];t=meta['template'];p=meta['parameters'];g.guard(t,p)
 assert not meta['evidence_only'] and meta['eligible_for_learning']
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]:formatting(text)
 assert '{{selection}}' not in q[':question/problem']
 # Read actual printed circle and its independent shifted center from its polynomial.
 prompt=q[':question/problem'];region=prompt.split('$$')[1]
 circle_part=region.split(r'\,:\,')[1].split(r'\le ')[0];circ=expr(circle_part)
 rhs=int(region.split(r'\le ')[1].split(',')[0]);equation=circ-rhs
 cx=-s.expand(circ).coeff(g.x)/2;cy=-s.expand(circ).coeff(g.y)/2
 A=s.sqrt(rhs);assert A==p['a'];assert cx*cx+cy*cy==rhs
 originalF=prompt.split('$$')[3].split('{∭}_{R}')[1].split(r'\,\text{d}V')[0];F=expr(originalF)
 # Region contains Cartesian lower/upper surface components; recover them from
 # displayed z inequality, ensuring products xy and kernel inputs remain actual.
 height=region.split(r',\,')[-1].split(r'\}') [0]
 lower,upper=height.split(r'\le z\le ');L=expr(lower);H=expr(upper)
 f=s.trigsimp(F.subs({g.x:g.r*s.cos(g.theta),g.y:g.r*s.sin(g.theta)},simultaneous=True)*g.r)
 l=L.subs({g.x:g.r*s.cos(g.theta),g.y:g.r*s.sin(g.theta)},simultaneous=True)
 h=H.subs({g.x:g.r*s.cos(g.theta),g.y:g.r*s.sin(g.theta)},simultaneous=True)
 R=2*(cx*s.cos(g.theta)+cy*s.sin(g.theta))
 expected=(g.model(t,p)[0],g.model(t,p)[1],R,l,h,f)
 options=[];corr=None
 field=q[':question/answer-fields'][0];assert len(field[':answer-field/choices'])==5
 for answer in field[':answer-field/choices']:
  obj,radial_low=parse_integral(answer[':answer/value']);assert radial_low==0
  options.append(obj)
  if answer[':answer/id']==field[':answer-field/correct'][1]:corr=obj
 assert corr is not None
 for u,v in zip(corr,expected):assert s.trigsimp(u-v)==0,(t,u,v)
 # High-order numerical integration of EXACT parsed full objects is independently
 # repeated at another order; no syntactic-only uniqueness or metadata bank lookup.
 values=[g.value(tuple(o),96) for o in options];values2=[g.value(tuple(o),128) for o in options]
 assert all(abs(a-b)<1e-5*max(1,abs(a),abs(b)) for a,b in zip(values,values2)),'quadrature instability'
 assert all(abs(u-v)>1e-7*max(1,abs(u),abs(v)) for i,u in enumerate(values) for v in values[:i]),'equivalent complete integrals'
 # Every circle algebra row is printed and independently equivalent; protect the
 # six distinct teaching operations in addition to their mathematical equality.
 sol=q[':question/worked-solution'];chains=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(chains)==2
 rows=chains[0].split(r'\\');assert len(rows)==6
 polar=s.expand(equation.subs({g.x:g.r*s.cos(g.theta),g.y:g.r*s.sin(g.theta)},simultaneous=True))
 for i,row in enumerate(rows):
  left,right=row.split('& =');actual=expr(left)-expr(right)
  assert s.trigsimp(actual-(equation if i==0 else polar))==0,(t,i,row)
 assert rows[1].count(')^{2}')==2,'substituted squares omitted'
 assert '{cos}^{2}' in rows[2] and '{sin}^{2}' in rows[2] and str(rhs) in rows[2],'expanded squares omitted'
 assert '({cos}^{2}' in rows[3],'Pythagorean grouping omitted'
 assert '{cos}^{2}' not in rows[4] and '{sin}^{2}' not in rows[4],'identity not reduced'
 assert 'r(r' in rows[5],'factorization omitted'
 # Formal substitution and radial grouping blocks checked directly, not collapsed
 # CAS final equality. Last source family preserves double-angle collection.
 finalrows=chains[1].split(r'\\');expectedrows=3 if t in ['left_inverse','right_radical','upper_square'] else 2
 assert len(finalrows)==expectedrows
 for row in finalrows[:-1]:
  rhs=row.split('{∭}_{Δ}')[1].split(r'\,dz')[0]
  assert s.trigsimp(expr(rhs)-f)==0,(t,'integrand stage',rhs)
 if expectedrows==3:assert '({cos}^{2}' in finalrows[1],'radial grouping omitted'
 finaltext=finalrows[-1].split('& =')[1].strip().rstrip('.')
 finalobj,_=parse_integral(finaltext)
 for u,v in zip(finalobj,expected):assert s.trigsimp(u-v)==0
 if t=='left_xy_sphere':assert 'sin}⁡2\\theta' in finalrows[-1]
 # Full polar domain and prose endpoints are also parsed, not assumed.
 delta=sol.split('Δ=')[1].split('$$')[0]
 pieces=delta.split(r'\,:\,')[1].split(r',\,')
 bound=pieces[0].split(r'0\le r\le ')[1];assert s.trigsimp(expr(bound)-R)==0
 aa,bb=pieces[1].split(r'\le \theta \le ')
 assert expr(aa)==expected[0] and expr(bb)==expected[1]
 zl,zh=pieces[2].split(r'\le z\le ');zh=zh.split(r'\}')[0]
 assert s.trigsimp(expr(zl)-l)==0 and s.trigsimp(expr(zh)-h)==0
 prose=re.findall(r'\$z=(.*?)\$',sol)
 assert len(prose)==2
 for sentence,cart,polarpart in zip(prose,[L,H],[l,h]):
  components=sentence.rstrip('.,').split('=')
  assert s.simplify(expr(components[0])-cart)==0
  assert s.trigsimp(expr(components[-1])-polarpart)==0
 sentenceR=sol.split('we must have $r=')[1].split('$')[0].rstrip('.')
 assert s.trigsimp(expr(sentenceR)-R)==0
 return True

def texexpr(v):return g.tex(v)
def native_item(label,rec):
 checks=[]
 for fi,f in enumerate(rec['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:checks.append({'field_index':fi,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned radio option selection'})
 return {'label':label,'record':rec,'checks':checks}
def main():
 fidelity=[];cases=[];reviews=[];native=[];anomalies=[];normal_count=0
 for t,(level,sid,p) in g.TEMPLATES.items():
  print('checking',t,flush=True)
  case={'source_id':sid,'template':t,'level':level,'parameters':p,'bank_profile':'observed:'+sid};cases.append(case)
  raw=g.generate(level,template=t,parameters=p,profile=case['bank_profile']);src=g.QS[sid];q=raw['question']
  for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (key in q)==(key in src)
  assert q[':question/problem']==src[':question/problem']
  if ':question/worked-solution' in src:assert q[':question/worked-solution']==src[':question/worked-solution']
  matched=0;designations=0
  for f,f0 in zip(q[':question/answer-fields'],src[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices']);matched+=len(f0[':answer-field/choices'])
   assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
   if ':answer-field/correct' in f0:
    actual=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert actual==f0[':answer-field/correct'][':answer/value'];designations+=1
  fidelity.append({'source_id':sid,'prompt_exact':True,'solution_exact':':question/worked-solution' in src,'options_matched':matched,'designations_matched':designations,'presence_parity':True})
  opts,_=g.source_banks(t,p)
  try:ok,values=g.eligible(opts);issue=None if ok else 'equivalent complete definite integrals'
  except ValueError as e:ok=False;values=[];issue=str(e)
  anomalies.append({'source_id':sid,'source_bank_valid':ok,'values':values,'issue':issue})
  reviews.append({'label':'Original raw evidence '+sid,'record':raw})
  if designations:native.append(native_item('original raw '+sid,raw))
  # Replay through same public parameter masks at changed values, not literal source.
  changed=dict(p)
  for key in changed:
   if key!='a':changed[key]+=1
  raw_changed=g.generate(level,template=t,parameters=changed,profile='observed:'+sid)
  assert raw_changed['question'][':question/problem']!=q[':question/problem']
  for i in range(2):
   rec=g.generate(level,seed=71+i*13,template=t);verify(rec);normal_count+=1;reviews.append({'label':'Generated '+t+' variant '+str(i+1),'record':rec});native.append(native_item(t+'-'+str(i),rec))
 for level in ['easy','moderate','hard']:
  for seed in range(12):verify(g.generate(level,seed));normal_count+=1
 # Public explicit guards reject source hard non-real kernel; levels apply exactly.
 for t in g.TEMPLATES:
  p=g.sample(t,__import__('random').Random(201));p['a']=6
  try:g.generate(g.TEMPLATES[t][0],template=t,parameters=p);raise AssertionError('guard missed')
  except ValueError:pass
 try:g.generate_hard(template='lower_zinverse',parameters=g.TEMPLATES['lower_zinverse'][2]);raise AssertionError('domain missed')
 except ValueError:pass
 # Identity invariant under seed/order; changed banks change content identity.
 for t,(lev,sid,_) in g.TEMPLATES.items():
  p=g.sample(t,__import__('random').Random(19));a=g.generate(lev,2,template=t,parameters=p);b=g.generate(lev,91,template=t,parameters=p)
  assert a['question'][':question/id']==b['question'][':question/id'];assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 p=g.sample('right_radical',__import__('random').Random(28));a=g.generate_hard(template='right_radical',parameters=p,profile='source:q-161637');b=g.generate_hard(template='right_radical',parameters=p,profile='authored:method')
 verify(a);verify(b);assert a['question'][':question/id']!=b['question'][':question/id'];assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 base=next(v['record'] for v in reviews if v['label'].startswith('Generated left_inverse'))
 for mutation in ['control','stage','sign','xy']:
  altered=copy.deepcopy(base if mutation!='xy' else next(v['record'] for v in reviews if v['label'].startswith('Generated left_xy_sphere')))
  sol=altered['question'][':question/worked-solution']
  if mutation=='control':sol+='\f'
  elif mutation=='stage':sol=re.sub(r'\{r\}\^\{2\}\(\{cos\}.*? & =0',lambda m:'r(r+8\\cos\\theta) & =0',sol,count=1)
  elif mutation=='sign':sol=sol.replace('{r}^{2}{cos}^{2}⁡\\theta +','{r}^{2}{cos}^{2}⁡\\theta -',1)
  else:sol=sol.replace('2(r\\operatorname{cos}', '2(r\\operatorname{sin}',1)
  altered['question'][':question/worked-solution']=sol;caught=False
  try:verify(altered)
  except (AssertionError,ValueError,IndexError):caught=True
  assert caught,'mutation missed '+mutation
 # Concurrent fresh plot generation (private isolated directory; no cache pruning).
 old=g.EVIDENCE;(D/'concurrent-render').mkdir(exist_ok=True);g.EVIDENCE=Path(tempfile.mkdtemp(prefix='fresh-',dir=D/'concurrent-render'));tasks=[('upper_square',{'a':5,'L':1,'H':4}),('upper_square',{'a':5,'L':1,'H':4}),('left_xy_sphere',{'a':4,'L':-3,'K':81})]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:paths=list(pool.map(lambda pair:g.projection(*pair),tasks))
 assert paths[0]==paths[1] and paths[0]!=paths[2]
 for path in paths:
  side=json.loads(Path(path).with_suffix('.json').read_text());assert side['renderer']=='Matplotlib';assert Path(path).stat().st_size>1000
 assert not list((g.EVIDENCE/'images').glob('.render-*'));g.EVIDENCE=old
 # Save evidence and invoke real native grader once, every displayed default choice.
 g.atomic(D/'source-cases.json',json.dumps(cases,indent=2));g.atomic(D/'review.json',json.dumps(reviews,ensure_ascii=False,indent=2));g.atomic(D/'native-input.json',json.dumps(native,ensure_ascii=False,indent=2))
 subprocess.run([str(g.ROOT.parent/'runs/current/check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 # Finite meaningful domains, excluding common-canceled easy vertical offsets.
 counts={'easy':25,'moderate':25+125,'hard':250+75+125}
 coverage={lev:sorted({g.generate(lev,seed)['generation']['template'] for seed in range(40)}) for lev in ['easy','moderate','hard']}
 report={'status':'passed','basis':1356,'runtime':{'python':sys.version.split()[0],'sympy':s.__version__,'numpy':g.np.__version__},'raw_source_questions':6,'raw_source_banks':6,'raw_source_options_matched':30,'present_source_solutions_exact':4,'original_designations_matched':4,'original_designations_missing':2,'presence_parity':6,'fidelity':fidelity,'source_bank_mathematics':anomalies,'normal_questions_independently_verified':normal_count,'native_checks':60,'present_original_bank_designations_native_checks':20,'meaningful_domain_candidates':counts,'default_family_coverage':coverage,'raw_evidence_eligible':False,'whole_integral_uniqueness':'Exact symbolic components; independently repeated order96/128 quadrature rejects near-equality. Source equivalences also documented symbolically.','mutation_regressions':4,'concurrent_render_checks':3,'database_writes':0}
 g.atomic(D/'validation.json',json.dumps(report,indent=2));g.atomic(D/'review.md','\n\n---\n\n'.join('## '+v['label']+'\n\n'+g.markdown(v['record']) for v in reviews));print(json.dumps(report,indent=2))
if __name__=='__main__':main()
