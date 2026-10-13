#!/usr/bin/env python3
"""Independent displayed-math, fidelity, domain, plot, identity and native QA."""
import concurrent.futures,hashlib,importlib.util,itertools,json,re,subprocess,tempfile
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
mr=g.mr
CASES=json.loads((HERE/'source-cases.json').read_text())
SOURCE=g.RECORD[':knowledge-point/questions'];ORIGINAL={q[':question/math-academy-id']:q for q in SOURCE}
def eq(a,b):return sp.trigsimp(sp.simplify(a-b))==0
def balanced(text):
 assert text.count('$$')%2==0
 assert text.replace('$$','').count('$')%2==0
 # Escaped literal braces have no group semantics.
 t=re.sub(r'\\[{}]','',text);depth=0
 for c in t:
  if c=='{':depth+=1
  elif c=='}':depth-=1
  assert depth>=0,('closing brace',text)
 assert depth==0,('unclosed braces',text)
 assert not re.search(r'(?<!\\)--|\+\-',text)
def actual_prompt_f(rec):
 p=rec['question'][':question/problem']
 # Source weird ∫_(D) notation remains observable in explicit replay only.
 m=re.search(r'\$(?:\\iint_D |\{∬\}_\{D\}|∬_\(D\))(.*?)\$',p,re.S);assert m,p
 f=re.split(r'\\,\\(?:text|mathrm)\{d\}A|dA',m[1])[0]
 return mr.expr(f)
def rhs_integrand(row):
 rhs=row.split('& =',1)[1] if '& =' in row else row.split('&=',1)[1]
 if r'\int_' in rhs or r'\int }_' in rhs:return mr.read_integral(rhs)
 # First substituted row uses a formal double integral, with no bounds.
 rhs=re.sub(r'^\s*(?:\{∬\}_\{Δ\}|\\iint_\\Delta)\s*','',rhs)
 rhs=re.split(r'\\text\{d\}|\\mathrm\{d\}',rhs)[0]
 rhs=rhs.replace(r'\,','').replace(r'\text{ }','').strip()
 return None,mr.expr(rhs)
def check(rec):
 assert set(rec['knowledge_point'])=={'db_id','id','title'}
 q=rec['question'];md=q[':question/problem'];solution=q[':question/worked-solution']
 owned=q[':question/answer-fields'][0]
 ck=g.fingerprint({'version':g.VERSION,'prompt':md,'solution':solution,'bank':sorted(a[':answer/value'] for a in owned[':answer-field/choices']),'difficulty':q[':question/difficulty'].split('/')[-1]})
 assert ck==rec['generation']['content_fingerprint']
 assert q[':question/id']==str(g.uuid.uuid5(g.uuid.NAMESPACE_URL,ck))
 base=next((v for v in g.DATA.values() if v['family']==rec['generation']['template']),None)
 if base:
  expected_prompt=re.sub(r'!\[\]\([^)]+\)',lambda _: '![]('+rec['generation']['plot']['prompt']+')',base['prompt'])
  if rec['generation']['bank_profile'] not in g.DATA:
   if base['family']=='xy2':expected_prompt=expected_prompt.replace('∬_(D)xy^{2}dA',r'\iint_D xy^2\,\mathrm{d}A')
   expected_prompt+='\n\n'+g.CRITERION
  assert md==expected_prompt, 'source prompt wording/layout changed'
 balanced(md);balanced(solution)
 f=actual_prompt_f(rec);expected=sp.trigsimp(f.subs({mr.x:mr.r*sp.cos(mr.theta),mr.y:mr.r*sp.sin(mr.theta)})*mr.r)
 assert eq(f,g.family_expr(rec['generation']['template']))
 a=sp.sympify(rec['generation']['domain']['alpha']);b=sp.sympify(rec['generation']['domain']['beta']);rad=sp.sqrt(rec['generation']['parameters']['radius_squared'])
 field=q[':question/answer-fields'][0];assert len(field[':answer-field/choices'])==5
 ids={x[':answer/id'] for x in field[':answer-field/choices']};assert len(ids)==5 and field[':answer-field/correct'][1] in ids
 signatures=[];eligible=[]
 for choice in field[':answer-field/choices']:
  balanced(choice[':answer/value']);bounds,z=mr.read_integral(choice[':answer/value']);aa,bb,lo,hi=bounds
  eligible.append(lo==0 and eq(hi,rad) and g.same_sector(aa,bb,a,b) and eq(z,expected))
  signatures.append(tuple(map(sp.srepr,[sp.Mod(aa,2*sp.pi),bb-aa,lo,hi]))+ (sp.srepr(sp.trigsimp(z)),))
 assert len(set(signatures))==5 and sum(eligible)==1
 assert next(c[':answer/id'] for c,valid in zip(field[':answer-field/choices'],eligible) if valid)==field[':answer-field/correct'][1]
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S);assert block
 rows=re.split(r'\\\\',block[1]);assert len(rows)>=2
 base=next((v for v in g.DATA.values() if v['family']==rec['generation']['template']),None)
 if base and base['solution']:
  original_block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',base['solution'],re.S)
  assert len(rows)==len(re.split(r'\\\\',original_block[1])), 'source stage count changed'
  assert solution.split('First, notice')[0]==base['solution'].split('First, notice')[0], 'shared formal formula/prose changed'
 for row in rows:
  bounds,z=rhs_integrand(row)
  assert eq(z,expected),('stage',rec['generation']['template'],row,z,expected)
  if bounds:assert all(eq(c,v) for c,v in zip(bounds,[a,b,0,rad]))
 # Check domain block independently from displayed radii and theta bounds.
 domain=re.search(r'\$\$\n([^$]*(?:Δ=|\\Delta=)[^$]*)\n\$\$',solution);assert domain
 ds=domain[1].replace(r'\leq',r'\le')
 m=re.search(r'0\\le\s*r\\le\s*(.*?)\\,?[,]',ds)
 # Normalize source \ , markup before comparison via explicit radius slot.
 if m:
  val=m[1].rstrip('\\').strip();assert eq(mr.expr(val),rad)
 plot=rec['generation']['plot'];assert Path(plot['prompt']).exists()
 if plot['sidecar']:
  pp=json.loads(Path(plot['sidecar']).read_text());assert pp['instance']=={'radius_squared':rec['generation']['parameters']['radius_squared'],'alpha_pi':str(sp.simplify(a/sp.pi)),'beta_pi':str(sp.simplify(b/sp.pi))}
 return len(rows)
def scalar_collisions(rec):
 opts=rec['question'][':question/answer-fields'][0][':answer-field/choices'];values=[]
 for c in opts:
  bounds,f=mr.read_integral(c[':answer/value']);a,b,lo,hi=bounds
  # Separable integrands across all observed families; integrate theta first.
  v=sp.integrate(f,(mr.theta,a,b));v=sp.integrate(v,(mr.r,lo,hi));values.append(sp.expand(v))
 collisions=[]
 for i,j in itertools.combinations(range(5),2):
  if values[i]==values[j] or abs(complex(sp.N(values[i]-values[j],30)))<1e-20:collisions.append([opts[i][':answer/id'],opts[j][':answer/id']])
 return {'values':list(map(str,values)),'equal_scalar_pairs':collisions,'setup_eligible_count':1,'criterion':'actual domain and pointwise transformed integrand, nonnegative r'}
def run():
 assert g.same_sector(-sp.pi/2,0,3*sp.pi/2,2*sp.pi)
 assert not g.same_sector(3*sp.pi/2,0,-sp.pi/2,0)
 originals=[];variants=[];bank_matches=0;values_matches=0;designation=0;raw_solution=0;normalized_solution=0;stages=[]
 for c in CASES:
  rec=g.generate(c['level'],seed=9,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);originals.append(rec);stages.append(check(rec));old=ORIGINAL[c['source_id']];f=rec['question'][':question/answer-fields'][0]
  ov=[v[':answer/value'] for v in old[':question/answer-fields'][0][':answer-field/choices']];nv=[v[':answer/value'] for v in f[':answer-field/choices']]
  assert sorted(ov)==sorted(nv);bank_matches+=1;values_matches+=len(ov)
  if ':answer-field/correct' in old[':question/answer-fields'][0]:
   cv=next(v[':answer/value'] for v in f[':answer-field/choices'] if v[':answer/id']==f[':answer-field/correct'][1]);assert cv==old[':question/answer-fields'][0][':answer-field/correct'][':answer/value'];designation+=1
  if ':question/worked-solution' in old:
   if rec['question'][':question/worked-solution']==old[':question/worked-solution']:raw_solution+=1
   else:
    repaired=old[':question/worked-solution'].replace('Δ={(r',r'Δ=\{(r').replace('2\\pi }.','2\\pi \\}.').replace('0}.','0\\}.')
    assert rec['question'][':question/worked-solution']==repaired
    normalized_solution+=1
 for template,level in g.TEMPLATES.items():
  for j,n in enumerate((9,25)):
   rotation=0 if level=='easy' or template=='xy2' else (j+1)
   rec=g.generate(level,seed=j,template=template,parameters={'radius_squared':n,'rotation':rotation});stages.append(check(rec));variants.append(rec)
   other=g.generate(level,seed=j+31,template=template,parameters={'radius_squared':n,'rotation':rotation})
   assert rec['question'][':question/id']==other['question'][':question/id']
   assert rec['generation']['parameter_fingerprint']==other['generation']['parameter_fingerprint']
 # Mathematical/formatting corners: reuse four geometries while varying every
 # integrand and the full quarter-turn direction range, avoiding costly plots.
 boundary_count=0
 for template,level in g.TEMPLATES.items():
  for n in (2,36):
   for rot in ((0,) if level=='easy' or template=='xy2' else (0,1,2,3)):
    check(g.generate(level,template=template,parameters={'radius_squared':n,'rotation':rot}));boundary_count+=1
 for bad in ({'radius_squared':1,'rotation':0},{'radius_squared':37,'rotation':0},{'radius_squared':4,'rotation':4},{'radius_squared':2.5,'rotation':0}):
  try:g.generate_hard(parameters=bad)
  except ValueError:pass
  else:raise AssertionError('invalid explicit parameters accepted')
 # Fresh private outputs test simultaneous identical and distinct geometry.
 (HERE/'concurrency').mkdir(exist_ok=True)
 private=Path(tempfile.mkdtemp(prefix='fresh-',dir=HERE/'concurrency'))
 instances=[{'radius_squared':7,'alpha_pi':'0','beta_pi':'1/2'},{'radius_squared':7,'alpha_pi':'0','beta_pi':'1/2'},{'radius_squared':13,'alpha_pi':'1','beta_pi':'3/2'}]
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:assets=list(ex.map(lambda p:g.render_plots(p,private),instances))
 assert assets[0]==assets[1]
 for p,a in zip(instances,assets):assert json.loads(Path(a['sidecar']).read_text())['instance']==p
 assert not list(private.glob('render-input-*')) and not list(private.glob('plot-*')) and not list(private.glob('sidecar-*'))
 grading=[]
 for rec in originals+variants:
  f=rec['question'][':question/answer-fields'][0];grading.append({'label':rec['generation']['template']+'-'+rec['question'][':question/id'],'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'real radio owned-ID grading; displayed setup independently checked'} for a in f[':answer-field/choices']]})
 (HERE/'native-input.json').write_text(json.dumps(grading,indent=2,ensure_ascii=False)+'\n')
 subprocess.run(['generate/runs/current/check-engine',str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True,capture_output=True)
 collisions={rec['generation']['source_id']:scalar_collisions(rec) for rec in originals}
 (HERE/'bank-collisions.json').write_text(json.dumps(collisions,indent=2)+'\n')
 (HERE/'review.json').write_text(json.dumps(variants,indent=2,ensure_ascii=False)+'\n')
 (HERE/'replayed-sources.json').write_text(json.dumps(originals,indent=2,ensure_ascii=False)+'\n')
 result={'status':'pass','practice_sources':9,'complete_raw_banks':{'matched':bank_matches,'total':9},'displayed_raw_options':{'matched':values_matches,'total':45},'observed_designations':{'matched':designation,'total':8},'independently_inferred_designations':1,'source_solutions':{'raw_exact':raw_solution,'presentation_normalized':normalized_solution,'total_present':8,'authored_missing':1},'generated_review_records':len(variants),'independent_displayed_math_records':len(originals)+len(variants)+boundary_count,'native_checks':len(grading)*5,'meaningful_finite_tasks':{'easy':105,'moderate':735,'hard':280},'authored_hard_templates':2,'setup_collisions':0,'scalar_collisions_report':'bank-collisions.json','raw_prompt_repairs':{'asset_paths':9,'normal_only_integral_notation':1,'normal_response_criterion':True},'concurrency':'fresh identical and distinct private outputs passed','stage_row_counts':stages,'native_engine_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'limits':['q-161044 has no observed key, difficulty or worked solution; inferred key and moderate label are explicitly authored.','Hard has no observed source labels; its two same-method extensions are authored.','Numerical integral coincidences do not satisfy the explicitly requested domain/integrand setup criterion; all raw banks retained.','Observed distractor error intent is uncertain; parameterized complete component patterns are recovered, not original authoring code.']}
 (HERE/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':run()
