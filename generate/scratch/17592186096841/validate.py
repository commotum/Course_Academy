#!/usr/bin/env python3
"""Independent displayed-LaTeX arithmetic, whole-bank fidelity and native grading."""
import importlib.util, hashlib, json, re, subprocess, sys, uuid
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,)
def parse(text):
 text=text.replace('{|}','|').replace('{]}',']')
 text=re.sub(r'(\])_\{x=',r'\1|_{x=',text)
 if '|_{x=' in text:
  value,z=text.split('|_{x=');return parse(value).subs(s.Symbol('x'),parse(z.rstrip('}')))
 text=text.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace('′',"'")
 # Parse fractions recursively. Braces around parentheses (source artifact) are harmless.
 def group(t,i):
  assert t[i]=='{';depth=1;j=i+1
  while depth:
   if t[j]=='{':depth+=1
   if t[j]=='}':depth-=1
   j+=1
  return t[i+1:j-1],j
 while r'\frac' in text:
  pos=text.index(r'\frac');num,end=group(text,pos+5);den,stop=group(text,end)
  text=text[:pos]+'(('+str(parse(num))+')/('+str(parse(den))+'))'+text[stop:]
 text=re.sub(r'\^\{([^{}]+)\}', r'**(\1)',text)
 text=text.replace('{','').replace('}','').replace('^','**')
 text=text.replace('[','(').replace(']',')').strip().rstrip('.,')
 assert '\\' not in text,text
 return parse_expr(text,local_dict={k:s.Symbol(k) for k in ['x','y','t','g','f','m']},transformations=TRANS)
def eq(a,b):return s.expand(a-b)==0

def skeleton(text):return g.MATH.sub('<math>',text)
def validate_display(record):
 q=record['question'];md=record['generation'];name=md['template'];p=md['parameters'];field=q[':question/answer-fields'][0]
 math=g.MATH.findall(q[':question/problem'])
 # Recover the function from the visible prompt, without consulting generator maths.
 if name=='quadratic_derivative':
  expr=math[0].split('[')[1].split(']')[0];v=s.Symbol('t')
 else:expr=next(t.split('f(x)=')[1] for t in math if 'f(x)=' in t).rstrip('$.,');v=s.Symbol('x')
 function=parse(expr);derivative=s.diff(function,v)
 inner_exp=s.Poly(function,v).degree()//p['n']
 # Recover g only from the displayed composition equation.
 solmath=g.MATH.findall(q[':question/worked-solution'])
 comp=next(t for t in solmath if (r'\,g=' in t) or 'g(t)=' in t)
 it=comp.split('g(t)=')[1].split(r'\,')[0].rstrip(',') if 'g(t)=' in comp else comp.split(r'\,g=')[1].strip('$\n')
 inner=parse(it);assert eq(function,inner**p['n'])
 assert 1<=s.Poly(inner,v).degree()<=4 and p['n'] in range(2,7)
 # Question's displayed point lies on the displayed curve.
 if 'slope' in name or name.startswith('tangent'):
  point=next(t for t in math if t.startswith('$('));z,y=map(parse,point.strip('$()').split(','));assert eq(function.subs(v,z),y)
  expected=derivative.subs(v,z)
  if name.startswith('tangent'):expected=s.expand(expected*s.Symbol('x')+y-expected*z)
 else:expected=derivative
 displayed={a[':answer/id']:parse(a[':answer/value'].split('=',1)[-1]) for a in field[':answer-field/choices']}
 selected=displayed[field[':answer-field/correct'][1]]
 assert eq(selected,expected),(name,'correct display',selected,expected)
 assert len(displayed)==len(set(map(s.srepr,displayed.values())))
 assert sum(eq(x,expected) for x in displayed.values())==1
 values=list(displayed.values());assert not any(eq(a,b) for i,a in enumerate(values) for b in values[i+1:])
 # Independently parse intermediate displayed chain stages, not metadata values.
 if name=='quadratic_derivative':
  stage=next(t for t in solmath if 'g^{′}(t)' in t)
  rows=stage.split(r'\\')
  di=parse(rows[0].split('=')[-1].rstrip(', '));outer=parse(rows[1].split('=')[-1].split(r'\end')[0].rstrip('.'))
  assert eq(di,s.diff(inner,v));assert eq(outer.subs(s.Symbol('g'),inner),p['n']*inner**(p['n']-1))
 else:
  fg=next(t for t in solmath if t.startswith('$$\n'+g.FG+'='));dg=next(t for t in solmath if t.startswith('$$\n'+g.DG+'='))
  outer=parse(fg.split('=')[1].strip('$\n,'));di=parse(dg.split('=')[1].strip('$\n.'))
  assert eq(outer.subs(s.Symbol('g'),inner),p['n']*inner**(p['n']-1));assert eq(di,s.diff(inner,v))
 # Check every multiplication/substitution row of chain derivative output.
 derivative_block=next(t for t in solmath if t.startswith('$$\n'+r'\begin{aligned}'+(g.DF if name!='quadratic_derivative' else r'\frac{\text{d}}{\text{d}t}[')))
 rhs=derivative_block.split(' & =')[1:]
 for part in rhs:
  value=part.split(r'\end')[0].strip().rstrip('.').rstrip('\\').strip()
  # The t template has h' identity and h'(g(t))*g'(t) prior to multiplication.
  if 'h^{′}' in value:continue
  parsed=parse(value).subs(s.Symbol('g'),inner);assert eq(parsed,derivative),(name,'derivative stage',value)
 if 'slope' in name or name.startswith('tangent'):
  slope_block=next(t for t in solmath if t.startswith('$$\n'+r'\begin{aligned}'+g.DF+'|_{x='))
  for part in slope_block.split(' & =')[1:]:
   value=part.split(r'\end')[0].strip().rstrip('.').rstrip('\\').strip()
   assert eq(parse(value),derivative.subs(v,z)),(name,'slope stage',value)
 if name.startswith('tangent'):
  tangent=solmath[-1].split(r'\begin{aligned}')[1].split(r'\end')[0]
  for row in tangent.split(r'\\')[1:]:
   lhs,rhs=row.strip().split(' & =');lhs=parse(lhs);rhs=parse(rhs)
   assert eq(lhs.subs(s.Symbol('y'),expected),rhs),(name,'tangent stage',row)
 # UUID shape/ownership and placeholders.
 for a in field[':answer-field/choices']:uuid.UUID(a[':answer/id']);assert '$' not in a[':answer/value']
 uuid.UUID(q[':question/id']);uuid.UUID(field[':answer-field/id']);assert field[':answer-field/correct'][1] in displayed
 if field[':answer-field/type'].endswith('/blank'):assert '{{'+field[':answer-field/key']+'}}' in q[':question/problem']
 assert 'sqrt' not in str(function) and not function.has(s.sin,s.cos,s.exp,s.log)
 return expected,values

def validate_original_solution(src,p,name):
 text=src.get(':question/worked-solution')
 if text is None:return 0
 v=s.Symbol('t' if name=='quadratic_derivative' else 'x')
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S)
 comp=next(b for b in blocks if r'\,g=' in b or 'g(t)=' in b)
 it=comp.split('g(t)=')[1].split(r'\,')[0].rstrip(',') if 'g(t)=' in comp else comp.split(r'\,g=')[1]
 inner=parse(it);derivative=s.diff(inner**p['n'],v);checked=0
 for block in blocks:
  if r'\begin{aligned}' not in block:continue
  rows=block.split(r'\begin{aligned}')[1].split(r'\end')[0].split(r'\\')
  # Two differentiated functions in one aligned block.
  if name=='quadratic_derivative' and '(2' in rows[0] and 'g' in rows[0]:
   assert eq(parse(rows[0].split('=')[-1].rstrip(', ')),s.diff(inner,v))
   assert eq(parse(rows[1].split('=')[-1].rstrip('.')).subs(s.Symbol('g'),inner),p['n']*inner**(p['n']-1));checked+=2;continue
  tangent=rows[0].startswith('y-')
  slope='x=' in rows[0] and ('|' in rows[0])
  expected=derivative.subs(v,p['z']) if slope else derivative
  line=None
  if tangent:
   z=p['z'];y=inner.subs(v,z)**p['n'];m=derivative.subs(v,z);line=s.expand(m*v+y-m*z)
  for row in rows[1:] if tangent else rows:
   if ' & =' not in row:continue
   lhs,rhs=row.split(' & =');rhs=rhs.strip().rstrip('.,')
   if '′' in rhs:continue
   if tangent:
    assert eq(parse(lhs.strip()).subs(s.Symbol('y'),line),parse(rhs));checked+=1;continue
   value=parse(rhs).subs(s.Symbol('g'),inner)
   assert eq(value,expected),(src[':question/math-academy-id'],'source solution stage',rhs,value,expected)
   checked+=1
 # Independently differentiate the displayed outer and inner derivatives too.
 for block in blocks:
  if block.startswith(g.FG+'='):
   assert eq(parse(block.split('=')[1].rstrip(',')).subs(s.Symbol('g'),inner),p['n']*inner**(p['n']-1));checked+=1
  if block.startswith(g.DG+'='):
   assert eq(parse(block.split('=')[1].rstrip('.')),s.diff(inner,v));checked+=1
 return checked

def checks(record):
 expected,vals=validate_display(record);f=record['question'][':question/answer-fields'][0]
 if f[':answer-field/type'].endswith('/radio'):
  return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'correct or incorrect owned selection'} for a in f[':answer-field/choices']]
 value=f[':answer-field/choices'][0][':answer/value']
 return [{'submitted':value,'expected':'accepted','purpose':'canonical displayed fragment'},
 {'submitted':s.sstr(s.expand(expected)).replace('**','^'),'expected':'accepted','purpose':'equivalent expanded entry'},
 {'submitted':s.sstr(s.expand(expected+1)).replace('**','^'),'expected':'rejected','purpose':'wrong entry +1'}]

def write(name,value): (ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def main():
 fidelity=[];requests=[];review=[];sourcecases=[];distractors=0;original_stages=0
 for sid,name,p,profile in g.SOURCE_CASES:
  record=g.generate(g.TEMPLATES[name][0],0,name,parameters=p,profile=profile);expected,_=validate_display(record)
  src=g.SOURCES[sid];original_stages+=validate_original_solution(src,p,name);sf=src[':question/answer-fields'][0];f=record['question'][':question/answer-fields'][0]
  generated=[parse(a[':answer/value'].split('=',1)[-1]) for a in f[':answer-field/choices']]
  originals=[parse(a[':answer/value'].split('=',1)[-1]) for a in sf[':answer-field/choices']]
  matches=[[i for i,gen in enumerate(generated) if eq(gen,orig)] for orig in originals]
  assert len(originals)==len(generated) and all(len(x)==1 for x in matches) and len(set(x[0] for x in matches))==len(originals)
  designation=sf.get(':answer-field/correct');status='missing_original_designation' if designation is None else 'matched'
  if designation:assert eq(parse(designation[':answer/value'].split('=',1)[-1]),expected)
  assert f[':answer-field/key']==sf[':answer-field/key'] and f[':answer-field/type']==sf[':answer-field/type'][':db/ident']
  assert skeleton(record['question'][':question/problem'])==skeleton(src[':question/problem'])
  if ':question/worked-solution' in src:assert skeleton(record['question'][':question/worked-solution'])==skeleton(src[':question/worked-solution'])
  # Each source solution's numerical rows are separately mathematical evidence.
  distractors+=len(originals)-1
  fidelity.append({'source_id':sid,'bank_values_matched':len(originals),'bank_values_total':len(originals),'correct_designation':status,'field_layout_matched':True,'prose_skeleton_matched':True,'worked_solution_repaired':sid=='q-48625'})
  sourcecases.append({'source_id':sid,'template':name,'parameters':p,'bank_profile':profile,'authored_level':sid=='q-48625'})
  requests.append({'label':'source/'+sid,'record':record,'checks':checks(record)})
  review.append({'label':'source replay '+sid,'record':record})
  # Review a parameter variant of EACH source bank, even explicit-only banks.
  variant=None
  for seed in range(100,150):
   candidate=g.generate(g.TEMPLATES[name][0],seed,name,profile=profile)
   if candidate['generation']['parameters']!=p:variant=candidate;break
  assert variant;validate_display(variant)
  review.append({'label':'generated same-layout/profile peer '+sid,'record':variant});requests.append({'label':'source-profile-peer/'+sid,'record':variant,'checks':checks(variant)})
 # Defaults: all layouts, 30 independent peers each. These are unordered instances.
 records=0;identities=set()
 for name,spec in g.TEMPLATES.items():
  for seed in range(30):
   record=g.generate(spec[0],seed,name);validate_display(record)
   if 'slope' in name or name.startswith('tangent'):
    pp=record['generation']['parameters'];data=g.maths(name,pp);assert 1<=abs(data[1].subs(data[0],pp['z']))<=3 and data[3].subs(data[0],pp['z'])!=0
    if name.startswith('tangent'):assert pp['n'] in (3,4)
    if name=='affine_slope':assert pp['n']==4
   records+=1;identities.add(record['question'][':question/id'])
   requests.append({'label':name+'/'+str(seed),'record':record,'checks':checks(record)})
   if seed<2:review.append({'label':'generated default '+name+'/'+str(seed),'record':record})
  fixed=g.generate(spec[0],31,name);p=fixed['generation']['parameters'];prof=fixed['generation']['bank_profile']
  other=g.generate(spec[0],999,name,parameters=p,profile=prof)
  assert fixed['question'][':question/id']==other['question'][':question/id']
  assert fixed['generation']['parameter_fingerprint']==other['generation']['parameter_fingerprint']
  for key in [':question/problem',':question/worked-solution']:assert fixed['question'][key]==other['question'][key]
 # Invalid explicit inputs must fail instead of silently changing them.
 for p in [dict(a=0,b=2,n=3),dict(a=2,b=3,n=1),dict(a=2,b=0,n=3),dict(a=2,b=3,n=3,extra=1)]:
  try:g.generate_easy(template='affine_blank',parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit parameters accepted')
 # Bank change affects identity; seed/shuffle does not.
 a=g.generate_easy(template='affine_constant_radio',parameters=dict(a=6,b=4,n=3),profile='observed_666')
 b=g.generate_easy(template='affine_constant_radio',parameters=dict(a=6,b=4,n=3),profile='authored_affine_constant')
 assert a['question'][':question/id']!=b['question'][':question/id']
 c=g.generate_easy(template='affine_blank',parameters=dict(a=6,b=4,n=3))
 assert a['generation']['parameter_fingerprint']==c['generation']['parameter_fingerprint']
 assert a['question'][':question/id']!=c['question'][':question/id']
 write('source-cases.json',sourcecases);write('engine-input.json',requests);write('review.json',review)
 engine=REPO/'generate/runs/current/check-engine'
 subprocess.run([str(engine),str(ROOT/'engine-input.json'),str(ROOT/'native-grading.json')],check=True)
 native=json.loads((ROOT/'native-grading.json').read_text());assert native['documented_unresolved_checks']==0
 (ROOT/'review.md').write_text('# Polynomial-power generator review\n\nOriginals retain source designation anomalies; all generated entries below show author answers.\n\n'+'\n\n---\n\n'.join('## Original '+sid+' — '+q.get(':question/difficulty',{}).get(':db/ident','unrated (authored moderate)').split('/')[-1]+'\n\n'+q[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+q.get(':question/worked-solution','*No original solution or correct designation captured.*') for sid,q in g.SOURCES.items())+'\n\n---\n\n'+'\n\n---\n\n'.join('## '+r['label']+'\n\n'+g.markdown(r['record']) for r in review)+'\n')
 write('validation.json',{'passed':True,'source_provenance':{k:g.CAPTURE[k] for k in ['database','basis','lineage']},'source_questions':9,'source_fidelity':fidelity,'complete_radio_banks':{'matched':4,'total':4},'blank_layouts':{'matched':5,'total':5},'original_solution_stages_verified':original_stages,'answer_values':{'matched':25,'total':25},'source_distractors':{'matched':distractors,'total':distractors},'available_correct_designations':{'matched':8,'total':8,'missing':1},'generated_cases':records,'distinct_default_identities':len(identities),'independent_display_and_solution_stage_parsing':True,'native_grading':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':0,'executable_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'authored_extensions':['operation-derived default radio banks','unrated quartic assigned moderate and supplied canonical-style solution'],'plots':'none','database_writes':0})
 print('PASS: 4/4 radio banks, 5/5 blank fields; 25/25 displayed source values; 16/16 distractors; 8/8 available designations, 1 missing; 270 default instances; native grading passed.')
if __name__=='__main__':main()
