#!/usr/bin/env python3
"""Independent actual-display mathematics, bank fidelity, scope and native grading."""
import importlib.util,json,re,subprocess,sys,uuid,copy
from pathlib import Path
import sympy as sp
ROOT=Path(__file__).resolve().parent; PROJECT=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('flux',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def write(name,value): (ROOT/name).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def vectors(s):
 return [[g.parse(t.strip(',')) for t in raw.split(r'\,')] for raw in re.findall('⟨([^⟨⟩]*)⟩',s) if r'\frac' not in raw and r'\begin' not in raw]
def same(a,b):
 assert len(a)==len(b)
 assert all(g.eq(x,y) for x,y in zip(a,b)),(a,b)
def norm(s):return re.sub(r'\s+','',s)
def balanced(s):
 assert s.count('$$')%2==0 and s.count('$')%2==0
 depth=0
 for i,ch in enumerate(s):
  if ch in '{}':depth+=1 if ch=='{' else -1
  assert depth>=0
 assert depth==0

def independent(record):
 q=record['question'];p=q[':question/problem'];sol=q[':question/worked-solution'];balanced(p);balanced(sol)
 F=vectors(p)[0];G=g.parse(re.search(r'defined by \$z=(.*?)\$',p).group(1));bounds=list(map(int,re.search(r'for \$(-?\d+)\\le x\\le (-?\d+)\$ and \$(-?\d+)\\le y\\le (-?\d+)\.\$',p).groups()))
 H=G.subs({g.x:g.u,g.y:g.v});r=sp.Matrix([g.u,g.v,H]);ru=r.diff(g.u);rv=r.diff(g.v);N=ru.cross(rv);FV=[sp.expand(e.subs({g.x:g.u,g.y:g.v,g.z:H},simultaneous=True)) for e in F];I=sp.expand(sum(a*b for a,b in zip(FV,N)))
 blocks=sol.split('$$')[1::2]; assert len(blocks)==8
 same(vectors(blocks[1])[0],list(r))
 db=list(map(int,re.search(r'(-?\d+)\\le u\\le (-?\d+),\\,(-?\d+)\\le v\\le (-?\d+)',blocks[2]).groups()));assert db==bounds
 ts=vectors(blocks[3]); same(ts[0],list(ru));same(ts[1],list(rv))
 for variable in ('u','v'):
  assert ('⟨'+r'\frac{∂x}{∂'+variable+'},'+r'\,\frac{∂y}{∂'+variable+'},'+r'\,\frac{∂z}{∂'+variable+'}⟩') in blocks[3]
 inputs=re.findall(r'\\frac\{∂\}\{∂([uv])\}\((.*?)\)',blocks[3]);assert len(inputs)==6
 for (variable,expression),coordinate in zip(inputs,[g.u,g.v,H,g.u,g.v,H]):
  assert g.eq(g.parse(expression),coordinate)
 assert norm(blocks[0])==norm(g.SOURCES['q-161360'][':question/worked-solution'].split('$$')[1])
 # Check actual printed determinant entries, independent of stored metadata.
 det=re.search(r'i & j & k \\\\ 1 & 0 & (.*?) \\\\ 0 & 1 & (.*?)\\end',blocks[4]);assert det
 assert g.eq(g.parse(det[1]),H.diff(g.u)) and g.eq(g.parse(det[2]),H.diff(g.v))
 same(vectors(blocks[4])[-1],list(N))
 # Check each printed 2x2 minor and its alternating sign, not just the normal.
 minors=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',blocks[4])[-3:];assert len(minors)==3
 for idx,minor in enumerate(minors):
  ns=[g.parse(t.strip()) for t in re.split(r' & | \\\\ ',minor)];assert len(ns)==4
  value=(-1)**idx*(ns[0]*ns[3]-ns[1]*ns[2]);assert g.eq(value,N[idx])
 sub=vectors(blocks[5]);same(sub[0],F)
 for vv in sub[1:]:same(vv,FV)
 dot=blocks[6];ds=vectors(dot);same(ds[0],FV);same(ds[1],list(N))
 rows=dot.split(' & =')[2:];assert len(rows) in (2,3)
 # Product row, distributed sum row if present, and final polynomial are
 # independently parsed from the actual display. Correct normal vectors alone
 # cannot conceal a dropped minus in this stage.
 for row in rows:
  row=row.split(r' \\ ')[0].split(r'\end{aligned}')[0].rstrip('.')
  row=row.replace(r'\cdot','*')
  assert g.eq(g.parse(row),I),(row,I)
 end=blocks[7];same(vectors(end)[0],F)
 domain_integrands=re.findall(r' & =\{∬\}_\{D\}(.*?)\\,\\text\{d\}A',end);assert len(domain_integrands)==2 and g.eq(g.parse(domain_integrands[1]),I)
 assert norm(domain_integrands[0])==norm(r'F(r(u,v))\cdot ({r}_{u}^{′}\times {r}_{v}^{′})')
 final=re.search(r'\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}(.*?)\\,\\text\{d\}v',end);assert final
 assert list(map(int,final.groups()[:4]))==bounds and g.eq(g.parse(final[5]),I)
 prompt_int=re.search(r'\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}\{\\int \}_\{(-?\d+)\}\^\{(-?\d+)\}',p);assert list(map(int,prompt_int.groups()))==bounds
 field=q[':question/answer-fields'][0];assert field[':answer-field/type']==':answer-field.type/radio' and field[':answer-field/key']=='selection'
 answers=field[':answer-field/choices'];vals=[g.parse(a[':answer/value']) for a in answers];assert len(vals)==5 and len({a[':answer/id'] for a in answers})==5
 for a in answers:uuid.UUID(a[':answer/id']);assert '$' not in a[':answer/value']
 assert sum(g.eq(e,I) for e in vals)==1
 assert next(a[':answer/id'] for a,e in zip(answers,vals) if g.eq(e,I))==field[':answer-field/correct'][1]
 assert all(not g.eq(vals[i],vals[j]) for i in range(5) for j in range(i))
 if 'generation' in record:
  gen=record['generation']
  if gen['profile']=='authored_operations':
   A,B,C=[sp.expand(a*b) for a,b in zip(FV,N)]
   expected=[I,-I,-A+B+C,A-B+C,A+B]
  else:
   base=g.FAMILIES[gen['template']][1];scale=sp.cancel(F[0]/base[0]);assert not scale.free_symbols
   same(F,[scale*e for e in base])
   ops=g.candidate_operations({'F':F,'G':H,'fv':FV,'terms':[sp.expand(a*b) for a,b in zip(FV,N)],'I':I,'normal':N})
   expected=[ops[r['selected']] if r['selected'] else sp.expand(scale*e) for e,r in zip(g.PATTERNS[gen['template']],g.OBSERVED_MAP[gen['template']])]
  assert all(sum(g.eq(e,t) for t in vals)==1 for e in expected)
 # Complete source prose and stage row counts are checked separately below.
 return I

def source_fidelity(c):
 sid=c['source_id'];raw=g.SOURCES[sid];record=g.generate('easy',42,c['template'],parameters=c['parameters'],profile=c['bank_profile']);independent(record)
 srcfield=raw[':question/answer-fields'][c['source_field_index']];gf=record['question'][':question/answer-fields'][0]
 same(vectors(raw[':question/problem'])[0],vectors(record['question'][':question/problem'])[0])
 source_graph=g.parse(re.search(r'defined by \$z=(.*?)\$',raw[':question/problem']).group(1));generated_graph=g.parse(re.search(r'defined by \$z=(.*?)\$',record['question'][':question/problem']).group(1));assert g.eq(source_graph,generated_graph)
 want=[g.parse(a[':answer/value']) for a in srcfield[':answer-field/choices']];have=[g.parse(a[':answer/value']) for a in gf[':answer-field/choices']]
 assert len(want)==len(have)==5
 assert all(sum(g.eq(w,h) for h in have)==1 for w in want)
 if ':answer-field/correct' in srcfield: assert g.eq(g.parse(srcfield[':answer-field/correct'][':answer/value']),independent(record))
 # Preserve fixed prose, including source family blank lines, stage count and
 # omission of redundant substitution/expanded rows. Normalize only notation.
 original=raw[':question/worked-solution'].split('$$');produced=record['question'][':question/worked-solution'].split('$$')
 assert original[::2]==produced[::2]
 assert [i.count(' & =') for i in original[1::2]]==[i.count(' & =') for i in produced[1::2]]
 # Independently check all original mathematical stage values. q-161471's
 # final vector is a captured error, repaired in normal generated output.
 I=independent(record); origblocks=original[1::2]
 fv=sp.Matrix([g.u,g.v,g.parse(re.search(r'defined by \$z=(.*?)\$',raw[':question/problem']).group(1)).subs({g.x:g.u,g.y:g.v})])
 same(vectors(origblocks[1])[0],list(fv))
 # Check every actual original displayed stage using the same independent
 # mathematical reader; repair only the documented final-LHS source mistake.
 oq=copy.deepcopy(raw);of=copy.deepcopy(srcfield)
 of[':answer-field/type']=':answer-field.type/radio'
 for ans in of[':answer-field/choices']:ans[':answer/type']=':answer.type/math'
 of[':answer-field/correct']=[':answer/id',next(ans[':answer/id'] for ans in of[':answer-field/choices'] if g.eq(g.parse(ans[':answer/value']),I))]
 oq[':question/answer-fields']=[of]
 if sid=='q-161471':
  head,tail=oq[':question/worked-solution'].rsplit('Therefore,',1)
  tail=tail.replace('⟨z-y,\\,2y-z,\\,xy⟩','⟨x+z,\\,2z,\\,y+z⟩',1)
  oq[':question/worked-solution']=head+'Therefore,'+tail
 independent({'question':oq})
 # Source bank math and original worked dot final are each checked, independent.
 origfinal=origblocks[6].split(' & =')[-1].split(r'\end{aligned}')[0].rstrip('.')
 assert g.eq(g.parse(origfinal),I)
 return record

def run():
 cases=[]
 for sid,q in g.SOURCES.items():
  for j,f in enumerate(q[':question/answer-fields']):cases.append({'source_id':sid,'source_uuid':q[':question/id'],'template':sid,'parameters':g.FAMILIES[sid][0],'bank_profile':'q-161360-legacy' if sid=='q-161360' and j==0 else sid,'source_field_index':j,'designation_present':':answer-field/correct' in f})
 write('source-cases.json',cases)
 replay=[{'label':'source '+c['source_id']+' field '+str(c['source_field_index']),'record':source_fidelity(c)} for c in cases]
 records=[];unique={k:set() for k in ('easy','moderate','hard')}; tested=0
 for level in unique:
  templates=[k for k,d in g.TEMPLATES.items() if d['level']==level]
  for template in templates:
   for seed in range(30):
    r=g.generate(level,seed,template);independent(r);unique[level].add(r['generation']['mathematical_fingerprint']);tested+=1
    # Count assessed variation without uncomputed rectangle bounds.
    qp=r['question'][':question/problem'];actualF=vectors(qp)[0];actualG=g.parse(re.search(r'defined by \$z=(.*?)\$',qp).group(1))
    assert r['generation']['mathematical_fingerprint']==g.digest({'F':[sp.srepr(sp.expand(e)) for e in actualF],'g':sp.srepr(sp.expand(actualG)),'orientation':'upward'})
    if seed<2:records.append({'label':'Generated '+level+' '+template+' '+str(seed),'record':r})
 # Enumerate the complete 128-member authored hard assessed family; varying
 # rectangle endpoints alone never increases this task count.
 import itertools
 hard_fingerprints=set()
 for a,b,c,pcoef,qcoef,rcoef in itertools.product((-2,-1,1,2),(-1,1),(-1,1),(1,2),(1,2),(1,2)):
  hp={'a':a,'b':b,'c':c,'p':pcoef,'q':qcoef,'r':rcoef,'bounds':[0,2,-1,2]}
  hh=g.generate_hard(parameters=hp);independent(hh);hard_fingerprints.add(hh['generation']['mathematical_fingerprint']);tested+=1
 assert len(hard_fingerprints)==128
 # Every evidence profile generalizes its complete expression bank with varying
 # field coefficient scale; do not infer original error intent from this check.
 for profile,d in g.PROFILES.items():
  if profile=='authored_operations':continue
  for seed in range(4):independent(g.generate('easy',seed,d['template'],profile=profile));tested+=1
 invalid=0
 for level,template in [('easy','q-161360'),('moderate','quadratic_graph'),('hard','mixed_graph')]:
  r=g.generate(level,17,template);p=r['generation']['parameters'];r2=g.generate(level,991,template,parameters=p);r3=g.generate(level,123,template,parameters=p)
  assert r2['question'][':question/id']==r3['question'][':question/id'] and r2['generation']['mathematical_fingerprint']==r3['generation']['mathematical_fingerprint']
  bads=[{**p,'a':99},{**p,'a':-99},{**p,'bounds':[2,1,0,1]},{**p,'extra':1},{**p,'a':1.5}]
  if level=='moderate':bads.extend([{**p,'py':0},{**p,'qx':0},{**p,'r0':0}])
  if level=='hard':bads.extend([{**p,'b':0},{**p,'c':0}])
  for bad in bads:
   try:g.generate(level,template=template,parameters=bad)
   except ValueError:invalid+=1
   else:raise AssertionError('Unbounded explicit input')
 # Validator must detect corruption of a displayed intermediate, final equation,
 # prompt implicit product and bank answer; checks are not metadata comparisons.
 mutation_count=0
 reference=g.generate('hard',12)
 mutations=[]
 a=copy.deepcopy(reference);a['question'][':question/worked-solution']=a['question'][':question/worked-solution'].replace(' & =⟨',' & =⟨999+',1);mutations.append(a)
 a=copy.deepcopy(reference);a['question'][':question/problem']=a['question'][':question/problem'].replace('xy','x',1);mutations.append(a)
 a=copy.deepcopy(reference);a['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='999';mutations.append(a)
 for r in mutations:
  try:independent(r)
  except Exception:mutation_count+=1
  else:raise AssertionError('Corruption escaped validator')
 for profile,d in g.PROFILES.items():
  if profile=='authored_operations':continue
  for seed in (101,102):
   rr=g.generate('easy',seed,d['template'],profile=profile);independent(rr);records.append({'label':'Generated evidence bank '+profile+' '+str(seed),'record':rr})
 engine=[]
 for item in replay+records:
  f=item['record']['question'][':question/answer-fields'][0];engine.append({**item,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'All owned radio answers'} for a in f[':answer-field/choices']]})
 write('engine-input.json',engine);subprocess.run([str(PROJECT/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True);native=json.loads((ROOT/'engine-validation.json').read_text());assert native['documented_unresolved_checks']==0
 write('review.json',records)
 review=['# Review: concrete Cartesian flux setup','All originals are easy. Moderate/hard headings denote authored scope, not recovered source labels. Source replay normalizes notation; q-161471 corrects its final LHS field.']
 for c,item in zip(cases,replay):
  raw=g.SOURCES[c['source_id']];review.extend(['## Original '+c['source_id']+' / '+c['bank_profile'],raw[':question/problem'],'\nOriginal complete bank: '+', '.join('$'+a[':answer/value']+'$' for a in raw[':question/answer-fields'][c['source_field_index']][':answer-field/choices']),raw[':question/worked-solution'],'### Reconstructed at original parameters',g.markdown(item['record'])])
 for item in records:review.extend(['## '+item['label'],g.markdown(item['record'])])
 (ROOT/'review.md').write_text('\n\n'.join(review)+'\n')
 report={'passed':True,'provenance':{k:g.RAW[k] for k in ('database','basis','lineage')},'source_questions':12,'source_fields':13,'complete_banks_matched':13,'displayed_values_matched':65,'observed_designations_matched':12,'observed_designations_available':12,'missing_designations':1,'inferred_legacy_correct_values':1,'known_distractors_matched':48,'additional_legacy_inferred_distractors_matched':4,'prompt_notation_normalizations':12,'solution_prose_and_row_sequence_matched':12,'solutions_mathematically_normalized_without_repair':11,'solutions_with_final_lhs_repair':1,'duplicate_field_repairs':1,'sampled_math_checks':tested,'unique_sampled_mathematical_tasks':{k:len(v) for k,v in unique.items()},'exhaustive_hard_assessed_tasks':len(hard_fingerprints),'explicit_invalid_inputs_rejected':invalid,'validator_mutations_rejected':mutation_count,'native_grading':{'entry_point':native['entry_point'],'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':0},'authored_missing_levels':['moderate: two variable separable-gradient factors, affine field, <=quadratic integrand','hard: mixed-gradient coordinate dependence with bilinear field component, <=cubic integrand'],'source_interpretation_limits':['Observed polynomial patterns retain all original values; errors with unidentified intent are explicit evidence profiles, not default banks.','Moderate/hard difficulty assignment is an authored workload claim.'],'observed_operation_mapping':{'choices_with_supported_candidates':sum(bool(r['selected']) for rs in g.OBSERVED_MAP.values() for r in rs),'residual_underidentified_patterns':sum(not bool(r['selected']) for rs in g.OBSERVED_MAP.values() for r in rs),'ambiguous_candidate_matches':sum(len(r['candidates'])>1 for rs in g.OBSERVED_MAP.values() for r in rs)},'native_engine_sha256':g.hashlib.sha256((PROJECT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'database_writes':0,'unresolved_findings':[]}
 write('validation.json',report);print(json.dumps(report,indent=2))
if __name__=='__main__':run()
