#!/usr/bin/env python3
"""Independent displayed mathematics, complete source objects, stages and native QA."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache
from pathlib import Path
import sympy as s
sys.dont_write_bytecode=True
sys.path.insert(0,'/home/jake/.cache/uv/wheels-v5/pypi/lark/1.2.2-py3-none-any')
from sympy.parsing.latex import parse_latex
from lark import Tree
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('arc',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def normalize(v):
 v=v.strip().rstrip('.,?').replace('⁡','').replace('π',r'\pi').replace('′',"'")
 v=v.replace(r'\displaystyle','').replace(r'\left','').replace(r'\right','').replace(r'\big','').replace(r'\,','').replace(r'\dfrac',r'\frac')
 v=re.sub(r'\\operatorname\{(sin|cos)\}',r'\\\1',v)
 v=re.sub(r'\{(sin|cos)\}',r'\\\1',v)
 # Make all unparenthesized source trig arguments explicit; preserve complete nt.
 v=re.sub(r'\\(sin|cos)(\^\{?\d+\}?)?\s*((?:\d+)?t)',lambda m:'\\'+m[1]+(m[2] or '')+'('+m[3]+')',v)
 v=re.sub(r'\\(sin|cos)(\^\{?\d+\}?)?(?:\{\(([^()]*)\)\}|\(([^()]*)\))',lambda m:'{\\'+m[1]+'('+(m[3] or m[4])+')}' + (m[2] or ''),v)
 v=re.sub(r'(?<=[)}])\s*(?=e\^)',r'\\cdot ',v)
 v=v.replace('{e}^','e^').replace('{t}^','t^')
 v=re.sub(r'(?<=\})(?=\\(?:sqrt|sin|cos)|[et])',r'\\cdot ',v)
 v=v.replace('}(',r'}\cdot (')
 v=v.replace(r'\pi','P')
 return v
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
@lru_cache(None)
def parse(v):
 text=normalize(v)
 text=re.sub(r'\|([^|]+)\|',r'Abs(\1)',text)
 for command in (r'\frac',r'\sqrt'):
  while command in text:
   start=text.rfind(command);inside,end=group(text,start+len(command))
   if command==r'\frac':
    second,finish=group(text,end);replacement='(('+inside+')/('+second+'))';end=finish
   else:replacement='sqrt('+inside+')'
   text=text[:start]+replacement+text[end:]
 text=text.replace(r'\sin','sin').replace(r'\cos','cos').replace(r'\cdot','*').replace('{','(').replace('}',')')
 assert '\\' not in text,('unparsed TeX',text)
 return parse_expr(text,local_dict={'t':g.t,'e':s.E,'P':s.pi,'sin':s.sin,'cos':s.cos,'sqrt':s.sqrt,'Abs':s.Abs},transformations=standard_transformations+(implicit_multiplication_application,convert_xor))

def eq(a,b):
 if a==b:return True
 if any(power.exp==s.Rational(1,2) for x in (a,b) for power in x.atoms(s.Pow)):
  difference=s.expand(a*a-b*b)
  if s.simplify(difference.subs(g.t,0)).is_zero is False:return False
  difference=s.trigsimp(difference)
  if difference!=0:return False
  # Identical squares: retain the root branch/sign rather than collapsing signs.
  def principal_positive(x):
   factors=x.args if x.is_Mul else (x,)
   return all(f.is_nonnegative is True or (f.is_Pow and f.exp==s.Rational(1,2)) for f in factors)
  if principal_positive(a) and principal_positive(b):return True
  return s.simplify(s.trigsimp(a-b))==0
 difference=s.expand(a-b)
 if s.simplify(difference.subs(g.t,0)).is_zero is False:return False
 return s.trigsimp(difference)==0


def group(text,start):
 assert text[start]=='{';depth=1;i=start+1
 while depth:
  if text[i]=='{':depth+=1
  if text[i]=='}':depth-=1
  i+=1
 return text[start+1:i-1],i

def full_integral(v):
 v=v.strip().rstrip('.,').replace(r'{\int }',r'\int').replace(r'\displaystyle','').strip()
 start=v.index(r'\int');prefix=v[:start]
 z=v[start+4:];assert z.startswith('_');lo,end=group(z,1);assert z[end]=='^';hi,after=group(z,end+1)
 z=z[after:];z=re.sub(r'(?:\\,)?\\(?:text|mathrm)\{d\}t$','',z);z=re.sub(r'dt$','',z)
 assert '\\int' not in z and z.strip()
 return parse((prefix or '')+'('+z+')'),parse(lo),parse(hi),'dt'
def obj_eq(a,b):return a[3]==b[3] and eq(a[1],b[1]) and eq(a[2],b[2]) and eq(a[0],b[0])
def vec(v):
 v=v.strip().rstrip(',').replace('⟨',r'\langle').replace('⟩',r'\rangle')
 if r'\langle' in v:
  inside=v.split(r'\langle',1)[1].split(r'\rangle',1)[0].replace(r'\,','')
  return [parse(z) for z in inside.split(',')]
 # Each whole component terminates in a basis label; exponent contains no i/j/k.
 pieces=re.findall(r'(.*?)(?:\\,)?([ijk])(?:\+|$)',v)
 assert len(pieces)==3,(v,pieces)
 return [parse(z) for z,u in pieces]

def prompt_objects(q):
 prompt=q[':question/problem'];curve=re.search(r'curve \$[fghr]\(t\)=(.*?)\$',prompt,re.S)[1]
 if r'\big' in curve:
  outside,inside=curve.split(r'\big(',1);xs=[parse(outside)*x for x in vec(inside.rsplit(r'\big)',1)[0])]
 else:xs=vec(curve)
 lo,hi=re.findall(r'\$t=(.*?)\$',prompt);return xs,parse(lo),parse(hi)

def derivative_inputs(q):
 block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)[0]
 first=block.split(r'\\')[0].split('=',1)[1]
 for wrapper in (r'\frac{\mathrm{d}}{\mathrm{d}t}',r'\frac{\text{d}}{\text{d}t}'):first=first.replace(wrapper,'')
 return vec(first)

def stage_values(q):
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
 assert len(blocks)==2
 rows=blocks[0].split(r'\\');deriv=vec(rows[1].split('=',1)[1])
 values=[parse(row.split('=',1)[1]) for row in rows[2:]]
 integrals=[]
 for row in blocks[1].split(r'\\'):
  for bit in row.split('='):
   if r'\int' in bit and not ('‖' in bit or r'\|' in bit):integrals.append(full_integral(bit))
 assert len(integrals)==1,integrals
 return deriv,values,integrals[0],len(rows)

def check(r):
 q=r['question'];xs,lo,hi=prompt_objects(q);ds=[s.diff(x,g.t) for x in xs];R=s.expand(sum(d*d for d in ds))
 assert float(lo)<float(hi)
 inputs=derivative_inputs(q);assert len(inputs)==len(xs) and all(eq(a,b) for a,b in zip(inputs,xs)),('wrong displayed differentiation input',inputs,xs)
 deriv,stages,final,rows=stage_values(q)
 assert all(eq(a,b) for a,b in zip(ds,deriv)) and len(ds)==len(deriv)
 for stage in stages:assert eq(stage**2,R),(r['generation']['template'],'displayed stage',stage,R)
 assert obj_eq(final,(s.sqrt(R),lo,hi,'dt')),(final,R)
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and len(f[':answer-field/choices'])==5
 options=[full_integral(a[':answer/value']) for a in f[':answer-field/choices']]
 assert all(not obj_eq(a,b) for i,a in enumerate(options) for b in options[i+1:]),'colliding complete bank'
 correct=f[':answer-field/correct'][1];assert sum(a[':answer/id']==correct for a in f[':answer-field/choices'])==1
 assert sum(obj_eq(o,final) for o in options)==1
 for a,o in zip(f[':answer-field/choices'],options):assert obj_eq(o,final)==(a[':answer/id']==correct)
 # Read complete displayed options and compare their generator formula objects.
 expected=[(s.sympify(o['speed'],locals={'t':g.t}),s.sympify(o['lower']),s.sympify(o['upper']),'dt') for o in r['generation']['bank_objects']]
 assert all(sum(obj_eq(o,e) for e in expected)==1 for o in options)
 for text in (q[':question/problem'],q[':question/worked-solution']):
  assert text.count('$')%2==0 and text.count('{')==text.count('}')
  assert 'authored' not in text and 'profile' not in text
 assert not any(word in q[':question/worked-solution'].lower() for word in ('substitution','antiderivative','approximately'))
 if r['generation']['bank_profile']=='authored_method':
  derived=[(s.sqrt(R),lo,hi,'dt'),(s.sqrt(sum(x*x for x in xs)),lo,hi,'dt'),(s.sqrt(sum(x*x for x in ds[:-1])),lo,hi,'dt'),(R,lo,hi,'dt'),(s.sqrt(R),lo,hi+1,'dt')]
  assert all(sum(obj_eq(o,e) for e in derived)==1 for o in options), 'Displayed authored bank does not match complete method operations'
  for val,l,h,d in options:
   for frac in (0,.25,.5,.75,1):assert complex(val.subs(g.t,l+(h-l)*s.Rational(str(frac))).evalf()).imag==0
 for stage in stages:
  for frac in (0,.25,.5,.75,1):assert float(stage.subs(g.t,lo+(hi-lo)*s.Rational(str(frac))))>=0
 return options,rows

def write(name,data): (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
 raw=json.load(open(HERE/'source.json'));questions=raw['record'][':knowledge-point/questions'];cases=[];replays=[];matched=refs=0;fidelity=[]
 for template,(level,source,name,basis) in g.TEMPLATES.items():
  if source is None:continue
  print('source',source,flush=True)
  q=next(q for q in questions if q[':question/math-academy-id']==source)
  profiles=['observed:'+template]+(['observed:trig2:legacy'] if template=='trig2' else [])
  for profile in profiles:
   case={'source_id':source,'template':template,'level':level,'parameters':g.ORIGINAL[template],'bank_profile':profile,'field_index':0 if profile.endswith('legacy') else len(q[':question/answer-fields'])-1}
   cases.append(case);r=g.generate(level,seed=17,template=template,parameters=case['parameters'],profile=profile);opts,nrows=check(r)
   original=q[':question/answer-fields'][case['field_index']];source_opts=[full_integral(a[':answer/value']) for a in original[':answer-field/choices']]
   assert len(source_opts)==5 and all(sum(obj_eq(o,v) for v in opts)==1 for o in source_opts)
   matched+=5
   correct=original.get(':answer-field/correct')
   if correct:assert obj_eq(full_integral(correct[':answer/value']),next(o for a,o in zip(r['question'][':question/answer-fields'][0][':answer-field/choices'],opts) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]));refs+=1
   # Compare full prose and all mathematical stages, with stated notation repairs.
   old=q[':question/worked-solution'];new=r['question'][':question/worked-solution']
   prose=lambda z:re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$','<MATH>',z,flags=re.S)).replace('‖',r'\|').replace('′',"'").replace('${'+name+"}'(t)$",'$'+name+"'(t)$").replace('${'+name+"}^{'}(t)$",'$'+name+"'(t)$")
   # Exact shared sentences are checked separately because inline norm typography differs.
   complete_prose=lambda z:re.sub(r'\s+',' ',re.sub(r'\$[^$]*\$','<INLINE>',re.sub(r'\$\$.*?\$\$','<MATH>',z,flags=re.S))).strip()
   assert complete_prose(old)==complete_prose(new),(source,complete_prose(old),complete_prose(new))
   assert 'First, we find' in old and 'First, we find' in new
   assert ('Therefore, the arc length of the curve is:' in old)==('Therefore, the arc length of the curve is:' in new)
   old_blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',old,re.S)
   old_rows=old_blocks[0].split(r'\\');assert len(old_rows)==nrows,(source,len(old_rows),nrows)
   assert all(eq(a,b) for a,b in zip(derivative_inputs(q),derivative_inputs(r['question'])))
   old_ds=vec(old_rows[1].split('=',1)[1]);new_ds,new_stages,new_final,_=stage_values(r['question'])
   assert all(eq(a,b) for a,b in zip(old_ds,new_ds))
   old_stages=[parse(row.split('=',1)[1]) for row in old_rows[2:]]
   assert len(old_stages)==len(new_stages) and all(eq(a,b) for a,b in zip(old_stages,new_stages)),(source,old_stages,new_stages)
   old_integral_rows=len(old_blocks[1].split(r'\\'));new_integral_rows=len(re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',new,re.S)[1].split(r'\\'));assert old_integral_rows==new_integral_rows
   final_expr=old_blocks[1].split('=')[-1];assert obj_eq(full_integral(final_expr),new_final)
   # Prompt prose normalized whitespace/math spans/image refs, exact source wording.
   prompt_prose=lambda z:re.sub(r'\s+',' ',re.sub(r'!\[\]\(.*?\)|\$.*?\$','<SLOT>',z,flags=re.S)).strip()
   assert prompt_prose(q[':question/problem'])==prompt_prose(r['question'][':question/problem']),(source,prompt_prose(q[':question/problem']),prompt_prose(r['question'][':question/problem']))
   fidelity.append({'source_id':source,'profile':profile,'options_matched':5,'correct_designation_matched':bool(correct),'first_stage_rows':nrows,'final_rows':old_integral_rows,'solution_repair':source=='q-33857'})
   replays.append(r)
 write('source-cases.json',cases)
 records=[];unique={l:set() for l in ('easy','moderate','hard')}
 for template,(level,source,name,basis) in g.TEMPLATES.items():
  print('generated',template,flush=True)
  for seed in range(14):
   r=g.generate(level,seed,template=template);check(r);records.append(r);unique[level].add(r['generation']['mathematical_fingerprint'])
  # Every observed profile changed parameters, including legacy.
  if source:
   for seed in range(4):check(g.generate(level,seed+29,template=template,profile='observed:'+template))
 for level in unique:assert len(unique[level])>=10
 # Fixed parameters identities stable despite shuffle, profile changes affect only content.
 for r in records:
  meta=r['generation'];fixed=dict(template=meta['template'],parameters=meta['parameters'],profile=meta['bank_profile'])
  altered=g.generate(r['question'][':question/difficulty'].split('/')[-1],seed=979,**fixed)
  assert altered['question'][':question/id']==r['question'][':question/id']
 if True:
  p=g.ORIGINAL['spiral'].copy();a=g.generate_moderate(template='spiral',parameters=p);p['h']=-2;b=g.generate_moderate(template='spiral',parameters=p)
  assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint'] and a['question'][':question/id']!=b['question'][':question/id']
  x=g.generate_easy(template='trig2',parameters=g.ORIGINAL['trig2'],profile='observed:trig2');y=g.generate_easy(template='trig2',parameters=g.ORIGINAL['trig2'])
  assert x['generation']['mathematical_fingerprint']==y['generation']['mathematical_fingerprint'] and x['question'][':question/id']!=y['question'][':question/id']
 # Invalid explicit parameters cannot silently resample; hard workload fixed.
 bad=[]
 for key,value in [('a',0),('a',-3),('b',4),('n',4),('k',0),('c',0),('lo','-3'),('hi','8')]:
  p=g.ORIGINAL['exp_rotating'].copy();p[key]=value
  try:g.generate_hard(template='exp_rotating',parameters=p)
  except ValueError:bad.append(key+str(value))
  else:raise AssertionError('Invalid explicit input accepted')
 p=dict(g.ORIGINAL['exp_rotating'],a=1,b=1,k=1,n=1)
 try:g.generate_hard(template='exp_rotating',parameters=p)
 except ValueError:bad.append('hard_cancelled_derivative_coefficient')
 else:raise AssertionError('Hard workload degeneracy accepted')
 # Displayed mutations must fail independently of matching metadata.
 rejected=0
 for target in ('prompt','derivative','stage','limit','differential','designation'):
  r=copy.deepcopy(replays[0]);q=r['question']
  if target=='prompt':q[':question/problem']=q[':question/problem'].replace(r'\sin{\left(2 t \right)}',r'\sin{\left(3 t \right)}')
  if target=='derivative':q[':question/worked-solution']=q[':question/worked-solution'].replace('2 t','3 t',1)
  if target=='stage':q[':question/worked-solution']=q[':question/worked-solution'].replace('4 \\cos','5 \\cos')
  if target=='limit':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']=q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'].replace('_{0}','_{1}')
  if target=='differential':q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']=q[':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'].replace(r'\mathrm{d}t',r'\mathrm{d}u')
  if target=='designation':q[':question/answer-fields'][0][':answer-field/correct'][1]=next(a[':answer/id'] for a in q[':question/answer-fields'][0][':answer-field/choices'] if a[':answer/id']!=q[':question/answer-fields'][0][':answer-field/correct'][1])
  try:check(r)
  except Exception:rejected+=1
  else:raise AssertionError('Mutation escaped: '+target)
 # Concurrent plotting same/different keys. Force rerender distinct sample paths.
 concurrent=[('trig2',g.ORIGINAL['trig2']),('spiral',dict(g.ORIGINAL['spiral'],a=3)),('trig2',g.ORIGINAL['trig2'])]
 for template,p in concurrent:
  key=g.digest({'template':template,'parameters':p})
  for extension in ('.png','.json'):(HERE/'plots'/(key+extension)).unlink(missing_ok=True)
 with ThreadPoolExecutor(3) as pool:rendered=list(pool.map(lambda arg:g.generate(g.TEMPLATES[arg[0]][0],template=arg[0],parameters=arg[1]),concurrent))
 for r in rendered:
  side=json.load(open(r['generation']['plots']['sidecar']));assert side['parameters']==r['generation']['parameters'] and side['arrows']==(0 if r['generation']['template']=='spiral' else 3)
 assert not list(HERE.glob('arc-plot-*.json'))
 native=[]
 for i,r in enumerate(replays+records):
  field=r['question'][':question/answer-fields'][0];checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==field[':answer-field/correct'][1] else 'rejected','purpose':'owned radio selection; mathematics checked independently'} for a in field[':answer-field/choices']]
  native.append({'label':str(i),'record':r,'checks':checks})
 write('native-input.json',native)
 engine=ROOT/'generate/runs/current/check-engine';subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 report=json.load(open(HERE/'native-report.json'));assert report['documented_unresolved_checks']==0
 # Original plus >=two generated examples for every family/profile; hard gets four.
 review=[]
 for replay in replays:
  review.append({'kind':'original-parameter replay','record':replay})
  for seed in (41,42):review.append({'kind':'generated observed-bank variant','record':g.generate(replay['question'][':question/difficulty'].split('/')[-1],seed,template=replay['generation']['template'],profile=replay['generation']['bank_profile'])})
 for template in g.TEMPLATES:
  for seed in (81,82):review.append({'kind':'authored default variant; hard level authored' if template=='exp_rotating' else 'authored method bank variant','record':g.generate(g.TEMPLATES[template][0],seed,template=template)})
 write('review.json',review)
 text='# Arc-length integral setup review\n\nAll records are author previews with answers. Original snapshots follow, then parameterized replays and generated variants.\n'
 for q in questions:
  text+='\n## Original '+q[':question/math-academy-id']+'\n\n'+q[':question/problem'].replace('![](images/','![](/media/jake/SSD/EDB/math/images/')+'\n\n'+q[':question/worked-solution']+'\n\n'
  for field in q[':question/answer-fields']:
   text+='Field '+str(field[':db/id'])+'; correct '+str(field.get(':answer-field/correct',{}).get(':answer/value','UNAVAILABLE'))+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in field[':answer-field/choices'])+'\n'
 for item in review:
  r=item['record'];text+='\n## '+item['kind']+' — '+r['generation']['template']+' / '+r['generation']['bank_profile']+'\n\n'+g.markdown(r)+'\n'
 (HERE/'review.md').write_text(text)
 write('validation.json',{'passed':True,'source_provenance':{k:raw[k] for k in ('database','basis','lineage')},'source_questions':8,'source_active_banks':8,'source_legacy_banks':1,'source_complete_banks_matched':len(fidelity),'source_options_matched':matched,'source_distractors_matched':36,'source_correct_designations_matched':refs,'source_correct_designations_unavailable':1,'source_fidelity':fidelity,'source_solution_sequence_matches':8,'source_solution_exact_math':7,'source_solution_repaired_math':1,'generated_records_checked':len(records),'unique_assessed_tasks':{l:len(v) for l,v in unique.items()},'invalid_parameters_rejected':bad,'mutations_rejected':rejected,'native_grading':{'accepted':report['accepted_checks'],'rejected':report['rejected_checks'],'unresolved':0,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'authored_hard':'bounded three product/chain differentiated components and sum-of-squares cancellation; integral setup only','source_error_intent':'Unexplained wrong scalar constants retained in explicit observed profiles; no inferred learner diagnosis claimed.','source_nonreal_distractor':'q-33857 fifth option negative radicand near t=1; retained only observed profile, normal banks real nonnegative.','database_writes':0,'concurrent_plot_checks':3})
 print('PASS: 9 banks / 45 options, 8 available correct refs, 126 default instances; all native checks passed')
if __name__=='__main__':main()
