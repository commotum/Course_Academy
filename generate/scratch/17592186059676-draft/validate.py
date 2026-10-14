"""Independent rendered-math, fidelity, baseline and native-grader verification; no EDB."""
from pathlib import Path
import sys,importlib.util,json,re,hashlib,subprocess,copy,itertools
sys.dont_write_bytecode=True
from functools import lru_cache
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
s=importlib.util.spec_from_file_location('draft_tangent',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
x=g.x
def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
@lru_cache(maxsize=None)
def expr(t):
 t=re.sub(r'\\\\(?=(?:frac|sqrt)\b)',r'\\',t)
 t=t.strip().rstrip('.').replace(r'\left','').replace(r'\right','').replace(r'\mathrm{d}',r'\text{d}').replace('⁡','').replace(r'\,','').replace(r'\cdot','*')
 t=re.sub(r'\\operatorname\{(tan|sec|cos|sin|csc|cot)\}',r'\1',t)
 t=re.sub(r'\{(sec|cos|sin|tan|csc|cot)\}',r'\1',t)
 t=re.sub(r'\\(tan|sec|cos|sin|csc|cot)\b',r'\1',t).replace(r'\pi','pi')
 def group(s,i):
  assert s[i]=='{',(s,i)
  d=1;j=i+1
  while d:
   d+=(s[j]=='{')-(s[j]=='}');j+=1
  return s[i+1:j-1],j
 def conv(s):
  out='';i=0
  while i<len(s):
   if s.startswith('\\frac',i) or s.startswith('\\dfrac',i):
    i+=len('\\dfrac') if s.startswith('\\dfrac',i) else len('\\frac');a,i=group(s,i);b,i=group(s,i);out+='(('+conv(a)+')/('+conv(b)+'))'
   elif s.startswith('\\sqrt',i):
    i+=5;a,i=group(s,i);out+='sqrt('+conv(a)+')'
   elif s[i]=='{':a,i=group(s,i);out+='('+conv(a)+')'
   elif s[i]=='^':out+='**';i+=1
   else:out+=s[i];i+=1
  return out
 t=conv(t).replace(' ','')
 # All observed trigonometric functions have one x, numeric, pi, sqrt(x),
 # or parenthesized exact argument; move optional exponents after the call.
 pattern=r'(tan|sec|cos|sin|csc|cot)(?:\*\*(\(\d+\)|\d+))?\s*'
 def trig(m):
  start=m.end();assert start<len(t)
  if t[start]=='(':
   d=1;j=start+1
   while d:d+=(t[j]=='(')-(t[j]==')');j+=1
   arg=t[start:j]
  elif t.startswith('sqrt(',start):
   d=1;j=start+5
   while d:d+=(t[j]=='(')-(t[j]==')');j+=1
   arg=t[start:j]
  else:
   mm=re.match(r'x|pi|\d+',t[start:]);assert mm,(t,start);arg=mm[0];j=start+len(arg)
  return m[1]+'('+arg+')'+('**'+m[2] if m[2] else ''),j
 while (m:=re.search(pattern,t)):
  # Remove the found function from later matching by temporary uppercase.
  val,j=trig(m);t=t[:m.start()]+val.replace(m[1],m[1].upper(),1)+t[j:]
 t=t.lower()
 return parse_expr(t,local_dict={'x':x,'pi':sp.pi,**{n:getattr(sp,n) for n in ('tan','sec','cos','sin','csc','cot','sqrt')}},transformations=standard_transformations+(implicit_multiplication_application,))
@lru_cache(maxsize=None)
def eq(a,b):
 d=sp.expand((a-b).rewrite(sp.cos))
 if d==0:return True
 if x in d.free_symbols:
  for z in (sp.Rational(2,5),sp.Rational(1,3)):
   v=sp.N(d.subs(x,z),30)
   if v.is_real and abs(v)>sp.Float('1e-22'):return False
 return sp.simplify(d)==0

def model(q):
 text=q[':question/problem']
 match=re.search(r'(?:f\(x\)|y)\s*=\s*([^$]+)',text);assert match,text
 f=expr(match[1]);point=None
 m=re.search(r'(?:when|at)\s*\$x\s*=\s*([^$]+)',text)
 if m:point=expr(m[1]);assert point.is_real and sp.simplify(sp.cos(point))!=0
 assert f.has(sp.tan(x)),('expected actual tangent of x, no chain rule',f)
 return f,point

@lru_cache(maxsize=None)
def differential_rhs(rhs):
 rhs=rhs.replace(r'\left','').replace(r'\right','').replace(r'\mathrm{d}',r'\text{d}')
 token=r'\frac{\text{d}}{\text{d}x}'
 rhs=rhs.strip().rstrip('.')
 if token not in rhs:return expr(rhs)
 # Independently evaluate every derivative operator's displayed operand.
 while token in rhs:
  i=rhs.index(token);j=i+len(token)
  assert rhs[j]=='(',('derivative operand missing',rhs)
  d=1;k=j+1
  while d:d+=(rhs[k]=='(')-(rhs[k]==')');k+=1
  operand=expr(rhs[j+1:k-1]);der=sp.diff(operand,x)
  rhs=rhs[:i]+'('+g.tex(der)+')'+rhs[k:]
 return expr(rhs)

def validate(rec):
 q=rec['question'];m=rec['generation'];g.validate_generated_record(rec)
 f,point=model(q);der=sp.diff(f,x);answer=sp.simplify(der.subs(x,point)) if point is not None else der
 assert 'cos(x)!=0' in m['domain']
 if f.has(sp.sqrt(x)):assert 'x>0' in m['domain']
 taskfun=sp.expand(f)
 if point is None:taskfun=taskfun.as_independent(x,as_Add=True)[1]
 expected_fp=g.digest([str(taskfun),str(point)]);assert m['mathematical_fingerprint']==expected_fp,'mathematical fingerprint'
 fs=q[':question/answer-fields'];assert len(fs)==1
 field=fs[0];bank=[expr(a[':answer/value']) for a in field[':answer-field/choices']]
 assert len(set(a[':answer/id'] for a in field[':answer-field/choices']))==len(bank)
 for i in range(len(bank)):
  for j in range(i):assert not eq(bank[i],bank[j]),('duplicate bank',m)
 correct=[a[':answer/id'] for a,v in zip(field[':answer-field/choices'],bank) if eq(v,answer)]
 assert correct==[field[':answer-field/correct'][1]],('wrong bank key',m,answer,bank)
 if field[':answer-field/type'].endswith('/blank'):
  assert len(bank)==1 and '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
 else:assert len(bank)==5
 sol=q[':question/worked-solution'];blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)==(2 if point is not None else 1)
 for bi,block in enumerate(blocks):
  rows=block.split(r'\\')
  required={'q-341495':(4,),'q-47983':(3,),'q-70911':(4,),'q-103081':(2,4),'q-17912':(2,3),'q-341825':(2,4),'q-341858':(2,3),'q-30990':(3,),'q-47905':(3,),'authored-four-term':(3,),'authored-point':(3,3)}
  assert len(rows)==required[m['template']][bi],('wrong operative stage count',m['template'],len(rows))
  lhs=rows[0].split('&')[0].replace(' ','')
  label='f' if 'f(x)' in q[':question/problem'] else 'y'
  simple=lhs.replace(r'\text{d}','d').replace('{','').replace('}','').replace('^','').replace('′',"'")
  assert simple.startswith(label+"'") or simple==r'\frac'+'d'+label+'dx',('wrong differentiated label',simple,label)
  if bi==1:
   ml=re.search(r'(?:′|\')\}?\((.*?)\)',lhs);assert ml,('missing prime point',lhs)
   assert eq(expr(ml[1]),point),('stale prime point',lhs,point)
  elif '(' in lhs and r'\frac' not in lhs:
   assert '(x)' in lhs,('wrong prime input',lhs)
  expected=der if bi==0 else answer
  required_formals={'q-341495':((1,2,0,0),),'q-47983':((1,0,0),),'q-70911':((1,1,0,0),),'q-103081':((1,0),(0,0,0,0)),'q-17912':((1,0),(0,0,0)),'q-341825':((1,0),(0,0,0,0)),'q-341858':((1,0),(0,0,0)),'q-30990':((1,2,0),),'q-47905':((1,2,0),),'authored-four-term':((1,4,0),),'authored-point':((1,2,0),(0,0,0))}
  for ri,row in enumerate(rows):
   assert re.search(r'&\s*=',row),('unreadable operative row',row)
   rhs=re.split(r'&\s*=',row,maxsplit=1)[1]
   normalized_rhs=rhs.replace(r'\mathrm{d}',r'\text{d}')
   assert normalized_rhs.count(r'\frac{\text{d}}{\text{d}x}')==required_formals[m['template']][bi][ri],('changed operative derivative structure',m['template'],bi,ri)
   value=differential_rhs(rhs)
   assert eq(value,expected),('incorrect worked stage',m['template'],m['parameters'],bi,rhs,value,expected)
 if 'Therefore' in sol:
  vals=re.findall(r'(?:is|slope is)\s*\$([^$]+)\$',sol)
  assert vals and eq(expr(vals[-1]),answer),('wrong conclusion',sol)
 return {'function':str(f),'point':str(point),'derivative':str(der),'answer':str(answer),'stages':sum(len(b.split(r'\\')) for b in blocks)}

def native(label,rec):
 field=rec['question'][':question/answer-fields'][0];bank=field[':answer-field/choices']
 if field[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'actual ID radio field'} for a in bank]
 else:
  val=bank[0][':answer/value'];z=expr(val)
  equivalent=sp.sstr(z.subs(sp.sec(x),1/sp.cos(x))).replace('**','^')
  checks=[{'submitted':val,'expected':'accepted','purpose':'canonical bare TeX blank'},{'submitted':'('+val+')','expected':'accepted','purpose':'parenthesized equivalent blank'},{'submitted':equivalent,'expected':'accepted','purpose':'cosine-form equivalent blank'},{'submitted':val+'+1','expected':'rejected','purpose':'incorrect blank'},{'submitted':sp.sstr(z+2).replace('**','^'),'expected':'rejected','purpose':'independently formed wrong blank'}]
 return {'label':label,'record':rec,'checks':checks}
def baseline():
 original=ROOT/'generate/scratch/17592186059676';actual=[original.with_suffix('.py')]+sorted(p for p in original.rglob('*') if p.is_file())
 current={str(p.relative_to(ROOT)):sha(p) for p in actual};saved=json.load(open(HERE/'registered-baseline.json'))['files']
 assert current==saved,'numeric baseline pathset/hash changed'
 return {'passed':True,'files':len(current),'pathset_and_hashes_unchanged':True}
def build():
 harness=ROOT/'generate/runs/current/check-engine.rs';local=HERE/'check-engine.rs';local.write_bytes(harness.read_bytes())
 deps=ROOT/'target/release/deps';edb=ROOT.parent/'EDB/target/release/deps';libs={name:max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')}
 cmd=['rustc','--edition=2024','-O',str(local)]
 for name,p in libs.items():cmd+=['--extern',name+'='+str(p)]
 cmd+=['-L','dependency='+str(edb),'-L','dependency='+str(deps),'-o',str(HERE/'check-current-engine')];subprocess.run(cmd,check=True)
 save('engine-build.json',{'harness_sha256':sha(local),'libraries':{str(p):sha(p) for p in libs.values()},'executable_sha256':sha(HERE/'check-current-engine'),'entry_point':'course_academy_engine::learning::grade_field','database_writes':0})

def main():
 initial=baseline()
 subprocess.run([sys.executable,str(HERE/'validate-cli.py')],check=True)
 for name,info in json.load(open(HERE/'frozen-snapshots.json')).items():
  assert sha(HERE/name)==info['sha256']==sha(ROOT/info['frozen_path']) and json.load(open(HERE/name))['basis']==2275
 inventory_wrapper=json.load(open(HERE/'independent-inventory.json'));assert inventory_wrapper['basis']==2275 and inventory_wrapper['lineage']==g.LINEAGE
 inventory=inventory_wrapper['questions'];independent=[q for q in g.SOURCE['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
 assert [q['record'] for q in inventory]==independent and all(q['role']=='independently authored inventory' and q['relationship_to_source_templates'] for q in inventory)
 build();inputs=[];checks=[];replay=[];mappings=[];reviews=[];counts={l:set() for l in g.SUPPORTED_LEVELS};slotcoverage={}
 # Exact source attrs/omissions replay, including unrated records, independent inventory separate.
 for sid,old in g.SOURCES.items():
  raw=g.generate(g.PROFILES[sid][0],template=sid,profile='observed_raw');assert raw['question']==old
  r=g.generate(g.PROFILES[sid][0],0,sid,g.PROFILES[sid][1]);result=validate(r);new=r['question'];of=old[':question/answer-fields'][0];nf=new[':question/answer-fields'][0]
  ov=[expr(a[':answer/value']) for a in of[':answer-field/choices']];nv=[expr(a[':answer/value']) for a in nf[':answer-field/choices']]
  matched=[next(i for i,v in enumerate(nv) if eq(z,v)) for z in ov];assert len(set(matched))==len(ov)
  if sid in g.ORIGINALS:
   assert new[':question/problem']==g.normalize_prose(old[':question/problem']);assert new[':question/worked-solution']==g.normalize_prose(old[':question/worked-solution'])
   assert matched.index(next(i for i,a in enumerate(nf[':answer-field/choices']) if a[':answer/id']==nf[':answer-field/correct'][1]))==next(i for i,a in enumerate(of[':answer-field/choices']) if a[':answer/id']==of[':answer-field/correct'][':answer/id'])
  replay.append({'source':sid,'raw_exact_record_attrs_and_omissions':True,'complete_mathematical_bank_match':True,'matched_choices':len(matched),'worked_solution_exact':sid in g.ORIGINALS,'omitted_solution':':question/worked-solution' not in old,'omitted_difficulty':':question/difficulty' not in old,'omitted_key':':answer-field/correct' not in of,'normal_authored_repairs':sid not in g.ORIGINALS,'normal_bank_command_escape_repairs':sum(a[':answer/value']!=g.clean(a[':answer/value']) for a in of[':answer-field/choices'])})
  mappings.append({'source':sid,'field':of[':answer-field/id'],'profile':sid,'choices':[{'source_answer_id':a[':answer/id'],'raw_value':a[':answer/value'],'symbolic_recipe_at_source':str(z),'generated_slot':i,'correct_designation':a[':answer/id']==of.get(':answer-field/correct',{}).get(':answer/id') if ':answer-field/correct' in of else 'absent'} for a,z,i in zip(of[':answer-field/choices'],ov,matched)]})
  reviews.append('## '+sid+'\n\nRaw original\n\n'+old[':question/problem']+'\n\n'+old.get(':question/worked-solution','[worked solution absent]')+'\n\nNormal source-parameter instance\n\n'+g.markdown(r)+'\n\nChanged coefficient instance\n\n'+g.markdown(g.generate(g.PROFILES[sid][0],41,sid)))
 # Bounded exhaustive source patterns and authored point/hard templates. Both authored field contracts.
 for level,templates in g.LEVEL_TEMPLATES.items():
  for sid in templates:
   slotcoverage[sid]={}
   print('validating',level,sid,flush=True)
   for p in g.parameters_for(sid):
    kinds=('radio','blank') if sid.startswith('authored-') else (None,)
    for kind in kinds:
     try:r=g.generate(level,12,sid,p,field_type=kind)
     except ValueError:continue
     result=validate(r);assert g.generate(level,999,sid,p,field_type=kind)['question']==r['question']
     counts[level].add(r['generation']['mathematical_fingerprint']);checks.append({'template':sid,'parameters':p,'field_type':kind or r['question'][':question/answer-fields'][0][':answer-field/type'],'rendered_math':result});inputs.append(native(sid+' '+str(p)+' '+str(kind),r))
     for k,v in p.items():slotcoverage[sid].setdefault(k,set()).add(v)
 # Explicit invalid bounds/schema inputs.
 invalid=[]
 for level,templates in g.LEVEL_TEMPLATES.items():
  for sid in templates:
   p=next(g.parameters_for(sid))
   for key in p:
    for value in (0,999,1.5):
     pp=dict(p);pp[key]=value
     try:g.generate(level,template=sid,parameters=pp)
     except ValueError:invalid.append([sid,key,value]);continue
     # point=0 is valid, and coefficients n/a=1 may be deliberately invalid.
     assert key=='point' and value==0
 # Mutation controls inspect actual math and operative rows even after refreshing fingerprint.
 mutations=[]
 for sid,level in [('q-341495','easy'),('q-70911','easy'),('q-103081','moderate'),('authored-point','moderate'),('authored-four-term','hard')]:
  r=g.generate(level,13,sid,field_type='blank' if sid.startswith('authored-') else None)
  sol=r['question'][':question/worked-solution']
  def formal_mutation(q):
   text=q[':question/worked-solution'];begin=text.index(r'\begin{aligned}')
   j=text.index(r'\frac',begin);operand=text.index('(',j);q[':question/worked-solution']=text[:operand+1]+'x+'+text[operand+1:]
  def single_stage(q):
   text=q[':question/worked-solution'];begin=text.index(r'\begin{aligned}');j=text.index(r'\\',begin);k=text.index(r'\\',j+2) if text.count(r'\\',begin)>=2 else text.index(r'\end{aligned}',j)
   q[':question/worked-solution']=text[:j]+text[k:]
  edits=[('formal_input',formal_mutation),('single_operative_stage_removed',single_stage),('wrong_key',lambda q:q[':question/answer-fields'][0].update({':answer-field/correct':[':answer/id','bad-id']})),('domain',lambda q:None)]
  for name,edit in edits:
   rr=copy.deepcopy(r);edit(rr['question'])
   if name=='domain':rr['generation']['domain']='all reals'
   try:validate(rr)
   except (AssertionError,ValueError,TypeError,IndexError,KeyError):mutations.append({'template':sid,'mutation':name,'rejected':True});continue
   raise AssertionError(('mutation survived',sid,name))
 # Point-change examples hold coefficients fixed and vary actual supplied evaluation target.
 a=g.generate('moderate',template='authored-point',parameters={'a':2,'b':3,'point':1},field_type='blank');b=g.generate('moderate',template='authored-point',parameters={'a':2,'b':3,'point':0},field_type='blank');validate(a);validate(b)
 assert a['generation']['mathematical_fingerprint']!=b['generation']['mathematical_fingerprint'];save('changed-input.json',{'point_only':[a,b]})
 save('native-input.json',inputs);subprocess.run([str(HERE/'check-current-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 native_report=json.load(open(HERE/'native-grading.json'));assert native_report['documented_unresolved_checks']==0
 save('source-replay.json',{'basis':2275,'raw_exact_records':9,'complete_mathematical_banks':9,'source_choices_matched':sum(z['matched_choices'] for z in replay),'captured_correct_designations':7,'absent_keys_explicit_authorship':2,'exact_captured_solutions':7,'absent_solutions':2,'independent_inventory_records':3,'cases':replay})
 save('source-choice-mapping.json',mappings);save('mathematical-validation.json',checks);save('structural-mutations.json',mutations)
 save('previews.json',{l:g.batch(l,5,7) for l in g.SUPPORTED_LEVELS});(HERE/'review.md').write_text('\n\n'.join(reviews)+'\n\n## Authored hard\n\n'+g.markdown(g.generate('hard',23))+'\n\n## Authored point-slot variants\n\n'+g.markdown(a)+'\n\n'+g.markdown(b)+'\n')
 final=baseline();summary={'passed':True,'basis':2275,'all_levels':list(g.SUPPORTED_LEVELS),'source_fidelity':json.load(open(HERE/'source-replay.json')),'bounded_eligible_instances':len(checks),'distinct_mathematical_tasks_by_level':{l:len(v) for l,v in counts.items()},'slot_coverage':{sid:{k:sorted(v) for k,v in slots.items()} for sid,slots in slotcoverage.items()},'invalid_inputs_rejected':len(invalid),'structural_mutations_rejected':len(mutations),'native_grading':{k:native_report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks','entry_point','database_writes')},'registered_baseline':final,'engine_build':json.load(open(HERE/'engine-build.json'))}
 save('validation.json',summary);print(json.dumps({k:v for k,v in summary.items() if k not in ('slot_coverage','source_fidelity','engine_build')},indent=2))
if __name__=='__main__':main()
