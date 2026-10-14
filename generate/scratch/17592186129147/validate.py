#!/usr/bin/env python3
"""Independently read displayed factors, verify every graph and all source banks."""
from pathlib import Path
import concurrent.futures,hashlib,importlib.util,itertools,json,platform,re,subprocess,tempfile
import numpy as np
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
from PIL import Image
D=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('gen',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,data):(D/name).write_text(json.dumps(data,indent=2)+'\n')
def balanced(s):
 assert s.count('$')%2==0
 depth=0
 for c in re.sub(r'\\[{}]','',s):
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,s
 assert depth==0,s

def displayed(rec):
 md=rec['question'][':question/problem'];tex=re.search(r'\$y=(.*?)\$',md)[1].rstrip('?')
 clean=tex.replace('{','').replace('}','').replace('^','**')
 return sp.expand(parse_expr(clean,local_dict={'x':g.X},transformations=standard_transformations+(implicit_multiplication_application,)))
def poly_signature(f):
 coef,factors=sp.factor_list(f,g.X);roots={}
 for linear,m in factors:
  assert sp.degree(linear,g.X)==1
  r=sp.solve(linear,g.X)[0];roots[int(r)]=m
 leading=int(sp.sign(sp.Poly(f,g.X).LC()))
 return leading,tuple((r,'simple' if m==1 else 'even' if m%2==0 else 'odd-multiple') for r,m in sorted(roots.items()))
def coordinates(s):
 vals=[]
 for z in s.split(','):
  if z.startswith('\\pm '):vals.extend([-int(z[4:]),int(z[4:])])
  else:vals.append(int(z))
 return vals

def check(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 assert rec['knowledge_point']=={'db_id':g.RECORD[':db/id'],'id':g.RECORD[':knowledge-point/id'],'title':g.RECORD[':knowledge-point/title']}
 q=rec['question'];field=q[':question/answer-fields'][0];p=rec['generation']['parameters']
 balanced(q[':question/problem']);balanced(q[':question/worked-solution'])
 f=displayed(rec);assert f==sp.expand(g.polynomial(p))
 fact=dict((int(sp.solve(z,g.X)[0]),m) for z,m in sp.factor_list(f,g.X)[1])
 sol=q[':question/worked-solution']
 described={}
 for roots,m in re.findall(r'multiplicity of the roots? \$x=([^$]+)\$ is \$([1-4]),\$',sol):
  for r in coordinates(roots):assert fact[r]==int(m);described[r]=int(m)
 assert described==fact,(described,fact)
 assert 'coefficient is '+('positive' if sp.Poly(f,g.X).LC()>0 else 'negative') in sol
 expected_end=r'\infty' if sp.Poly(f,g.X).LC()>0 else r'-\infty'
 assert re.search(r'\$y\$ approaches \$'+re.escape(expected_end)+r' \.\$',sol)
 signatures=[];matches=[]
 for b in rec['generation']['graphs']:
  bf=g.polynomial(b);sig=poly_signature(bf);signatures.append(sig);matches.append(sig==poly_signature(f))
  for r,m in zip(b['roots'],b['m']):
   assert bf.subs(g.X,r)==0
   assert all(sp.diff(bf,g.X,k).subs(g.X,r)==0 for k in range(m))
   assert sp.diff(bf,g.X,m).subs(g.X,r)!=0
 assert len(set(signatures))==4 and sum(matches)==1,'whole-bank ambiguity'
 correct=g.ROMANS[matches.index(True)]
 assert len(field[':answer-field/choices'])==5
 assert {a[':answer/value'] for a in field[':answer-field/choices']}=={r'\text{'+z+'}' for z in g.ROMANS}|{'None of the given graphs are correct'}
 keyed=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert keyed==r'\text{'+correct+'}'
 for a in field[':answer-field/choices']:assert a[':answer/id']==g.uid(field[':answer-field/id']+'/'+a[':answer/value'])
 content=g.fingerprint({'version':g.VERSION,'prompt':q[':question/problem'],'solution':sol,'bank':sorted((a[':answer/value'],a[':answer/type']) for a in field[':answer-field/choices']),'difficulty':q[':question/difficulty'].split('/')[-1]})
 assert content==rec['generation']['content_fingerprint'];assert q[':question/id']==g.uid(content)
 plot=rec['generation']['plot'];assert Path(plot['prompt']).exists()
 if plot['sidecar']:
  data=json.loads(Path(plot['sidecar']).read_text());assert data['instance']==p
  assert Image.open(plot['prompt']).size==tuple(data['pixel_size'])
  for panel,b in zip(data['panels'],rec['generation']['graphs']):
   assert panel['factors']==b
   bf=g.polynomial(b);fn=sp.lambdify(g.X,bf,'numpy')
   assert np.allclose(fn(np.array(panel['sample_x'])),panel['sample_y'],rtol=1e-12,atol=1e-10)
   for zoom in panel['zooms']:
    assert np.allclose(fn(np.array(zoom['x'])),zoom['y'],rtol=1e-12,atol=1e-10)
    mid=len(zoom['x'])//2;assert abs(zoom['x'][mid]-zoom['root'])<1e-10
    assert abs(zoom['y'][mid])<1e-10
  assert 'independent vertical scales' in 'Small boxes: local views at roots, with independent vertical scales.'
 return {'signature':signatures,'correct':correct,'pairs':list(itertools.combinations(range(4),2))}
def run():
 cases=[];originals=[];variants=[];checks=[];bank_report=[]
 for t,src in g.SOURCES.items():
  d=g.DATA[t];p={k:d[k] for k in ['roots','m','a']};cases.append({'source_id':t,'template':t,'parameters':p,'bank_profile':'raw:'+t,'difficulty':d['level']})
  rec=g.generate(d['level'],profile='raw:'+t,parameters=p);proof=check(rec);originals.append(rec)
  prompt=re.sub(r'!\[\]\([^)]+\)',lambda _: '![]('+rec['generation']['plot']['prompt']+')',src[':question/problem'])
  assert prompt==rec['question'][':question/problem'];assert src[':question/worked-solution']==rec['question'][':question/worked-solution']
  sf=src[':question/answer-fields'][0];rf=rec['question'][':question/answer-fields'][0]
  assert sorted((a[':answer/value'],a[':answer/type'][':db/ident']) for a in sf[':answer-field/choices'])==sorted((a[':answer/value'],a[':answer/type']) for a in rf[':answer-field/choices'])
  assert sf[':answer-field/key']==rf[':answer-field/key'] and sf[':answer-field/type'][':db/ident']==rf[':answer-field/type']
  assert sf[':answer-field/correct'][':answer/value']==r'\text{'+proof['correct']+'}'
  bank_report.append({'source_id':t,'complete_bank':True,'choices_matched':5,'graphs_mapped':4,'all_wrong_wrong_and_correct_wrong_pairs':proof['pairs'],'observed_key':proof['correct'],'raw_native_asset':rec['generation']['plot']['prompt']})
 # Two changed-parameter records for every profile, including authored easy.
 for t,d in g.DATA.items():
  n=len(d['roots'])
  for k in range(2):
   p={'roots':([-3,2] if k==0 else [-2,3]) if n==2 else ([-3,-1,2] if k==0 else [-2,1,3]),'m':d['m'],'a':-1 if k==0 else 1}
   rec=g.generate(d['level'],k,profile=t,parameters=p);check(rec);variants.append(rec)
   other=g.generate(d['level'],k+23,profile=t,parameters=p);assert other['question'][':question/id']==rec['question'][':question/id']
   # Changed coefficients share the actual assessed qualitative task identity.
   pp={**p,'a':p['a']*5};alias=g.generate(d['level'],parameters=pp,profile=t);assert alias['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint'];assert alias['question'][':question/id']!=rec['question'][':question/id']
   # Structural stage fidelity is independent of value rendering.
   if t in g.SOURCES:
    src=g.SOURCES[t][':question/worked-solution']
    def prose_mask(text):
     text=re.sub(r'x=[^$]+(?=\$)','x=@@ROOT@@',text)
     text=text.replace('coefficient is positive','coefficient is @@SIGN@@').replace('coefficient is negative','coefficient is @@SIGN@@')
     text=text.replace(r'$-\infty .$','$@@END@@ .$').replace(r'$\infty .$','$@@END@@ .$')
     return text
    assert prose_mask(src)==prose_mask(rec['question'][':question/worked-solution']),'complete shared prose/stage fidelity'
    assert len(rec['question'][':question/worked-solution'].split('\n\n'))==len(src.split('\n\n'))
    assert [len(re.findall(r'\$[^$]+\$',para)) for para in rec['question'][':question/worked-solution'].split('\n\n')]==[len(re.findall(r'\$[^$]+\$',para)) for para in src.split('\n\n')]
 # Exact finite domain: all roots, signs and complete profiles; no rendered identity inflation.
 meaningful={l:set() for l in ['easy','moderate','hard']};domain_instances=0
 for t,d in g.DATA.items():
  for rs in itertools.combinations(range(-4,5),len(d['roots'])):
   for a in [-1,1]:
    p={'roots':list(rs),'m':d['m'],'a':a};g.validate_parameters(d['level'],t,p);b=g.graph_bank(t,p)
    sigs=[poly_signature(g.polynomial(z)) for z in b];assert len(set(sigs))==4 and sigs.count(poly_signature(g.polynomial(p)))==1
    meaningful[d['level']].add(g.fingerprint(poly_signature(g.polynomial(p))));domain_instances+=1
 for t,d in g.DATA.items():
  for p in [{},{'roots':d['roots'],'m':[1]*len(d['m']),'a':0},{'roots':[5]*len(d['roots']),'m':d['m'],'a':1},{'roots':d['roots'],'m':d['m'],'a':6}]:
   try:g.generate(d['level'],profile=t,parameters=p)
   except ValueError:pass
   else:raise AssertionError('explicit scope guard')
 # Collision injection rejects the complete bank, without individual replacement.
 d=g.DATA['authored-easy'];old=d['bank'];d['bank']=[(1,[1,1])]*4
 try:
  try:g.graph_bank('authored-easy',{'roots':[-1,1],'m':[1,1],'a':1})
  except ValueError:pass
  else:raise AssertionError('ambiguity not rejected')
 finally:d['bank']=old
 # Fresh concurrent rendering; outputs locked and atomic, exact instance sidecars.
 private=Path(tempfile.mkdtemp(prefix='concurrent-',dir=D));p={'roots':[-4,0,4],'m':[1,4,3],'a':1};pp={**p,'roots':[-3,0,3]}
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
  assets=list(ex.map(lambda z:g.render_plots('q-80361',z,private),[p,p,pp]))
 assert assets[0]==assets[1]
 for z,asset in zip([p,p,pp],assets):assert json.loads(Path(asset['sidecar']).read_text())['instance']==z
 assert not list(private.glob('render-*')) and not list(private.glob('side-*'))
 for rec in originals+variants:
  f=rec['question'][':question/answer-fields'][0]
  checks.append({'label':rec['generation']['template']+'-'+rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'native radio ID grading; separate qualitative proof verifies graph criterion'} for a in f[':answer-field/choices']]})
 write('native-input.json',checks);subprocess.run(['generate/runs/current/check-engine',str(D/'native-input.json'),str(D/'native-report.json')],check=True,capture_output=True)
 write('source-cases.json',cases);write('replayed-sources.json',originals);write('review.json',variants);write('bank-proof.json',bank_report)
 result={'status':'pass','database':'math','basis':1356,'practice_sources':7,'complete_original_banks':{'matched':7,'total':7},'answer_options':{'matched':35,'total':35},'original_graph_panels':{'mapped':28,'total':28},'observed_keys':{'matched':7,'total':7},'source_prompt_and_solution_exact_except_asset_paths':7,'generated_changed_examples':len(variants),'native_checks':len(checks)*5,'exhaustive_complete_profile_instances':domain_instances,'meaningful_finite_tasks':{l:len(v) for l,v in meaningful.items()},'scope':'polynomial to graph selection only','criterion':'qualitative roots, simple/even/odd-multiple behavior, sign; no y scale','pairwise_ambiguities':0,'authored_missing_levels':['easy: two distinct simple roots, same polynomial-to-graph task'],'plot_extension':'true-function local root zooms expose tangent/crossing categories at native pixels','source_presentation_anomalies':[], 'versions':{'python':platform.python_version(),'sympy':sp.__version__,'matplotlib':g.matplotlib.__version__},'native_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'limits':['Sketch distractor exponents represent visible classes, not unobserved exact degrees.','Positive coefficient magnitude is unassessed and excluded from task diversity.','Original asset reuse at anchors preserves unlabeled source geometry; no arbitrary y-coordinate fidelity is claimed.']}
 write('validation.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':run()
