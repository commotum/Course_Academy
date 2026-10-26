#!/usr/bin/env python3
"""Independent visible-content audit. Run with --workspace W --job J --evidence E."""
import argparse,collections,copy,hashlib,importlib.util,json,platform,re,shutil,subprocess,sys
from pathlib import Path
from fractions import Fraction as F
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ap=argparse.ArgumentParser();ap.add_argument('--workspace',type=Path,required=True);ap.add_argument('--job',type=Path,required=True);ap.add_argument('--evidence',type=Path,required=True)
a=ap.parse_args();W,J,E=a.workspace.resolve(),a.job.resolve(),a.evidence.resolve();R=next(p for p in W.parents if (p/'scripts/generator_review.py').is_file())
sys.path.insert(0,str(W));import generator as g
spec=importlib.util.spec_from_file_location('shared_format',R/'scripts/question_capture/math_format.py');mf=importlib.util.module_from_spec(spec);spec.loader.exec_module(mf)
def read(p):return json.loads(Path(p).read_text())
def write(n,d):p=E/n;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def enum(v):return (v.get(':db/ident') if isinstance(v,dict) else v).split('/')[-1]
def key(f):
 c=f[':answer-field/correct'];cid=c[':answer/id'] if isinstance(c,dict) else c[1]
 return next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==cid)
def expr(t):
 t=t.strip().rstrip('.,:').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\dfrac',r'\frac')
 while r'\frac' in t:
  t,n=re.subn(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',t);assert n,t
 t=t.replace(r'\cdot','*').replace('{','(').replace('}',')').replace('^','**')
 return sp.expand(parse_expr(t,transformations=standard_transformations+(implicit_multiplication_application,),local_dict={v:sp.Symbol(v,real=True) for v in 'xytzw'}))
def shown(r):
 p=r['question'][':question/problem'];t=re.search(r'\$([^$]+)\$',p)[1];pol=expr(t);v,=pol.free_symbols;P=sp.Poly(pol,v)
 assert P.degree()==2 and P.nth(2)==1
 m=-P.nth(1);c=P.nth(0);assert m.is_integer and m>0 and m%2==1
 return pol,v,m,c,m/2,c-m*m/4

def boundaries(r):
 q=r['question'];mf.validate_generated_record(copy.deepcopy(r))
 for n in (':question/problem',':question/worked-solution'):
  mf.validate_prose(q[n])
  for emphasis in re.findall(r'\*\*([^*]+)\*\*',q[n]):assert emphasis.strip()==emphasis and emphasis
 for f in q[':question/answer-fields']:
  for choice in f[':answer-field/choices']:
   if enum(choice[':answer/type'])=='text':mf.validate_prose(choice[':answer/value'])
   for k,v in choice.items():
    if 'feedback' in k and isinstance(v,str):mf.validate_prose(v)
 for k,v in q.items():
  if 'feedback' in k and isinstance(v,str):mf.validate_prose(v)

def path(r,ref):
 boundaries(r);pol,v,m,c,h,k=shown(r);q=r['question'];b=enum(q[':question/difficulty']);s=q[':question/worked-solution'];block,=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',s,re.S)
 rows=[]
 for row in block.split(r'\\'):
  row=row.strip()
  if not row:continue
  row=re.sub(r'\\underbrace\{(.*?)\}_\{\\text\{perfect square\}\}',r'\1',row)
  lhs,rhs=row.split('&=');assert not lhs or sp.simplify(expr(lhs)-pol)==0
  assert sp.simplify(expr(rhs)-pol)==0,(ref,row)
  rows.append(rhs.strip().rstrip('.'))
 assert len(rows)==3,rows
 final=rows[-1]
 # A finished completion must actually display the source-directed binomial.
 # Equivalent reversed binomials require their own shown conversion; none is served.
 match=re.fullmatch(r'\\left\('+str(v)+r'-(\\frac\{\d+\}\{2\})\\right\)\^2(.*)',final)
 assert match,'Unshown or unfinished form: '+final
 assert expr(match[1])==h and expr(match[2] or '0')==k
 vals={f[':answer-field/key']:expr(key(f)) for f in q[':question/answer-fields']}
 expected={'field-1':-h if b=='hard' else h,'field-2':k if b=='hard' else abs(k)};assert vals==expected,(ref,vals,expected)
 if b!='hard':
  sign=re.search(r'\)\^2([+-])\$',q[':question/problem'])[1];assert (sign=='+' and k>=0) or (sign=='-' and k<0)
 else:
  assert 'Comparing with' in s and '$a=-' in s and '$b=' in s
 case=[]
 for f in q[':question/answer-fields']:
  conversion={'rule':'Extract '+('signed parameters a=-h, b=k' if b=='hard' else 'positive half h and magnitude |k| at the supplied sign')+' from the completed square.',
   'scope_source':'q-223639/q-223640 two-blank field scope; hard signed-parameter comparison is the documented authored progression in source-analysis.json and matched-difficulty.json.',
   'shown_step':s.split('\n\n')[-1],'status':'passed'}
  case.append({'template':b,'field_key':f[':answer-field/key'],'final_expression':final,'keyed_answer':key(f),'domain':'Real '+str(v)+'; exact numeric fragment, not a whole polynomial.','conclusion':'Three displayed rows preserve the polynomial. Final form is completed; the displayed field interpretation yields precisely this key.','sample_refs':[ref],'status':'passed','conversions':[conversion]})
 return {'polynomial':str(pol),'m':str(m),'c':str(c),'h':str(h),'k':str(k),'case':'zero' if k==0 else 'positive' if k>0 else 'negative','rows':rows,'field_values':{z:str(y) for z,y in vals.items()}},case

commands=[]
def run(argv):
 result=subprocess.run([str(z) for z in argv],capture_output=True,text=True);commands.append({'argv':[str(z) for z in argv],'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr});write('commands.json',commands)
 assert result.returncode==0,result.stderr+result.stdout
 return result.stdout

source=read(J/'source/source.json');exemplars=read(J.parent/'1/investigation/published-exemplars.json');binding=read(E/'final-binding.json');binding=binding.get('binding',binding)
allsets={};paths=[];math_results={};final_ids={}
for b in ('easy','moderate','hard'):
 seed=binding['verification_batches'][b]['seed'];count=binding['verification_batches'][b]['count']
 fn=J/('samples.json' if b=='hard' else 'samples-'+b+'.json');records=read(fn)
 assert len(records)==count and hashlib.sha256(json.dumps(records,sort_keys=True,separators=(',',':'),ensure_ascii=False).encode()).hexdigest()==binding['verification_batches'][b]['batch_hash']
 assert records==g.generate(b,count,seed)
 write('final-'+b+'.json',records);allsets['final-'+b+'.json']=records
 fresh=g.generate(b,6,927631+['easy','moderate','hard'].index(b));assert fresh==g.generate(b,6,927631+['easy','moderate','hard'].index(b))
 write('control-'+b+'.json',fresh);allsets['control-'+b+'.json']=fresh;final_ids[b]=[r['question'][':question/id'] for r in records]

boundary_records=[]
for b in ('easy','moderate','hard'):
 for m,c in [(3,F(9,4)-F(1,4)),(3,F(9,4)),(3,F(9,4)+F(1,4)),(15,F(-3)),(15,F(0)),(7,F(5,4)),(7,F(8)),(11,F(25))]:boundary_records.append(g.construct(m,c,'x',b))
write('boundaries.json',boundary_records);allsets['boundaries.json']=boundary_records
cf=[]
for b in ('easy','moderate','hard'):
 cf.extend(g.construct(m,c,v,b) for m,c,v in [(5,F(17,4),'x'),(5,F(25,4),'x'),(5,F(29,4),'x'),(5,F(29,4),'z'),(7,F(29,4),'x')])
write('counterfactual-records.json',cf);allsets['counterfactual-records.json']=cf
matched=[g.construct(5,F(7),'x',b) for b in ('easy','moderate','hard')];write('matched-difficulty.json',matched);allsets['matched-difficulty.json']=matched
for ref,rs in allsets.items():
 results=[]
 for r in rs:
  checked,p=path(r,ref);results.append(checked);paths+=p
 math_results[ref]={'count':len(rs),'cases':dict(collections.Counter(x['case'] for x in results)),'records':results}
write('independent-math.json',math_results)
# Negative control: exact algebraic equivalence is insufficient for an unshown reversed result.
bad=copy.deepcopy(matched[1]);final=path(bad,'matched-difficulty.json')[0]['rows'][-1];replacement=r'\left(\frac{5}{2}-x\right)^2+\frac{3}{4}';assert expr(final)==expr(replacement)
bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace('&='+final+'.','&='+replacement+'.')
try:path(bad,'negative-scope.json')
except AssertionError as error:write('negative-scope.json',{'record':bad,'algebraically_equivalent':True,'rejected_as_expected':str(error),'reason':'The served source-directed completion changes to a reversed binomial without showing or justifying that conversion.'})
else:raise AssertionError('Negative scope control passed')
write('solution-paths.json',{'cases':paths,'negative_control':'negative-scope.json','coverage':'All final records, every ordinary response shape, sign boundaries, original constants, and matched difficulty controls.'})
# Original complete evidence and investigation exemplar fidelity, independent of author fidelity report.
original=[q for q in source['material']['kp'][':knowledge-point/questions'] if ':question/worked-solution' in q]+[r.get('question',r) for r in exemplars]
replay=g.replay_sources();assert len(replay)==len(original)==8;fidelity=[]
for old,new in zip(original,replay):
 boundaries(new);q=new['question'];assert q[':question/problem']==mf.normalize_prose(old[':question/problem']);assert q[':question/worked-solution']==mf.normalize_prose(old[':question/worked-solution'])
 oldfields={f[':answer-field/key']:f for f in old[':question/answer-fields']};pol,v,m,c,h,k=shown(new)
 for f in q[':question/answer-fields']:
  o=oldfields[f[':answer-field/key']];assert enum(f[':answer-field/type'])==enum(o[':answer-field/type'])
  assert [expr(z[':answer/value']) for z in o[':answer-field/choices']]==[expr(z[':answer/value']) for z in f[':answer-field/choices']]
  assert expr(key(o))==expr(key(f))
  if enum(f[':answer-field/type'])=='radio':assert sum(expr(z[':answer/value'])==pol for z in f[':answer-field/choices'])==1 and expr(key(f))==pol
  else:
   expected=h if f[':answer-field/key']=='field-1' else abs(k) if 'nonnegative' in q[':question/problem'] or new==replay[3] or new==replay[5] else k
   if old[':question/id']=='aae80fdb-9519-54f8-9106-0189ec7972b1':expected=-h if f[':answer-field/key']=='field-1' else k
   assert expr(key(f))==expected,(old[':question/id'],f[':answer-field/key'],expected,key(f))
 fidelity.append({'source_id':old[':question/id'],'normalized_prompt_solution_equal':True,'all_fields_choices_and_keys_equal':True,'correctness_checked':True})
write('source-replay-records.json',replay);write('source-replay-checks.json',{'complete_sources_and_exemplars':fidelity,'canonical_identity':'construct(7,0,x,easy): x²-7x=(x-7/2)²-49/4; checked independently in canonical-check.json.','partial_imports':'q-221418 and q-52277 retain prompts, partial fields/bank unchanged; full square method and variable w supported. No missing-source-field reconstruction requested.'})
# Actual delivery filtering: separate each band and its independently chosen control sample.
delivery={}
for b in ('easy','moderate','hard'):
 for kind in ('final','control'):
  name=kind+'-'+b
  run([sys.executable,R/'generate/pipeline/check_delivery.py','--input',E/(name+'.json'),'--source',J/'source/source.json','--inventory',J/'source/inventory.json','--difficulty',b,'--output',E/('delivery-'+name),'--asset-root',J/('outputs-0'+('' if b=='hard' else '-'+b)),'--math-root','/media/jake/SSD/EDB/math'])
  survivors=read(E/('delivery-'+name)/'accepted.json');report=read(E/('delivery-'+name)/'delivery.json');assert len(survivors)==len(allsets[name+'.json']),report
  assert [shown(r)[-1] for r in survivors]==[shown(r)[-1] for r in allsets[name+'.json']]
  delivery[name]=report|{'cases_after':dict(collections.Counter('zero' if shown(r)[-1]==0 else 'positive' if shown(r)[-1]>0 else 'negative' for r in survivors))}
write('delivery-summary.json',delivery)
# Native grading: equivalents and wrong/stale values, with independent expected keys from visible input.
cases=[]
for ref,rs in list(allsets.items())+[('source-replay-records.json',replay)]:
 for index,r in enumerate(rs):
  checks=[]
  for i,f in enumerate(r['question'][':question/answer-fields']):
   val=expr(key(f))
   if enum(f[':answer-field/type'])=='radio':
    pol=shown(r)[0]
    checks += [{'field_index':i,'submitted_answer_id':z[':answer/id'],'expected':'accepted' if expr(z[':answer/value'])==pol else 'rejected','purpose':'Complete bank: independently expanded polynomial determines correctness.'} for z in f[':answer-field/choices']]
   else:
    assert val.is_Rational
    for value,expected,purpose in [(str(val),'accepted','Exact fraction'),(str(float(val)),'accepted','Equivalent terminating decimal'),(str(float(val))+'00','accepted','Equivalent decimal trailing zeros'),(f'{2*val.p}/{2*val.q}','accepted','Unreduced equivalent fraction; no simplest-form requirement'),(str(val+F(1,4)),'rejected','Nearby wrong value'),(str(-val) if val else '1','rejected','Sign mistake or nonzero answer for zero')]:
     checks.append({'field_index':i,'submitted':value,'expected':expected,'purpose':purpose})
  cases.append({'label':ref+':'+str(index),'record':r,'checks':checks})
# Explicit stale-key counterfactual tests: c changes require field-2; changing m requires both.
for start in (0,5,10):
 before,after=cf[start],cf[start+2]
 checks=[{'field_index':1,'submitted':str(expr(key(before['question'][':question/answer-fields'][1]))),'expected':'rejected','purpose':'Relevant original constant changed across the square; stale response must fail.'}]
 cases.append({'label':'counterfactual-stale-constant-'+str(start),'record':after,'checks':checks})
 before,after=cf[start+2],cf[start+4]
 checks=[{'field_index':i,'submitted':str(expr(key(before['question'][':question/answer-fields'][i]))),'expected':'rejected','purpose':'Changed odd coefficient changes the half and compensation.'} for i in (0,1)]
 cases.append({'label':'counterfactual-stale-coefficient-'+str(start),'record':after,'checks':checks})
write('grading-input.json',cases);run([R/'generate/runs/current/check-engine',E/'grading-input.json',E/'grading-report.json'])
# Manifest files, relocation, runtime, deterministic public CLI and capacity handling.
manifest=read(W/'package.json');assert manifest['dependencies']=={'python':platform.python_version(),'packages':{}}
rel=E/'relocated-package';rel.mkdir(exist_ok=True)
for f in manifest['files']:shutil.copy2(W/f,rel/f)
relocation={}
for b in ('easy','moderate','hard'):
 seed=binding['verification_batches'][b]['seed'];count=binding['verification_batches'][b]['count']
 argv=[sys.executable,rel/'generator.py','--difficulty',b,'--count',str(count),'--seed',str(seed),'--format','json'];out=run(argv)
 assert json.loads(out)==allsets['final-'+b+'.json'];relocation[b]={'deterministic_and_relocated':True,'count':count,'external_outputs':[]}
for count in (-1,100000):
 result=subprocess.run([sys.executable,rel/'generator.py','--count',str(count)],capture_output=True,text=True);assert result.returncode!=0
 relocation['invalid-count-'+str(count)]={'returncode':result.returncode,'message':result.stderr[-500:]}
write('packaging.json',{'manifest':manifest,'actual_python':platform.python_version(),'runtime_third_party_imports':[],'checks':relocation,'shared_prose_boundary_validation':'Applied shared validate_generated_record/validate_prose to every prompt, solution, math/text choice and any feedback. No text choices/feedback, diagrams, tables or matrix partition lines occur.','binding':binding})
# Selection analysis uses exact source rule: positive weighted band, uniform pool index.
selection=R/'engine/rust/question_selection.rs';text=selection.read_text();assert 'pool[(uniform(8) * pool.len() as f64) as usize]' in text
write('selection-analysis.json',{'implementation_sha256':hashlib.sha256(selection.read_bytes()).hexdigest(),'source_lines':'engine/rust/question_selection.rs:118-199','captured_basis':read(J/'source/inventory.json')['basis'],'stages_examined':['finite no-replacement catalog; first-three sign selection and fallback when a case is exhausted','shared delivery stages in delivery-summary.json','rated-band filtering and within-band uniform selection, conditional on fresh usable candidates'], 'before_after_cases':{k:v['cases_after'] for k,v in delivery.items()},'positive_weight_band_support':{b:{'eligible':len(allsets['final-'+b+'.json']),'conditional_probability_per_member':1/len(allsets['final-'+b+'.json']),'no_sign_or_numeric_key_filter':True} for b in ('easy','moderate','hard')},'selection_limits':['Unknown future policy weights/history cannot be reproduced from the captured bank. Under configured positive weights each remaining band member has equal conditional probability. Zero-weight bands are excluded by policy; legacy unconfigured policy selects minimum entity ID, not a math outcome.','No claim that generated verification samples were published; live inventory and learner history can reduce fresh candidates.']})
write('audit-summary.json',{'status':'passed','ordinary_records_checked':sum(map(len,allsets.values())),'source_banks_checked':len(replay),'final_ids':final_ids,'native_grading':{k:v for k,v in read(E/'grading-report.json').items() if k!='records'},'final_binding':binding})
(E/'session-state.md').write_text('Finalized repaired package. Independent exact math, displayed solution paths (including negative control), eight source/exemplar replays, delivery of all final/control bands, native grading and relocation pass. Next: render final and counterfactual/matched records, inspect screenshots, quantify conditional shortcut probes, write/validate final report.\n')
print(json.dumps({'status':'passed','ordinary':sum(map(len,allsets.values())),'source_banks':len(replay),'grading_checks':sum(len(x['checks']) for x in cases)}))
