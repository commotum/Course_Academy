"""Independent calculus, full source-bank replay and actual learner grading."""
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('log_generator',H.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sp=g.sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
x=sp.Symbol('x',real=True)
def parse(value):
 s=value.removeprefix('y=').replace(r'\operatorname{ln}',r'\ln').replace('ln\u2061',r'\ln').replace('ln',r'\ln')
 s=s.replace(r'\\ln',r'\ln').replace(r'\log',r'\ln').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*')
 s=re.sub(r'\\+ln',lambda _:r'\ln',s)
 def group(s,i):
  assert s[i]=='{';start=i+1;depth=1;i+=1
  while depth:
   if s[i]=='{':depth+=1
   elif s[i]=='}':depth-=1
   i+=1
  return s[start:i-1],i
 while r'\frac' in s:
  i=s.rfind(r'\frac');a,j=group(s,i+5);b,k=group(s,j);s=s[:i]+'(('+a+')/('+b+'))'+s[k:]
 # Source ln argument is either a group, parenthesized expression, or numeric literal.
 s=re.sub(r'\{x\}\^\{(\d+)\}',r'x^\1',s)
 s=re.sub(r'\\ln\s*\{([^{}]+)\}',r'log(\1)',s)
 s=re.sub(r'\\ln\s*(\d+)x',r'log(\1*x)',s)
 s=re.sub(r'\\ln\s*(\d+)',r'log(\1)',s)
 s=re.sub(r'\\ln\s*x\^\{?(\d+)\}?',r'log(x^\1)',s)
 s=s.replace(r'\ln','log').replace('{','(').replace('}',')').replace('^','**')
 s=re.sub(r'(?<=[0-9x)])log',r'*log',s)
 assert '\\' not in s,s
 expr=parse_expr(s,local_dict={'x':x,'log':sp.log},transformations=standard_transformations+(implicit_multiplication_application,))
 assert expr.free_symbols <= {x},('Unknown mathematical symbols',s,expr)
 return expr
def check(r):
 meta=r['generation'];t=meta['template'];p=next(iter(meta['parameters'].values()));q=r['question'];mid,param,orig,bounds=g.CONFIG[t]
 assert p in bounds and r==g.generate(t,meta['seed'],p)
 # Independently reconstruct the function and evaluation from the declared source family.
 if t.startswith('scale-'):fun=sp.log(p*x);answer=sp.diff(fun,x)
 elif t=='power-radio':fun=sp.log(x**p);answer=sp.diff(fun,x)
 elif t=='polynomial-blank':fun=sp.log(3-5*x**6);answer=sp.diff(fun,x)
 elif t=='slope-polynomial':fun=sp.log(p*x*x+4);answer=sp.diff(fun,x).subs(x,1)
 elif t=='slope-affine':fun=sp.log(p-4*x);answer=sp.diff(fun,x).subs(x,-1)
 else:
  point=0 if t=='tangent-origin' else p
  fun=sp.log(p*x+1) if t=='tangent-origin' else sp.log(p+1-x) if t=='tangent-shift' else p*sp.log(2*x)
  answer=sp.diff(fun,x).subs(x,point)*(x-point)+fun.subs(x,point)
 fields=q[':question/answer-fields'];assert len(fields)==1;f=fields[0]
 choices=f[':answer-field/choices'];expected=5 if f[':answer-field/type'].endswith('/radio') else 1
 assert len(choices)==expected
 values=[parse(a[':answer/value']) for a in choices]
 for i,a in enumerate(values):
  for b in values[i+1:]:assert sp.simplify(a-b)!=0,(t,p,'duplicate bank')
 matches=[i for i,v in enumerate(values) if sp.simplify(v-answer)==0];assert len(matches)==1,(t,p,values,answer)
 assert f[':answer-field/correct'][1]==choices[matches[0]][':answer/id']
 for text in [q[':question/problem'],q[':question/worked-solution']]:
  assert text.count('$')%2==0 and text.count('{')==text.count('}')
 # For new variants inspect every displayed symbolic u, du, derivative, slope and tangent value.
 if p!=orig:
  prompt_function=re.search(r'\$[fg]\(x\)=(.*?)\$',q[':question/problem'])
  assert prompt_function and sp.simplify(parse(prompt_function[1])-fun)==0
  u=sp.exp(fun) if t!='tangent-scaled' else 2*x
  u={ 'power-radio':x**p,'slope-polynomial':p*x*x+4,'slope-affine':p-4*x,'tangent-origin':p*x+1,'tangent-shift':p+1-x,'tangent-scaled':2*x}[t]
  s=q[':question/worked-solution'];assert 'u='+sp.latex(u)+'.' in s
  assert r'\frac{\text{d}u}{\text{d}x}='+sp.latex(sp.diff(u,x))+'.' in s
  assert r'&='+sp.latex(sp.simplify(sp.diff(fun,x)))+r'.\end{aligned}' in s
  if t.startswith('tangent-'):
   rendered=re.search(r'y &=([^\n]+?)\.\\end\{aligned\}',s)
   assert rendered and sp.simplify(parse(rendered[1])-answer)==0
  if t.startswith('slope-'):assert '}='+sp.latex(answer)+'.$$' in s
 assert ':question/math-academy-id' not in q
 return answer

def engine_item(label,r):
 target=check(r);f=r['question'][':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  for a in f[':answer-field/choices']:checks.append({'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every source-profile selection'})
 else:
  canonical=f[':answer-field/choices'][0][':answer/value']
  numerator,denominator=sp.fraction(target)
  equivalent=r'\frac{'+sp.latex(sp.expand(2*numerator))+'}{'+sp.latex(sp.expand(2*denominator))+'}'
  for s,expected,purpose in [(canonical,'accepted','Canonical'),(equivalent,'accepted','Equivalent fraction with doubled numerator and denominator'),(sp.latex(-target),'rejected','Wrong sign'),(sp.latex(target+1),'rejected','Wrong offset')]:checks.append({'field_index':0,'submitted':s,'expected':expected,'purpose':purpose})
 return {'label':label,'record':r,'checks':checks}

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 rows=[];replay=[];banks=0;options=0
 for t,(mid,param,orig,bounds) in g.CONFIG.items():
  source=g.SOURCES[mid];r=g.generate(t,0,orig);check(r)
  f=r['question'][':question/answer-fields'][0];sf=source[':question/answer-fields'][0]
  assert r['question'][':question/problem']==source[':question/problem']
  assert [a[':answer/value'] for a in f[':answer-field/choices']]==[a[':answer/value'] for a in sf[':answer-field/choices']]
  assert f[':answer-field/choices'][next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])][':answer/value']==sf[':answer-field/correct'][':answer/value']
  assert all(sp.simplify(parse(a[':answer/value'])-sp.sympify(recipe,locals={'x':x}))==0 for a,recipe in zip(sf[':answer-field/choices'],r['generation']['recipes']))
  if f[':answer-field/type'].endswith('/radio'):banks+=1;options+=5
  replay.append({'template':t,'source':mid,'complete_bank':True,'options':len(f[':answer-field/choices'])})
  for p in bounds:
   r=g.generate(t,77,p);check(r);assert r['question']==g.generate(t,99,p)['question'];rows.append(r)
 engine_input=[engine_item(str(i),r) for i,r in enumerate(rows)]
 for level in ['moderate','hard']:
  complete=g.batch(level,len(g.candidates(level)),125)
  assert len(complete)==len({r['generation']['mathematical_key'] for r in complete})
  assert [r['question'] for r in complete]==[r['question'] for r in g.batch(level,len(complete),125)]
  for invalid_count in [-1,len(complete)+1]:
   try:g.batch(level,invalid_count,125)
   except ValueError:pass
   else:raise AssertionError('Invalid finite batch request accepted')
 (H/'engine-input.json').write_text(json.dumps(engine_input,indent=2))
 subprocess.run([str(H/'check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
 e=json.loads((H/'engine-report.json').read_text());assert e['documented_unresolved_checks']==0
 (H/'review.md').write_text('\n\n'.join('## '+t+' — source and boundary variants\n\n'+'\n\n'.join(g.markdown(g.generate(t,0,p)) for p in sorted(set([c[2],c[3][0],c[3][-1]]))) for t,c in g.CONFIG.items()))
 (H/'source-bank-replay.json').write_text(json.dumps(replay,indent=2))
 report={'passed':True,'source_basis':g.SOURCE['basis'],'supported_levels':['moderate','hard'],'instances_checked':len(rows),'full_source_banks':banks,'matched_source_options':options,'matched_source_distractors':options-banks,'source_blank_replays':4,'grading':{k:e[k] for k in ['entry_point','accepted_checks','rejected_checks','documented_unresolved_checks']},'fidelity':'All five complete observed rated radio banks replayed; all four blanks replayed. New variants preserve mathematical sequence and source instructional prose with SymPy-rendered notation. Three incomplete/unrated sources explicitly excluded.','files':{str(p.relative_to(ROOT)):sha(p) for p in [H.with_suffix('.py'),Path(__file__),H/'source.json',H/'source.edn',H/'check-engine',H/'check-engine.rs',H/'capability.json',H/'source-components.json',H/'classification.md',H/'template-extraction.md',H/'plot-extraction.md']}}
 (H/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
