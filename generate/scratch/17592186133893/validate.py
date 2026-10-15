"""Parse rendered TeX, integrate independently and exercise the actual grader.

Validation dependency: antlr4-python3-runtime==4.11.1, optionally installed in
/tmp/course-academy-line-integral-deps. The generator itself needs only SymPy.
"""
import functools,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,'/tmp/course-academy-line-integral-deps')
from sympy.parsing.latex import parse_latex
spec=importlib.util.spec_from_file_location('line_integral',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,t,u=sp.symbols('x y t u',real=True)
def write(p,v):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def eq(a,b):return sp.simplify(sp.trigsimp(a-b))==0

def tex(s):
 s=g.clean(s).strip().rstrip('.,')
 s=re.sub(r'\\operatorname\{(sin|cos)\}',lambda m:'\\'+m[1]+' ',s)
 s=re.sub(r'\\(sin|cos)(?:\^\{([^{}]+)\})?\s*(\\pi\s*[txy]|\\pi|[txy])',lambda m:'\\'+m[1]+'('+m[3]+')'+('^{'+m[2]+'}' if m[2] else ''),s)
 s=s.replace(r'{\int }',r'\int').replace(r'\text{d}', 'd')
 s=re.sub(r'\\cdot\s*d([tu])',r'd\1',s)
 return s

@functools.lru_cache(None)
def parse(s):
 z=parse_latex(tex(s),strict=True)
 z=z.xreplace({s:({'x':x,'y':y,'t':t,'u':u,'e':sp.E,'pi':sp.pi}.get(str(s),s)) for s in z.free_symbols})
 z=z.replace(lambda a:isinstance(a,sp.core.function.AppliedUndef) and str(a.func) in ('t','x','y','u','pi'),lambda a:({'t':t,'x':x,'y':y,'u':u,'pi':sp.pi}[str(a.func)])*sp.Mul(*a.args))
 return z

@functools.lru_cache(None)
def evaluate(s):
 s=s.strip().rstrip('.,')
 m=re.fullmatch(r'(\d+)\\left\((.*)\\right\)',s,re.S)
 if m:return int(m[1])*evaluate(m[2])
 s=tex(s)
 # Evaluate the entire antiderivative (including its outside coefficient).
 m=re.search(r'(?:\{\|\}|\\,\{\|\}|\\,\||\|)?_\{([^{}]+)\}\^\{([^{}]+)\}$',s)
 if m and r'\int' not in s:
  primitive=s[:m.start()].rstrip().rstrip(',');primitive=primitive.removesuffix(r'\,')
  z=parse(primitive);var=u if u in z.free_symbols else t
  return sp.simplify(z.subs(var,parse(m[2]))-z.subs(var,parse(m[1])))
 return sp.simplify(parse(s).doit())

def displayed(q):
 m=re.search(r'Evaluate \$\{\\int \}_\{C\}(.*?)(\\,\\text\{d\}([xy]))',q[':question/problem']);assert m
 return parse(m[1]),m[3]

def fingerprint(q):
 f,d=displayed(q)
 # Oriented path and differential are part of the task; bank and seed are not.
 path=q[':question/problem'].split('where $C$',1)[1]
 return hashlib.sha256(json.dumps([sp.srepr(sp.simplify(f)),d,path],sort_keys=True).encode()).hexdigest()

def audit(rec):
 q=rec['question'];meta=rec['generation'];mid=meta['template'];c=meta['parameters']['c'];src=g.SOURCE_BY_ID[mid]
 f,d=displayed(q);base,path,bounds,sd=g.DATA[mid];assert d==sd and eq(f,c*base)
 # Exact preserved prompt suffix proves fixed oriented geometry and endpoint roles.
 assert q[':question/problem'].split('where $C$',1)[1]==g.clean(src[':question/problem']).split('where $C$',1)[1]
 path=tuple(map(sp.sympify,path));pull=sp.simplify(f.subs({x:path[0],y:path[1]},simultaneous=True));derivative=sp.diff(path[0 if d=='x' else 1],t)
 integrand=sp.trigsimp(pull*derivative);answer=sp.simplify(sp.integrate(integrand,(t,*bounds)))
 assert answer.is_real is not False and not answer.has(sp.zoo,sp.oo,sp.nan)
 sf=q[':question/answer-fields'][0];assert sf[':answer-field/type']==':answer-field.type/radio' and sf[':answer-field/key']=='selection'
 values=[parse(a[':answer/value']) for a in sf[':answer-field/choices']];assert len(values)==5
 assert len({a[':answer/id'] for a in sf[':answer-field/choices']})==5
 for a,z in zip(sf[':answer-field/choices'],values):assert eq(z,answer)==(a[':answer/id']==sf[':answer-field/correct'][1]),(mid,c,a,answer)
 assert all(not eq(a,b) for k,a in enumerate(values) for b in values[k+1:])
 solution=q[':question/worked-solution'];since=re.search(r'Now, since \$f\(x,y\)=(.*?)\$',solution)[1].rstrip(',');assert eq(parse(since),f)
 formula=re.search(r'\{\\int \}_\{C\}f\(x,y\)\\,\\text\{d\}([xy])=',solution);assert formula[1]==d
 n=0
 for block in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',solution,re.S):
  rows=block.split(r'\\')
  if block.startswith('r(t)'):
   for row in rows:
    vector=re.search('⟨(.*?)⟩',row)[1].split(r'\,');assert len(vector)==2
    assert all(eq(parse(a),b) for a,b in zip(vector,path));n+=2
  elif block.startswith(r'\frac{\text{d}'):
   assert eq(parse(rows[0].rsplit('=',1)[1]),derivative);n+=1
  elif block.startswith('f(r(t))'):
   for row in rows:assert eq(evaluate(row.split('& =',1)[1]),pull),(mid,c,row,pull);n+=1
  elif r'{\int }' in block:
   for k,row in enumerate(rows):
    lhs,rhs=row.split('& =',1)
    if k==0 and 'f(r(t))' in rhs:
     assert r'\text{d}'+d in lhs
     continue
    z=evaluate(rhs);assert eq(z,answer),(mid,c,row,z,answer);n+=1
 return {'fingerprint':fingerprint(q),'displayed_solution_values_checked':n,'exact_integral':str(answer)}

def native(records,path):
 path.mkdir(parents=True,exist_ok=True)
 inp=[{'label':str(k),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1] else 'rejected','purpose':'all complete bank choices through actual grade_field'} for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]} for k,r in enumerate(records)]
 write(path/'native-input.json',inp);binary=HERE/'reference/native/check-engine'
 z=subprocess.run([str(binary),str(path/'native-input.json'),str(path/'native-report.json')],capture_output=True,text=True,check=True,timeout=55);(path/'native.log').write_text(z.stdout+z.stderr)
 result=json.loads((path/'native-report.json').read_text());assert result['documented_unresolved_checks']==0;return result

def main():
 all_records=[];fidelity=[];components=[];review=[];coverage={}
 for mid,z in sorted(g.TEMPLATES.items()):
  print('Validating',mid,flush=True);src=g.SOURCE_BY_ID[mid];r=g.generate(z['level'],template=mid,parameters={'c':1});audit(r)
  assert r['question'][':question/problem']==g.normalize_prose(g.clean(src[':question/problem']))
  assert r['question'][':question/worked-solution']==g.corrected_solution(src)
  sf=src[':question/answer-fields'][0];gf=r['question'][':question/answer-fields'][0]
  matched=[]
  for a in sf[':answer-field/choices']:
   found=[b for b in gf[':answer-field/choices'] if eq(parse(a[':answer/value']),parse(b[':answer/value']))];assert len(found)==1
   assert (a[':answer/id']==sf[':answer-field/correct'][':answer/id'])==(found[0][':answer/id']==gf[':answer-field/correct'][1]);matched.append(a[':answer/id'])
  fidelity.append({'source':mid,'template':mid,'profile':z['profile'],'distractors_matched':4,'distractors_total':4,'complete_bank_matched':True,'missing':[],'extra':[],'prompt_exact_after_normalization':True,'solution_exact_after_recorded_corrections':True})
  f,path,bounds,d=g.DATA[mid]
  components.append({'source':mid,'source_db_id':src[':db/id'],'level':z['level'],'field_type':'radio','field_key':'selection','integrand':str(f),'oriented_path':list(map(str,path)),'bounds':list(map(str,bounds)),'differential':d,'source_prompt':src[':question/problem'],'source_solution':src[':question/worked-solution'],'parameter_slot':{'c':{'observed':1,'sampled':list(g.SCALES),'role':'positive multiplier of the supplied integrand; same differential, path and workload','dependencies':['prompt integrand','f(x,y)','each f(r(t)) value','each evaluated integral or substitution value','entire source choice bank'],'fixed_components_reason':'Path slots are deliberately narrow in this version because their endpoints and orientation control the integration and the reused diagram.'}},'profile':z['profile'],'choices':[{'answer_id':a[':answer/id'],'source_field':sf[':answer-field/id'],'observed_value':a[':answer/value'],'recipe':'c * ('+str(parse(a[':answer/value']))+')','correct':a[':answer/id']==sf[':answer-field/correct'][':answer/id'],'interpretation':'observed exact value scaled by linearity; underlying distractor misconception unresolved'} for a in sf[':answer-field/choices']]})
  coverage[mid]=[];all_records.append(r)
  for c in g.SCALES:
   v=g.generate(z['level'],seed=7,template=mid,parameters={'c':c});audit(v);all_records.append(v);coverage[mid].append(c)
   assert v==g.generate(z['level'],seed=7,template=mid,parameters={'c':c})
   assert v['question']==g.generate(z['level'],seed=8,template=mid,parameters={'c':c})['question']
   if c in (2,9):review.append({'source':src,'variant':v})
 assert len({fingerprint(r['question']) for r in all_records})==len(all_records)
 report=native(all_records,HERE/'reference/validation')
 write(HERE/'source-fidelity.json',fidelity);write(HERE/'source-components.json',components);write(HERE/'review.json',review)
 (HERE/'review.md').write_text('\n\n---\n\n'.join('Source '+z['source'][':question/math-academy-id']+'\n\n'+z['source'][':question/problem']+'\n\n'+z['source'][':question/worked-solution']+'\n\nVariant\n\n'+g.markdown(z['variant']) for z in review))
 write(HERE/'validation.json',{'status':'passed','source_basis':g.CAPTURE['basis'],'lineage':g.CAPTURE['lineage'],'templates':len(g.TEMPLATES),'complete_banks':len(fidelity),'matched_distractors':4*len(fidelity),'total_distractors':4*len(fidelity),'bounded_domain_instances':len(all_records),'distinct_mathematical_tasks':len(all_records),'sampled_slot_coverage':coverage,'all_displayed_solution_values_checked':True,'deterministic_replay':True,'seed_changes_not_new_content':True,'native':report,'native_binary_sha256':hashlib.sha256((HERE/'reference/native/check-engine').read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'excluded_sources':g.EXCLUDED,'dependencies':{'sympy':sp.__version__,'antlr4-python3-runtime':'4.11.1'}})
 print('Validated',len(all_records),'instances',flush=True)
if __name__=='__main__':main()
