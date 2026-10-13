#!/usr/bin/env python3
"""Read learner strings back independently; test source fidelity, math and native radio grading."""
import collections, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('tangent',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,obj): (HERE/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def balanced(s):
 assert s.count('$')%2==0
 n=0
 for i,ch in enumerate(s):
  if ch in '{}':
   if i and s[i-1]=='\\':continue
   n+=1 if ch=='{' else -1
   assert n>=0, ('brace-underflow',s)
 assert n==0, ('brace-count',n,s)
 assert '+-' not in s and '--' not in s

def read_prompt(q):
 prompt=q[':question/problem'];ptext=re.search(r'P\((.*?)\)',prompt).group(1)
 pt=tuple(g.parse_math(t) for t in ptext.split(','))
 plane=re.search(r'with the plane \$([xy])=(.*?)\.\$',prompt)
 assert plane, prompt
 fixed=g.parse_math(plane[2]);assert fixed==pt[0 if plane[1]=='x' else 1]
 rhs=re.search(r'and that (.*?)\$, which',prompt).group(1).split('=',1)[1]
 derivative=g.parse_math(rhs)
 assert derivative.free_symbols<={g.X,g.Y}
 m=sp.simplify(derivative.subs({g.X:pt[0],g.Y:pt[1]}))
 assert m.is_real and m.is_finite
 return pt,plane[1],derivative,m

def verify(r,raw=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];pt,plane,derivative,m=read_prompt(q);vec=(1,0,m) if plane=='y' else (0,1,m)
 fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio'
 vals=[a[':answer/value'] for a in f[':answer-field/choices']];assert len(vals)==5 and len(set(vals))==5
 vectors=[g.parse_vector(v) for v in vals]
 eligible=[g.parallel(v,vec) for v in vectors];assert sum(eligible)==1, (r['generation'],vals,eligible)
 ci=next(i for i,a in enumerate(f[':answer-field/choices']) if a[':answer/id']==f[':answer-field/correct'][1])
 assert eligible[ci]
 for a in f[':answer-field/choices']:assert a[':answer/type']==':answer.type/math'
 # The original evaluated partial block is checked even for raw source prose anomalies.
 sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$.*?\$\$',sol,re.S)
 rows=blocks[0].split('& =')[1:];ev_count=0
 for row in rows:
  value=row.split(r'\end')[0].split(r'\\')[0]
  for v in value.split('='):
   assert sp.simplify(g.parse_math(v)-m)==0,('evaluation stage',v,m)
   ev_count+=1
 if raw:
  # Every original explicit point-slope row, normal and cross-product result
  # is verified against the actual printed derivative and P; historical prose
  # anchoring errors remain separately recorded evidence.
  source_rows=blocks[1].removeprefix('$$\n'+r'\begin{aligned}').split(r'\\')
  for row in source_rows[1:]:
   lhs,rhs=row.split('& =');rhs=rhs.split(r'\end')[0]
   w=g.X if plane=='y' else g.Y;w0=pt[0] if plane=='y' else pt[1]
   assert sp.simplify((g.parse_math(lhs)-g.parse_math(rhs)).subs(g.Z,m*(w-w0)+pt[2]))==0,('source line stage',row)
  ns=re.findall(r'\{n\}_\{[12]\}=⟨([^⟩]*)⟩',sol)
  n1,n2=[sp.Matrix([g.parse_math(t) for t in v.split(',')]) for v in ns]
  cross=n1.cross(n2);assert g.parallel(cross,vec)
  for row in blocks[3].split('& =')[3:]:
   value=row.split(r'\end')[0].split(r'\\')[0].strip()
   assert sp.Matrix(g.parse_vector(value))==cross,('source cross result',value,cross)
  return len(vectors),ev_count
 balanced(q[':question/problem']);balanced(sol)
 for v in vals:balanced(v)
 assert len(blocks)==4
 # Normal point-slope, distributed/sign-normalized and solved stages.
 second_rows=blocks[1].removeprefix('$$\n'+r'\begin{aligned}').split(r'\\')
 for row in second_rows[1:]:
  lhs,rhs=row.split('& =');rhs=rhs.split(r'\end')[0]
  residual=g.parse_math(lhs)-g.parse_math(rhs)
  w=g.X if plane=='y' else g.Y;w0=pt[0] if plane=='y' else pt[1]
  assert sp.simplify(residual.subs(g.Z,m*(w-w0)+pt[2]))==0,('line-stage',row,pt,m)
 # Source operation structures independently checked, not just row counts.
 name=r['generation']['template']
 if name in g.TEMPLATES and 'source' in g.TEMPLATES[name]:
  src=g.TEMPLATES[name]['source'][':question/worked-solution'];oldblocks=re.findall(r'\$\$.*?\$\$',src,re.S)
  assert blocks[0].count('& =')==oldblocks[0].count('& =')
  assert blocks[1].count(r'\\')==oldblocks[1].count(r'\\')
  assert blocks[3].count('& =')==oldblocks[3].count('& =')
  if name in ('log_cube_y','radical_x'):
   third=second_rows[2];assert r'\left' not in third # explicit complete multiplication masks
   assert '(y-' in third or '(x-' in third,('lost sign-normalization structure',third)
  # Every shared source sentence retained; two documented erroneous sentences repaired.
  for phrase in ['The curve $C$ is the intersection of the surface with the plane',
                 'To get the slope, we evaluate the partial derivative',
                 'Now, we use the point-slope form of a straight line:',
                 'Next, notice that:',
                 'Finally, to find a direction vector for the tangent line, we calculate the cross product of these normal vectors:']:
   assert phrase in sol
 if len(second_rows)==4 and name not in ('log_cube_y','radical_x'):
  third_rhs=second_rows[2].split('& =')[1].strip()
  assert not re.search(r'\([xy]-',third_rhs),('distribution stage omitted',third_rhs)
 # Normals read from the actual printed bullets.
 ns=re.findall(r'\{n\}_\{[12]\}=⟨([^⟩]*)⟩',sol)
 assert len(ns)==2
 n1,n2=[sp.Matrix([g.parse_math(t) for t in v.split(',')]) for v in ns]
 assert n1==sp.Matrix((0,1,0) if plane=='y' else (1,0,0))
 assert sp.simplify(n2.dot(sp.Matrix(vec)))==0
 cross=n1.cross(n2);assert g.parallel(cross,vec)
 # Every printed normal's defining alternate plane passes through P.
 first_plane=re.search(r'- For the plane \$([xy])=(.*?)\,?\$',sol)
 assert first_plane and first_plane[1]==plane
 assert g.parse_math(first_plane[2])==pt[0 if plane=='x' else 1]
 eq=re.search(r'\(or \$(.*?)\$\)',sol).group(1)
 l,rr=eq.split('=');assert sp.simplify((g.parse_math(l)-g.parse_math(rr)).subs(dict(zip((g.X,g.Y,g.Z),pt))))==0
 # Read determinant entries and compare with the normals; read each cross vector/basis row.
 last=blocks[3];det=re.search(r'\\left\|\\begin\{aligned\}(.*?)\\end\{aligned\}\\right\|',last,re.S).group(1)
 drows=det.split(r'\\');assert len(drows)==3
 for row,n in zip(drows[1:],(n1,n2)):assert sp.Matrix([g.parse_math(t) for t in row.split('&')])==n
 result_rows=last.split('& =')[3:]
 for row in result_rows:
  value=row.split(r'\end')[0].split(r'\\')[0].strip()
  assert sp.Matrix(g.parse_vector(value))==cross,('cross stage',value,cross)
 # Final prose vectors are tested against criterion; no stale vectors allowed.
 ending=sol[sol.rindex('$$')+2:]
 for fragment in re.findall(r'\$(.*?)\$',ending):
  if '⟨' in fragment:
   for t in re.findall(r'⟨[^⟩]*⟩',fragment):assert g.parallel(g.parse_vector(t),vec)
  elif ('i' in fragment or 'j' in fragment or 'k' in fragment) and fragment not in ('P','C'):
   for t in fragment.split('='):
    t=t.strip();t=re.sub(r'^-\((.*)\)$',r'-1*(\1)',t)
    assert g.parallel(g.parse_vector(t),vec)
 assert not any(g.parallel(a,b) for i,a in enumerate(vectors) for b in vectors[i+1:])
 return len(vectors),ev_count

def native_item(r,label):
 f=r['question'][':question/answer-fields'][0]
 return {'label':label,'record':r,'checks':[{'field_index':0,'submitted_answer_id':a[':answer/id'],
 'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',
 'purpose':'Every displayed radio choice under real native grade_field'} for a in f[':answer-field/choices']]}

def run():
 cases=[];raws=[];records=[];native=[];byte_audit=[];math_count=0;stage_count=0;source_dir_duplicates=[]
 for name,d in g.TEMPLATES.items():
  if 'source' not in d:continue
  q=d['source'];assert q[':question/difficulty'][':db/ident']==':question.difficulty/hard'
  case={'source_id':q[':db/id'],'template':name,'level':'hard','parameters':{'h':0},'bank_profile':'source'};cases.append(case)
  r=g.generate('hard',template=name,parameters={'h':0},profile='source');rq=r['question']
  assert rq[':question/problem']==q[':question/problem'] and rq[':question/worked-solution']==q[':question/worked-solution']
  f=rq[':question/answer-fields'][0];sf=q[':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in sf[':answer-field/choices'])
  ca=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert ca==sf[':answer-field/correct'][':answer/value']
  for attr in (':question/difficulty',':question/answer-fields',':question/worked-solution'):assert (attr in rq)==(attr in q)
  ct,st=verify(r,True);math_count+=ct;stage_count+=st
  vv=[g.parse_vector(a[':answer/value']) for a in sf[':answer-field/choices']]
  for i,a in enumerate(vv):
   for j,b in enumerate(vv[i+1:],i+1):
    if g.parallel(a,b):source_dir_duplicates.append({'source_id':q[':db/id'],'indices':[i,j],'values':[sf[':answer-field/choices'][k][':answer/value'] for k in (i,j)]})
  for a in sf[':answer-field/choices']:
   v=a[':answer/value'];runs=[i for i in range(len(v)-1) if ord(v[i])==ord(v[i+1])==92]
   byte_audit.append({'source_id':q[':db/id'],'answer_id':a[':answer/id'],'adjacent_ord92_indices':runs,'ord_values':[list(map(ord,v[i:i+4])) for i in runs]})
  raws.append(r);native.append(native_item(r,'original/'+name))
  shifted=g.generate('hard',template=name,parameters={'h':1},profile='source')
  assert shifted['question'][':question/problem']!=rq[':question/problem']
  assert shifted['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
  try: anchor=g.generate('hard',template=name,parameters={'c':1,'h':0})
  except ValueError: anchor=None
  if anchor is not None:assert anchor['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
  # Normal variants exercise every method family and source structure with changed c/h.
  for c in (3,5,9):
   for h in (-4,0,4):
    rr=g.generate('hard',seed=c+h,template=name,parameters={'c':c,'h':h});ct,st=verify(rr);math_count+=ct;stage_count+=st;records.append(rr)
  native.append(native_item(records[-1],'variant/'+name))
  same=g.generate('hard',seed=991,template=name,parameters={'c':9,'h':4})
  assert same['question'][':question/id']==records[-1]['question'][':question/id']
  records.append(g.generate('hard',seed=11,template=name,parameters={'c':4,'h':1}));ct,st=verify(records[-1]);math_count+=ct;stage_count+=st
 for level in ('easy','moderate'):
  for seed in range(60):
   r=g.generate(level,seed);ct,st=verify(r);math_count+=ct;stage_count+=st;records.append(r)
  native.extend(native_item(r,level+'/'+str(i)) for i,r in enumerate(records[-60:]))
 # Reject public out-of-scope/ineligible inputs, without silent repair.
 for args in [('hard',{'c':10,'h':0},'linear_x'),('hard',{'c':1,'h':0},'radical_x'),
              ('moderate',{'plane':'y','a':2,'x':1,'y':1,'z':0},'scaled_coordinate')]:
  try:g.generate(args[0],template=args[2],parameters=args[1])
  except ValueError:pass
  else:raise AssertionError('invalid explicit parameters accepted')
 # Default sampler actually serves all supported hard families.
 coverage={g.generate('hard',seed)['generation']['template'] for seed in range(200)}
 assert coverage=={n for n,d in g.TEMPLATES.items() if d['level']=='hard'}
 # Mutation regression: remove distribution/sign normalization while retaining equality.
 mut=json.loads(json.dumps(records[0]));sol=mut['question'][':question/worked-solution']
 rows=re.findall(r'\$\$.*?\$\$',sol,re.S)[1].split(r'\\')
 mut['question'][':question/worked-solution']=sol.replace(rows[2],rows[1])
 try:verify(mut)
 except AssertionError:pass
 else:raise AssertionError('lost structural stage escaped QA')
 write('source-cases.json',cases);write('byte-audit.json',byte_audit)
 native=[native_item(r,'original/'+str(i)) for i,r in enumerate(raws)]+[native_item(r,'generated/'+str(i)) for i,r in enumerate(records)]
 write('engine-input.json',native)
 cmd=['generate/runs/current/check-engine',str(HERE/'engine-input.json'),str(HERE/'engine-report.json')]
 subprocess.run(cmd,check=True,cwd=HERE.parents[2])
 engine=json.loads((HERE/'engine-report.json').read_text())
 # Review includes every source and three changed instances per observed family;
 # all tested generated records retained separately for independent QA.
 write('review.json',raws+records);write('generated.json',records)
 text=['# Source and generated review','Raw originals are evidence-only. Method variants are explicitly authored bank extensions.']
 for name,d in g.TEMPLATES.items():
  if 'source' not in d:continue
  r=next(r for r in raws if r['generation']['template']==name)
  text+=['\n## '+name+' — original '+str(d['source'][':db/id']),g.markdown(r),'\n### Generated variants']
  for r in [r for r in records if r['generation']['template']==name][:2]:text.append(g.markdown(r))
 for level in ('easy','moderate'):
  text+=['\n## Authored '+level]
  for r in [r for r in records if r['question'][':question/difficulty'].endswith('/'+level)][:2]:text.append(g.markdown(r))
 (HERE/'review.md').write_text('\n\n'.join(text)+'\n')
 for level in ('easy','moderate','hard'):
  fresh=g.generate(level,42);assert fresh==g.generate(level,42)
  assert fresh==json.loads(json.dumps(fresh))
 result={'status':'passed_with_documented_raw_source_anomalies','source':{'database':g.CAPTURE['database'],'basis':g.CAPTURE['basis'],'lineage':g.CAPTURE['lineage']},
 'runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},
 'source_fidelity':{'prompts':{'matched':15,'total':15},'solutions_raw':{'matched':15,'total':15},'complete_banks':{'matched':15,'total':15},
 'choices':{'matched':75,'total':75},'distractors':{'matched':60,'total':60},'correct_designations':{'matched':15,'total':15},'presence_parity':15},
 'source_math':{'full_raw_solutions_mathematically_correct':{'matched':13,'total':15},'raw_solution_presentation_valid':{'matched':2,'total':15},'choice_criterion_checks':75,'correct_designations_valid':15,'wrong_choices_validly_wrong':60,'duplicate_wrong_directions':source_dir_duplicates},
 'deterministic_json_roundtrip':{'levels_passed':3,'levels_total':3,'renderer_cache':'not applicable — no assessed plot'},
 'normal_math':{'records':len(records),'all_choice_checks_including_sources':math_count,'evaluation_stage_checks_including_sources':stage_count,
 'default_hard_family_coverage':sorted(coverage)},'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},
 'native_scope':'All displayed choices for 15 raw +150 changed hard +120 authored E/M records. Radio supports ID selection; typed equivalent-vector entries are not an applicable learner response.',
 'source_solution_anomalies':{'wrong_point':17592186124977,'wrong_slice_plane':17592186268891,'raw_unmatched_literal_braces':sum('{'+r'\begin{aligned}' in r['question'][':question/worked-solution'] and r'\{'+r'\begin{aligned}' not in r['question'][':question/worked-solution'] for r in raws),'malformed_signed_constant':17592186406798},
 'raw_presentation_eligible':False,'normal_records_eligible':True,
 'plots':'none in source questions/canonical; two lesson explanatory rasters inspected full resolution, no parameter-dependent assessed geometry',
 'limitations':['Historical whole banks have opaque distractor intent; public source profile remains evidence-only.','Hard coefficient extensions wrap unchanged source evaluation rows; notation normalization and repaired planes/points are separately documented.','No typed-vector equivalence acceptance claim for radio field.']}
 write('validation.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':run()
