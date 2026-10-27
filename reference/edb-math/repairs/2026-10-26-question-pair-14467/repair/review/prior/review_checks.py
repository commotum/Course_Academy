"""Independent displayed-equation audit. Run with repo .venv/bin/python; no DB writes."""
import copy, hashlib, importlib.util, json, pathlib, random, re, shutil, subprocess, sys
from collections import Counter
from fractions import Fraction as F
E=pathlib.Path(__file__).resolve().parent; J=E.parent
R=pathlib.Path('/home/jake/Developer/Course_Academy'); W=J/'workspace'; PY=R/'.venv/bin/python'
sys.path.insert(0,str(W)); import generator as g
sys.path.insert(0,str(R)); from scripts.question_capture.math_format import normalize_prose,normalize_tex,validate_prose,validate_math_boundaries,validate_tex

def save(n,a): (E/n).write_text(json.dumps(a,indent=2,ensure_ascii=False)+'\n')
def load(p): return json.loads(pathlib.Path(p).read_text())
def run(argv,name):
 r=subprocess.run(list(map(str,argv)),capture_output=True,text=True);save(name,{'argv':list(map(str,argv)),'returncode':r.returncode,'stdout':r.stdout,'stderr':r.stderr}); assert r.returncode==0,(name,r.stderr[-1500:]);return r

def coeff(expr):
 expr=re.sub(r'\\(?:dfrac|frac)\{(-?\d+)\}\{(\d+)\}',r'\1/\2',expr).replace(' ','').replace('&','').strip().rstrip('.,?')
 assert re.fullmatch(r'[+\-0-9/xy]+',expr),expr
 out=[F(0),F(0),F(0)]
 for t in re.findall(r'[+-]?[^+-]+',expr):
  v=t[-1] if t[-1] in 'xy' else None; k=t[:-1] if v else t
  z=F(1) if k in ('','+') else F(-1) if k=='-' else F(k)
  out[{'x':0,'y':1,None:2}[v]]+=z
 return out

def line(text):
 l,r=text.split('=');a,b=coeff(l),coeff(r);A,B,C=[x-y for x,y in zip(a,b)];assert B!=0,text;return -A/B,-C/B

def observe(rec):
 q=rec['question'];field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];given=next(t for t in re.findall(r'\$([^$]+)\$',q[':question/problem']) if '=' in t);m,b=line(given)
 values=[line(c[':answer/value']) for c in choices];valid=[i for i,(n,c) in enumerate(values) if n==m and c!=b];assert len(valid)==1,(given,values)
 correct=field[':answer-field/correct'];cid=correct[1] if isinstance(correct,list) else correct[':answer/id'];target=next(i for i,c in enumerate(choices) if c[':answer/id']==cid);assert valid==[target],(valid,target)
 assert len(set(values))==len(values)
 return {'id':q[':question/id'],'given':given,'slope':str(m),'intercept':str(b),'lines':[[str(x),str(y)] for x,y in values],'target':target,'key':choices[target][':answer/value'],'coincident':[i for i,x in enumerate(values) if x==(m,b)],'fraction':m.denominator>1,'negative':m<0}

def boundary(rec):
 q=rec['question'];texts=[q[':question/problem'],q[':question/worked-solution']]
 for f in q[':question/answer-fields']:
  for c in f[':answer-field/choices']:
   kind=c[':answer/type'];kind=kind.get(':db/ident') if isinstance(kind,dict) else kind
   if kind==':answer.type/text':texts.append(c[':answer/value'])
   else:validate_tex(c[':answer/value'])
   for key in (':answer/feedback',':answer/explanation'):
    if c.get(key):texts.append(c[key])
 for t in texts:
  validate_prose(t);validate_math_boundaries(t,strict=True)
  assert not re.search(r'\*\*\s|\s\*\*|\*\s+\*',t),repr(t)
 return len(texts)

def scope(rec):
 o=observe(rec);q=rec['question'];s=q[':question/worked-solution'];level=q[':question/difficulty'].split('/')[-1]
 displays=re.findall(r'\$\$(.*?)\$\$',s,re.S);conversions=[]
 # Verify every displayed isolation row describes the given geometric line.
 for block in displays:
  if '\\begin{aligned}' not in block:continue
  rows=re.sub(r'\\(?:begin|end)\{aligned\}','',block).strip().split('\\\\')
  for row in rows:
   row=row.strip();
   if not row:continue
   if '\\Longrightarrow' in row:
    left,right=row.split(r'\quad\Longrightarrow\quad');left=left.replace('&','').strip();right=right.strip()
    assert line(left)==line(right),(left,right)
    conversions.append({'rule':'Solve the candidate linear equation for y','scope_source':'Prerequisite e-13979; same algebra on candidates is an authored repetition of the target operation.','shown_step':row,'status':'passed'})
   else:
    assert line(row)==(F(o['slope']),F(o['intercept'])),row
    conversions.append({'rule':'Move the x term and divide both sides by the y coefficient','scope_source':'e-14367 and prerequisite e-13979','shown_step':row,'status':'passed'})
 if level!='easy':
  for c in q[':question/answer-fields'][0][':answer-field/choices']:
   assert any(c[':answer/value'] in z['shown_step'] and '\\Longrightarrow' in z['shown_step'] for z in conversions),c
 if o['coincident']:assert 'same line' in s and 'intercept' in s and 'not a distinct' in s
 # Answer is selected as displayed; no unseen reverse algebra required.
 assert o['key'] in s
 return {'template':level+' / radio complete line','field_key':'selection','final_expression':o['key'],'keyed_answer':o['key'],'domain':'Distinct nonvertical real lines; nonzero slopes in the supported signed integer/familiar-rational pool.','conclusion':'All displayed isolation and candidate conversion rows preserve the equation; slope/intercept criterion identifies exactly this displayed choice.','status':'passed','conversions':conversions}

binding=load(E/'final-binding.json'); batches={};rows={};paths=[]
for band,b in binding['verification_batches'].items():
 p=J/('samples.json' if band=='easy' else 'samples-'+band+'.json'); raw=p.read_bytes();assert hashlib.sha256(json.dumps(json.loads(raw),sort_keys=True,separators=(',',':')).encode()).hexdigest()==b['batch_hash'];records=json.loads(raw);assert len(records)==b['count']==5
 save('final-'+band+'.json',records);batches[band]=records;rows[band]=[]
 for i,r in enumerate(records):
  boundary(r);o=observe(r);o['sample_index']=i;rows[band].append(o);c=scope(r);c['sample_refs']=['final-'+band+'.json'];paths.append(c)
save('final-observations.json',rows)
# Independent control samples; fresh seeds chosen for this audit, not author tests.
controls={};measure={}
for band in ('easy','moderate','hard'):
 seed=90731+('easy','moderate','hard').index(band);records=g.batch(band,24,seed);assert records==g.batch(band,24,seed)
 save('control-'+band+'.json',records);controls[band]=records
 obs=[]
 for r in records:boundary(r);obs.append(observe(r));c=scope(r);c['sample_refs']=['control-'+band+'.json'];paths.append(c)
 measure[band]={'seed':seed,'count':len(records),'positive':sum(not o['negative'] for o in obs),'negative':sum(o['negative'] for o in obs),'fractional':sum(o['fraction'] for o in obs),'target_positions':dict(Counter(o['target'] for o in obs)),'given_zero_intercepts':sum(F(o['intercept'])==0 for o in obs)}
save('control-observations.json',measure)
# Complete source and exemplar replay: compare full prompt, solution and entire answer bank.
source=load(J/'source/source.json');kp=source['material']['kp'];ex=load(J/'investigation/published-exemplars.json');sources=kp[':knowledge-point/questions']+ex
replays=[];replay_result=[]
for src in sources:
 if not src.get(':question/worked-solution') or not src.get(':question/answer-fields',[{}])[0].get(':answer-field/correct'):continue
 sid=src[':question/id'];r=g.replay(sid);q=r['question'];assert q[':question/problem']==normalize_prose(src[':question/problem']);assert q[':question/worked-solution']==normalize_prose(src[':question/worked-solution'])
 assert [c[':answer/value'] for c in q[':question/answer-fields'][0][':answer-field/choices']]==[normalize_tex(c[':answer/value']) for c in src[':question/answer-fields'][0][':answer-field/choices']]
 boundary(r);observe(r);replays.append(r);replay_result.append({'source_id':sid,'full_prompt_solution_bank':'matched normalized source','math':'passed'})
partial=[]
for src in kp[':knowledge-point/questions']:
 if src.get(':question/worked-solution'):continue
 given=re.findall(r'\$([^$]+)\$',src[':question/problem'])[0];m,b=line(given);cs=src[':question/answer-fields'][0][':answer-field/choices'];match=[c[':answer/value'] for c in cs if line(c[':answer/value'])[0]==m];assert len(match)==1;partial.append({'source_id':src[':question/id'],'given':given,'independently_inferred_match':match[0],'note':'Partial imported record unchanged; not represented as complete source replay.'})
canonical=kp[':knowledge-point/canonical-example'];assert line('12x-y=3')[0]==line('y=12x+1')[0];save('source-replay.json',{'replayed':replay_result,'partial_evidence':partial,'canonical':{'source_id':canonical[':question/id'],'given':'12x-y=3','candidates':['y=4x-8','y=12x+1','y=3x-12'],'unique_match':'II','solution_isolation':['12x-y=3','-y=-12x+3','y=12x-3']}});save('source-replay-records.json',replays)
# Controlled pairs: fixed visible bank, changed target, and irrelevant equation scaling.
pairs=[];pair_rows=[]
for band in ('easy','moderate','hard'):
 bank=g.make_bank(band,random.Random(1967)); eligible=[i for i,c in enumerate(bank) if band!='hard' or sum(d['m']==c['m'] for d in bank)==2]
 target=eligible[0];other=next(i for i in eligible if i!=target and (band!='hard' or bank[i]['m']==bank[target]['m']))
 def given(t):
  m=bank[t]['m'];b=next(c['b'] for i,c in enumerate(bank) if i!=t and c['m']==m) if band=='hard' else next(F(k) for k in range(-5,6) if F(k)!=bank[t]['b']);return m,b,1
 before=g.record(band,given(target),bank,target,1967);after=g.record(band,given(other),bank,other,1967);scaled=g.record(band,(*given(target)[:2],-3),bank,target,1967)
 for r in (before,after,scaled):boundary(r);observe(r);c=scope(r);c['sample_refs']=['counterfactual-records.json'];paths.append(c)
 ids=[r['question'][':question/answer-fields'][0][':answer-field/correct'][1] for r in (before,after,scaled)]
 assert observe(before)['target']!=observe(after)['target'];assert observe(before)['target']==observe(scaled)['target']; assert [c[':answer/value'] for c in before['question'][':question/answer-fields'][0][':answer-field/choices']]==[c[':answer/value'] for c in after['question'][':question/answer-fields'][0][':answer-field/choices']]
 pair_rows.append({'band':band,'indices':[len(pairs),len(pairs)+1,len(pairs)+2],'relevant':'Change only given target slope/intercept; hard swaps coincidence within the same slope pair.','expected_targets':[target,other,target],'observed_targets':[observe(r)['target'] for r in (before,after,scaled)],'irrelevant':'Multiply the given equation by -3; preserve geometric line and target.'});pairs.extend([before,after,scaled])
save('counterfactual-records.json',pairs);save('counterfactual-tests.json',pair_rows)
# Scope negative witness: algebraic equivalence alone must not accept a missing normalization.
neg=copy.deepcopy(batches['moderate'][0]);key=observe(neg)['key'];sol=neg['question'][':question/worked-solution'];start=sol.index('Rewrite the choices');end=sol.index('\n\n',sol.index('\\end{aligned}',start));neg['question'][':question/worked-solution']=sol[:start]+sol[end:];caught=False
try:scope(neg)
except AssertionError:caught=True
assert caught;save('scope-negative-control.json',{'record':neg,'equivalent_key':key,'expected':'reject unshown candidate conversion','observed':'rejected by independent displayed-path check','passed':True})
save('solution-paths.json',{'cases':paths,'negative_control':'scope-negative-control.json'})
# Genuine grader: every option of final batches, source replays, controls and counterfactuals.
cases=[]
for label,records in [('final-'+b,rs) for b,rs in batches.items()]+[('controls-'+b,rs) for b,rs in controls.items()]+[('counterfactual',pairs),('replay',replays)]:
 for i,r in enumerate(records):
  o=observe(r);cs=r['question'][':question/answer-fields'][0][':answer-field/choices'];cases.append({'label':label+':'+str(i),'record':r,'checks':[{'field_index':0,'submitted_answer_id':c[':answer/id'],'expected':'accepted' if n==o['target'] else 'rejected','purpose':'independent slope/distinctness criterion, not stored-key assumption'} for n,c in enumerate(cs)]})
save('grader-input.json',cases)
run([R/'generate/runs/current/check-engine',E/'grader-input.json',E/'grading.json'],'grading-command.json')
# Packaging: exact declared runtime, clean relocated CLI, no unintended files, replay and rejection.
manifest=load(W/'package.json');assert manifest['dependencies']=={'python':sys.version.split()[0],'packages':{}}
rel=E/'relocated-package';rel.mkdir(exist_ok=True)
for f in manifest['files']:shutil.copy2(W/f,rel/f)
package_tests=[]
for band,b in binding['verification_batches'].items():
 argv=[PY,'-I',rel/manifest['entrypoint'],'--difficulty',band,'--count','5','--seed',str(b['seed'])]
 # -I excludes script directory, so normal isolated packaging uses empty env + normal Python script sys.path.
 argv.remove('-I');p=subprocess.run(list(map(str,argv)),capture_output=True,text=True,cwd=rel,env={'PATH':'/usr/bin:/bin','PYTHONDONTWRITEBYTECODE':'1'});assert p.returncode==0,p.stderr;assert json.loads(p.stdout)==batches[band];package_tests.append({'band':band,'argv':list(map(str,argv)),'replay_identical':True})
for args in (['--count','0'],['--difficulty','unsupported']):
 p=subprocess.run([str(PY),str(rel/manifest['entrypoint']),*args],capture_output=True,text=True);assert p.returncode!=0;package_tests.append({'args':args,'rejected':True,'stderr':p.stderr})
assert {p.name for p in rel.iterdir()}<=set(manifest['files'])|{'__pycache__'}
save('packaging.json',{'runtime':sys.version.split()[0],'dependencies':manifest['dependencies'],'declared_files':manifest['files'],'tests':package_tests,'external_outputs':'none; stdout JSON only','generation_rejection':'Inspection: all finite sampled banks have distinct slope/intercept pairs; intercept choice excludes coincidence; hard eligible targets are exactly members of the two slope pairs. Only content-ID duplicates are rejected. No mathematical regions silently filtered.','command':str(PY)+' '+str(E/'review_checks.py')})
# Render every final item and the controlled pairs, plus one replay per response representation.
render_records=sum([batches[b] for b in ('easy','moderate','hard')],[])+pairs+[replays[0],replays[-2],replays[-1]]
save('render-records.json',render_records)
save('math-checks.json',{'passed':True,'final_counts':{k:len(v) for k,v in batches.items()},'control_counts':{k:len(v) for k,v in controls.items()},'counterfactual_count':len(pairs),'replay_count':len(replays),'method':'Parse displayed equations with rational arithmetic independently of generation metadata; compare unique distinct equal-slope candidates and every displayed algebra row.','boundary':'Shared validate_prose and strict validate_math_boundaries on every prompt, solution, text choice and feedback; validate_tex on all math choices.','scope_negative_control':'scope-negative-control.json'})
(E/'session-state.md').write_text('Finalized package; independent exact math, source replay, solution paths, counterfactuals, native grader and relocation checks completed. Rendering and delivered-pool shortcut checks next.\n')
print(json.dumps({'math':'passed','final_records':15,'control_records':72,'grader_cases':len(cases),'render_records':len(render_records),'coverage':measure},indent=2))
