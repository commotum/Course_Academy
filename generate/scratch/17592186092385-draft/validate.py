#!/usr/bin/env python3
"""Standalone private rendered readback, full banks, domain and actual native grading."""
import sys
sys.dont_write_bytecode=True
import importlib.util,json,hashlib,copy,subprocess,collections
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
def load(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=load('generator',H.with_suffix('.py'));p=load('frozen_private_readback',H/'private_readback.py')
def save(name,value):(H/name).write_text(json.dumps(value,indent=2)+'\n')
def baseline():
 b=json.loads((H/'registered-baseline.json').read_text());paths=[Path('generate/scratch/17592186092385.py')]+sorted(x for x in Path('generate/scratch/17592186092385').rglob('*') if x.is_file());assert list(map(str,paths))==b['pathset']
 for path in paths:assert hashlib.sha256(path.read_bytes()).hexdigest()==b['files'][str(path)],str(path)
 return {'status':'unchanged','files':len(paths)}
def checks(r):
 out=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('radio'):
   out.extend({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every complete owned coordinate option'} for a in f[':answer-field/choices'])
  else:
   value=f[':answer-field/choices'][0][':answer/value'];a=p.expression(value)
   tests=[(value,'accepted','Canonical coordinate'),('('+value+r')\cdot2/2','accepted','Equivalent exact coordinate'),('0','accepted' if a==0 else 'rejected','Ordinary numeric 0'),('1','accepted' if a==1 else 'rejected','Ordinary numeric 1'),(g.tex(a+1),'rejected','Correct coordinate plus 1')]
   out.extend({'field_index':i,'submitted':z,'expected':e,'purpose':purpose} for z,e,purpose in tests)
 return out

def validate_record(r):
 g.fmt.validate_generated_record(copy.deepcopy(r));assert r['generation']['content_hash']==g.content_hash(r['question']);info=p.validate(r['question']);m=r['generation']
 if m['parameters']:
  assert m['domain']==info['domain'];actual=p.actual(r['question']);assert m['mathematical_fingerprint']==g.digest([p.sp.srepr(actual[0]),str(actual[1]),actual[7]])
 if m['profile']=='authored' and r['question'][':question/answer-fields'][0][':answer-field/type'].endswith('radio'):
  # Read the printed curve first; derive every companion error line independently.
  f,px,y0,tangent,normal,b,a,axis,dom=p.actual(r['question'])
  slopes=[normal,tangent,1/tangent,normal,normal];shifts=[px,px,px,0,px];ordinates=[y0,y0,y0,y0,0]
  expected=[p.sp.simplify(-(y-slope*shift)/slope) if axis=='x' else p.sp.simplify(y-slope*shift) for slope,shift,y in zip(slopes,shifts,ordinates)]
  choices=r['question'][':question/answer-fields'][0][':answer-field/choices'];assert len(choices)==5
  for answer,want in zip(choices,expected):
   point=tuple(map(p.expression,answer[':answer/value'].strip('()').split(',')));p.equality(point[0],want if axis=='x' else p.sp.Integer(0),dom);p.equality(point[1],p.sp.Integer(0) if axis=='x' else want,dom)
 return info

def mutation_controls(records):
 r=next(r for r in records if r['generation']['template']=='q-10871' and r['generation']['parameters']=={'scale':1,'point':1,'axis':'x'})
 cases=[]
 def rejected(label,part,old,new):
  z=copy.deepcopy(r);text=z['question'][part];assert old in text,(label,old);z['question'][part]=text.replace(old,new,1)
  try:p.validate(z['question'])
  except (AssertionError,ValueError,TypeError,IndexError,AttributeError):cases.append({'mutation':label,'rejected':True})
  else:raise AssertionError('Undetected '+label)
 rejected('printed function differs',':question/problem','2 x^{2} + x','2 x^{2} + 2 x')
 rejected('formal derivative input differs',':question/worked-solution',"f'(x)","f'(1)")
 rejected('derivative operator input adds invisible constant',':question/worked-solution','(2 x^{2} + x)','(2 x^{2} + x+1)')
 rejected('slope evaluation target differs',':question/worked-solution',"m=f'(1)","m=f'(2)")
 rejected('substituted intermediate is wrong',':question/worked-solution','4 (1) + 1','4 (1) + 2')
 rejected('normal equation stale',':question/worked-solution','y-(3)','y-(4)')
 rejected('changed requested axis leaves stale worked solution',':question/problem','intersects the $x$-axis','intersects the $y$-axis')
 rejected('intercept axis operation differs',':question/worked-solution','setting $y=0$','setting $x=0$')
 z=copy.deepcopy(r);f=z['question'][':question/answer-fields'][0];f[':answer-field/choices'][1][':answer/value']=f[':answer-field/choices'][0][':answer/value']
 try:p.validate(z['question'])
 except AssertionError:cases.append({'mutation':'complete point bank duplicates correct point','rejected':True})
 else:raise AssertionError('Undetected bank mutation')
 z=copy.deepcopy(r);field=z['question'][':question/answer-fields'][0];correct=p.expression(field[':answer-field/choices'][0][':answer/value'].strip('()').split(',')[0]);field[':answer-field/choices'][1][':answer/value']='('+g.tex(correct+1)+',0)';z['generation']['content_hash']=g.content_hash(z['question'])
 try:validate_record(z)
 except AssertionError:cases.append({'mutation':'replace tangent-line distractor with generic correct+1 while retaining a unique correct bank','rejected':True})
 else:raise AssertionError('Undetected offset recipe substitution')
 return cases

def main():
 base=baseline();fidelity=[];sourcecases=[];served=[];independent=[];raws=[]
 for mid,raw in g.ROWS.items():
  r=g.source_replay(mid);assert r['question']==raw;raws.append(r);info=p.validate(raw,allow_missing=True)
  case={'source_id':mid,'origin':'Math Academy original' if mid.startswith('q-') else 'non-MA later generated','raw':r,'readback':info,'exact_prompt':True,'exact_solution':True,'exact_full_field_records_and_feedback':True,'presence_parity':True}
  if mid.startswith('nonMA-'):independent.append(case)
  else:fidelity.append({'source':mid,'exact_prompt':True,'exact_solution':True,'exact_banks_and_feedback':True,'field_count':len(raw.get(':question/answer-fields',[])),'values':sum(len(f.get(':answer-field/choices',[])) for f in raw.get(':question/answer-fields',[]))})
  try:sr=g.source_replay(mid,'observed_served')
  except ValueError as exc:case['served_exclusion']=str(exc)
  else:validate_record(sr);served.append(sr);case['served']=sr
  sourcecases.append(case)
 allnormal=[];capacity={};review=[]
 for level in g.SUPPORTED_LEVELS:
  pertype={}
  for ft in ('radio','blank'):
   records=g.catalog(level,ft)
   for r in records:validate_record(r)
   assert records
   pertype[ft]={'records':len(records),'distinct_math_tasks':len({r['generation']['mathematical_fingerprint'] for r in records}),'templates':dict(collections.Counter(r['generation']['template'] for r in records)),'axes':dict(collections.Counter(r['generation']['parameters']['axis'] for r in records)),'points_by_template':{t:sorted({r['generation']['parameters']['point'] for r in records if r['generation']['template']==t}) for t in g.NORMAL_TEMPLATES[level]}}
   if ft=='radio':
    present={(r['generation']['template'],r['generation']['parameters']['scale'],r['generation']['parameters']['point'],r['generation']['parameters']['axis']) for r in records}
    pertype[ft]['rejected_complete_bank_parameters']=[{'template':t,'scale':sc,'point':pt,'axis':axis,'reason':'Authored complete bank has equivalent/duplicate/correct distractor'} for t in g.NORMAL_TEMPLATES[level] for sc in range(1,9) for pt in g.points(t) for axis in ('x','y') if (t,sc,pt,axis) not in present]
   for bad in pertype.get('radio',{}).get('rejected_complete_bank_parameters',[]) if ft=='radio' else []:
    pp={k:bad[k] for k in ('scale','point','axis')}
    for fn,args in [(g.generate,(level,)),(getattr(g,'generate_'+level),())]:
     try:fn(*args,template=bad['template'],parameters=pp,profile='authored',field_type='radio')
     except ValueError:pass
     else:raise AssertionError('Degenerate error profile escaped explicit normal API')
   allnormal.extend(records)
   assert len(g.batch(level,999,17,field_type=ft))==pertype[ft]['distinct_math_tasks']
   assert g.batch(level,5,33,field_type=ft)==g.batch(level,5,33,field_type=ft)
   examples=[]
   for axis in ('x','y'):
    examples.append(next(r for r in records if r['generation']['parameters']['axis']==axis and r['generation']['parameters']['point']==g.points(r['generation']['template'])[1]))
   review.extend(examples)
  for seed in range(50):
   validate_record(g.generate(level,seed));validate_record(g.generate(level,seed,field_type='blank'))
  capacity[level]=pertype
 # Complete observed banks are selected together at fixed target and varying scale.
 bankvariants=[]
 for t in ('q-10871','q-11124','q-104073','q-104075'):
  for scale in range(1,9):
   r=g.generate(g.SPECS[t][3],template=t,parameters={'scale':scale,'point':g.SPECS[t][1],'axis':g.SPECS[t][2]},profile='source_bank');validate_record(r);bankvariants.append(r)
   if scale==1:
    raw=g.ROWS[t];rf=r['question'][':question/answer-fields'][0];sf=raw[':question/answer-fields'][0]
    assert sorted(a[':answer/value'].replace(' ','') for a in rf[':answer-field/choices'])==sorted(a[':answer/value'].replace(' ','') for a in sf[':answer-field/choices'])
 # All normal API no-field originals fail closed, independently of seed/parameters.
 exclusions=[]
 for t in ('q-10878','q-71542'):
  for fn,args in [(g.generate,('easy',)),(g.generate_easy,())]:
   for profile in ('authored','source_bank','observed_served'):
    try:fn(*args,template=t,profile=profile)
    except ValueError:pass
    else:raise AssertionError('Excluded field contract escaped')
  exclusions.append({'source':t,'reason':'No captured answer-field contract; raw replay only','all_normal_apis_fail_closed':True})
 boundary=[]
 for level in g.SUPPORTED_LEVELS:
  t=g.NORMAL_TEMPLATES[level][0]
  for bad in ({'scale':0,'point':g.points(t)[0],'axis':'x'},{'scale':9,'point':g.points(t)[0],'axis':'x'},{'scale':1,'point':-1,'axis':'x'},{'scale':1,'point':g.points(t)[0],'axis':'z'}):
   try:g.generate(level,template=t,parameters=bad)
   except ValueError:boundary.append({'level':level,'parameters':bad,'rejected':True})
   else:raise AssertionError('Outside domain accepted')
 controls=mutation_controls(allnormal)
 cli=[]
 for ft in ('radio','blank'):
  command=[sys.executable,str(H.with_suffix('.py')),'--difficulty','all','--count','5','--seed','7','--field-type',ft,'--format','json'];result=subprocess.run(command,check=True,capture_output=True,text=True);rows=json.loads(result.stdout);assert len(rows)==15 and collections.Counter(r['question'][':question/difficulty'].split('/')[-1] for r in rows)=={'easy':5,'moderate':5,'hard':5}
  for row in rows:validate_record(row)
  cli.append({'field_type':ft,'format':'json','records':len(rows),'all_levels':True})
 result=subprocess.run([sys.executable,str(H.with_suffix('.py')),'--difficulty','all','--count','1','--format','markdown'],check=True,capture_output=True,text=True);assert result.stdout.count('Find where the normal line to the curve')==3;cli.append({'field_type':'radio','format':'markdown','records':3,'all_levels':True})
 native_records=served+allnormal+bankvariants
 native=[{'label':str(i)+':'+r['generation']['template'],'record':r,'checks':checks(r)} for i,r in enumerate(native_records)]
 save('engine-input.json',native)
 checker=ROOT/'generate/runs/current/check-engine';assert hashlib.sha256(checker.read_bytes()).hexdigest()=='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
 subprocess.run([str(checker),str(H/'engine-input.json'),str(H/'engine-validation.json')],check=True)
 native_report=json.loads((H/'engine-validation.json').read_text());assert native_report['documented_unresolved_checks']==0
 save('source-cases.json',sourcecases);save('independent-inventory.json',independent);save('source-fidelity.json',fidelity);save('capacity.json',capacity);save('review.json',{'originals':raws,'served_replays':served,'normal_examples':review,'source_bank_examples':[r for r in bankvariants if r['generation']['parameters']['scale'] in (1,8)]})
 result={'status':'pass','approval_status':'working; root independent QA required','basis':2275,'registered_baseline':base,'ma_originals':len(fidelity),'ma_exact_prompts':len(fidelity),'ma_exact_solutions':len(fidelity),'ma_answer_values':sum(a['values'] for a in fidelity),'non_ma_inventory':len(independent),'served_source_replays':len(served),'normal_records':len(allnormal),'distinct_normal_math_tasks':len({r['generation']['mathematical_fingerprint'] for r in allnormal}),'source_bank_variants':len(bankvariants),'capacity':capacity,'source_exclusions':exclusions,'native':{k:native_report[k] for k in ('entry_point','accepted_checks','rejected_checks','documented_unresolved_checks','database_writes')},'native_records':len(native_records),'mutation_controls':controls,'cli_all_validation':cli,'boundary_controls':boundary,'default_seeds_checked_per_level_and_field':50,'private_parser_sha256':hashlib.sha256((H/'private_readback.py').read_bytes()).hexdigest()}
 save('validation.json',result);assert baseline()==base;print(json.dumps(result,indent=2))
if __name__=='__main__':main()
