#!/usr/bin/env python3
"""Raw byte/presence fidelity, independent displayed math, scope and native QA."""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
D=Path(__file__).resolve().parent;ROOT=D.parents[2];SCRIPT=D.with_suffix('.py')
spec=importlib.util.spec_from_file_location('matrix_draft',SCRIPT);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sys.path.insert(0,str(ROOT/'generate/runs/current'))
import importlib
F=importlib.import_module('root-source-fidelity')
def dump(name,obj):(D/name).write_text(json.dumps(obj,indent=2)+'\n')
def parse_cells(text):
 m=g.MATRIX.fullmatch(text.strip());assert m
 rows=[]
 for row in m[1].split(r'\\'):
  rows.append([sp.sympify(v.strip()) for v in row.split('&')])
 return sp.Matrix(rows)
def eval_expr(expression,matrices):
 assert re.fullmatch(r'[A-Z0-9+()\- ]+',expression),expression
 shape=next(iter(matrices.values())).shape
 return sp.Matrix(shape[0],shape[1],lambda i,j:sp.sympify(expression,locals={n:v[i,j] for n,v in matrices.items()}))
def inspect(r):
 q=r['question'];p=q[':question/problem'];sol=q[':question/worked-solution']
 assert r['knowledge_point']==g.KP
 for text in [p,sol,*[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]]:
  assert not any(ord(c)<32 and c not in '\n\t\r' for c in text),'Control character'
  assert not re.search(r'(?<!-)--(?!-)|\+-',text),'Bare signed adjacency'
 expression=re.search(r'Find \$(.*?)\$',p)[1]
 matrices={m[1]:parse_cells(m[2]) for m in re.finditer(r'([A-Z])\s*=\s*(\\begin\{bmatrix\}.*?\\end\{bmatrix\})',p,re.S)}
 assert len(matrices)==(4 if r['generation']['template']=='authored-hard' else 3)
 correct=eval_expr(expression,matrices)
 assert correct==g.result(r['generation']['parameters'],r['generation']['template'])
 # Read operative distribution and cancellation rows as printed, not metadata.
 formal=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1]
 rows=formal.split(r'\\');assert len(rows)==3
 lhs=rows[0].split('&')[0].strip();assert lhs.replace(' ','')==expression.replace(' ','')
 symbols={n:sp.Symbol(n) for n in matrices};original=sp.sympify(expression,locals=symbols)
 rhs=[row.split('=',1)[1].strip() for row in rows]
 for v in rhs:
  clean=re.sub(r'\\cancel\{([A-Z])\}',r'\1',v)
  assert sp.expand(sp.sympify(clean,locals=symbols)-original)==0,(v,expression)
 assert '(' not in rhs[0] and ')' not in rhs[0], 'Missing distribution stage'
 negative_groups=re.findall(r'-\(([^)]+)\)',expression.replace(' ',''))
 assert len(negative_groups)==1
 negative_terms=len(re.findall('[A-Z]',negative_groups[0]))
 assert negative_terms==(3 if r['generation']['template']=='authored-hard' else 2)
 cancels=re.findall(r'\\cancel\{([A-Z])\}',rhs[1]);assert len(cancels)==(2 if q[':question/difficulty'].endswith('/easy') else 4)
 assert rhs[1]!=rhs[0],'Missing operative cancellation markings'
 coefficients={n:sp.expand(original).coeff(v) for n,v in symbols.items()}
 plus=[n for n,c in coefficients.items() if c==1];minus=[n for n,c in coefficients.items() if c==-1]
 assert len(plus)==1 and len(minus)<=1
 expected_x=plus[0];expected_y=minus[0] if minus else None
 numeric=[parse_cells(m[0]) for m in g.MATRIX.finditer(sol)]
 if expected_y is None:assert len(numeric)==1 and numeric[0]==matrices[expected_x]
 else:
  assert len(numeric)==4
  assert numeric[0]==matrices[expected_x] and numeric[1]==matrices[expected_y]
  assert numeric[2]==correct and numeric[3]==correct
  operative=list(g.MATRIX.finditer(sol))[2][1]
  # The intermediate must expose EACH signed subtraction, not repeat final.
  arithmetic=[v.strip() for row in operative.split(r'\\') for v in row.split('&')]
  for cell,x,y in zip(arithmetic,matrices[expected_x],matrices[expected_y]):
   expected=str(x)+'-'+('('+str(y)+')' if y<0 else str(y));assert cell==expected
 fields=q[':question/answer-fields']
 for i,f in enumerate(fields):
  vals=[parse_cells(a[':answer/value']) if g.MATRIX.fullmatch(a[':answer/value']) else sp.sympify(a[':answer/value']) for a in f[':answer-field/choices']]
  correct_a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);actual=parse_cells(correct_a[':answer/value']) if g.MATRIX.fullmatch(correct_a[':answer/value']) else sp.sympify(correct_a[':answer/value'])
  if f[':answer-field/type'].endswith('/blank'):
   key=f[':answer-field/key'];index=int(key.split('-')[-1])-1
   assert '{{'+key+'}}' in p;assert actual==correct[index]
  else:
   assert actual==correct
   assert len(vals)==5 and len({tuple(v) for v in vals})==5
   zero_names=[n for n,c in coefficients.items() if c==0];z=matrices[zero_names[0]];a=matrices[expected_x]
   if expected_y is None:
    c=matrices[zero_names[1]];expected=[correct,a-2*c,a+2*z,a-z,a-c]
   else:
    b=matrices[expected_y];expected=[correct,a+b,b-a,correct+z,correct-z]
   assert {tuple(v) for v in vals}=={tuple(v) for v in expected},'Wrong-operation bank does not match printed method'
 g.validate_generated_record(r)
 return correct

def inspect_raw_bank(r):
 """Independent complete historical bank calculation from the printed givens."""
 q=r['question'];t=r['generation']['template'];prompt=q[':question/problem']
 matrices={m[1]:parse_cells(m[2]) for m in re.finditer(r'([A-Z])\s*=\s*(\\begin\{bmatrix\}.*?\\end\{bmatrix\})',prompt,re.S)}
 expression=re.search(r'Find \$(.*?)\$',prompt)[1];correct=eval_expr(expression,matrices)
 original=g.ORIGINALS[t]
 for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:
  assert (key in q)==(key in original),'Raw source presence changed'
 if t=='q-13550':return
 if t=='q-279581':
  expected=None
 elif t in ['q-13535','q-13543']:
  expected=[correct]
  for row in range(2):
   for col in range(2):
    v=correct.copy();v[row,col]-=1;expected.append(v)
 elif t=='q-13536':
  A=matrices['A'];expected=[A,matrices['B'],matrices['C'],sp.zeros(2),sp.Matrix([[A[1,1],A[0,1]],[A[0,1],A[1,1]]])]
 elif t=='q-69623':
  G,F=matrices['G'],matrices['F'];c=correct
  expected=[c,sp.Matrix([list(c.row(1)),list(c.row(0))]),
   sp.Matrix([[c[0,1],c[0,0],c[0,2]],[c[1,1],c[1,0],c[1,2]]]),
   sp.Matrix([[G[0,0]+F[0,0],G[0,1]+F[0,1],F[0,2]-G[0,2]],[G[1,0]+F[1,0],G[1,1],G[1,2]+F[1,2]]]),
   sp.Matrix([list(c.row(0)),[-G[1,0]-F[1,0],-G[1,1]+F[1,1],G[1,2]+F[1,2]]])]
 elif t=='q-69627':
  V,N=matrices['V'],matrices['N'];c=correct;added=V+N;added[2,0]=V[2,0]-N[2,0]
  expected=[c,matrices['C'],sp.Matrix([list(c.row(0)),[c[1,1],c[1,0]],list(c.row(2))]),sp.Matrix([list(c.row(0)),list(c.row(2)),list(c.row(1))]),added]
 else:raise AssertionError('Unexpected source family')
 assert len(q[':question/answer-fields'])==len(original[':question/answer-fields'])
 for field,old in zip(q[':question/answer-fields'],original[':question/answer-fields']):
  assert field[':answer-field/key']==old[':answer-field/key']
  assert (':answer-field/correct' in field)==(':answer-field/correct' in old)
  if expected is None:
   value=sp.sympify(field[':answer-field/choices'][0][':answer/value']);index=int(field[':answer-field/key'].split('-')[-1])-1
   assert value==correct[index]
  else:
   displayed=[parse_cells(a[':answer/value']) for a in field[':answer-field/choices']]
   assert len(displayed)==len(expected)==5
   assert {tuple(m) for m in displayed}=={tuple(m) for m in expected},'Recovered complete source coordinate operations changed'
   assert len({tuple(m) for m in displayed})==5
   assert sum(m==correct for m in displayed)==1
   if ':answer-field/correct' in field:
    selected=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1]);assert parse_cells(selected[':answer/value'])==correct
 assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning']

def native_item(r,label):
 checks=[]
 for i,f in enumerate(r['question'][':question/answer-fields']):
  if f[':answer-field/type'].endswith('/radio'):
   for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every complete displayed option'})
  else:
   v=int(f[':answer-field/choices'][0][':answer/value'])
   for text,expect,purpose in [(str(v),'accepted','canonical integer'),(str(v-2)+'+2','accepted','unreduced equivalent integer sum'),(str(v+1),'rejected','wrong neighbor')]:checks.append({'field_index':i,'submitted':text,'expected':expect,'purpose':purpose})
 return {'record':r,'label':label,'checks':checks}

def main():
 baseline=json.loads((D/'baseline-inventory.json').read_text())
 paths=[ROOT/'generate/scratch/17592186100992.py',*[p for p in (ROOT/'generate/scratch/17592186100992').rglob('*') if p.is_file()]]
 actual={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths)}
 assert actual==baseline['files'],'Registered baseline changed'
 originals,raw_counts=F.check(g,'17592186100992',D)
 cases=json.loads((D/'source-cases.json').read_text());assert len(cases)==len(originals)==7
 independent=json.loads((D/'independent-inventory.json').read_text());assert independent['questions']==[]
 ledger=json.loads((D/'source-components.json').read_text())
 assert {row['source_id']:row['captured_record'] for row in ledger['questions']}==originals
 reviews=[];native=[];coverage={l:{} for l in ['easy','moderate','hard']};keys={l:set() for l in coverage};positions=set()
 for c in cases:
  raw=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='source-original');inspect_raw_bank(raw)
  prompt=raw['question'][':question/problem'];expr=re.search(r'Find \$(.*?)\$',prompt)[1]
  matrices={m[1]:parse_cells(m[2]) for m in re.finditer(r'([A-Z])\s*=\s*(\\begin\{bmatrix\}.*?\\end\{bmatrix\})',prompt,re.S)}
  expected=eval_expr(expr,matrices)
  valid=[f for f in raw['question'].get(':question/answer-fields',[]) if ':answer-field/correct' in f]
  for f in valid:
   a=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);v=a[':answer/value']
   if f[':answer-field/type'].endswith('/radio'):assert parse_cells(v)==expected,'Incorrect source designation'
   else:assert sp.sympify(v)==expected[int(f[':answer-field/key'].split('-')[-1])-1],'Incorrect source cell designation'
  if valid:
   fixture=copy.deepcopy(raw);fixture['question'][':question/answer-fields']=valid
   fixture['generation']['native_fixture_role']='captured valid fields only; raw public record preserved separately'
   native.append(native_item(fixture,'captured-valid-fields-'+c['source_id']))
 for level in coverage:
  for seed in range(300):
   r=g.generate(level,seed=seed);inspect(r);keys[level].add(r['generation']['mathematical_key']);t=r['generation']['template'];coverage[level][t]=coverage[level].get(t,0)+1
   if seed<15:native.append(native_item(r,level+'-'+str(seed)))
   f=r['question'][':question/answer-fields'][0]
   if f[':answer-field/type'].endswith('/radio'):positions.add(next(i for i,v in enumerate(f[':answer-field/choices']) if v[':answer/id']==f[':answer-field/correct'][1]))
  for t,s in g.SPECS.items():
   if s[0]!=level:continue
   for seed in [801,809]:
    r=g.generate(level,seed=seed,template=t);inspect(r);reviews.append(r);native.append(native_item(r,t+'-'+str(seed)))
   a=g.generate(level,seed=1,template=t);b=g.generate(level,seed=67,template=t,parameters=a['generation']['parameters']);assert a['question'][':question/id']==b['question'][':question/id']
   q=a['question'];f=q[':question/answer-fields'][0]
   if f[':answer-field/type'].endswith('/radio'):positions.add(next(i for i,v in enumerate(f[':answer-field/choices']) if v[':answer/id']==f[':answer-field/correct'][1]))
 assert len(coverage['easy'])==6 and len(coverage['moderate'])==1 and len(coverage['hard'])==1
 assert len(positions)>1
 # Public field_type selectors must choose supported family before parameters.
 assert g.generate('easy',seed=12,field_type='blank')['generation']['template']=='q-279581'
 # Reject complete-bank collisions, never pool individual fallback options.
 p={n:[[0,0],[0,0]] for n in 'MNO'}
 try:g.generate('easy',template='q-13543',parameters=p)
 except ValueError:pass
 else:raise AssertionError('Whole-bank collision accepted')
 # Canceled supplied entries change presentation but never assessed fingerprints.
 for level,t in [('easy','q-13543'),('moderate','q-13536'),('hard','authored-hard')]:
  a=g.generate(level,123,template=t);p=copy.deepcopy(a['generation']['parameters']);n=g.SPECS[t][5];p[n][0][0]=p[n][0][0]+1 if p[n][0][0]<9 else -9
  b=g.generate(level,123,template=t,parameters=p);assert a['generation']['mathematical_key']==b['generation']['mathematical_key'];assert a['question'][':question/id']!=b['question'][':question/id']
 # No selected-cell slots: each radio assesses the whole matrix, each blank
 # assesses all four entries. Changing one answer-cell changes its printed
 # arithmetic, key and matrix answer with the other supplied data held fixed.
 a=g.generate('easy',51,template='q-279581');p=copy.deepcopy(a['generation']['parameters']);p['A'][0][1]+=1 if p['A'][0][1]<9 else -1
 b=g.generate('easy',51,template='q-279581',parameters=p);inspect(b)
 aa={f[':answer-field/key']:f[':answer-field/choices'][0][':answer/value'] for f in a['question'][':question/answer-fields']};bb={f[':answer-field/key']:f[':answer-field/choices'][0][':answer/value'] for f in b['question'][':question/answer-fields']};assert [k for k in aa if aa[k]!=bb[k]]==['field-2']
 # Mutation checks must detect lost operations even when final result is intact.
 mutation_tests=[]
 def must_fail(name,mutation):
  try:inspect(mutation)
  except (AssertionError,ValueError,TypeError,sp.SympifyError):mutation_tests.append(name)
  else:raise AssertionError('Mutation passed '+name)
 sample=g.generate('easy',801,template='q-13543')
 m=copy.deepcopy(sample);m['question'][':question/worked-solution']=m['question'][':question/worked-solution'].replace('M+O-N-M','M+O-N+M');must_fail('distributed-sign',m)
 m=copy.deepcopy(sample);m['question'][':question/worked-solution']=m['question'][':question/worked-solution'].replace(r'\cancel{M}','M');must_fail('operative-cancellation-removed',m)
 m=copy.deepcopy(sample);m['question'][':question/worked-solution']+='\f';must_fail('control-character',m)
 m=copy.deepcopy(b);m['question'][':question/answer-fields'][1][':answer-field/choices'][0][':answer/value']=aa['field-2'];must_fail('stale-changed-cell',m)
 raw_checks=0;raw_variants=[]
 for c in cases:
  for seed in range(80):
   raw=g.generate(c['level'],seed=6000+seed,template=c['template'],profile='source-original');inspect_raw_bank(raw);raw_checks+=1
   if seed<2:
    raw_variants.append(raw)
    valid=[f for f in raw['question'].get(':question/answer-fields',[]) if ':answer-field/correct' in f]
    if valid:
     fixture=copy.deepcopy(raw);fixture['question'][':question/answer-fields']=valid;fixture['generation']['native_fixture_role']='changed-parameter captured valid fields only; complete raw public record preserved separately'
     native.append(native_item(fixture,'changed-captured-valid-fields-'+c['source_id']+'-'+str(seed)))
 # Explicit raw whole-bank collision guards apply even to ineligible evidence.
 for t,p in [('q-13536',{'A':[[0,0],[0,0]],'B':[[1,2],[3,4]],'C':[[5,6],[7,8]]}),('q-69623',{'F':[[1,2,3],[4,5,6]],'G':[[2,4,6],[5,7,9]],'H':[[9,8,7],[6,5,4]]}),('q-69627',{'C':[[1,2],[3,4],[5,6]],'V':[[7,8],[5,6],[9,8]],'N':[[2,3],[1,2],[3,2]]})]:
  try:g.generate(g.SPECS[t][0],template=t,parameters=p,profile='source-original')
  except ValueError:pass
  else:raise AssertionError('Raw complete-bank equivalence accepted '+t)
 # The earlier anchor-only offset generalization must fail independently.
 for t in ['q-13536','q-69623','q-69627']:
  p=copy.deepcopy(g.anchor(t));p[g.SPECS[t][3]][0][0]+=1
  raw=g.generate(g.SPECS[t][0],template=t,parameters=p,profile='source-original');inspect_raw_bank(raw)
  mutated=copy.deepcopy(raw);delta=g.result(p,t)-g.result(g.anchor(t),t)
  for f,original_field in zip(mutated['question'][':question/answer-fields'],g.ORIGINALS[t][':question/answer-fields']):
   oldvalues=[parse_cells(a[':answer/value'])+delta for a in original_field[':answer-field/choices']]
   for a,value in zip(f[':answer-field/choices'],oldvalues):a[':answer/value']=g.matrix(value.tolist())
  try:inspect_raw_bank(mutated)
  except AssertionError:mutation_tests.append('reject-anchor-offset-bank-'+t)
  else:raise AssertionError('Literal source residual offsets passed '+t)
 # Source-profile replays under changed operands remain parameterized; original
 # metadata omissions and duplicated keys still remain evidence-only.
 for c in cases:
  p=copy.deepcopy(c['parameters']);p[g.SPECS[c['template']][3]][0][0]+=1
  r=g.generate(c['level'],template=c['template'],parameters=p,profile='source-original');assert r['generation']['evidence_only'] and not r['generation']['eligible_for_learning'];assert r['question'][':question/problem']!=originals[c['source_id']][':question/problem']
 for template,level in [('q-13543','easy'),('q-13536','moderate'),('authored-hard','hard')]:
  r=g.generate(level,11,template=template);p=copy.deepcopy(r['generation']['parameters']);p[g.SPECS[template][3]][0][0]=10
  try:g.generate(level,parameters=p,template=template)
  except ValueError:pass
  else:raise AssertionError('Explicit domain guard bypassed')
 dump('review.json',reviews);dump('source-bank-review.json',raw_variants);dump('native-input.json',native)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(D/'native-input.json'),str(D/'native-report.json')],check=True)
 report=json.loads((D/'native-report.json').read_text())
 validation={'status':'pass','script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),'registered_baseline_unchanged_files':len(actual),'source_basis':2275,'source_fidelity':raw_counts,'source_cases':7,'normal_math_checks':900+len(reviews),'changed_parameter_source_replays_checked':raw_checks,'changed_parameter_source_fields_checked':800,'meaningful_task_counts_sampled':{l:len(v) for l,v in keys.items()},'default_family_coverage':coverage,'radio_correct_positions_seen':sorted(positions),'mutation_regressions_rejected':mutation_tests,'changed_cell_regression':'field-2 changed; other three fixed; actual prompt/solution/key parsed','native':{k:v for k,v in report.items() if k!='records'},'hard_calibration':'authored uncertain; double cancellation + residual signed 3x2 subtraction','runtime':{'python':sys.version.split()[0],'sympy':sp.__version__},'plots':'none','independent_inventory_count':0}
 dump('validation.json',validation)
 review=['# Distributivity source and generated review','Frozen basis2275. Raw missing grade/key/solution/fields and duplicate legacy fields remain evidence-only. Normal variants below are authored method banks. Hard is authored; calibration remains uncertain.']
 for c in cases:
  raw=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='source-original');normal=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile='authored-method')
  review+=['## Original '+c['source_id'],g.markdown(raw),'## Authored method bank at original parameters',g.markdown(normal)]
 for r in raw_variants:review+=['## Changed-parameter captured bank / '+r['generation']['template']+' (evidence-only; ineligible)',g.markdown(r)]
 for r in reviews:review+=['## Generated '+r['generation']['template']+' / '+r['question'][':question/difficulty'].split('/')[-1],g.markdown(r)]
 (D/'review.md').write_text('\n\n'.join(review)+'\n')
 print(json.dumps(validation,indent=2))
if __name__=='__main__':main()
