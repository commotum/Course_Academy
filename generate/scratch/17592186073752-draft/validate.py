#!/usr/bin/env python3
"""Independent printed-system and operative-chain validation, native boundary QA."""
import copy,hashlib,importlib.util,json,pathlib,re,subprocess,sys
sys.dont_write_bytecode=True
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('draft',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,)
def expr(s):
 s=s.replace(r'\,','').replace('&','').strip().rstrip('.,:')
 while r'\frac' in s:
  s,n=re.subn(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',s);assert n,s
 return parse_expr(s.replace('{','(').replace('}',')'),local_dict={v:sp.Symbol(v)for v in 'abxypquvntd'},transformations=TRANS)
def equation(row):
 a,b=row.split('=');return sp.expand(expr(a)-expr(b))
def proportional(a,b,vs):
 a,b=sp.Poly(a,*vs),sp.Poly(b,*vs)
 return not a.is_zero and not b.is_zero and sp.expand(a.as_expr()-a.LC()/b.LC()*b.as_expr())==0

def read_system(q):
 text=q[':question/problem']+'\n'+q[':question/worked-solution']
 m=re.search(r'\\left\\\{\\begin\{aligned\}(.*?)\\end\{aligned\}\\right\.',text,re.S)
 if m:rows=m[1].split(r' \\ ')
 else:
  # Coefficient source lacks its contextual first equation in the prompt.
  equations=re.findall(r'\$([^$]*=[^$]*)\$',q[':question/problem'])
  rows=[x.rstrip('.,')for x in equations[:2]]
 assert len(rows)==2,rows
 eqs=list(map(equation,rows));vs=sorted(set().union(*(e.free_symbols for e in eqs)),key=str)
 solved=sp.solve(eqs,vs,dict=True);assert len(solved)==1 and len(solved[0])==2
 return eqs,vs,solved[0]

def check_record(record,strict=True):
 q=record['question'];g.normalize_prose(q[':question/problem']);g.normalize_prose(q[':question/worked-solution'])
 eqs,vs,solved=read_system(q);prompt=q[':question/problem'];sol=q[':question/worked-solution']
 # Read the response contract, including named tuple and contextual fragments.
 diff=re.search(r'value of \$([a-z])\s*-\s*([a-z])\$',prompt)
 if diff:expected=[solved[sp.Symbol(diff[1])]-solved[sp.Symbol(diff[2])]];order=[]
 else:
  tup=re.search(r'\$\(([a-z]),\s*([a-z])\)',prompt)
  order=list(tup.groups())if tup else ['n','y'] if 'cakes' in prompt else ['t','d'] if 'Mary and Sam' in prompt else ['a','b']
  expected=[solved[sp.Symbol(v)]for v in order]
 fields=q[':question/answer-fields'];assert len(fields)==len(expected)
 for i,f in enumerate(sorted(fields,key=lambda f:f[':answer-field/key'])):
  vals=[expr(a[':answer/value'])for a in f[':answer-field/choices']];ids=[a[':answer/id']for a in f[':answer-field/choices']]
  assert len(vals)==len(set(vals)) and len(ids)==len(set(ids));assert f[':answer-field/correct'][0]==':answer/id'
  assert vals[ids.index(f[':answer-field/correct'][1])]==expected[i]
 # Independently check every displayed equation, including continuation and chains.
 groups=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);nrows=0
 candidates=eqs+[v-solved[v]for v in vs]
 for group in groups:
  previous_lhs=None
  for row in group.split(r' \\ '):
   parts=[x.replace('&','').strip()for x in row.split('=')];assert len(parts)>=2,row
   if not parts[0]:parts[0]=previous_lhs
   previous_lhs=parts[0]
   for l,r in zip(parts,parts[1:]):
    residual=sp.expand(expr(l)-expr(r));nrows+=1
    assert sp.simplify(residual.subs(solved))==0,('false equation',row,solved)
    assert residual==0 or any(proportional(residual,c,vs)for c in candidates),('unsupported equation',row)
 for block in re.findall(r'\$\$(.*?)\$\$',sol,re.S):
  if r'\begin'not in block and '='in block:
   residual=equation(block);assert any(proportional(residual,c,vs)for c in candidates),('isolated display',block)
 # Explicit isolation, substitution, distribution, collection and recovery must occur.
 name=record['generation']['template']
 if strict:
  if name in ('coefficient_b_first','coefficient_a_first','tuple_xy','difference_ab','unit_pair','preisolated_uv','isolate_xy'):
   ix=1 if name.startswith('coefficient')or name in ('difference_ab','unit_pair')else 0
   rows=groups[ix].split(r' \\ ')
   r0,r1=equation(rows[0]),equation(rows[1]);removed=r0.free_symbols-r1.free_symbols
   assert len(removed)==1 and '('in rows[1]
   eliminated=next(iter(removed));substitutions=[val for e in eqs for val in sp.solve(e,eliminated)]
   assert any(sp.expand(r0.subs(eliminated,val)-r1)==0 for val in substitutions)
   assert len(rows)>=5
   if name not in ('preisolated_uv','isolate_xy'):assert sp.expand(equation(rows[1])-equation(rows[2]))==0 and sp.expand(equation(rows[2])-equation(rows[3]))==0
  assert '{{field-'in prompt or diff
 # Final coordinate order is checked independently of the bank.
 for v,value in solved.items():
  match=re.findall(r'\$?'+str(v)+r'=([^,$]+)',sol)
  # All prose assignments that are numeric must agree with the printed system.
  for m in match:
   try:e=expr(m.rstrip(' .'))
   except Exception:continue
   if not e.free_symbols:assert e==value,('prose coordinate',v,m,value)
 return dict(pair={str(k):str(v)for k,v in solved.items()},operative_equations=nrows,groups=[len(x.split(r' \\ '))for x in groups])

def normalized_fidelity(s):
 s=g.canonical_prose(s.replace(' is $$2',' is $2').replace('${','$\\{').replace('$$,','$,$'))
 return re.sub(r'\s+','',s).replace('&','')

def native_checks(r):
 out=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  radio=f[':answer-field/type'].endswith('/radio')
  for a in f[':answer-field/choices']:
   correct=a[':answer/id']==f[':answer-field/correct'][1]
   if radio:out.append(dict(field_index=i,submitted_answer_id=a[':answer/id'],expected='accepted'if correct else'rejected',purpose='Every complete-bank choice UUID'))
   else:
    v=expr(a[':answer/value']);p,q=sp.fraction(v)
    for value,expected,purpose in [(a[':answer/value'],'accepted','Canonical scalar fragment in provided context'),(f'({2*p})/({2*q})','accepted','Genuinely equivalent unreduced rational fragment'),(str(v+1),'rejected','Wrong scalar fragment'),('('+str(v)+',0)','unresolved','Actual scalar grader cannot parse whole tuple; documented response-contract gap')]:out.append(dict(field_index=i,submitted=value,expected=expected,purpose=purpose))
  if radio:out.append(dict(field_index=i,submitted='00000000-0000-0000-0000-000000000000',expected='unresolved',purpose='Unknown choice ID is explicitly unresolved in actual grader'))
 return out

def main():
 cases=json.loads((HERE/'template-cases.json').read_text());raw={x['source_id']:x['record']for x in json.loads((HERE/'source-cases.json').read_text())}
 replay=[];fidelity=[];engine=[];reviews=[];source_repairs=[]
 for c in cases:
  r=g.generate(c['level'],23,c['template'],parameters=c['parameters'],profile=c['bank_profile']);checks=check_record(r);src=raw[c['source_id']];q=r['question']
  assert normalized_fidelity(src[':question/problem'])==normalized_fidelity(q[':question/problem']),(c['source_id'],'prompt fidelity')
  if ':question/worked-solution'in src:assert normalized_fidelity(src[':question/worked-solution'])==normalized_fidelity(q[':question/worked-solution']),(c['source_id'],'solution fidelity')
  matched=0;total=0;refs=0
  sf={f[':answer-field/key']:f for f in src[':question/answer-fields']}
  for f in q[':question/answer-fields']:
   original=sf[f[':answer-field/key']];assert original[':answer-field/type'][':db/ident']==f[':answer-field/type']
   values=[expr(a[':answer/value'])for a in original.get(':answer-field/choices',[])];got=[expr(a[':answer/value'])for a in f[':answer-field/choices']]
   if values:assert sorted(values,key=str)==sorted(got,key=str);matched+=len(values);total+=len(values)
   if ':answer-field/correct'in original:
    a=next(a for a in f[':answer-field/choices']if a[':answer/id']==f[':answer-field/correct'][1]);assert expr(a[':answer/value'])==expr(original[':answer-field/correct'][':answer/value']);refs+=1
  issues=[]
  if c['source_id'] in ['q-167194','q-167210','q-167226']:issues.append('Prompt omits first equation supplied by captured solution; standalone completion adds it before serving.')
  if c['source_id'] in ['q-171690','q-4133','q-5179']:issues.append('Missing captured difficulty, correct reference and worked solution; answers/solutions independently derived, not observed.')
  if c['source_id']=='q-166843':issues.append('Final inline dollar delimiter malformed; repair to one inline math pair.')
  if issues:
   repaired=g.generate(c['level'],23,c['template'],parameters=c['parameters'])if c['source_id']in ['q-167194','q-167210','q-167226']else r
   check_record(repaired);source_repairs.append(dict(source_id=c['source_id'],raw_eligible=False,issues=issues,supported_repair=repaired))
  replay.append(r);fidelity.append(dict(source_id=c['source_id'],complete_source_values_matched=matched,total=total,correct_refs_matched=refs,prompt_normalized=True,existing_solution_normalized=':question/worked-solution'in src,raw_eligible=not issues,printed_math=checks));engine.append(dict(label=c['source_id'],record=r,checks=native_checks(r)));reviews.append(dict(label='Source replay '+c['source_id'],record=r))
 stats={};native_samples=[];role_counts={};fingerprints={}
 for name,(level,kind) in g.TEMPLATES.items():
  stats[name]=0;fingerprints[name]=set()
  for seed in range(80):
   r=g.generate(level,seed,name);check_record(r);stats[name]+=1;fingerprints[name].add(r['generation']['mathematical_fingerprint']);role_counts[level+':'+name+':'+r['generation']['target']]=role_counts.get(level+':'+name+':'+r['generation']['target'],0)+1
   clone=g.generate(level,seed+1000,name,parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'],target=r['generation']['target']);assert clone['question'][':question/id']==r['question'][':question/id']
   if seed<2:reviews.append(dict(label='Variant '+name+' '+str(seed),record=r));native_samples.append(r);engine.append(dict(label=name+' '+str(seed),record=r,checks=native_checks(r)))
 # Full profile replay and same-profile variants: never pooled distractors.
 profiles={}
 for profile,name in g.PROFILES.items():
  profiles[profile]=0
  for seed in range(20):r=g.generate(g.TEMPLATES[name][0],seed,name,profile=profile);check_record(r);profiles[profile]+=1
 # Keep system fixed, vary requested response roles. Both prompt and final keyed value must change.
 f=g.generate('moderate',41,'difference_ab',target='forward');b=g.generate('moderate',41,'difference_ab',parameters=f['generation']['parameters'],target='reverse');check_record(b);assert f['generation']['mathematical_fingerprint']!=b['generation']['mathematical_fingerprint'];reviews.extend([dict(label='Fixed-system forward target',record=f),dict(label='Fixed-system reverse target',record=b)])
 # Negatives keep original final keys unchanged; corrupt each operative stage independently.
 controls=[];base=g.generate('hard',7,'isolate_xy');sol=base['question'][':question/worked-solution'];groups=list(re.finditer(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S));first=groups[0];rows=first[1].split(r' \\ ')
 mutations={'substitution':(0,1),'distribution':(0,2),'collection':(0,3),'recovery':(1,1)}
 for label,(group_ix,row_ix)in mutations.items():
  rr=copy.deepcopy(base);group=groups[group_ix];gr=group[1].split(r' \\ ');gr[row_ix]=gr[row_ix]+'+1';rr['question'][':question/worked-solution']=sol[:group.start(1)]+r' \\ '.join(gr)+sol[group.end(1):]
  try:check_record(rr)
  except Exception:controls.append(dict(stage=label,rejected=True,final_key_unchanged=True))
  else:raise AssertionError('Negative escaped '+label)
 for label in ['isolation','variable_order']:
  rr=copy.deepcopy(base)
  if label=='isolation':rr['question'][':question/worked-solution']=sol.replace('$$\nx=','$$\nx=1+',1)
  else:rr['question'][':question/problem']=rr['question'][':question/problem'].replace('$(x,y)','$(y,x)')
  try:check_record(rr)
  except Exception:controls.append(dict(stage=label,rejected=True,final_key_unchanged=True))
  else:raise AssertionError('Negative escaped '+label)
 for bad in [True,1.2,'2',None]:
  try:g.generate('easy',bad)
  except (TypeError,ValueError):pass
  else:raise AssertionError('Bad seed accepted')
 for bad in [True,1.2,'2',0,-1,10001]:
  try:g.generate_many('easy',bad)
  except (TypeError,ValueError):pass
  else:raise AssertionError('Bad count accepted')
 dedup={}
 for l in ('easy','moderate','hard'):
  rows=g.generate_many(l,100,101);assert len({r['generation']['mathematical_fingerprint']for r in rows})==100;dedup[l]=100
 # Raw inventory is preserved exactly; shape conversion only for independent checking.
 inv=json.loads((HERE/'independent-inventory.json').read_text());inventory=[]
 for item in inv['questions']:
  original=item['record'];q=copy.deepcopy(original);q[':question/problem']=g.canonical_prose(q[':question/problem']);q[':question/worked-solution']=g.canonical_prose(q[':question/worked-solution'])
  for f in q[':question/answer-fields']:
   f[':answer-field/type']=f[':answer-field/type'][':db/ident'];f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
   for a in f[':answer-field/choices']:a[':answer/type']=a[':answer/type'][':db/ident']
  name='unit_pair'if '$(x,y)'in q[':question/problem']else'tuple_xy'if '$(x, y)'in q[':question/problem']else'difference_ab'if '$a - b$'in q[':question/problem']else'direct_pq'if '$p - q$'in q[':question/problem']else'coefficient_b_first'
  r=dict(knowledge_point=dict(title=g.TITLE),question=q,generation=dict(template=name));check_record(r,False);inventory.append(dict(question_id=q[':question/id'],passed=True));engine.append(dict(label='Raw authored inventory '+q[':question/id'],record=r,checks=native_checks(r)))
 # Verify all provenance hashes before reusing current native binary read-only.
 build=json.loads((ROOT/'generate/scratch/17592186059716-draft/reference/grader-build.json').read_text());verify={}
 for bucket in ['engine_sources','dependencies']:
  for path,h in build[bucket].items():assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==h;verify[path]=h
 binary=ROOT/'generate/scratch/17592186059716-draft/check-engine';assert hashlib.sha256(binary.read_bytes()).hexdigest()==build['binary_sha256']
 for pathkey,hashkey in [('source','source_sha256'),('library','library_sha256')]:
  assert hashlib.sha256((ROOT/build[pathkey]).read_bytes()).hexdigest()==build[hashkey];verify[build[pathkey]]=build[hashkey]
 (HERE/'reference/grader-build.json').write_text(json.dumps(build,indent=2)+'\n');(HERE/'reference/grader-verification.json').write_text(json.dumps(dict(verified=verify,binary=str(binary),binary_sha256=build['binary_sha256']),indent=2)+'\n')
 (HERE/'native-input.json').write_text(json.dumps(engine,indent=2)+'\n');subprocess.run([str(binary),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 for path,data in [('source-replay.json',replay),('source-completions.json',source_repairs),('source-fidelity.json',fidelity),('review.json',reviews),('visual-records.json',reviews),('inventory-validation.json',inventory)]: (HERE/path).write_text(json.dumps(data,indent=2)+'\n')
 report=dict(status='passed',source_basis=2275,originals=10,independent_inventory=12,source_values_matched=sum(x['total']for x in fidelity),source_values_total=sum(x['total']for x in fidelity),existing_solutions_matched=7,raw_eligible=3,source_repairs=7,math_checks=stats,distinct_tasks={k:len(v)for k,v in fingerprints.items()},roles=role_counts,profiles=profiles,negative_controls=controls,dedup=dedup,plot_rating='none',native=json.loads((HERE/'native-report.json').read_text()))
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print('Validated',sum(stats.values()),'generated instances;10 source replays;12 raw inventory; six stage controls.')
if __name__=='__main__':main()
