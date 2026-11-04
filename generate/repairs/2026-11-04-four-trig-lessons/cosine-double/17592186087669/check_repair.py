"""Read visible TeX independently of generation metadata and runtime answer recipes."""
from pathlib import Path
import collections,hashlib,importlib.util,json,math,os,shutil,subprocess,sys,tempfile
H=Path(__file__).resolve().parent
ROOT=next(p for p in H.parents if (p/'generate/principles.md').exists())
AUDIT=ROOT/'reference/edb-math/audits/2026-11-04-four-trig-lessons'
sys.path.insert(0,str(AUDIT));sys.path.insert(0,str(H))
from numeric_audit import audit,Numeric,nodes,target,field_key
# Reuse the independent audit's equality reader without its top-level database-snapshot runner.
code=(AUDIT/'solutions_audit.py').read_text().split('\nresults=[]')[0]
namespace={'__file__':str(AUDIT/'solutions_audit.py')};exec(compile(code,str(AUDIT/'solutions_audit.py'),'exec'),namespace)
solution_check=namespace['check']
import generator as g
KP=str(g.KP if isinstance(g.KP,int) else g.KP['db_id'])
E=H/'evidence';E.mkdir(exist_ok=True)
results=[];all_records=[];sample_refs=[]
for band in ('easy','moderate','hard'):
 for seed in (71,204):
  argv=[sys.executable,str(H/'generator.py'),'--difficulty',band,'--count','5','--seed',str(seed),'--format','json']
  payload=subprocess.check_output(argv); assert payload==subprocess.check_output(argv),'non-deterministic CLI'
  records=json.loads(payload);assert len(records)==5
  (E/f'{band}-{seed}.json').write_bytes(payload);sample_refs.append(f'evidence/{band}-{seed}.json')
  assert len({r['question'][':question/problem'] for r in records})==len(records)
  for i,r in enumerate(records):
   q=r['question'];label=f'{band}-{seed}/{i}'
   v=audit(q,label,KP);assert v['status']=='match' and not v['choice_ambiguities'],v
   sol=solution_check(q,label,KP);assert not sol['suspected_bad_equalities'] and not sol['unparsed_equalities'],sol
   f=q[':question/answer-fields'][0]; vals=[Numeric(nodes(a[':answer/value']),{}).evaluate() for a in f[':answer-field/choices']]
   assert len(vals)==1 or all(abs(x-y)>1e-9 for j,x in enumerate(vals) for y in vals[:j]),'equal-valued choices'
   assert not any(w in q[':question/problem'].lower() for w in ('use the','recall','identity','substitute'))
   if KP.endswith(('669','670')):
    assert '^4' not in q[':question/problem'] and '^{4}' not in q[':question/problem']
    import re
    arg=re.search(r'\\(?:cos|sin)(?:\^\{?\d\}?)?\\left\((.*?)\\right\)',target(q)).group(1)
    degrees=Numeric(nodes(arg),{}).evaluate()*180/math.pi
    assert abs(degrees/30-round(degrees/30))>1e-8 and abs(degrees/45-round(degrees/45))>1e-8,('original standard-angle bypass',degrees)
    if band=='hard':
     visible=nodes(target(q))
     proper=any(n[0]=='frac' and 0<Numeric((n,),{}).evaluate()<1 for n in visible)
     assert proper or visible[0]==('char','-'),('hard adds no fractional/reordering demand',target(q))
   if KP.endswith('671'):
    expr=target(q); numeric_nodes=nodes(expr)
    # Visible original angle extracted independently: evaluate first sin/cos argument using parser structure.
    import re
    a=re.search(r'\\(?:cos|sin)(?:\^\{?\d\}?)?\\left\((.*?)\\right\)',expr).group(1)
    angle=Numeric(nodes(a),{}).evaluate()*180/math.pi
    assert all(abs(angle-s)>1e-8 for s in (0,30,45,60,90,120,135,150,180)),angle
    assert abs(Numeric(nodes(field_key(f)),{}).evaluate())>1e-9
   results.append({'label':label,'numeric':v,'solution_equality_checks':sol['checks']})
   all_records.append(r)
# Relocation with only declared runtime closure, from an unrelated working directory.
closure=['generator.py','math_format.py']+(['source-replay.json'] if KP.endswith('670') else ['replay-data.json'] if KP.endswith('671') else [])
with tempfile.TemporaryDirectory(prefix='cosine-double-portable-') as tmp:
 for f in closure:shutil.copyfile(H/f,Path(tmp)/f)
 for band in ('easy','moderate','hard'):
  actual=subprocess.check_output([sys.executable,str(Path(tmp)/'generator.py'),'--difficulty',band,'--count','5','--seed','71','--format','json'],cwd='/tmp')
  assert actual==(E/f'{band}-71.json').read_bytes(),('relocation',band)
# Original source families at source parameters; no defective bank copied to valid output.
source=json.loads((AUDIT/'kps'/KP/'kp.json').read_text())
byid={q[':db/id']:q for q in source[':knowledge-point/questions']+[source[':knowledge-point/canonical-example']]}
source_records=[]
if KP.endswith('669'):
 cases=[(17592186345258,'easy',14,'deg','rational',1),(17592186598626,'easy',g.F(2,5),'rad','rational',1),(17592186598584,'easy',g.F(5,6),'rad','rational',1),(17592186660919,'easy',41,'deg','rational',1),(17592186256392,'moderate',g.F(1,8),'rad','rational',2),(17592186256393,'moderate',35,'deg','sqrt',3),(17592186256394,'moderate',38,'deg','rational',g.F(5,2)),(17592186256395,'moderate',16,'deg','rational',5),(17592186345214,'moderate',g.F(1,12),'rad','rational',3)]
 for sid,band,x,unit,kind,n in cases:
  for profile in g.PROFILES:
   try:r=g.construct(band,'difference',x,unit,kind,n,profile);break
   except ValueError:continue
  original=Numeric(nodes(target(byid[sid])),{}).evaluate();new=Numeric(nodes(target(r['question'])),{}).evaluate();assert abs(original-new)<1e-9
  r['generation']['controlled_source_case']=sid;source_records.append(r)
elif KP.endswith('670'):
 source_records=g.replay_sources()
 assert not ({17592186598566,17592186345265}&{r['generation']['source_question_ids'][0] for r in source_records})
else:
 source_records=g.source_replay()
 assert 'q-332151' not in {r['generation']['source_ids'][0] for r in source_records}
 # Constructor-level regression: weak old stored angle and its 45-degree analogue must reject.
 for d in (90,270):
  try:g.make('hard',d,'square','degrees','blank')
  except ValueError:pass
  else:raise AssertionError('Known-angle hard bypass still constructible')
 assert 'difference' in {r['generation']['template'] for r in all_records if r['question'][':question/difficulty'].endswith('/moderate')}
source_checks=[]
for i,r in enumerate(source_records):
 v=audit(r['question'],f'source/{i}',KP);assert v['status']=='match' and not v['choice_ambiguities'],v
 sol=solution_check(r['question'],f'source/{i}',KP);assert not sol['suspected_bad_equalities'] and not sol['unparsed_equalities'],sol
 source_checks.append(v)
(E/'source-family-cases.json').write_text(json.dumps(source_records,indent=2))
# Visible bank-only cue measurement: ranks/position independent of generator profiles.
probes={}
for band in ('easy','moderate','hard'):
 rr=[r for r in all_records if r['question'][':question/difficulty'].endswith('/'+band)]
 for family in sorted({r['generation']['template'] for r in rr}):
  group=[r for r in rr if r['generation']['template']==family];positions=[];ranks=[]
  for r in group:
   f=r['question'][':question/answer-fields'][0]
   if not f[':answer-field/type'].endswith('/radio'):continue
   ch=f[':answer-field/choices'];idx=next(i for i,a in enumerate(ch) if a[':answer/id']==f[':answer-field/correct'][1]);vals=[Numeric(nodes(a[':answer/value']),{}).evaluate() for a in ch]
   positions.append(idx);ranks.append(sorted(range(len(vals)),key=lambda i:vals[i]).index(idx))
  probes[band+'/'+family]={'radio_count':len(positions),'correct_positions':dict(collections.Counter(positions)),'correct_numeric_ranks':dict(collections.Counter(ranks))}
(E/'all-samples.json').write_text(json.dumps(all_records,indent=2))
summary={'kp':KP,'cli_records':len(all_records),'deterministic_cli_calls':6,'relocated_bands':3,'independent_math_and_choice_checks':len(results),'solution_equalities':sum(x['solution_equality_checks'] for x in results),'source_family_cases':len(source_checks),'source_checks':source_checks,'samples':sample_refs,'bank_only_observations':probes,'limits':['Numerical witnesses and equality parsing independently inspect displayed TeX, not a symbolic proof of all future outputs.','Native learner grading and actual UI rendering are root reviewer responsibilities.','Live publication/deduplication was not performed by this isolated author workspace.']}
(E/'validation-results.json').write_text(json.dumps(summary,indent=2))
(E/'math-checks.json').write_text(json.dumps(results,indent=2))
manifest={'entrypoint':'generator.py','runtime_files':closure,'dependencies':{'python':sys.version.split()[0],'packages':{}},'offline':True,'assets':[],'sha256':{f:hashlib.sha256((H/f).read_bytes()).hexdigest() for f in closure}}
(H/'runtime-manifest.json').write_text(json.dumps(manifest,indent=2))
print(json.dumps({k:summary[k] for k in ('kp','cli_records','solution_equalities','source_family_cases','relocated_bands')}))
