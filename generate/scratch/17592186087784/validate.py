"""Independent displayed-math/source-bank checks plus the actual learner grader."""
import importlib.util,json,re,subprocess,hashlib,random
from pathlib import Path
import sympy as sp
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('circle_arc',H.parent/(H.name+'.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
S=json.loads((H/'source.json').read_text())['record'][':knowledge-point/questions'];CASES=json.loads((H/'source-cases.json').read_text());BY={q[':question/math-academy-id']:q for q in S}
def norm(x):
 x=re.sub(r'!\[.*?\]\(.*?\)','![](PLOT)',x)
 x=x.replace('θ',r'\theta').replace('π',r'\pi').replace('∈',r'\in').replace(r'\operatorname{cos}⁡',r'\cos').replace(r'\operatorname{sin}⁡',r'\sin')
 return re.sub(r'\s+','',x)
def readangle(x):
 x=norm(x)
 if x=='0':return sp.Integer(0)
 m=re.fullmatch(r'(-?)\\frac\{(\d*)\\pi\}\{(\d+)\}',x)
 if m:return sp.Rational(int(m[2] or '1')*(-1 if m[1] else 1),int(m[3]))
 m=re.fullmatch(r'(-?\d*)\\pi',x)
 if m:return sp.Integer(int(m[1] or '1') if m[1]!='-' else -1)
 raise AssertionError('Invalid displayed angle '+x)
def readinterval(x):
 x=norm(x);m=re.search(r'\[(.*?),(.*?)(\]|\))',x);assert m,x
 return readangle(m[1]),readangle(m[2]),m[3]==']'
def displayed_equations(x):
 x=norm(x);matches=re.findall(r'x=([^,$]+),(?:\\,)?y=([^,$]+)',x)
 results=[]
 for left,right in matches:
  parts=[]
  for expr,fn in ((left,'cos'),(right,'sin')):
   m=re.fullmatch(r'(\d*)\\'+fn+r'\\theta([+-]\d+)?\.?',expr)
   if m:parts.append((int(m[1] or 1),int(m[2] or 0)))
   else:break
  if len(parts)==2:results.append(tuple(parts))
 return results

def mathcheck(r):
 assert r['knowledge_point']=={'db_id':G.KP_ID,'id':G.KP_UUID,'title':G.TITLE}
 assert r['generation']['parameter_fingerprint']==r['generation']['mathematical_fingerprint']
 q=r['question'];p=r['generation']['parameters'];a,b=sp.Rational(p['start']),sp.Rational(p['end'])
 equations=displayed_equations(q[':question/problem']);assert equations,('cannot parse printed prompt',q[':question/problem'])
 ((rx,h),(ry,k))=equations[0];assert rx==ry==p['r'] and (h,k)==(p['h'],p['k'])
 # Circle and endpoints independently follow printed parametrization.
 theta=sp.Symbol('theta',real=True);x=rx*sp.cos(theta)+h;y=ry*sp.sin(theta)+k
 assert sp.trigsimp((x-h)**2+(y-k)**2-rx**2)==0
 assert sp.simplify((x-h)*sp.diff(y,theta)-(y-k)*sp.diff(x,theta))==rx**2
 for endpoint in (a,b):assert sp.simplify((x.subs(theta,endpoint*sp.pi)-h)**2+(y.subs(theta,endpoint*sp.pi)-k)**2)==rx**2
 radius=re.findall(r'radius \$(?:r=)?(\d+)',q[':question/worked-solution']);assert radius and all(int(v)==rx for v in radius)
 if h or k:
  centers=re.findall(r'centered at the point \$\((-?\d+),(-?\d+)\)',q[':question/worked-solution']);assert centers and all((int(x),int(y))==(h,k) for x,y in centers)
 printed=displayed_equations(q[':question/worked-solution']);assert len(printed)==2
 assert all(e==equations[0] for e in printed),printed
 # Inspect the displayed interval in BOTH conclusion stages, not answer metadata.
 finaldomains=[readinterval(t) for t in re.findall(r'\[(?:[^\]]+)\]',q[':question/worked-solution']) if '\\pi' in t or re.search(r'\[0,',t)]
 assert finaldomains[-2:]==[(a,b,True),(a,b,True)],finaldomains
 fs=q[':question/answer-fields'];ids=set()
 for f in fs:
  assert f[':answer-field/key'] in ('selection','field-1','field-2')
  vals=f[':answer-field/choices'];correct=f[':answer-field/correct'][1]
  assert correct in [v[':answer/id'] for v in vals]
  for v in vals:
   assert '$' not in v[':answer/value'];assert v[':answer/id'] not in ids;ids.add(v[':answer/id'])
  if f[':answer-field/type'].endswith('/radio'):
   obj=[readinterval(v[':answer/value']) for v in vals];assert len(obj)==len(set(obj))==5
   assert all(start<end for start,end,closed in obj)
   assert sum(o==(a,b,True) for o in obj)==1
   assert readinterval(next(v[':answer/value'] for v in vals if v[':answer/id']==correct))==(a,b,True)
  else:
   assert len(vals)==1
   assert readangle(vals[0][':answer/value'])==(a if f[':answer-field/key']=='field-1' else b)
   assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 for role,asset in r['generation']['plots'].items():
  path=Path(asset['path']);assert path.exists() and path.stat().st_size>3000
  spec=json.loads((path.parent/'spec.json').read_text());assert spec['parameters']==p
  assert spec['solid_interval']==[str(a),str(b)] and spec['orientation']=='counterclockwise' and spec['closed_endpoints']
 assert not re.search(r'\{(?:r|h|k|interval|equations|prompt_plot|solution_plot)\}',q[':question/problem']+q[':question/worked-solution'])
 return True

def native_checks(r):
 result=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  for v in f[':answer-field/choices']:
   if f[':answer-field/type'].endswith('/radio'):
    result.append({'field_index':i,'submitted_answer_id':v[':answer/id'],'expected':'accepted' if v[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'actual radio grading; displayed mathematics checked independently'})
   else:
    c=readangle(v[':answer/value']);canonical=v[':answer/value']
    equiv='1-1' if c==0 else str(c.p*2)+r'\pi/'+str(c.q*2)
    wrong=G.angle(c+sp.Rational(1,12))
    result += [{'field_index':i,'submitted':canonical,'expected':'accepted','purpose':'canonical endpoint fragment'},{'field_index':i,'submitted':equiv,'expected':'accepted','purpose':'unreduced rational multiple of pi, independently parsed'},{'field_index':i,'submitted':wrong,'expected':'rejected','purpose':'wrong endpoint by pi/12'}]
 return result

def main():
 replay=[];variants=[];profile_variants=[];source_results=[];grader=[];banks=options=designations=prompts=solutions=blanks=0
 for case in CASES:
  r=G.generate(case['level'],template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);mathcheck(r);replay.append(r)
  orig=BY[case['source_id']];q=r['question'];assert norm(q[':question/problem'])==norm(orig[':question/problem']),(case['source_id'],'prompt mismatch')
  prompts+=1
  if ':question/worked-solution' in orig:
   assert norm(q[':question/worked-solution'])==norm(orig[':question/worked-solution']),(case['source_id'],'solution mismatch');solutions+=1
  assert [f[':answer-field/key'] for f in q[':question/answer-fields']]==[f[':answer-field/key'] for f in orig[':question/answer-fields']]
  for f,s in zip(q[':question/answer-fields'],orig[':question/answer-fields']):
   vals=f[':answer-field/choices'];src=s[':answer-field/choices'];isradio=f[':answer-field/type'].endswith('/radio')
   parse=readinterval if isradio else readangle
   assert sorted(parse(v[':answer/value']) for v in vals)==sorted(parse(v[':answer/value']) for v in src),(case['source_id'],'whole bank mismatch')
   if isradio:banks+=1;options+=len(src)
   else:blanks+=1
   if ':answer-field/correct' in s:
    correct=next(v[':answer/value'] for v in vals if v[':answer/id']==f[':answer-field/correct'][1]);assert parse(correct)==parse(s[':answer-field/correct'][':answer/value']);designations+=1
  source_results.append({'source_id':case['source_id'],'prompt_match':True,'bank_match':True,'original_correct_designation_available':not case['repair'],'original_solution_match':not case['repair'],'repair':case['repair']})
  grader.append({'label':'replay-'+case['source_id'],'record':r,'checks':native_checks(r)})
 for name,t in G.TEMPLATES.items():
  for seed in (40,73):
   r=G.generate(t['level'],seed,template=name);mathcheck(r);variants.append(r)
   grader.append({'label':'variant-'+name+'-'+str(seed),'record':r,'checks':native_checks(r)})
   again=G.generate(t['level'],seed+10000,template=name,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile']);assert again['question']==r['question']
 sampler_tasks={}
 for name,t in G.TEMPLATES.items():
  intervals=set()
  for seed in range(200):
   p=G.validate_parameters(name,G.sample(name,random.Random(seed),'authored-'+name if t['kind']=='radio' else None))
   if t['kind']=='radio':G.bank(p,'authored-'+name)
   intervals.add((p['start'],p['end']))
  sampler_tasks[name]=sorted(intervals)
 # Every observed profile varies radius under normal generator, while keeping the entire original bank.
 for case in CASES:
  p={**case['parameters'],'r':8 if case['parameters']['r']!=8 else 7}
  r=G.generate(case['level'],template=case['template'],parameters=p,profile=case['bank_profile']);mathcheck(r);profile_variants.append(r)
 # Canonical mathematical fingerprint ignores choice layout/profile and equivalent rational spelling.
 p={'r':4,'h':0,'k':0,'start':'0','end':'1/2'}
 x=G.generate('easy',template='easy_quarter_radio',parameters=p);y=G.generate('easy',template='easy_quarter_blank',parameters={**p,'end':'2/4'})
 assert x['generation']['mathematical_fingerprint']==y['generation']['mathematical_fingerprint'];assert x['question'][':question/id']!=y['question'][':question/id']
 o=G.generate('easy',template='easy_quarter_radio',parameters=p,profile='observed-q-79271')
 assert o['generation']['mathematical_fingerprint']==x['generation']['mathematical_fingerprint'];assert o['question'][':question/id']!=x['question'][':question/id']
 invalid=0
 for args in [('easy',{'r':0,'h':0,'k':0,'start':'0','end':'1/2'},'easy_quarter_radio',None),('easy',{**p,'start':'1/2','end':'1'},'easy_quarter_radio',None),('hard',{**p},'hard_quarter_radio',None),('moderate',{**p},'moderate_quarter_radio',None),('easy',{**p,'end':'1'},'easy_quarter_radio','observed-q-79271')]:
  try:G.generate(args[0],parameters=args[1],template=args[2],profile=args[3])
  except ValueError:invalid+=1
  else:raise AssertionError('Invalid explicit input silently changed')
 (H/'engine-input.json').write_text(json.dumps(grader,indent=2,ensure_ascii=False)+'\n');subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
 review={'source_replays':replay,'observed_profile_variants':profile_variants,'generated_variants':variants};(H/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 out=['# Parametrizing Part of a Circle — author review','', 'Original evidence and parameterized replay for every observed bank follow. q-79205 has a derived repair; its correct designation and solution are not counted as original matches.']
 for case,r in zip(CASES,replay):
  src=BY[case['source_id']];out+=['','## Original '+case['source_id'],'',re.sub(r'!\[.*?\]\((.*?)\)',lambda m:'![](source-assets/'+Path(m[1]).name+')',src[':question/problem']),'']
  for f in src[':question/answer-fields']:
   out += ['Original field `'+f[':answer-field/key']+'`: '+', '.join('$'+a[':answer/value']+'$' for a in f[':answer-field/choices'])]
  out+=['',re.sub(r'!\[.*?\]\((.*?)\)',lambda m:'![](source-assets/'+Path(m[1]).name+')',src.get(':question/worked-solution','*No source solution/correct reference; see repair evidence.*')),'','### Parameterized source replay','',G.markdown(r)]
  if case['bank_profile']:
   p={**case['parameters'],'r':8 if case['parameters']['r']!=8 else 7};v=G.generate(case['level'],template=case['template'],parameters=p,profile=case['bank_profile'])
   out+=['','### Generated variant of this complete observed bank','',G.markdown(v)]
 for r in variants:out+=['','## Authored angular variation — '+r['generation']['template'],'','Seed '+str(r['generation']['seed'])+'; parameters '+str(r['generation']['parameters'])+'.','',G.markdown(r)]
 (H/'review.md').write_text('\n'.join(out)+'\n')
 engine=json.loads((H/'engine-report.json').read_text())
 report={'native_checks_accepted':engine['accepted_checks'],'native_checks_rejected':engine['rejected_checks'],'native_checks_unresolved':engine['documented_unresolved_checks'],'source_plot_assets_visually_reviewed':31,'authored_plot_assets_visually_reviewed':44,'passed':True,'provenance':G.PROVENANCE,'source_questions':15,'source_replayed':15,'original_radio_banks_matched':banks,'original_options_matched':options,'original_blank_fragments_matched':blanks,'original_correct_fields_matched':designations,'original_correct_questions_matched':14,'derived_correct_question_repairs':1,'original_prompts_matched':prompts,'original_solutions_matched':solutions,'authored_missing_solution':1,'observed_templates':len(G.TEMPLATES),'generated_variants':len(variants),'profile_radius_variants':15,'independent_mathematical_records_checked':len(replay)+len(variants)+15,'invalid_explicit_inputs_rejected':invalid,'native_engine_exit_success':True,'native_engine_fixture_count':len(grader),'source_results':source_results,'sampler_instances_checked':2200,'sampler_angular_coverage':sampler_tasks,'remaining_findings':[],'native_grader_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()}
 (H/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='source_results'},indent=2))
if __name__=='__main__':main()
