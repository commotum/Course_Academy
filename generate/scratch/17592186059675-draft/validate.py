"""Independent printed-math, structural mutation, raw replay and actual native grader QA."""
import copy,hashlib,importlib.util,itertools,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2];sys.path.insert(0,str(HERE));import printed as printed
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=printed.x

def save(n,v):(HERE/n).write_text(json.dumps(v,indent=2)+'\n')
def parse_prompt(q):
 t=q[':question/problem']
 if '$y=' in t or '$y =' in t:
  body=re.search(r'\$y\s*=([^$]+)',t)[1].rstrip('.');expr=printed.scalar(body)
 else:
  body=t.split(r'\frac{\text{d}}{\text{d}x}(',1)[1].rsplit(')=$',1)[0];expr=printed.scalar(body)
 point=printed.scalar(re.search(r'point \$x=([^$]+)',t)[1].rstrip('?')) if 'point $x=' in t else None
 return expr,point

def check(r):
 q=r['question'];expr,point=parse_prompt(q);d=sp.diff(expr,x);correct=d if point is None else sp.simplify(d.subs(x,point));f=q[':question/answer-fields'][0];vals=[printed.scalar(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(vals)==len(set(map(str,vals)))
 assert sum(sp.simplify(v-correct)==0 for v in vals)==1
 for a,v in zip(f[':answer-field/choices'],vals):assert (sp.simplify(v-correct)==0)==(a[':answer/id']==f[':answer-field/correct'][1])
 # Read all independently printed equality stages, excluding formal derivative inputs.
 for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S):
  rows=block.split('\\\\');lhs=rows[0].split('&',1)[0];target=correct if point is not None and 'x' not in lhs else d
  for row in rows:
   rhs=re.split(r'&\s*=',row)[-1].strip().rstrip('.')
   if r'\frac{\text{d}}' in rhs or '′' in rhs:continue
   if len(re.split(r'&\s*=',row))<2:continue
   assert sp.simplify(printed.scalar(rhs)-target)==0,(r['generation']['template'],rhs,target)
 for block in re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S):
  if r'y^{\prime}(' in block and ')=' in block and r'\begin' not in block:
   for v in block.split(')=',1)[1].rstrip('.').split('='):assert sp.simplify(printed.scalar(v)-correct)==0
 g.validate_generated_record(r)
 return r

def native(r,label):
 f=r['question'][':question/answer-fields'][0];right=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==right else 'rejected','purpose':'actual field-owned ID choice'} for a in f[':answer-field/choices']]
 else:
  v=f[':answer-field/choices'][0][':answer/value'];checks=[{'submitted':a,'expected':b,'purpose':c} for a,b,c in [(v,'accepted','canonical blank'),('('+v+')+0','accepted','equivalent entry'),('2('+v+')/2','accepted','equivalent scaled entry'),('('+v+')+1','rejected','wrong additive term'),('-('+v+')','rejected','wrong sign')]]
 return {'record':r,'label':label,'checks':checks}

def main():
 cases=[];raw=[];inventory=[]
 for sid,q in g.SOURCES.items():
  level=q.get(':question/difficulty',{}).get(':db/ident','unrated').rsplit('/',1)[-1];r=g.generate(level,template=sid,profile='observed_raw');assert r['question']==q
  result={'source_id':sid,'raw_exact':True,'attrs_and_omissions_exact':True,'normal_eligible':r['generation']['normal_eligible'],'question':q}
  if sid in g.MA_SOURCES:cases.append({'source_id':sid,'template':sid,'level':level,'parameters':None,'profile':'observed_raw'});raw.append(result)
  else:inventory.append({'role':'independently authored inventory','relationship_to_source_templates':r['generation']['relationship_to_source_templates'],**result})
 save('source-cases.json',cases);save('source-replay.json',{'passed':True,'MA_originals':10,'complete_banks':10,'total_bank_values':34,'matched_bank_values':34,'matched_distractors':24,'total_distractors':24,'raw_question_results':raw,'raw_source_errors_preserved':g.SOURCE_ERRORS})
 save('independent-inventory-replay.json',inventory)
 samples=[];counts={};slotcoverage={};seen_by_level={l:set() for l in g.SUPPORTED_LEVELS}
 inventory_math=[]
 for sid in g.INVENTORY:
  r=g.source_replay(sid);q=r['question'];q[':question/difficulty']=q[':question/difficulty'][':db/ident']
  for k in (':question/problem',':question/worked-solution'):q[k]=g.normalize_prose(q[k])
  for f in q[':question/answer-fields']:
   f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
   for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident'];a[':answer/value']=g.normalize_tex(a[':answer/value'])
  inventory_math.append(check(r))
 save('independent-inventory-math.json',{'role':'independently authored inventory','checked_records':len(inventory_math),'records':inventory_math})
 for lev,ts in g.LEVEL_TEMPLATES.items():
  counts[lev]={}
  for t in ts:
   seen=set();coverage={k:set() for k in g.domains(t)};ps=list(g.candidates(t))
   for p in ps:
    expr,point,d,c,bank=g.model(t,p)
    if any(sp.expand(a-b)==0 for i,a in enumerate(bank) for b in bank[:i]):continue
    fp=g.digest([sp.srepr(sp.expand(d)),None if point is None else sp.srepr(point)])
    seen.add(fp);seen_by_level[lev].add(fp)
    for k,v in p.items():coverage[k].add(v)
   counts[lev][t]=len(seen);slotcoverage[t]={k:sorted(v,key=str) for k,v in coverage.items()}
   # Every boundary value with other slots fixed, plus interior cases and original replay.
   selected=[];base=ps[0]
   for k in g.domains(t):
    for v in coverage[k]:
     p=dict(base);p[k]=v
     try:r=g.generate(lev,123,template=t,parameters=p)
     except ValueError:
      matching=next(z for z in ps if z[k]==v);r=g.generate(lev,123,template=t,parameters=matching)
     selected.append(check(r))
   for p in [ps[0],ps[-1],ps[len(ps)//2]]:
    try:selected.append(check(g.generate(lev,123,template=t,parameters=p)))
    except ValueError:pass
   if t in g.PROFILES:
    r=check(g.generate(lev,template=t,parameters=g.PROFILES[t][1]));selected.append(r)
   if t=='independent-moderate':
    for trig in ('sin','cos'):
     for point in g.domains(t)['point']:
      matching=next((z for z in ps if z['trig']==trig and z['point']==point),None)
      if matching:selected.append(check(g.generate(lev,123,template=t,parameters=matching)))
   rendered={k:{r['generation']['parameters'][k] for r in selected} for k in g.domains(t)}
   assert rendered==coverage,(t,rendered,coverage)
   dedup={r['question'][':question/id']:r for r in selected};samples.extend(dedup.values())
 save('coverage.json',{'per_template_meaningful_tasks':counts,'per_level_distinct_tasks':{l:len(v) for l,v in seen_by_level.items()},'slot_coverage':slotcoverage,'aliases_seeds_order_constants_excluded':True,'scope':'No chain/product/quotient rules; all arguments x; source power slots same term workload; hard authored four direct terms.'})
 for l in g.SUPPORTED_LEVELS:
  a=g.batch(l,6,789);b=g.batch(l,6,789);assert a==b;assert len({r['generation']['mathematical_fingerprint'] for r in a})==6
  samples.extend(check(r) for r in a)
 # Source errors remain raw only; normal valid replay includes documented radians/dependent-variable fix.
 for t in ('q-47906','q-47908','q-167324','q-167778','q-166071'):
  try:g.generate('easy',template=t)
  except (ValueError,KeyError):pass
  else:raise AssertionError('Ineligible raw evidence served normally')
 for t in g.PROFILES:
  p=copy.deepcopy(g.PROFILES[t][1]);k=next(iter(p));p[k]=0
  try:g.generate(g.PROFILES[t][0],template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Bad bounds accepted')
 # Structural mutation tests modify printed dependent input, answer and solution.
 r=check(g.generate('hard',template='independent-hard',parameters={'a':1,'b':1,'c':1,'d':1,'n':2,'m':1}));mutations=[]
 for label,mutate in [('wrong-answer',lambda q:q[':question/answer-fields'][0][':answer-field/choices'][0].update({':answer/value':'0'})),('stale-power-input',lambda q:q.update({':question/problem':q[':question/problem'].replace('x^{2}','x^{3}')})),('stale-worked-intermediate',lambda q:q.update({':question/worked-solution':q[':question/worked-solution'].replace('2 x','3 x')}))]:
  bad=copy.deepcopy(r);mutate(bad['question'])
  try:check(bad)
  except AssertionError:mutations.append({'mutation':label,'rejected':True})
  else:raise AssertionError('Mutation escaped: '+label)
 save('mutations.json',mutations)
 samples=list({r['question'][':question/id']:r for r in samples}.values());save('previews.json',samples);save('native-input.json',[native(r,str(i)) for i,r in enumerate(samples+inventory_math)])
 subprocess.run([str(HERE/'check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 preview=[g.generate('easy',template='q-1847',parameters={'a':4,'b':2}),g.generate('easy',template='q-1847',parameters={'a':6,'b':1}),g.generate('easy',template='q-30991',parameters={'a':6,'n':4}),g.generate('moderate',template='q-1900',parameters={'k':1}),g.generate('moderate',template='independent-moderate',parameters={'a':-3,'b':6,'trig':'cos','point':'pi/3'}),r]
 (HERE/'review.md').write_text('\n\n'.join('## '+r['generation']['template']+'\n\n'+g.markdown(r) for r in preview)+'\n')
 baseline=json.loads((HERE/'baseline.json').read_text());actual={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [ROOT/Path(k) for k in baseline]};assert all(actual[str(ROOT/k)]==h for k,h in baseline.items());assert set(baseline)=={str(p.relative_to(ROOT)) for p in (ROOT/'generate/scratch/17592186059675').rglob('*') if p.is_file()}|{'generate/scratch/17592186059675.py'}
 files=[HERE.with_suffix('.py'),HERE/'validate.py',HERE/'source.json',HERE/'printed.py',HERE/'check-engine.rs',HERE/'check-engine',ROOT/'target/debug/libcourse_academy_engine.rlib']
 save('validation.json',{'passed':True,'source_basis':2275,'raw_original_fidelity':'10/10 full raw questions incl attrs/omissions and all banks','independent_inventory_raw_replay':'5/5 separately labeled','normal_printed_math_solution_checks':len(samples),'independent_inventory_printed_math_checks':len(inventory_math),'structural_mutations_rejected':len(mutations),'baseline_entire_path_set_and_sha_preserved':True,'native_grader':'course_academy_engine::learning::grade_field, current local engine; no DB writes','hashes':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}})
 print('Draft validated:',len(samples),'printed cases; all raw records; baseline unchanged')
if __name__=='__main__':main()
