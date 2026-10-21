#!/usr/bin/env python3
"""Independent full-bank fidelity, displayed math, raster geometry/native checks."""
import importlib.util,json,re,pathlib,math,subprocess,concurrent.futures,hashlib
import sympy as sp
H=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('kp',H.with_suffix('.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)

def load_rhs(prompt):
 # Read the actual displayed complete RHS, independently of generation metadata.
 t=prompt.split('x}=')[-1].split('?$')[0]
 def group(text,i):
  assert text[i]=='{';depth=1;j=i+1
  while depth:
   if text[j]=='{':depth+=1
   if text[j]=='}':depth-=1
   j+=1
  return text[i+1:j-1],j
 def convert(text):
  text=text.replace(r'\left','').replace(r'\right','').replace(' ','').replace('{e}', 'e');out='';i=0
  while i<len(text):
   if text.startswith(r'\frac',i):
    num,j=group(text,i+5);den,j=group(text,j);out+='(('+convert(num)+')/('+convert(den)+'))';i=j
   elif text.startswith('e^{',i):
    exponent,j=group(text,i+2);out+='exp('+convert(exponent)+')';i=j
   elif text.startswith('^{',i):
    power,j=group(text,i+1);out+='**('+convert(power)+')';i=j
   elif text[i]=='{':
    sub,j=group(text,i);out+='('+convert(sub)+')';i=j
   else:out+=text[i];i+=1
  return out
 t=convert(t);t=re.sub(r'(?<=\d)(?=[xy])','*',t);t=t.replace('xy','x*y')
 return sp.sympify(t,locals={'x':G.X,'y':G.Y,'exp':sp.exp})
def angular_distance(a,b):
 d=abs(a-b);return min(d,math.pi-d)
def braces(text):
 depth=0
 for i,c in enumerate(text):
  if i and text[i-1]=='\\':continue
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,'Unbalanced brace'
 assert depth==0,'Unbalanced brace'
 assert text.count('$')%2==0,'Unbalanced math delimiters'

def inspect_record(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];f=q[':question/answer-fields'][0];a=f[':answer-field/choices'];assert len(a)==5 and f[':answer-field/type']==':answer-field.type/radio'
 assert len(set(x[':answer/id'] for x in a))==5;assert len(set(x[':answer/value'] for x in a))==5
 assert f[':answer-field/correct'][0]==':answer/id';assert f[':answer-field/correct'][1] in [x[':answer/id'] for x in a]
 braces(q[':question/problem']);braces(q[':question/worked-solution'])
 assert len(re.findall(r'!\[\]\((.*?)\)',q[':question/worked-solution']))==2
 for x in a:
  assert x[':answer/type']==':answer.type/image'
  p=pathlib.Path(x[':answer/value']) if x[':answer/value'].startswith('/') else pathlib.Path('/media/jake/SSD/EDB/math')/x[':answer/value'];assert p.exists()
 if r['generation']['equation']:
  actual=load_rhs(q[':question/problem']);assert sp.simplify(actual-G.sym(r['generation']['equation']))==0
  assert G.depends(actual)=='xy'
 if r['generation']['authored']:
  exprs=[G.sym(x['expression']) for x in r['generation']['plot_objects']];deps=[G.depends(e) for e in exprs]
  assert deps.count('xy')==(4 if q[':question/difficulty'].endswith('/hard') else 1)
  for i,e in enumerate(exprs):
   for other in exprs[:i]:assert sp.simplify(e-other)!=0
  # Read renderer's exact slope input, then verify independently against each
  # symbolic display/field object. Actual PNG pixels checked separately below.
  by_content={}
  for x in a:
   side=json.loads(pathlib.Path(x[':answer/value']).with_suffix('.json').read_text());ps=side['points'];errors=[]
   for e in exprs:
    fnum=sp.lambdify((G.X,G.Y),e,'math');errors.append(max(abs(fnum(x,y)-m) for x,y,m in ps))
   assert sum(v<1e-10 for v in errors)==1

def source_geometry_check():
 reports=[]
 for sid,q in G.QS.items():
  for i,a in enumerate(q[':question/answer-fields'][0][':answer-field/choices']):
   v=a[':answer/value'];g=G.GEOMETRY[v];ps=g['segments_normalized'];spread=[]
   for k in (0,1):
    groups={}
    for p in ps:groups.setdefault(round(p[k]*16),[]).append(math.atan(p[2]))
    ds=sorted(max(v)-min(v) for v in groups.values() if len(v)>7);spread.append(ds[len(ds)//2])
   dep=('x' if spread[0]<.15 else '')+('y' if spread[1]<.15 else '')
   # A invariant vertical column => x-only; invariant horizontal row => y-only.
   actual='x' if spread[0]<.15 else ('y' if spread[1]<.15 else 'xy')
   expected=G.source_bank(sid,1)[1][i]['dependence'];assert actual==expected,(sid,i,actual,expected,spread)
   assert hashlib.sha256((pathlib.Path('/media/jake/SSD/EDB/math')/v).read_bytes()).hexdigest()==g['source_sha256']
   report={'source':sid,'option_index':i,'asset':v,'independent_dependence':actual,'median_column_angle_spread':spread[0],'median_row_angle_spread':spread[1]}
   if sid in G.SOURCE_TYPES and i==G.SPECS[sid][-1]:
    bounds=(-1,3,-2.5,1) if sid=='q-96476' else (-2.5,2.5,-2.5,2.5);x0,x1,y0,y1=bounds;expr=load_rhs(q[':question/problem']);fn=sp.lambdify((G.X,G.Y),expr,'math');err=[]
    for u,w,m in ps:err.append(abs(math.atan(m*(y1-y0)/(x1-x0))-math.atan(fn(x0+(x1-x0)*u,y0+(y1-y0)*w))))
    err.sort();assert err[len(err)//2]<.07 and err[int(.9*len(err))]<.25
    report['equation_geometry_median_angular_error']=err[len(err)//2];report['equation_geometry_p90_angular_error']=err[int(.9*len(err))];report['raster_estimation_limit']='finite pixel PCA; clipped/short segment outliers retained, no exact slope recovery claim'
   reports.append(report)
 return reports

def main():
 cases=[];replays=[];fidelity=[]
 for asset in json.loads((H/'original-assets.json').read_text()):
  local=(H/asset['asset']).read_bytes();original=(pathlib.Path('/media/jake/SSD/EDB/math')/asset['asset']).read_bytes();assert local==original;assert hashlib.sha256(local).hexdigest()==asset['sha256']
 for sid,(level,t,base,tex,correct) in G.SPECS.items():
  case={'source_id':sid,'template':t,'parameters':{'scale':1},'bank_profile':sid,'level':level,'authored_level_assignment':sid=='q-96477'};cases.append(case)
  r=G.generate(level,template=t,parameters=case['parameters'],profile=sid);inspect_record(r);replays.append(r);q=G.QS[sid];field=r['question'][':question/answer-fields'][0]
  original=q[':question/answer-fields'][0];assert sorted(a[':answer/value'] for a in original[':answer-field/choices'])==sorted(a[':answer/value'] for a in field[':answer-field/choices'])
  assert q[':question/problem']==r['question'][':question/problem']
  has_correct=':answer-field/correct' in original
  if has_correct:
   actual=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert actual==original[':answer-field/correct'][':answer/value']
  has_solution=':question/worked-solution' in q
  if has_solution:assert q[':question/worked-solution']==r['question'][':question/worked-solution'],sid
  fidelity.append({'source_id':sid,'bank_options_matched':5,'bank_options_total':5,'prompt_exact':True,'original_designation_present':has_correct,'original_designation_matched':has_correct,'solution_present':has_solution,'solution_exact':has_solution,'inferred_correct':not has_correct})
 (H/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 # At least two changed examples for every observed complete bank/profile.
 variants=[]
 for sid,(level,t,*_) in G.SPECS.items():
  for scale in (.5,-1):variants.append(G.generate(level,seed=11,template=t,parameters={'scale':scale},profile=sid))
 # At least two variants for each authored template and every level.
 authored=[]
 for level,templates in G.TEMPLATES.items():
  for t in templates:
   for seed in (19,23):authored.append(G.generate(level,seed=seed,template=t))
 for r in variants+authored:inspect_record(r)
 records=replays+variants+authored
 # Fixed objects/content identity unaffected by shuffle; changed banks distinct.
 for r in records:
  g=r['generation'];other=G.generate(r['question'][':question/difficulty'].split('/')[-1],999,template=g['template'],parameters=g['parameters'],profile=g['bank_profile']);assert other['question'][':question/id']==r['question'][':question/id']
 assert len({r['generation']['mathematical_fingerprint'] for r in records})==3
 # Incidental template inputs cannot split identical displayed content IDs.
 for level,t,keys in [('easy','possible_linear',['orientation']),('moderate','possible_exp',['px','py','orientation','single']),('moderate','possible_product',['orientation','single']),('hard','impossible_x',['px','py','orientation'])]:
  base=G.generate(level,71,template=t);p=dict(base['generation']['parameters'])
  for k in keys:p[k]=({'px':3-p['px'],'py':3-p['py'],'orientation':'x' if p['orientation']=='y' else 'y','single':'quadratic' if p['single']=='linear' else 'linear'})[k]
  changed=G.generate(level,81,template=t,parameters=p)
  assert changed['question'][':question/id']==base['question'][':question/id'],(t,p)

 # Enumerate displayed symbolic banks without counting unused parameter slots.
 from itertools import product
 object_banks={'easy':set(),'moderate':set(),'hard':set()}
 vals=(-2,-1,1,2)
 for a,b,c in product(vals,vals,range(-2,3)):
  target=a*G.X+b*G.Y+c;bank=[target,a*G.X+c,b*G.Y+c,-a*G.X+c,-b*G.Y+c]
  object_banks['easy'].add((str(target),tuple(sorted(map(str,bank)))))
 for a,b in product(vals,vals):
  targets=[a*G.X**px*G.Y**py for px,py in product((1,2),(1,2))]+[a*G.Y+b*G.X**2,a*G.X+b*G.Y**2,sp.exp(a*G.X*G.Y)]
  for target in targets:object_banks['moderate'].add((str(target),tuple(sorted(map(str,[target,a*G.X,b*G.Y,a*G.X**2,b*G.Y**2])))))
  for z in [G.X,G.Y]:
   for target in [a*z,a*z**2,sp.exp(a*z)]:object_banks['hard'].add((str(target),tuple(sorted(map(str,[a*G.X+b*G.Y,a*G.X*G.Y,a*G.Y+b*G.X**2,sp.exp(a*G.X*G.Y),target])))))
 assert {k:len(v) for k,v in object_banks.items()}=={'easy':80,'moderate':112,'hard':96}
 # Explicit boundary guards (not just sampler guards).
 invalid=[('easy','possible_product',None),('easy','possible_linear',{'a':0,'b':1,'px':1,'py':1,'orientation':'y','single':'linear'}),('easy','possible_linear',{'a':1.0,'b':1,'px':1,'py':1,'orientation':'y','single':'linear'}),('easy','possible_linear',{'a':1,'b':1,'c':3,'px':1,'py':1,'orientation':'y','single':'linear'}),('moderate','possible_mixed',{'a':3,'b':1,'px':1,'py':1,'orientation':'y','single':'linear'}),('hard','impossible_y',{'a':1,'b':1,'px':0,'py':1,'orientation':'y','single':'linear'})]
 for level,t,p in invalid:
  try:G.generate(level,template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit parameters accepted')
 # Unique-input/atomic concurrent rendering exercises cold paths.
 jobs=[{'bounds':[-2,2,-2,2],'points':G.points(G.X+G.Y/3)},{'bounds':[-2,2,-2,2],'points':G.points(G.X-G.Y/3)}]
 for j in jobs:
  key=G.digest({'renderer':G.PROVENANCE,'version':G.VERSION,**j});path=H/'plots'/(key+'.png');path.unlink(missing_ok=True);path.with_suffix('.json').unlink(missing_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:outs=list(pool.map(lambda j:G.render_plots([j])[0],[jobs[0],jobs[0],jobs[1],jobs[1]]))
 assert outs[0]==outs[1] and outs[2]==outs[3] and outs[0]!=outs[2]
 for path,j in zip([outs[0],outs[2]],jobs):assert json.loads(pathlib.Path(path).with_suffix('.json').read_text())['points']==j['points']
 # A PNG-only cache entry is incomplete and must rebuild the sidecar.
 pathlib.Path(outs[0]).with_suffix('.json').unlink();assert G.render_plots([jobs[0]])[0]==outs[0];assert pathlib.Path(outs[0]).with_suffix('.json').exists()
 assert not list(H.glob('render-input-*.json'))
 # All displayed choices graded through the application's actual native grader.
 checks=[]
 for i,r in enumerate(records):
  field=r['question'][':question/answer-fields'][0];cid=field[':answer-field/correct'][1]
  checks.append({'label':str(i)+':'+r['generation']['bank_profile'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==cid else 'rejected','purpose':'complete five-image bank native grading'} for a in field[':answer-field/choices']]})
 (H/'engine-input.json').write_text(json.dumps(checks,indent=2)+'\n');subprocess.run(['generate/runs/current/check-engine',str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
 (H/'review.json').write_text(json.dumps(records,indent=2)+'\n')
 subprocess.run([G.RENDERER,str(H/'check_png.py'),str(H/'review.json'),str(H/'png-geometry.json')],check=True)
 png=json.loads((H/'png-geometry.json').read_text());png_reports=[]
 # Compare actual raster line geometry of every authored image to its unique
 # exact field formula (including all wrong choices), independently of IDs.
 for r in authored:
  exprs=[G.sym(v['expression']) for v in r['generation']['plot_objects']]
  for a in r['question'][':question/answer-fields'][0][':answer-field/choices']:
   path=a[':answer/value'];ps=png[path]['points'];assert len(ps)>100
   scores=[]
   for e in exprs:
    f=sp.lambdify((G.X,G.Y),e,'math');errs=sorted(angular_distance(angle,math.atan(f(x,y))) for x,y,angle in ps);scores.append((errs[len(errs)//2],errs[int(.9*len(errs))],str(e)))
   scores.sort();assert scores[0][0]<.06 and scores[0][1]<.20,(path,scores[0]);assert scores[1][0]>.08,(path,scores)
   png_reports.append({'image':path,'independent_matching_expression':scores[0][2],'median_angular_error':scores[0][0],'p90_angular_error':scores[0][1]})
 # Invariance classification and pairwise visual distinction from actual PNGs
 # for every changed replay and default bank, with no source ID assumptions.
 bank_pixel_checks=[]
 for r in variants+authored:
  field=r['question'][':question/answer-fields'][0];actual=[];signatures=[]
  for a in field[':answer-field/choices']:
   path=a[':answer/value'];ps=png[path]['points'];spread=[]
   for k in (0,1):
    groups={}
    for v in ps:groups.setdefault(round((v[k]+2)*4),[]).append(v[2])
    values=sorted(max(v)-min(v) for v in groups.values() if len(v)>7);assert values
    spread.append(values[len(values)//2])
   dep='x' if spread[0]<.15 else ('y' if spread[1]<.15 else 'xy');actual.append(dep)
   if a[':answer/id']==field[':answer-field/correct'][1]:assert dep==('xy' if r['generation']['template'].startswith('possible') else r['generation']['template'][-1]),(r['generation']['bank_profile'],dep)
   signature=[]
   for j in range(1,16):
    for i in range(1,16):
     x=-2+i/4;y=-2+j/4;closest=min(ps,key=lambda p:(p[0]-x)**2+(p[1]-y)**2);signature.append(closest[2])
   signatures.append(signature)
  assert actual.count('xy')==(1 if r['generation']['template'].startswith('possible') else 4),(r['generation']['bank_profile'],actual)
  gaps=[]
  for i,sig in enumerate(signatures):
   for other in signatures[:i]:
    diff=[angular_distance(a,b) for a,b in zip(sig,other)];diff.sort();gap=diff[len(diff)//2];assert gap>.06,(r['generation']['bank_profile'],gap);gaps.append(gap)
  bank_pixel_checks.append({'question_id':r['question'][':question/id'],'bank_profile':r['generation']['bank_profile'],'independent_option_dependences':actual,'minimum_pairwise_median_angular_gap':min(gaps)})
 (H/'bank-pixel-checks.json').write_text(json.dumps(bank_pixel_checks,indent=2)+'\n')
 # Every generated guide's underlying field matches the corresponding chosen
 # option, independent of guide metadata; blue lines may split a few gray marks.
 guide_checks=[]
 for r in variants+authored:
  q=r['question'];field=q[':question/answer-fields'][0];chosen=next(a[':answer/value'] for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);guide=re.findall(r'!\[\]\((.*?)\)',q[':question/worked-solution'])[-1]
  ps=png[guide]['points'];sourceps=png[chosen]['points'];errors=[]
  for x,y,angle in ps:
   nearest=min(sourceps,key=lambda p:(p[0]-x)**2+(p[1]-y)**2)
   if (nearest[0]-x)**2+(nearest[1]-y)**2<.012:errors.append(angular_distance(angle,nearest[2]))
  errors.sort();assert len(errors)>100 and errors[len(errors)//2]<.03,(guide,len(errors))
  guide_checks.append({'guide':guide,'chosen_plot':chosen,'median_angle_error':errors[len(errors)//2]})
 (H/'guide-pixel-checks.json').write_text(json.dumps(guide_checks,indent=2)+'\n')
 source_reports=source_geometry_check();(H/'source-geometry-checks.json').write_text(json.dumps(source_reports,indent=2)+'\n');(H/'png-checks.json').write_text(json.dumps(png_reports,indent=2)+'\n')
 review=['# Originals and generated variants','Basis 1356; originals retain all raw fields in source.json. Replay profiles preserve complete images. q-96477 has authored hard assignment and independently inferred designation, not an original designation match.']
 for r in records:
  g=r['generation'];label='Original replay' if r in replays else ('Generated empirical-bank variant' if not g['authored'] else 'Generated authored method bank')
  review+=['## '+label+' — '+g['template']+' / '+g['bank_profile'],json.dumps(g['parameters']),G.markdown(r)]
 (H/'review.md').write_text(('\n\n'.join(review)+'\n').replace(str(H.resolve())+'/', ''))
 eng=json.loads((H/'engine-report.json').read_text())
 result={'status':'passed','source_basis':1356,'source_practice_questions':8,'exact_source_banks':8,'matched_source_options':40,'total_source_options':40,'existing_correct_designations_matched':7,'existing_correct_designations_total':7,'missing_designations_independently_inferred':1,'original_exact_prompts':8,'original_exact_solutions':7,'original_available_solutions':7,'authored_missing_solutions':1,'raw_exact_vs_presentation_repaired':{'prompts':{'exact':8,'repaired':0},'solutions':{'exact':7,'repaired':0}},'source_fidelity':fidelity,'review_records':len(records),'authored_records':len(authored),'empirical_geometry_changed_variants':len(variants),'native_accepted':eng['accepted_checks'],'native_rejected':eng['rejected_checks'],'finite_meaningful_categorical_tasks':3,'task_categories':['possible both-variable field','exclude x-only field','exclude y-only field'],'parameter_coefficients_not_counted_as_tasks':True,'independent_source_option_geometry_checks':len(source_reports),'independent_generated_png_checks':len(png_reports),'independent_changed_bank_pixel_checks':len(bank_pixel_checks),'independent_guide_pixel_checks':len(guide_checks),'sampled_distinct_symbolic_bank_objects':{'easy':80,'moderate':112,'hard':96},'source_assets_byte_exact':len(json.loads((H/'original-assets.json').read_text())),'concurrent_atomic_rendering':'passed identical and different cold inputs','unresolved_findings':['Original wrong-field authoring formulas/intent absent; empirical banks are explicit replay profiles, not claimed recovered symbolic error recipes.','q-96477 lacks original designation, difficulty and worked solution; mathematical inference and authored hard/solution explicitly documented.'],'database_writes':0}
 (H/'validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
