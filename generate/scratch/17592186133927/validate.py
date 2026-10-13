#!/usr/bin/env python3
"""Private exact, source, display, scope, identity and native-grading checks."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,tempfile,shutil
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)

def group(text,start):
 assert text[start]=='{';depth=1;i=start+1
 while depth:
  if text[i]=='{':depth+=1
  elif text[i]=='}':depth-=1
  i+=1
 return text[start+1:i-1],i

def readmath(text):
 text=text.strip().rstrip('.,').replace('π',r'\pi').replace('⁡','')
 for cmd in ('\\left','\\right',r'\,',r'\!',r'\;'):text=text.replace(cmd,'')
 while '\\frac' in text or '\\sqrt' in text:
  candidates=[(text.index(c),c) for c in ('\\frac','\\sqrt') if c in text];at,cmd=min(candidates)
  u,j=group(text,at+len(cmd));u=str(readmath(u))
  if cmd=='\\frac':v,j=group(text,j);value='(('+u+')/('+str(readmath(v))+'))'
  else:value='sqrt('+u+')'
  text=text[:at]+value+text[j:]
 text=text.replace('\\theta','theta').replace('\\pi','pi').replace('\\sin','sin').replace('\\cos','cos').replace('\\cdot','*').replace('\\ln','log')
 text=text.replace('{','(').replace('}',')').replace('[','(').replace(']',')').replace('^','**')
 local={'x':g.X,'y':g.Y,'z':g.Z,'r':g.R,'theta':g.T,'pi':s.pi,'e':s.E,'sin':s.sin,'cos':s.cos,'sqrt':s.sqrt,'log':s.log}
 return s.simplify(parse_expr(text,local_dict=local,transformations=standard_transformations+(implicit_multiplication_application,)))

def equal(a,b):assert s.simplify(a-b)==0,(a,b)
def mathformat(t):
 assert t.count('$')%2==0
 depth=0
 for c in t:
  if c=='{':depth+=1
  elif c=='}':depth-=1
  assert depth>=0
 assert depth==0
 assert '--' not in t and '+-' not in t

def validate_record(r):
 q=r['question'];m=r['generation'];name=m['template'];p=m['parameters']
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 if m['evidence_only']:return
 for key in (':question/problem',':question/worked-solution'):mathformat(q[key])
 for f in q[':question/answer-fields']:
  vals=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(set(vals))==len(vals)
  for val in vals:mathformat(val)
  if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 # Read actual prompt field and solution graph, then recompute derivatives,
 # substituted curl, oriented flux, complete bank integrals and endpoints.
 prompt=q[':question/problem'];sol=q[':question/worked-solution']
 graph=readmath(re.search(r'\$\$z=g\(x,y\)=(.*?)\.\$\$',sol).group(1))
 curltext=re.search(r'\\text\{curl\}\\,F=\\langle (.*?)\\rangle',prompt).group(1)
 curl=tuple(readmath(v) for v in curltext.split(',\\,'));assert len(curl)==3
 equal(sum(s.diff(c,v) for c,v in zip(curl,(g.X,g.Y,g.Z))),0)
 ref=g.model(name,p);equal(graph,ref['g'])
 for a,b in zip(curl,ref['c']):equal(a,b)
 # Printed boundary graph must match the selected graph, including shifted
 # coordinates and nonzero plane slopes.
 assert ('$z='+g.tex(graph)+'$' in prompt) or name in ('horizontal','exponential','negative_cone')
 derivatives=re.findall(r'\\right\)=(.*?)\.?(?:\\\\|\.\\end)',sol)
 assert len(derivatives)>=2
 equal(readmath(derivatives[0]),s.diff(graph,g.X));equal(readmath(derivatives[1]),s.diff(graph,g.Y))
 sub=tuple(c.subs(g.Z,graph) for c in curl);terms=(-sub[0]*s.diff(graph,g.X),-sub[1]*s.diff(graph,g.Y),sub[2]);flux=s.simplify(sum(terms))
 rows=sol.split(r'\\')
 displayed_flux=next(row for row in rows if row.startswith('\n&=\\iint_D\\left(') and '\\end{aligned}' in row)
 body=displayed_flux.split(r'\left(',1)[1].split(r'\right)\,\mathrm{d}A',1)[0]
 equal(readmath(body),flux)
 # The actual printed substituted vector and every distributed component.
 vectors=re.findall(r'&=\\langle (.*?)\\rangle',sol)
 assert len(vectors)>=2
 for v,w in zip(vectors[-1].split(',\\,'),sub):equal(readmath(v),w)
 products=next(row for row in rows if row.startswith('\n&=\\iint_D\\left(-\\left('))
 equal(readmath(products.split(r'\left(',1)[1].split(r'\right)\,\mathrm{d}A',1)[0]),flux)
 expanded=next(row for row in rows if row.startswith('\n&=\\iint_D\\left(('))
 equal(readmath(expanded.split(r'\left(',1)[1].split(r'\right)\,\mathrm{d}A',1)[0]),flux)
 bank,recipes,values=g.bank(name,ref,p)
 field=q[':question/answer-fields'][0]
 expected=[v if isinstance(v,str) else g.tex(v) for v in bank]
 if field[':answer-field/choices'][0][':answer/type']==':answer.type/text':expected=['$$\n'+r'\begin{aligned}'+v+r'\end{aligned}'+'\n$$' for v in expected]
 assert sorted(expected)==sorted(a[':answer/value'] for a in field[':answer-field/choices'])
 correct=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert correct==expected[0]
 if ref['dom']:
  if name=='tilted_blank':equal(readmath(correct),flux)
  else:
   # Parse complete displayed ordered integrals, including every incorrect bank.
   observed_numeric=[]
   for value,num in zip(expected,values if values is not None else [None]*len(expected)):
    value=value.replace('$$','').replace(r'\begin{aligned}','').replace(r'\end{aligned}','').strip()
    match=re.fullmatch(r'\\int_\{(.*?)\}\^\{(.*?)\}\\int_\{(.*?)\}\^\{(.*?)\}\\left\((.*?)\\right\)\\,\\mathrm\{d\}y\\,\\mathrm\{d\}x',value)
    assert match,value
    x0,x1,y0,y1,integrand=map(readmath,match.groups())
    if name!='reciprocal':equal(g.setup_value(integrand,(x0,x1,y0,y1)),num)
    else:
     fn=s.lambdify((g.X,g.Y),integrand,'mpmath');import mpmath as mp
     val=mp.quad(lambda x:mp.quad(lambda y:fn(x,y),[float(y0),float(y1)]),[float(x0),float(x1)])
     observed_numeric.append(val)
   if name=='reciprocal':
    assert all(abs(u-v)>1e-8 for i,u in enumerate(observed_numeric) for v in observed_numeric[:i])
    # Exact analytic bank proof uses exp(3)>19; its positive Taylor terms
    # through degree six already exceed 19.
    assert sum(s.Rational(3)**j/s.factorial(j) for j in range(7))>19
    assert s.Rational(11,8)<2
 else:
  pol=flux.subs({g.X:g.R*s.cos(g.T),g.Y:g.R*s.sin(g.T)},simultaneous=True)*g.R
  prim=s.integrate(pol,g.T);ang=s.simplify(prim.subs(g.T,2*s.pi)-prim.subs(g.T,0));rad=s.integrate(ang,g.R)
  polarrows=[row[row.index(r'&=\int_0^'):] for row in rows if r'&=\int_0^' in row and r'\int_0^{2\pi}' in row]
  assert len(polarrows)==2
  for row in polarrows:
   bound,end=group(row,row.index(r'\int_0^')+len(r'\int_0^'));equal(readmath(bound),ref['disk'])
  displayed_sub=polarrows[0].split(r'\left(',1)[1].split(r'\right)r\,',1)[0]
  equal(readmath(displayed_sub)*g.R,pol)
  displayed_pol=polarrows[1].split(r'\left(',1)[1].split(r'\right)\,',1)[0]
  equal(readmath(displayed_pol),pol)
  angle_eval=next(row for row in rows if row.startswith('\n&=\\int_0^') and r'\left[\left(' in row)
  equal(readmath(angle_eval.split(r'\left[',1)[1].split(r'\right]\,',1)[0]),ang)
  endpoint_row=next(row for row in rows if row.startswith('\n&=\\left[') and r'\right]-\left[' in row)
  equal(readmath(endpoint_row.split('&=',1)[1]),rad.subs(g.R,ref['disk'])-rad.subs(g.R,0))

  # Read each actual displayed primitive. Never infer from generation metadata.
  br=[]
  for mm in re.finditer(r'\\left\[(.*?)\\right\]_0\^',sol):
   bound,end=group(sol,mm.end());br.append((mm.group(1),bound))
  assert len(br)==2
  equal(s.diff(readmath(br[0][0]),g.T),pol);equal(readmath(br[0][1]),2*s.pi)
  equal(s.diff(readmath(br[1][0]),g.R),ang);equal(readmath(br[1][1]),ref['disk'])
  result=s.simplify(rad.subs(g.R,ref['disk'])-rad.subs(g.R,0));equal(readmath(correct),result)
  final=re.search(r'&=([^&]*?)\.\\end\{aligned\}\$\$\s*$',sol).group(1).split(r'\\')[-1]
  equal(readmath(final),result)
  for v in field[':answer-field/choices']:readmath(v[':answer/value'])
 return True

def engine_item(r,label):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  for a in f[':answer-field/choices']:
   if f[':answer-field/type'].endswith('/blank'):
    checks.extend([{'field_index':i,'submitted':a[':answer/value'],'expected':'accepted','purpose':'canonical math blank'}, {'field_index':i,'submitted':r'\left('+a[':answer/value']+r'\right)+1-1','expected':'accepted','purpose':'equivalent unreduced polynomial plus cancelling constants'}, {'field_index':i,'submitted':'0','expected':'rejected','purpose':'wrong integrand'}])
   else:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned ID radio grading; math separately checked'})
 return {'label':label,'record':r,'checks':checks}

def source_integral(value):
 value=value.replace(r'{\int }',r'\int').replace(r'\displaystyle','').replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('$$','').strip()
 value=value.replace(r'\text{d}y',r'\mathrm{d}y').replace(r'\text{d}x',r'\mathrm{d}x')
 pos=0;bounds=[]
 for _ in range(2):
  pos=value.index(r'\int',pos)+len(r'\int');assert value[pos]=='_';lo,pos=group(value,pos+1);assert value[pos]=='^';hi,pos=group(value,pos+1);bounds.extend([readmath(lo),readmath(hi)])
 integrand=value[pos:value.index(r'\mathrm{d}y',pos)].strip().rstrip(r'\,')
 return readmath(integrand),tuple(bounds)

def audit_sources():
 audit=[]
 for sid,q in g.Q.items():
  name=g.SOURCE_FAMILY[sid];m=g.model(name,g.ORIGINAL[name]);entry={'source_id':sid,'graph':str(m['g']),'partials':[str(m['gx']),str(m['gy'])],'substituted_curl':list(map(str,m['sub'])),'flux':str(m['f']),'field_banks':[],'independent_curl_divergence_zero':True}
  equal(sum(s.diff(c,v) for c,v in zip(m['c'],(g.X,g.Y,g.Z))),0)
  answer=g.polar_value(m['polar'],m) if m['disk'] is not None else g.setup_value(m['f'],m['dom']) if name!='reciprocal' else None
  entry['circulation']=str(answer)
  for f in q[':question/answer-fields']:
   bank={'field_id':f[':db/id'],'choices':[]};vals=[]
   for a in f[':answer-field/choices']:
    value=a[':answer/value']
    if f[':db/id']==17592186130942:
     bank['choices'].append({'raw':value,'status':'malformed legacy powers; raw-preserved, mathematically ineligible'});continue
    if r'\int' in value:
     expr,dom=source_integral(value)
     if name=='reciprocal':
      import mpmath as mp
      fn=s.lambdify((g.X,g.Y),expr,'mpmath');v=mp.quad(lambda x:mp.quad(lambda y:fn(x,y),[float(dom[2]),float(dom[3])]),[float(dom[0]),float(dom[1])])
     else:v=g.setup_value(expr,dom)
     bank['choices'].append({'raw':value,'integrand':str(expr),'ordered_bounds':list(map(str,dom)),'complete_value':str(v)});vals.append(v)
     if a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id'):
      equal(expr,m['f']);assert dom==m['dom']
    else:
     v=readmath(value);vals.append(v);bank['choices'].append({'raw':value,'complete_value':str(v)})
     if a[':answer/id']==f.get(':answer-field/correct',{}).get(':answer/id'):equal(v,m['f'] if name=='tilted_blank' else answer)
   duplicate_pairs=[(i,j) for i,v in enumerate(vals) for j,w in enumerate(vals[:i]) if abs(complex(s.N(v-w)))<1e-10]
   bank['equal_complete_values']=duplicate_pairs
   assert not duplicate_pairs or sid=='q-162361'
   entry['field_banks'].append(bank)
  # Independently demonstrate the two source primitive defects; expected source
  # defects are evidence findings, never mathematical successes.
  if sid=='q-162373':
   bad=-g.R**3*g.T+3*g.R**2*s.cos(g.T)-g.R*g.T
   needed=-g.R**3+2*g.R**2*s.cos(g.T)-g.R**2*s.sin(g.T)-g.R
   assert s.simplify(s.diff(bad,g.T)-needed)!=0
   equal(-8*s.pi*(-s.Rational(1,4)-s.Rational(1,2)),6*s.pi)
   equal(answer,-6*s.pi);entry['primitive_errors_verified']=2
  audit.append(entry)
 (HERE/'source-math-audit.json').write_text(json.dumps(audit,indent=2,ensure_ascii=False)+'\n')

def concurrency_check():
 saved=g.HERE
 with tempfile.TemporaryDirectory(dir=HERE,prefix='render-stress-') as folder:
  fresh=Path(folder);(fresh/'assets').mkdir();shutil.copyfile(HERE/'render.py',fresh/'render.py');g.HERE=fresh
  try:
   calls=[('triangle',1),('triangle',1),('xy_triangle',3),('cone_triangle',2)]
   with ThreadPoolExecutor(max_workers=4) as pool:
    paths=list(pool.map(lambda call:g.render_plots(call[0],{'a':call[1]}),calls))
   assert paths[0]==paths[1] and len(set(paths))==3
   sides=[json.loads(Path(path).with_suffix('.json').read_text()) for path in paths]
   for side,(name,a) in zip(sides,calls):assert side['parameters']['name']==name and side['parameters']['a']==a
   assert not list(fresh.glob('*.render-input.json'))
   (HERE/'render-concurrency.json').write_text(json.dumps({'fresh_writes':4,'same_instance_atomic':True,'different_instances_isolated':True,'unique_inputs_cleaned_after_all_calls':True,'sidecars':sides},indent=2)+'\n')
  finally:g.HERE=saved

def main():
 audit_sources()
 concurrency_check()
 rec=[];native=[];cases=[];fidelity={'questions':0,'fields':0,'choices':0,'correct_designations':0,'absent_correct_designations':0,'worked_solutions':0,'missing_worked_solutions':0,'raw_attribute_presence':True};coverage={}
 for source in g.Q.values():
  sid=source[':question/math-academy-id'];name=g.SOURCE_FAMILY[sid];level=g.FAMILIES[name][0]
  case={'source_id':sid,'template':name,'level':level,'parameters':{'k':1},'bank_profile':'raw:'+sid};cases.append(case)
  r=g.generate(level,template=name,parameters={'k':1},profile='raw:'+sid);q=r['question'];fidelity['questions']+=1
  assert q[':question/problem']==source[':question/problem']
  assert (':question/difficulty' in q)==(':question/difficulty' in source)
  assert (':question/worked-solution' in q)==(':question/worked-solution' in source)
  if ':question/worked-solution' in source:assert q[':question/worked-solution']==source[':question/worked-solution'];fidelity['worked_solutions']+=1
  else:fidelity['missing_worked_solutions']+=1
  for f,old in zip(q[':question/answer-fields'],source[':question/answer-fields']):
   fidelity['fields']+=1;assert f[':answer-field/type']==old[':answer-field/type'][':db/ident'];assert f[':answer-field/key']==old[':answer-field/key']
   assert sorted((a[':answer/value'],a[':answer/type']) for a in f[':answer-field/choices'])==sorted((a[':answer/value'],a[':answer/type'][':db/ident']) for a in old[':answer-field/choices']);fidelity['choices']+=len(f[':answer-field/choices'])
   assert (':answer-field/correct' in f)==(':answer-field/correct' in old)
   if ':answer-field/correct' in old:
    value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert value==old[':answer-field/correct'][':answer/value'];fidelity['correct_designations']+=1
   else:fidelity['absent_correct_designations']+=1
  # Native original fixture can only grade fields containing correct refs. Keep
  # raw public record intact and label the separate native fixture explicitly.
  fixture=copy.deepcopy(r);fixture['question'][':question/answer-fields']=[f for f in q[':question/answer-fields'] if ':answer-field/correct' in f]
  if fixture['question'][':question/answer-fields']:native.append(engine_item(fixture,'original native fixture '+sid))
  rec.append(r)
  scaled=g.generate(level,template=name,parameters={'k':2},profile='raw:'+sid);assert scaled['question'][':question/problem']!=r['question'][':question/problem'] or sid=='q-168625'
 for name,(level,sid) in g.FAMILIES.items():
  if name=='unrated':continue
  coverage[name]=0
  for seed in range(4):
   r=g.generate(level,seed,template=name);validate_record(r);coverage[name]+=1;rec.append(r);native.append(engine_item(r,name+'/'+str(seed)))
   p=r['generation']['parameters'];rr=g.generate(level,seed+100,template=name,parameters=p)
   assert rr['question'][':question/id']==r['question'][':question/id'];assert rr['generation']['math_fingerprint']==r['generation']['math_fingerprint']
  for p in ({'k':1,'a':1,'h':2},{'k':4,'a':3,'h':4}):
   try:r=g.generate(level,template=name,parameters=p)
   except ValueError as e:
    assert 'bank' in str(e);continue
   validate_record(r);rec.append(r);native.append(engine_item(r,name+'/boundary/'+str(p)))
  for key,val in [('k',0),('a',4),('h',5)]:
   p={'k':1,'a':1,'h':2};p[key]=val
   try:g.generate(level,template=name,parameters=p)
   except ValueError:pass
   else:raise AssertionError('out-of-scope explicit parameters admitted')
 # Default family coverage: seeded family selection does not silently omit sources.
 defaults={l:set() for l in ['easy','moderate','hard']}
 for l in defaults:
  for seed in range(35):defaults[l].add(g.generate(l,seed)['generation']['template'])
  assert defaults[l]=={n for n,(ll,_) in g.FAMILIES.items() if ll==l and n!='unrated'}
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(rec,indent=2,ensure_ascii=False)+'\n')
 (HERE/'engine-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine.json')],check=True)
 eng=json.loads((HERE/'engine.json').read_text())
 report={'status':'passed_with_explicit_ineligible_original_evidence','source_fidelity':fidelity,'normal_math_records':len(rec)-len(g.Q),'normal_family_coverage':coverage,'default_family_coverage':{l:sorted(v) for l,v in defaults.items()},'native':{k:v for k,v in eng.items() if k!='records'},'source_math_anomalies':['q-162373 angular primitive cos instead of sin; radial negative primitive under -8pi produces +6pi despite final -6pi','q-168625 prompt omits graph/vector-field context supplied in solution','q-161927 duplicate legacy field with malformed unpowered exponents and no correct ref','q-161926 unrated, missing correct ref and solution','q-162361 two distractor integrals have equal complete scalar value; one minimally repaired in normal bank','q-162374 extra closing parenthesis in original flux row; balanced in normal solution'],'unresolved':0,'ineligible_original_fields_missing_native_correct':2,'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'database_writes':0}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 lines=['# Originals and clearly labelled generated variants','Frozen basis 1356. Raw originals are evidence only, including opaque banks.','']
 for r in rec:
  m=r['generation'];lines.extend(['## '+m['template']+' — '+('ORIGINAL EVIDENCE' if m['evidence_only'] else 'GENERATED '+r['question'][':question/difficulty'].split('/')[-1]),'Parameters: '+json.dumps(m['parameters']),g.markdown(r),''])
 (HERE/'review.md').write_text('\n\n'.join(lines))
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
