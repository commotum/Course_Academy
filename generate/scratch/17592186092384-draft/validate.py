#!/usr/bin/env python3
"""Private displayed operand/target/readback audit and frozen native grade_field."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
def module(name,path):
 sp=importlib.util.spec_from_file_location(name,path);obj=importlib.util.module_from_spec(sp);sp.loader.exec_module(obj);return obj
g=module('normal_generator',H.with_suffix('.py'));p=module('private_tex_parser',H/'math_parser.py');x=p.x
SHA='71d435e31aa0cdea66d992aa4d4bd1043cdd871aaffc7a3af9f54e9b0f846dea'
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def save(n,obj):(H/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False,default=str)+'\n')
def equal(a,b):
 diff=s.simplify(a-b)
 return diff==0 or s.simplify(diff.subs(x,s.Symbol('positive_read_x',positive=True)))==0

def prompt(q):
 text=q[':question/problem'];fraw=re.search(r'\$y\s*=([^$]*)\$',text)[1].rstrip('.,');F=p.scalar(fraw)
 raw=re.search(r'at the point \$\((.*?)\)',text)[1];u,v=raw.split(',');t,y=map(p.scalar,(u,v));assert equal(F.subs(x,t),y),'Printed point off curve'
 assert 'slope' in text and 'normal line' in text
 return F,t,y

def normalize(z):
 z=z.strip().rstrip('.,').replace('′',"'").replace(r'\prime',"'").replace(r'\,','').replace(r'\cdot','*')
 z=re.sub(r'\{([fm])\}',r'\1',z);z=re.sub(r"\^\{(')\}",r'\1',z)
 z=z.replace(r'\text{d}', 'd').replace(' ', '')
 return z

def math_value(raw,F,t,m):
 z=normalize(raw);D=r'\frac{d}{dx}'
 # Parse actual bound operator and operand; this is not a string skip.
 if z.startswith(D):
  operand=z[len(D):];assert operand.startswith('(') and operand.endswith(')'),('Missing derivative operand',z)
  obj=p.scalar(operand[1:-1]);assert equal(obj,F),'Actual formal operand differs from printed f';return s.diff(obj,x)
 # Substitutions are read from the displayed target; f'(x), f'(point), m, m'.
 def derivative(match):
  arg=p.scalar(match[1]);return '('+s.sstr(s.diff(F,x).subs(x,arg))+')'
 z=re.sub(r"f'\(([^()]*)\)",derivative,z)
 z=re.sub(r'f\(([^()]*)\)',lambda match:'('+s.sstr(F.subs(x,p.scalar(match[1])))+')',z)
 z=z.replace("m'",'('+s.sstr(-1/m)+')');z=re.sub(r'(?<![A-Za-z])m(?![A-Za-z])','('+s.sstr(m)+')',z)
 # Parser input stays printed TeX; only exact values computed from printed givens
 # are inserted as TeX to prevent Python ** grammar from leaking into parser.
 z=z.replace('**','^')
 return p.scalar(z)

def solution(q,F,t,y):
 work=q[':question/worked-solution'];d=s.diff(F,x);m=s.simplify(d.subs(x,t));count=0
 declared=re.search(r'\$f\(x\)\s*=([^$]*)\$',work);assert declared and equal(p.scalar(declared[1]),F),'Wrong f operand'
 blocks=re.findall(r'\$\$\s*(.*?)\s*\$\$',work,re.S);assert len(blocks)==3
 for i,b in enumerate(blocks):
  z=re.sub(r'\\(?:begin|end)\{aligned\}','',b)
  rows=z.split(r'\\');previous=None
  for row in rows:
   row=row.strip().replace('&','');pieces=row.split('=');assert len(pieces)>=2
   if not pieces[0].strip():assert previous is not None;pieces=pieces[1:];values=[previous]+[math_value(v,F,t,m) for v in pieces]
   else:values=[math_value(v,F,t,m) for v in pieces]
   assert all(equal(a,b) for a,b in zip(values,values[1:])),('False displayed chain',row,values)
   previous=values[-1];count+=len(values)-1
  first=normalize(rows[0].replace('&','')).split('=')[0]
  if i==0:assert first=="f'(x)",('Formal derivative target',first)
  if i==1:
   # Source q103531 etc target f'(point); scalar m is optional.
   match=re.search(r"f'\(([^()]*)\)",normalize(rows[0]));assert match and equal(p.scalar(match[1]),t),('Evaluation target',first)
   assert equal(previous,m)
  if i==2:assert first=="m'" and equal(previous,-1/m),'Normal target/negative reciprocal'
 points=re.findall(r'point \$\((.*?)\)',work)
 for point in points:
  u,v=point.split(',');assert equal(p.scalar(u),t) and equal(p.scalar(v),y),'Stale solution point'
 for arg in re.findall(r"f'\(([^()]*)\)",normalize(work)):
  a=p.scalar(arg);assert equal(a,x) or equal(a,t),'Stale derivative target in prose'
 return count

def independent(r):
 q=r['question'];assert not r['generation']['evidence_only'] and r['generation']['eligible_for_learning']
 g.fmt.validate_generated_record(copy.deepcopy(r));F,t,y=prompt(q);d=s.diff(F,x);m=s.simplify(d.subs(x,t));a=s.simplify(-1/m)
 assert a.is_finite and m!=0
 exponents=[v.as_powers_dict().get(x,s.Integer(0)) for v in s.expand(s.powdenest(F,force=True)).as_ordered_terms()]
 domain='x>0' if any(e.is_Rational and e.q!=1 for e in exponents) else 'x!=0' if any(e<0 for e in exponents) else 'real x'
 assert r['generation']['domain']==domain,'Domain mismatches printed function'
 if domain=='x>0':assert t>0
 if domain=='x!=0':assert t!=0
 fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0];ft=f[':answer-field/type'];answers=f[':answer-field/choices'];values=[p.scalar(z[':answer/value']) for z in answers]
 assert len(values)==(5 if ft.endswith('/radio') else 1)
 assert len({v for v in values})==len(values);valid=[v[':answer/id'] for v,obj in zip(answers,values) if equal(obj,a)];assert valid==[f[':answer-field/correct'][1]]
 if ft.endswith('/radio'):
  mid=r['generation']['template'];fpoly=s.expand(s.powdenest(F,force=True))
  if mid=='q-103531':z=-fpoly.coeff(x,2)/2;expected=[m,-s.Rational(5,2)*z,2/(5*z),a,-2/(5*z)]
  elif mid=='q-103532':expected=[-s.Integer(1),1/m,-m,m,a]
  elif mid=='q-103543':expected=[s.Integer(1),1/m,a,m,-m]
  elif mid=='q-47449':z=fpoly.coeff(x,2);expected=[1/m,-s.Integer(1),1/(2*z),-1/(2*z),a]
  elif mid=='q-71524':z=fpoly.coeff(x,2);expected=[a,s.Rational(4,5),m,-2*z,1/m]
  else:raise AssertionError('Unknown whole bank')
  assert all(sum(equal(v,e) for e in expected)==1 for v in values),'Printed distractor recipe mismatch'
 assert r['generation']['parameter_fingerprint']==g.task_fingerprint(F,t),'Fingerprint does not reflect printed givens'
 if ft.endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 return solution(q,F,t,y)

def nativechecks(r):
 f=r['question'][':question/answer-fields'][0];cid=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'all source bank IDs'} for a in f[':answer-field/choices']]
 raw=f[':answer-field/choices'][0][':answer/value'];a=p.scalar(raw)
 probes=[(raw,'canonical'),('2('+raw+')/2','unreduced equivalent'),('0','ordinary zero'),('1','ordinary one'),('('+raw+')+1','ordinary correct+1')]
 return [{'field_index':0,'submitted':v,'expected':'accepted' if equal(p.scalar(v),a) else 'rejected','purpose':why} for v,why in probes]

def reject(fn):
 try:fn()
 except (ValueError,AssertionError,KeyError,StopIteration,TypeError):return
 raise AssertionError('Fail-closed negative control accepted')

def main():
 assert g.SOURCE==json.loads((ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186092384.json').read_text())
 raws=[];normals=[];cases=[];counts={};steps=0;replays=[];negative=0
 for mid,q in g.SOURCES.items():
  raw=g.generate('easy',template=mid,profile='raw');assert raw['question']==q;raws.append(raw)
  cases.append({'source_id':mid,'raw_original_parameters':raw['generation']['parameters'],'full_object_replay':True,'source_options':sum(len(f[':answer-field/choices']) for f in q.get(':question/answer-fields',[])),'source_worked_solution':':question/worked-solution' in q,'source_fields':len(q.get(':question/answer-fields',[])),'exclusion':g.EXCLUDED.get(mid)})
 for mid in [*g.SPECS,*g.AUTHORED]:
  level='easy' if mid in g.SPECS else g.AUTHORED[mid][0];local=[]
  for n,param in enumerate(g.parameters_for(mid)):
   try:r=g.generate(level,n,template=mid,parameters=param)
   except ValueError:continue
   steps+=independent(r);assert g.generate(level,n,template=mid,parameters=param)==r
   local.append(r);normals.append(r)
  counts[mid]={'level':level,'authored':mid in g.AUTHORED,'valid_instances':len(local),'parameters':[r['generation']['parameters'] for r in local]}
  if mid in g.SPECS:
   served=g.generate('easy',template=mid,parameters={'scale':1});f=served['question'][':question/answer-fields'][0];sf=g.SOURCES[mid][':question/answer-fields'][0]
   for ans in sf[':answer-field/choices']:assert sum(equal(p.scalar(ans[':answer/value']),p.scalar(a[':answer/value'])) for a in f[':answer-field/choices'])==1
   assert equal(p.scalar(sf[':answer-field/correct'][':answer/value']),p.scalar(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])))
   assert served['question'][':question/problem']==g.fmt.normalize_prose(g.SOURCES[mid][':question/problem'])
   expected=g.SOURCES[mid][':question/worked-solution'];expected=expected.replace(r'=\frac{1}{2\sqrt{{x}^{3}}}=','=') if mid=='q-342153' else expected
   assert served['question'][':question/worked-solution']==g.fmt.normalize_prose(expected)
   replays.append({'source':mid,'full_bank':True,'options':len(f[':answer-field/choices']),'distractors':len(f[':answer-field/choices'])-1,'prompt_normalized_exact':True,'solution_normalized_exact':mid!='q-342153','source_feedback_attributes':[k for a in sf[':answer-field/choices'] for k in a if 'feedback' in k],'repair':'remove unevaluated x from fixed-point evaluation' if mid=='q-342153' else None})
  for base in local[:1]:
   for kind in ['derivative-target','operator-operand','point','eval-target','normal-sign','answer','key','domain']:
    r=copy.deepcopy(base);q=r['question'];w=q[':question/worked-solution']
    if kind=='derivative-target':q[':question/worked-solution']=w.replace("f'(x)","f'(x+1)",1).replace("{f}^{'}(x)","{f}^{'}(x+1)",1).replace('{f}^{′}(x)','{f}^{′}(x+1)',1)
    if kind=='operator-operand':q[':question/worked-solution']=w.replace(r'\frac{\text{d}}{\text{d}x}(',r'\frac{\text{d}}{\text{d}x}(7+',1)
    if kind=='point':q[':question/problem']=q[':question/problem'].replace('at the point $(', 'at the point $(7+',1)
    if kind=='eval-target':q[':question/worked-solution']=w.replace("m=f'(","m=f'(7+",1).replace("m={f}^{'}(","m={f}^{'}(7+",1).replace('m={f}^{′}(','m={f}^{′}(7+',1)
    if kind=='normal-sign':q[':question/worked-solution']=w.replace(r'-\frac{1}{m}',r'\frac{1}{m}')
    if kind=='answer':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']+=' + 1'
    if kind=='domain':r['generation']['domain']='unrestricted'
    if kind=='key':q[':question/answer-fields'][0][':answer-field/correct'][1]='absent'
    if r!=base:
     try:reject(lambda:independent(r))
     except AssertionError as e:raise AssertionError((mid,kind,str(e)))
     negative+=1
 for kwargs in [{'level':'invalid'},{'level':'moderate','template':'q-308798'},{'level':'easy','template':'q-308798','parameters':{'scale':True}},{'level':'easy','template':'q-308798','parameters':{'scale':0}},{'level':'easy','template':'q-308798','parameters':{'scale':13}},{'level':'easy','template':'q-308798','parameters':{'scale':1,'extra':2}},{'level':'easy','profile':'unknown'},{'level':'easy','field_type':'checkbox'},{'level':'hard','profile':'raw'},{'level':'easy','template':'q-47407'},{'level':'easy','template':'q-308798','profile':'raw','parameters':{'scale':2}}]:reject(lambda kw=kwargs:g.generate(**kw));negative+=1
 for level in g.SUPPORTED_LEVELS:
  for seed in range(12):independent(g.generate(level,seed));independent(getattr(g,'generate_'+level)(seed))
  batch=g.batch(level,5,33);assert len(batch)==5
  assert len({v['generation']['parameter_fingerprint'] for v in batch})==5 and all(v['generation']['parameter_fingerprint'] not in g.RESERVED_TASKS for v in batch)
 reject(lambda:g.batch('easy',0));reject(lambda:g.batch('hard',1000))
 engine=[{'label':str(i)+' '+r['generation']['template']+' '+str(r['generation']['parameters']),'record':r,'checks':nativechecks(r)} for i,r in enumerate(normals)]
 save('native-input.json',engine);binary=ROOT/'generate/runs/current/check-engine';assert sha(binary)==SHA
 proc=subprocess.run([str(binary),str(H/'native-input.json'),str(H/'native-report.json')],capture_output=True,text=True);(H/'native.log').write_text(proc.stdout+proc.stderr);assert proc.returncode==0,proc.stderr
 native=json.loads((H/'native-report.json').read_text());assert native['documented_unresolved_checks']==0
 base=json.loads((H/'registered-baseline.json').read_text())['files'];paths=[ROOT/'generate/scratch/17592186092384.py',*sorted((ROOT/'generate/scratch/17592186092384').rglob('*'))];actual={str(f.relative_to(ROOT)):sha(f) for f in paths if f.is_file()};assert actual==base,'Registered baseline changed'
 save('source-cases.json',cases);save('source-fidelity.json',{'raw_full_questions':13,'complete_banks':10,'matched_options':30,'matched_distractors':20,'full_prompt_solution_feedback_replays':replays,'raw_source_errors':{'q-342153':'fixed-point f prime chain contains unevaluated x; raw retained','q-71525':'6(1) omits square, equal here but incomplete fields; raw retained'},'excluded':g.EXCLUDED})
 save('capacity.json',{'domains':counts,'batch_capacity':{l:len({r['generation']['parameter_fingerprint'] for r in normals if r['generation']['level']==l and r['generation']['parameter_fingerprint'] not in g.RESERVED_TASKS}) for l in g.SUPPORTED_LEVELS},'unique_task_counts':{l:len({r['generation']['parameter_fingerprint'] for r in normals if r['generation']['level']==l}) for l in g.SUPPORTED_LEVELS},'whole_bank_rejections':{m:len(g.parameters_for(m))-counts[m]['valid_instances'] for m in counts}})
 review=[]
 for mid in counts:
  a=[r for r in normals if r['generation']['template']==mid];review.extend([a[0],a[-1]])
 save('review.json',{'raw':raws,'served':review});(H/'review.md').write_text('# Normal-slope draft review\n\nAll13 frozen records retained exactly as raw evidence. Ten complete source banks and shared prose replay after presentation normalization. q-342153 removes a free x at fixed-point evaluation. Missing fields/key/solution are not invented. Moderate/hard are authored same-method power-rule variations, with provisional labels and no equation/intercept tasks.\n\n'+'\n\n'.join('## '+('Raw ' if r['generation']['evidence_only'] else 'Served '+r['generation']['level']+' ')+r['generation']['template']+' '+str(r['generation']['parameters'])+'\n\n'+g.markdown(r) for r in raws+review)+'\n')
 report={'status':'pass','basis':2275,'raw_object_replay':13,'complete_source_banks':10,'matched_source_options':30,'matched_source_distractors':20,'public_domain_instances':len(normals),'all_displayed_equations_checked':steps,'formal_operand_target_checked':True,'negative_controls':negative,'exclusions':g.EXCLUDED,'native_grading':{k:v for k,v in native.items() if k!='records'},'native_checker_sha256':SHA,'baseline_unchanged':True,'script_sha256':sha(H.with_suffix('.py'))};save('validation.json',report)
 save('freeze.json',{'version':g.VERSION,'baseline_unchanged':True,'hashes':{str(f.relative_to(ROOT)):sha(f) for f in [H.with_suffix('.py'),*sorted(H.rglob('*'))] if f.is_file() and f.name!='freeze.json' and '__pycache__' not in str(f)}});print(json.dumps(report,indent=2))
if __name__=='__main__':main()
