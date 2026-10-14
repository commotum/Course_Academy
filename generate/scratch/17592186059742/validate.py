#!/usr/bin/env python3
"""Private fail-closed independent checks on actual printed operand/stage mathematics."""
import collections,copy,hashlib,importlib.util,itertools,json,re,shutil,subprocess,sys,uuid
from pathlib import Path
import sympy as S
R=Path(__file__).resolve().parent;ROOT=R.parents[2]
spec=importlib.util.spec_from_file_location('lmc',R.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def require(c,m):
 if not c:raise AssertionError(m)
def parse(t):
 t=t.strip()
 while '\\frac' in t:
  z=re.search(r'\\frac\{(-?\d+)\}\{(\d+)\}',t);require(z,'rational syntax '+t);t=t[:z.start()]+'('+z[1]+'/'+z[2]+')'+t[z.end():]
 t=t.replace(r'\cdot','*');require(re.fullmatch(r'[\d+*/()\-\s]+',t) is not None,'unparsed scalar '+t)
 return S.sympify(t)
def cells(s):return [x.strip()for x in re.split(r'&|\\\\',s)]
def mats(s):return re.findall(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',s,re.S)
def shape(s):return [len(x.split('&'))for x in s.split('\\\\')]
def balanced(t):
 require(t.count('$')%2==0,'math delimiters');depth=0
 for c in t:
  require(ord(c)>=32 or c in '\n\t','control character');depth+=(c=='{')-(c=='}');require(depth>=0,'braces')
 require(depth==0,'braces balanced')
def independent(rec):
 q=rec['question'];meta=rec['generation'];name=meta['template'];r,c=g.TEMPLATES[name][1:3];raw=meta['evidence_only'];p=meta['parameters'];g.guard(name,p)
 require(set(rec['knowledge_point'])=={'db_id','id','title'},'outer shape');uuid.UUID(q[':question/id']);balanced(q[':question/problem'])
 text=q[':question/problem'];given=mats(text);require(len(given)==2 and all(shape(z)==[c]*r for z in given),'prompt two supplied matrices')
 A,B=[[parse(x)for x in cells(z)]for z in given];a,b=S.Rational(p['a']),S.Rational(p['b']);op=p['op'];n,m=p['names']
 expr=re.search(r'Calculate \$(.*?)\$, where',text)[1];require(expr.replace(' ','')==g.term(a,n)+op+g.term(b,m),'actual requested coefficients/names')
 require(re.search(r'\$'+n+r'\s*=\s*\\begin',text) and re.search(r'\$'+m+r'\s*=\s*\\begin',text),'matrix label assignment')
 require(A==[S.Rational(x)for row in p['A']for x in row] and B==[S.Rational(x)for row in p['B']for x in row],'actual printed operands vs parameters')
 X=[a*x for x in A];Y=[b*x for x in B];C=[x+y if op=='+'else x-y for x,y in zip(X,Y)]
 if ':question/worked-solution'in q:
  sol=q[':question/worked-solution'];balanced(sol);st=mats(sol);require(len(st)==8,'2+2+2+1+1 stage matrices');require(all(shape(z)==[c]*r for z in st),'stage shapes')
  require([parse(x)for x in cells(st[0])]==A and [parse(x)for x in cells(st[1])]==B,'stage one supplied operands')
  for k,(factor,operands)in enumerate(((a,A),(b,B))):
   for tok,v in zip(cells(st[2+k]),operands):
    parts=tok.split(r'\cdot');require(len(parts)==2 and parse(parts[0])==factor and parse(parts[1])==v,'ordered explicit entry products')
  require([parse(x)for x in cells(st[4])]==X and [parse(x)for x in cells(st[5])]==Y,'evaluated products')
  require(all(r'\cdot'not in x and not re.search(r'\d[+*]',x) for z in st[4:6]for x in cells(z)),'evaluated stage remains scalars')
  # Unevaluated combination stage must expose both evaluated operands in order.
  def local_tex(x):return S.latex(x)
  def operand(x):return '('+local_tex(x)+')'if x<0 else local_tex(x)
  expected=[]
  for x,y in zip(X,Y):
   expected.append(local_tex(x)+'-'+local_tex(-y)if name=='partial_blank'and op=='+'and y<0 else local_tex(x)+op+operand(y))
  require(cells(st[6])==expected,'single ordered entrywise combination mask')
  require([parse(x)for x in cells(st[6])]==C and [parse(x)for x in cells(st[7])]==C,'all operative final values')
  skeleton=re.sub(r'\\begin\{bmatrix\}.*?\\end\{bmatrix\}',lambda z:'M'+str(0),sol,flags=re.S)
  tail=skeleton.split(r'\begin{aligned}',1)[1].split(r'\end{aligned}',1)[0];rows=tail.split(r'\\  & =');require(len(rows)==5,'five ordered solution stages')
  require(rows[0].startswith(g.term(a,n)+op+g.term(b,m)+' & ='),'initial solution matches requested expression')
  expected_patterns=[g.group(a)+'M0'+op+g.tex(b)+'M0','M0'+op+'M0','M0'+op+'M0','M0','M0'];require([z.split('& =',1)[-1].strip()for z in rows]==expected_patterns,'scaled operands and matrix combination structures')
  intro=f"We multiply each entry of ${n}$ by ${local_tex(a)}$ and each entry of ${m}$ by ${local_tex(b)},$ and then {'add'if op=='+'else 'subtract'} the resulting matrices, as follows:"
  require(sol.split('\n\n')[0]==intro,'actual-instance instructional prose')
 fs=q.get(':question/answer-fields',[])
 if fs and fs[0][':answer-field/type'].endswith('/blank'):
  target=p.get('targets',list(range(4)));require(len(fs)==4,'four blank fields')
  if name=='row_blank':
   table=text.split('\n\n')[1];tokens=re.findall(r'\{\{field-\d\}\}',table);require(tokens==['{{field-'+str(i+1)+'}}'for i in range(4)],'row blank ordered target cells')
   columns=[x.strip()for x in table.splitlines()[0].split('|')[1:-1]];require(columns[2:6]==tokens and len(columns)==7,'row blank field layout')
  if name=='partial_blank':
   table=text.split('\n\n')[1];table_cells=re.findall(r'\{\{field-\d\}\}|\$(-?\d+)\$',table) # Independently read table cells with token scan below.
   tokens=re.findall(r'\{\{field-\d\}\}|\$-?\d+\$',table);require(len(tokens)==6,'four requested two supplied cells')
   lines=table.splitlines();top=[x.strip()for x in lines[0].split('|')[1:-1]];bottom=[x.strip()for x in lines[2].split('|')[1:-1]]
   require(len(top)==len(bottom)==6,'table column count');require(top[2:5]==tokens[:3],'top target positions')
   require(bottom[(1 if raw else 2):(4 if raw else 5)]==tokens[3:],'bottom target column roles')
   for j,tok in enumerate(tokens):
    require(tok=='{{field-'+str(target.index(j)+1)+'}}'if j in target else parse(tok.strip('$'))==C[j],'actual target/given table consistency')
  for f in fs:
   key=f[':answer-field/key'];idx=int(key[-1])-1;require('{{'+key+'}}'in text,'blank placeholder');require(parse(f[':answer-field/choices'][0][':answer/value'])==C[target[idx]],'blank target key')
 else:
  for f in fs:
   require(all(len(mats(z[':answer/value']))==1 for z in f[':answer-field/choices']),'whole matrix answer');vv=[[parse(x)for x in cells(mats(z[':answer/value'])[0])]for z in f[':answer-field/choices']];require(len(vv)==5 and len({tuple(x)for x in vv})==5,'every whole-bank pair distinct');require(sum(x==C for x in vv)==1,'one mathematically correct option')
 for f in fs:
  uuid.UUID(f[':answer-field/id'])
  for z in f[':answer-field/choices']:uuid.UUID(z[':answer/id']);require(z[':answer/type']==':answer.type/math'and'$'not in z[':answer/value'],'owned answer schema')
  if ':answer-field/correct'in f:
   correct=f[':answer-field/correct'];require(correct[0]==':answer/id','lookup shape');z=next((z for z in f[':answer-field/choices']if z[':answer/id']==correct[1]),None);require(z is not None,'owned correct ref')
   if f[':answer-field/type'].endswith('/radio'):require([parse(x)for x in cells(mats(z[':answer/value'])[0])]==C,'radio key')
 rendered=[z[':answer/value']for f in fs for z in f[':answer-field/choices']]
 expected_hash=g.digest({'version':g.VERSION,'level':q.get(':question/difficulty','').split('/')[-1]or None,'problem':text,'solution':q.get(':question/worked-solution'),'bank':sorted(rendered),'fields_present':':question/answer-fields'in q,'correct_present':all(':answer-field/correct'in f for f in fs) if fs else True})
 # Fieldless evidence has no correct reference attribute; its identity uses presence=False.
 if not fs:expected_hash=g.digest({'version':g.VERSION,'level':q.get(':question/difficulty','').split('/')[-1]or None,'problem':text,'solution':q.get(':question/worked-solution'),'bank':[],'fields_present':False,'correct_present':True})
 require(meta['content_hash']==expected_hash and q[':question/id']==g.ident(expected_hash),'actual content identity')
 actual_task={'A':[[str(x)for x in A[j*c:(j+1)*c]]for j in range(r)],'B':[[str(x)for x in B[j*c:(j+1)*c]]for j in range(r)],'a':str(a),'signed_b':str(b*(1 if op=='+'else -1)),'targets':p.get('targets',list(range(r*c)))if g.TEMPLATES[name][3]=='blank'else'whole','response':g.TEMPLATES[name][3]}
 require(meta['math_fingerprint']==g.digest(actual_task),'actual operative math fingerprint')
 require(meta['eligible_for_learning']==(not raw),'raw evidence eligibility');return C

def failure(fn,label):
 try:fn()
 except(ValueError,AssertionError):return
 raise AssertionError('negative control passed '+label)
source_path=ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186059742.json';shutil.copyfile(source_path,R/'source.json');source=json.loads(source_path.read_text());original={q[':question/math-academy-id']:q for q in source['record'][':knowledge-point/questions']};cases=[];replays=[];details=[]
for name,t in g.TEMPLATES.items():
 if not t[4]:continue
 case={'source_id':t[4],'level':t[0],'template':name,'parameters':g.DEFAULTS[name],'bank_profile':'observed-'+t[4]};cases.append(case);rec=g.generate(case['level'],template=name,parameters=case['parameters'],profile=case['bank_profile']);independent(rec);replays.append(rec);q=rec['question'];old=original[t[4]]
 for attr in (':question/difficulty',':question/worked-solution',':question/answer-fields'):require((attr in q)==(attr in old),'source presence '+t[4]+' '+attr)
 require(q[':question/problem']==old[':question/problem'],'source prompt '+t[4]);require(q.get(':question/worked-solution')==old.get(':question/worked-solution'),'entire source solution '+t[4])
 oldfs={f[':answer-field/key']:f for f in old.get(':question/answer-fields',[])};newfs={f[':answer-field/key']:f for f in q.get(':question/answer-fields',[])};require(oldfs.keys()==newfs.keys(),'source field keys')
 for key,of in oldfs.items():
  nf=newfs[key];require(nf[':answer-field/type']==of[':answer-field/type'][':db/ident'],'source field type');require((':answer-field/correct'in of)==(':answer-field/correct'in nf),'correct presence')
  require(sorted(a[':answer/value']for a in of[':answer-field/choices'])==sorted(a[':answer/value']for a in nf[':answer-field/choices']),'every source choice exact')
  if ':answer-field/correct'in of:require(next(a[':answer/value']for a in nf[':answer-field/choices']if a[':answer/id']==nf[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value'],'source designation')
 details.append({'source_id':t[4],'prompt_exact':True,'all_available_fields_values_refs_and_solution_exact':True,'missing_attributes':[attr for attr in (':question/difficulty',':question/worked-solution',':question/answer-fields')if attr not in old]})
(R/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
records=[];variants=[];capacity=collections.defaultdict(set);slots=set();families=collections.Counter()
for name,t in g.TEMPLATES.items():
 for seed in range(100):
  rec=g.generate(t[0],seed=seed,template=name);independent(rec);records.append(rec);capacity[t[0]].add(rec['generation']['math_fingerprint']);families[name]+=1
  if name=='partial_blank':slots.add(tuple(rec['generation']['parameters']['targets']))
  if seed<2:variants.append(rec)
 if t[4]and name!='subtract_square':
  for seed in range(10):
   rec=g.generate(t[0],seed=500+seed,template=name,profile='observed-'+t[4]);independent(rec);records.append(rec)
   if seed<2:variants.append(rec)
# Default sampler covers all supported shapes before sampling their values.
default_families={level:sorted({g.generate(level,s)['generation']['template']for s in range(100)})for level in ('easy','moderate','hard')};require(all(set(v)=={n for n,t in g.TEMPLATES.items()if t[0]==k}for k,v in default_families.items()),'default family coverage')
# Hold matrices/scalars fixed, move the four requested cells; all 15 role-equivalent masks.
for targets in itertools.combinations(range(6),4):
 p=copy.deepcopy(g.DEFAULTS['partial_blank']);p['targets']=list(targets);rec=g.generate_hard(template='partial_blank',parameters=p);independent(rec);records.append(rec)
 require(rec['generation']['math_fingerprint']!=g.generate_hard(template='partial_blank',parameters=g.DEFAULTS['partial_blank'])['generation']['math_fingerprint']or list(targets)==[0,2,4,5],'target fingerprint')
negative=0
for name in g.TEMPLATES:
 p=copy.deepcopy(g.DEFAULTS[name]);p['a']='0';failure(lambda:g.generate(g.TEMPLATES[name][0],template=name,parameters=p),'zero coefficient');negative+=1
for name in ('easy_integer','row_blank','partial_blank'):
 p=copy.deepcopy(g.DEFAULTS[name]);p['A'][0][0]=100;failure(lambda:g.generate(g.TEMPLATES[name][0],template=name,parameters=p),'bounds');negative+=1
for name in ('half_plus','rect_radio','partial_blank'):
 base=g.generate(g.TEMPLATES[name][0],template=name,parameters=g.DEFAULTS[name]);C=independent(base)
 for mutation in ('product','evaluated','combine','final','prose','control','answer','id'):
  bad=copy.deepcopy(base);q=bad['question'];sol=q[':question/worked-solution'];mm=mats(sol)
  if mutation in ('product','evaluated','combine','final'):
   index={'product':2,'evaluated':4,'combine':6,'final':7}[mutation];old=mm[index];replacement=old.replace(cells(old)[0],tex:=str(C[0]+99),1)if mutation!='combine'else g.matrix(list(map(g.tex,C)),g.TEMPLATES[name][1],g.TEMPLATES[name][2]);q[':question/worked-solution']=sol.replace(r'\begin{bmatrix}'+old+r'\end{bmatrix}',r'\begin{bmatrix}'+replacement+r'\end{bmatrix}',1)
  elif mutation=='prose':q[':question/worked-solution']=sol.replace('multiply','divide',1)
  elif mutation=='control':q[':question/problem']+='\x0c'
  elif mutation=='answer':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='999'
  else:q[':question/answer-fields'][0][':answer-field/correct'][1]=str(uuid.uuid4())
  failure(lambda:independent(bad),mutation);negative+=1
p=copy.deepcopy(g.DEFAULTS['partial_blank']);p['targets']=[0,1,3,5];bad=g.generate_hard(template='partial_blank',parameters=p);bad['question'][':question/problem']=g.generate_hard(template='partial_blank',parameters=g.DEFAULTS['partial_blank'])['question'][':question/problem'];failure(lambda:independent(bad),'stale target with fixed matrices');negative+=1
# Seed and choice order do not change identity; all changed operative stages validated above.
for case in cases:
 a=g.generate(case['level'],1,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);b=g.generate(case['level'],9,template=case['template'],parameters=case['parameters'],profile=case['bank_profile']);require(a['question'][':question/id']==b['question'][':question/id'],'stable identity')
engine=[]
anchors=[g.generate(case['level'],template=case['template'],parameters=case['parameters'])for case in cases]
for rec in anchors:independent(rec)
for i,rec in enumerate(anchors+replays+variants+records[::25]):
 if any(':answer-field/correct'not in f for f in rec['question'].get(':question/answer-fields',[]))or ':question/answer-fields'not in rec['question']:continue
 checks=[]
 for j,f in enumerate(rec['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   checks.extend({'field_index':j,'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==f[':answer-field/correct'][1]else'rejected','purpose':'owned radio answer'}for a in f[':answer-field/choices'])
  else:
   value=f[':answer-field/choices'][0][':answer/value'];target=rec['generation']['parameters'].get('targets',list(range(4)))[j];p=rec['generation']['parameters'];A=[x for row in p['A']for x in row];B=[x for row in p['B']for x in row];equivalent='('+p['a']+')*('+A[target]+')'+p['op']+'('+p['b']+')*('+B[target]+')'
   checks.extend({'field_index':j,'submitted':v,'expected':expected,'purpose':purpose}for v,expected,purpose in ((value,'accepted','canonical scalar'),(equivalent,'accepted','genuine unreduced scalar products'),('('+value+')+1','rejected','wrong scalar')))
 engine.append({'label':str(i),'record':rec,'checks':checks})
(R/'engine-input.json').write_text(json.dumps(engine,indent=2));binary=ROOT/'generate/runs/current/check-engine';run=subprocess.run([str(binary),str(R/'engine-input.json'),str(R/'engine-report.json')],capture_output=True,text=True);(R/'engine.log').write_text(run.stdout+run.stderr);require(run.returncode==0,'native engine '+run.stderr)
report={'status':'worker_validation_pass','not_parent_qa':True,'source':{k:source[k]for k in ('database','basis','lineage')},'sources':8,'exact_prompts':8,'exact_available_solutions':5,'available_source_solutions':5,'complete_source_banks':7,'source_values_matched':33,'available_correct_designations_matched':11,'missing_correct_designations':2,'fieldless_sources':1,'unrated_sources':2,'source_details':details,'checked_generated_instances':len(records),'capacity':json.loads((R/'level-capacity.json').read_text()),'unique_sampled_tasks_by_level':{k:len(v)for k,v in capacity.items()},'default_family_coverage':default_families,'partial_target_masks_sampled':len(slots),'partial_target_masks_exhausted_fixed_operands':15,'negative_controls':negative,'native':json.loads((R/'engine-report.json').read_text()),'script_sha256':hashlib.sha256(R.with_suffix('.py').read_bytes()).hexdigest(),'engine_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'runtime':{'python':sys.version.split()[0],'sympy':S.__version__},'unresolved':['Original q-11536 and q-126009 compound distractor intention underidentified; public opaque evidence profiles retain operand-projection masks; normal authored method banks used.','No easy source difficulty exists; easy is an authored nonnegative eight-product four-sum workload.','Calculator metadata absent in supplemental 86-record snapshot; unknown, no flag inferred.']}
(R/'validation.json').write_text(json.dumps(report,indent=2)+'\n');(R/'review.json').write_text(json.dumps({'original_replays':replays,'generated_variants':variants},indent=2)+'\n');print(json.dumps({k:v for k,v in report.items()if k!='native'},indent=2))
