#!/usr/bin/env python3
"""Read actual learner mathematics, independently differentiate and integrate it.
No generator metadata is used as the mathematical oracle. Native fixture grading
is separate from all symbolic/display fidelity checks.
"""
import hashlib, importlib.util, itertools, json, math, re, subprocess, sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
ROOT=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('closedflux',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z=g.VARIABLES
LOCALS={'x':x,'y':y,'z':z,'e':s.E,'pi':s.pi,'sin':s.sin,'cos':s.cos,'ln':s.log,'log':s.log}
def grouped(t,pos,op='{',cl='}'):
 assert t[pos]==op,(t,pos)
 depth=1;i=pos+1
 while depth:
  assert i<len(t),('unbalanced group',t)
  if t[i]==op:depth+=1
  if t[i]==cl:depth-=1
  i+=1
 return t[pos+1:i-1],i

def parse(t):
 """Small independent TeX arithmetic reader covering all displayed source forms."""
 t=t.strip().rstrip('.')
 t=t.replace('⁡','').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\:','').replace(r'\cdot','*').replace(r'\pi','pi')
 for name in ('sin','cos','ln'):t=t.replace(r'\operatorname{'+name+'}',' '+name+' ')
 t=t.replace(r'\ln',' ln ').replace(r'\sin',' sin ').replace(r'\cos',' cos ')
 while r'\frac' in t:
  i=t.index(r'\frac');a,j=grouped(t,i+5);b,k=grouped(t,j)
  t=t[:i]+'(('+str(parse(a))+')/('+str(parse(b))+'))'+t[k:]
 t=t.replace('{','(').replace('}',')').replace('^','**')
 t=re.sub(r'(sin|cos|ln)(?=[a-z0-9])',r'\1 ',t)
 # Function arguments written as ln e or sin z are handled by implicit application.
 return parse_expr(t,local_dict=LOCALS,transformations=standard_transformations+(implicit_multiplication_application,))

def split_product(t):
 return [p.strip() for p in t.split(r'\cdot ')]
def bound(t,pos):
 assert t[pos]=='_';a,i=grouped(t,pos+1);assert t[i]=='^';b,j=grouped(t,i+1)
 return a,b,j

def integral_data(t):
 # Repeated integral means dz dy dx; all pairs read from the displayed row.
 bounds=[]
 while t.startswith(r'{\int }'):
  a,b,j=bound(t,len(r'{\int }'));bounds.append((parse(a),parse(b)));t=t[j:]
 matches=list(re.finditer(r'\\text\{d\}([xyz])',t));assert len(matches)==len(bounds),(t,bounds)
 expr=t[:matches[0].start()].replace(r'\,','').strip() or '1'
 integrand=parse(expr);vars=[LOCALS[m.group(1)] for m in matches]
 pairs=list(zip(reversed(vars),bounds))
 value=integrand
 for var,(a,b) in reversed(pairs):value=s.integrate(value,(var,a,b))
 return integrand,pairs,s.simplify(value)

def primitive_data(t):
 # Extra braces around fraction primitives belong to source notation.
 if t.startswith('{['):
  assert ']}' in t;t=t[1:].replace(']}',']',1)
 assert t.startswith('[');end=t.index(']');P=parse(t[1:end]);a,b,j=bound(t,end+1);assert j==len(t)
 va,lo=a.split('=',1);vb,hi=b.split('=',1);assert va==vb and va in LOCALS
 v=LOCALS[va];lo=parse(lo);hi=parse(hi)
 return P,v,lo,hi,s.simplify(P.subs(v,hi)-P.subs(v,lo))

def rowvalue(t,bounds):
 if t.startswith(r'{∭}_{R}'):
  d=parse(t[len(r'{∭}_{R}'):].replace(r'\,\text{d}V',''))
  for v,(a,b) in reversed(list(zip((x,y,z),bounds))):d=s.integrate(d,(v,a,b))
  return s.simplify(d)
 parts=split_product(t);values=[]
 for p in parts:
  if p.startswith(r'{\int }'):values.append(integral_data(p)[2])
  elif p.startswith('[') or p.startswith('{['):values.append(primitive_data(p)[4])
  else:values.append(parse(p))
 return s.simplify(s.prod(values))

def prompt_data(q):
 t=q[':question/problem'];eq=re.findall(r'\$([xyz])\s*=\s*(.*?)\$',t);assert len(eq)==6
 assert [a for a,b in eq]==list('xxyyzz')
 b=[parse(v.rstrip(',.')) for var,v in eq];bounds=list(zip(b[::2],b[1::2]))
 assert all((hi-lo).is_positive for lo,hi in bounds)
 field=re.search(r'\$F\s*=\s*(.*?)\$,? find',t).group(1).rstrip(',')
 # Only the basis letters at component endings are separators; function names
 # contain i/n but are protected by their complete command grammar here.
 field=field.replace(r'\,','')
 pieces=re.split(r'([ijk])(?=\s*[+-]|$)',field)
 assert len(pieces)==7,pieces
 F=[parse(pieces[0]),parse(pieces[2]),parse(pieces[4])]
 assert pieces[1::2]==list('ijk')
 return F,bounds

def endpoint_parts(t):
 assert t.startswith('(') and t.endswith(')'),t
 inner=t[1:-1];depth=0;positions=[]
 for i,c in enumerate(inner):
  if c in '({':depth+=1
  elif c in ')}':depth-=1
  elif c=='-' and depth==0 and i>0:positions.append(i)
 assert len(positions)==1,(inner,positions)
 i=positions[0];return parse(inner[:i]),parse(inner[i+1:])

def formatting(q):
 for t in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in t),'control char'
  assert t.count('$')%2==0,'math delimiters'
  n=0
  for c in t:
   if c=='{':n+=1
   elif c=='}':n-=1
   assert n>=0,'TeX brace'
  assert n==0,'TeX brace'
  assert '--' not in t and '+-' not in t,'bare adjacent signs'
 for f in q[':question/answer-fields']:
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']

def check_record(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];formatting(q)
 f=q[':question/answer-fields'][0];a=f[':answer-field/choices'];assert len({v[':answer/id'] for v in a})==len(a)
 if r['generation']['template']=='context_setup':
  # No original field is supplied. Only the fragment and displayed solution can
  # be verified; full prompt correctness is honestly unavailable.
  matches=re.findall(r'\\text\{div\}\\,F=(.*?)\.\\end',q[':question/worked-solution']);assert len(matches)==1
  val=parse(matches[0]);assert s.simplify(val-parse(a[0][':answer/value']))==0
  return val
 F,bounds=prompt_data(q);partials=[s.diff(C,v) for C,v in zip(F,(x,y,z))];D=sum(partials)
 expected=D
 for v,(lo,hi) in reversed(list(zip((x,y,z),bounds))):expected=s.integrate(expected,(v,lo,hi))
 expected=s.simplify(expected)
 sol=q.get(':question/worked-solution')
 if sol:
  blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert len(blocks)>=2
  divrows=blocks[0].split(r'\\  & =');assert len(divrows)==3
  formal=divrows[0].split('& =',1)[1].strip()
  inputs=[];operators=[];pos=0
  while pos<len(formal):
   m=re.match(r'\\frac\{∂\}\{∂([xyz])\}\(',formal[pos:]);assert m,formal[pos:]
   op=m.group(1);start=pos+m.end()-1;arg,end=grouped(formal,start,'(',')');inputs.append(parse(arg));operators.append(LOCALS[op]);pos=end
   if pos<len(formal):assert formal[pos]=='+';pos+=1
  assert operators==[x,y,z]
  assert all(s.simplify(u-v)==0 for u,v in zip(inputs,F))
  # Split substituted held partials at top-level +, without hiding negative terms.
  terms=[];depth=0;start=0;t=divrows[1]
  for i,c in enumerate(t):
   if c in '({':depth+=1
   elif c in ')}':depth-=1
   elif c=='+' and depth==0:terms.append(parse(t[start:i]));start=i+1
  terms.append(parse(t[start:]));assert len(terms)==3
  assert all(s.simplify(u-v)==0 for u,v in zip(terms,partials)),('held partials',terms,partials)
  assert s.simplify(parse(divrows[2].rstrip('.'))-D)==0
  rows=blocks[1].split(r'\\  & =');rows[0]=rows[0].split('& =',1)[1];rows[-1]=rows[-1].rstrip('.')
  # Independent primitive comparison also enforces source stage structure.
  assert rows[0].startswith(r'{∭}_{R}') and rows[1].count(r'{\int }')==3
  repeated,pairs,value=integral_data(rows[1]);assert [v for v,b in pairs]==[x,y,z] and [b for v,b in pairs]==bounds
  assert s.simplify(repeated-D)==0
  factors=split_product(rows[2]);assert len(factors)==3
  factor_data=[integral_data(p) for p in factors]
  assert [a[1][0] for a in factor_data]==list(zip((x,y,z),bounds))
  assert s.simplify(s.prod(a[0] for a in factor_data)-D)==0
  prim=split_product(rows[3]);assert len(prim)==3
  evaluated=split_product(rows[4]);assert len(evaluated)==3
  for i,(p,e,fd) in enumerate(zip(prim,evaluated,factor_data)):
   integrand=fd[0];v,(lo,hi)=fd[1][0]
   if p.startswith('[') or p.startswith('{['):
    P,pv,pl,ph,_=primitive_data(p);assert (pv,pl,ph)==(v,lo,hi)
    assert s.simplify(s.diff(P,v)-integrand)==0,('primitive',p)
    top,bottom=endpoint_parts(e)
    assert s.simplify(top-P.subs(v,hi))==0,('upper endpoint',e)
    assert s.simplify(bottom-P.subs(v,lo))==0,('lower endpoint',e)
   else:
    assert integrand==1
    top,bottom=endpoint_parts(p);assert (top,bottom)==(hi,lo)
    assert s.simplify(parse(e)-(hi-lo))==0
  assert all(s.simplify(rowvalue(t,bounds)-expected)==0 for t in rows),('solution stage',rows,expected)
  # Affine normal addition: verify both component sums separately.
  if len(blocks)>2:
   components=blocks[2].rstrip('.').split(r'\\ ')
   assert len(components)==2
   for row,a0 in zip(components,[bounds[0][1],bounds[0][0]]):
    lhs,rhs=row.split('&=',1);assert s.simplify(parse(lhs)-parse(rhs))==0
    actual=rhs.split('+');assert len(actual)==2 and [parse(q) for q in actual]==[a0*a0,2*a0]
 if ':answer-field/correct' in f:
  correct=f[':answer-field/correct'][1];cv=next(v for v in a if v[':answer/id']==correct)
  assert s.simplify(parse(cv[':answer/value'])-expected)==0
 if r['generation']['eligible_for_learning']:
  vals=[parse(v[':answer/value']) for v in a]
  assert len(vals)==5 and all(s.simplify(u-v)!=0 for i,u in enumerate(vals) for v in vals[:i])
  name=r['generation']['template']
  def I(e):
   for var,(lo,hi) in reversed(list(zip((x,y,z),bounds))):e=s.integrate(e,(var,lo,hi))
   return s.simplify(e)
  bx,by,bz=bounds;wx=bx[1]-bx[0];wy=by[1]-by[0];wz=bz[1]-bz[0]
  if name in ('xy_a','xy_b','cancel_x','cancel_x2','cancel_z','canonical'):
   nonzero=[p for p in partials if p!=0]
   wrong1=I(sum(-p if p.could_extract_minus_sign() else p for p in partials)) if name in ('cancel_x','cancel_x2','cancel_z') else I(nonzero[0])
   expected_bank=[expected,-expected,wrong1,I(sum(s.diff(C,var,2) for C,var in zip(F,(x,y,z)))),expected/wz]
  elif name=='cos':expected_bank=[expected,-expected,I(x*s.cos(z)),I(2*x*s.sin(z)),(bx[1]**2-bx[0]**2)*wy*wz]
  elif name=='log':expected_bank=[expected,-expected,(s.log(bx[1])-s.log(bx[0]))*wy*wz,I(y),(s.log(bx[1])-s.log(bx[0]))*(by[1]**2-by[0]**2)*wz]
  elif name=='exp':expected_bank=[expected,-expected,(bx[1]**3-bx[0]**3)*wy*wz,(bx[1]**3-bx[0]**3)*wy*s.exp(bz[1]),(bx[1]**2-bx[0]**2)*wy*(s.exp(bz[1])-s.exp(bz[0]))]
  elif name=='affine':expected_bank=[expected,-expected,I(2*x),I(2),(bx[1]**2+2*bx[1])*wy*wz]
  elif name=='xz':expected_bank=[expected,-expected,I(z),I(2),wx*wy*bz[1]**2]
  else:expected_bank=[expected,-expected,expected/wx,expected/wy,expected/wz]
  assert len(expected_bank)==len(vals) and all(sum(s.simplify(a-b)==0 for b in expected_bank)==1 for a in vals),'displayed method bank'

 return expected


def fidelity():
 cases=[];records=[];banks=0;values=0;solutions=0;corrects=0
 for q in g.QUESTIONS:
  name=next((n for n,d in g.FAMILIES.items() if d['source']==q[':db/id']),'context_setup')
  parameters={'bounds':list(map(str,g.FAMILIES[name]['anchor']))} if name!='context_setup' else {'c':2,'cap':4}
  case={'source_id':q[':db/id'],'template':name,'level':'moderate','parameters':parameters,'bank_profile':'observed:'+str(q[':db/id'])}
  cases.append(case);r=g.generate('moderate',template=name,parameters=parameters,profile=case['bank_profile']);records.append(r);p=r['question']
  for k in (':question/problem',':question/worked-solution',':question/difficulty',':question/answer-fields',':question/math-academy-id'):
   assert (k in q)==(k in p),(q[':db/id'],'presence',k)
  assert p[':question/problem']==q[':question/problem']
  assert p[':question/math-academy-id']==q[':question/math-academy-id']
  if ':question/worked-solution' in q:assert p[':question/worked-solution']==q[':question/worked-solution'];solutions+=1
  if ':question/difficulty' in q:assert p[':question/difficulty']==q[':question/difficulty'][':db/ident']
  for f1,f2 in zip(q[':question/answer-fields'],p[':question/answer-fields']):
   assert f1[':answer-field/key']==f2[':answer-field/key'] and f1[':answer-field/type'][':db/ident']==f2[':answer-field/type']
   a1=f1[':answer-field/choices'];a2=f2[':answer-field/choices'];assert sorted(a[':answer/value'] for a in a1)==sorted(a[':answer/value'] for a in a2)
   assert (':answer-field/correct' in f1)==(':answer-field/correct' in f2)
   if ':answer-field/correct' in f1:
    v2=next(a[':answer/value'] for a in a2 if a[':answer/id']==f2[':answer-field/correct'][1]);assert v2==f1[':answer-field/correct'][':answer/value'];corrects+=1
   banks+=1;values+=len(a1)
  check_record(r)
 (ROOT/'source-cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=2)+'\n')
 return records,{'prompts':{'matched':11,'total':11},'complete_banks':{'matched':banks,'total':11},'option_values':{'matched':values,'total':51},'existing_solutions':{'matched':solutions,'total':10},'existing_correct_designations':{'matched':corrects,'total':10},'missing_designation_inferred_only':1,'key_omissions_preserved':True}


def main():
 originals,source_results=fidelity();generated=[];evidence_variants=[];coverage=set();tests=0
 for level in ('easy','moderate','hard'):
  templates=['constant'] if level=='easy' else ['canonical'] if level=='hard' else [n for n,d in g.FAMILIES.items() if d['source']]
  for name in templates:
   for seed in range(12):
    r=g.generate(level,seed,template=name);check_record(r);tests+=1;coverage.add(name)
    same=g.generate(level,seed+100,template=name,parameters=r['generation']['parameters'])
    assert same['question'][':question/id']==r['question'][':question/id']
    assert same['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
    if seed<2:generated.append(r)
 positions={next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]) for r in generated}
 assert len(positions)>1,'correct answer always in one position'
 # Changed explicit historical profiles remain evidence-only; mathematical
 # source designation (when present) still agrees with the displayed new box.
 for source in g.QUESTIONS:
  name=next((n for n,d in g.FAMILIES.items() if d['source']==source[':db/id']),'context_setup')
  for k in range(2):
   for seed in range(70+k*100,170+k*100):
    params={'c':3+k,'cap':5+k} if name=='context_setup' else g.generate('moderate',seed,template=name)['generation']['parameters']
    try:r=g.generate('moderate',seed,template=name,parameters=params,profile='observed:'+str(source[':db/id']))
    except ValueError:continue
    break
   else:raise AssertionError('historical changed profile availability')
   check_record(r);tests+=1;evidence_variants.append(r)
 # Exercise unbiased default coverage, all returned instances are valid.
 default_templates=set()
 for seed in range(60):
  r=g.generate('moderate',seed);check_record(r);default_templates.add(r['generation']['template']);tests+=1
 assert default_templates=={n for n,d in g.FAMILIES.items() if d['source']}
 # Whole-bank collision rejection, explicit scope limits, and formatting regressions.
 mutations=0
 for name in ('cos','affine','exp','canonical'):
  level='hard' if name=='canonical' else 'moderate';r=g.generate(level,41,template=name)
  for mutation in ('primitive','endpoint','partial','formal','factorization','control'):
   mutant=json.loads(json.dumps(r));q=mutant['question'];sol=q[':question/worked-solution']
   if mutation=='control':q[':question/problem']+='\x0c'
   elif mutation=='formal':q[':question/worked-solution']=sol.replace(r'\frac{∂}{∂x}',r'\frac{∂}{∂y}',1)
   elif mutation=='partial':q[':question/worked-solution']=sol.replace(r'\\  & =',r'\\  & =1+',1)
   elif mutation=='factorization':
    blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);block=blocks[1];rows=block.split(r'\\  & =');rows[2]=rows[-1];q[':question/worked-solution']=sol.replace(block,r'\\  & ='.join(rows),1)
   elif mutation=='primitive':
    block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1];rows=block.split(r'\\  & =');rows[3]=rows[3].replace('[','[1+',1);q[':question/worked-solution']=sol.replace(block,r'\\  & ='.join(rows),1)
   else:
    block=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1];rows=block.split(r'\\  & =');factors=split_product(rows[4]);upper,lower=endpoint_parts(factors[0]);factors[0]='(('+g.tex(upper)+')+1-(('+g.tex(lower)+')+1))';rows[4]=r'\cdot '.join(factors);q[':question/worked-solution']=sol.replace(block,r'\\  & ='.join(rows),1)
   try:check_record(mutant)
   except Exception:mutations+=1
   else:raise AssertionError('mutation escaped '+mutation)
 # Primitive constant shift alone is a legal primitive and must only fail when
 # its displayed endpoint values do not shift too: independent checks catch this.
 for level,name,b in [('hard','canonical',[0,1,0,2,1,2]),('moderate','cos',[0,6,0,1,0,'pi/2']),('easy','constant',[0,2,0,2,0,2])]:
  try:g.generate(level,template=name,parameters={'bounds':b,**({'a':2} if name=='constant' else {})})
  except ValueError:pass
  else:raise AssertionError('scope guard')
 for invalid_a in (1,10,-2,2.5):
  try:g.generate('easy',template='constant',parameters={'bounds':[0,2,0,3,0,4],'a':invalid_a})
  except ValueError:pass
  else:raise AssertionError('easy coefficient guard')
 for level,name in [('easy','constant'),('moderate','cos'),('hard','canonical')]:
  try:g.generate(level,template=name,parameters={})
  except ValueError:pass
  else:raise AssertionError('empty explicit parameters silently sampled')
 # Grader tests every owned choice on every generated review question and all
 # source records with observed correct refs, plus a supported equivalent blank.
 engine=[]
 for i,r in enumerate(originals+generated+evidence_variants):
  f=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue
  correct=f[':answer-field/correct'][1];checks=[]
  if f[':answer-field/type'].endswith('/blank'):
   checks=[{'submitted':t,'expected':e,'purpose':p} for t,e,p in [(f[':answer-field/choices'][0][':answer/value'],'accepted','fragment'),(str(r['generation']['parameters'].get('c',2)-1)+'x+x','accepted','independent equivalent sum'),(str(r['generation']['parameters'].get('c',2)+1)+'x','rejected','wrong derivative')]]
  else:
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'owned correct or distractor'} for a in f[':answer-field/choices']]
  engine.append({'label':str(i),'record':r,'checks':checks})
 (ROOT/'engine-input.json').write_text(json.dumps(engine,ensure_ascii=False,indent=2)+'\n')
 subprocess.run(['generate/runs/current/check-engine',str(ROOT/'engine-input.json'),str(ROOT/'engine-report.json')],check=True)
 (ROOT/'review.json').write_text(json.dumps(generated+evidence_variants,ensure_ascii=False,indent=2)+'\n')
 md=['# Source and generated review\n\nRaw observed profiles are evidence-only; generated variants use complete method-derived banks.\n']
 for i,r in enumerate(originals):
  sid=g.QUESTIONS[i][':db/id'];md+=['## Original '+str(sid)+'\n',g.markdown(r)]
  if r['generation']['template']!='context_setup':
   for v in generated:
    if v['generation']['template']==r['generation']['template']:md+=['### Generated '+v['generation']['template']+' '+str(v['generation']['seed'])+'\n',g.markdown(v)]
 for r in evidence_variants:md+=['## Generated historical bank evidence '+r['generation']['profile']+' seed '+str(r['generation']['seed'])+' (ineligible)\n',g.markdown(r)]
 for r in generated:
  if r['generation']['level'] in ('easy','hard'):md+=['## Authored '+r['generation']['level']+' '+str(r['generation']['seed'])+'\n',g.markdown(r)]
 (ROOT/'review.md').write_text('\n\n'.join(md)+'\n')
 report={'status':'pass_with_documented_ineligible_source_context','source_fidelity':source_results,'mathematical_records_checked':tests+11,'mutation_regressions_rejected':mutations,'default_moderate_family_coverage':sorted(default_templates),'native':json.loads((ROOT/'engine-report.json').read_text()),'scope':'same KP, rectangular closed surfaces, exact held partials and separable integration','authored_levels':['easy','hard'],'plots':'none','runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'finite_sampler_catalog':json.loads((ROOT/'catalog.json').read_text()) if (ROOT/'catalog.json').exists() else None,'native_binary_sha256':hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest(),'unresolved_source_context':{'source_id':17592186235537,'full_prompt_correctness':'unavailable: original refers to missing prior part','normal_default':False},'unresolved_bank_intentions':'All observed scalar distractor intentions underdetermined. Public replay patterns reproduce evidence; default banks use documented actual method operations.'}
 (ROOT/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print('PASS',tests+11,'independent records;',source_results)
if __name__=='__main__':main()
