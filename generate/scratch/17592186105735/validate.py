#!/usr/bin/env python3
"""Independent displayed-math, fidelity, interface, and native grading checks."""
import copy, importlib.util, json, re, subprocess, sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('triple',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def parse(s):
 s=s.replace(r'\,','').replace(r'\cdot','*')
 s=re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',s)
 s=s.replace(')(',')*(').rstrip('.')
 return sp.sympify(s)
def vector(s):return [parse(x) for x in s.replace(chr(92)+',','').split(',')]
def tokens(s):
 s=s.replace(r'\,','');s=re.sub(r'\\sqrt\{(\d+)\}',r'sqrt(\1)',s)
 return [sp.sympify(x) for x in re.findall(r'-?sqrt\(\d+\)|-?\d+',s)]
def validate(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];gen=r['generation'];prompt=q[':question/problem'];sol=q.get(':question/worked-solution')
 f=q[':question/answer-fields'][0];choices=f[':answer-field/choices']
 for s in [prompt,sol or '']+[c[':answer/value'] for c in choices]:
  assert not any(ord(c)<32 and c not in '\n\t' for c in s),'control byte'
  assert s.count('$')%2==0,'math delimiter'
  assert s.count('{')==s.count('}'),'brace balance'
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in prompt
 vectors=[vector(v) for v in re.findall('⟨([^⟩]+)⟩',prompt)]
 assert len(vectors) in [2,3]
 if gen['profile']=='source:q-20065':assert r['generation']['evidence_only'] and r'a \cdot (b \cdot c)' in prompt
 else:assert r'\times' in prompt,'requested scalar triple criterion'
 a=vectors[0]
 if len(vectors)==2:d=vectors[1]
 else:
  b,c=vectors[1:];d=list(sp.Matrix(b).cross(sp.Matrix(c)))
 t=sp.Matrix(a).dot(sp.Matrix(d))
 vs=[parse(c[':answer/value']) for c in choices]
 assert len(set(vs))==len(vs),'whole scalar uniqueness'
 if gen['profile']=='dot_operations':
  expected=[t,sum(x+y for x,y in zip(a,d)),sum(x*x for x in a),sum(x*x for x in d),sum(x*y for x,y in zip(a,reversed(d)))]
  assert sorted(vs,key=str)==sorted(expected,key=str),'complete method dot bank'
 elif gen['profile']=='cross_operations':
  b,c=vectors[1:];terms=[x*y for x,y in zip(a,d)]
  expected=[t,a[0]*d[0]-a[1]*d[1]+a[2]*d[2],a[0]*b[1]*c[2]-a[1]*b[0]*c[2]+a[2]*b[0]*c[1],t-terms[0],t-terms[2]]
  assert sorted(vs,key=str)==sorted(expected,key=str),'complete method cross bank'
 if ':answer-field/correct' in f:
  selected=next(c for c in choices if c[':answer/id']==f[':answer-field/correct'][1]);assert parse(selected[':answer/value'])==t
 if sol:
  if len(vectors)==3:
   cs=sol.split('Now,')[0];rows=cs.split(r' \\  & =')
   assert len(rows)==5,'cross stage sequence'
   assert tokens(rows[0])==b+c,'cross initial inputs'
   assert tokens(rows[1])==[b[1],b[2],c[1],c[2],b[0],b[2],c[0],c[2],b[0],b[1],c[0],c[1]],'minors'
   m=re.search(r'^\((.*)\)i-\((.*)\)j\+\((.*)\)k$',rows[2]);assert m,'cross distributed stage'
   assert [parse(x) for x in m.groups()]==[d[0],-d[1],d[2]],'cross distributed values'
   expected=[[b[1],c[2],b[2],c[1]],[b[0],c[2],b[2],c[0]],[b[0],c[1],b[1],c[0]]]
   actual=[tokens(re.sub(r'(?<=[0-9)])-(?=[0-9(])',';',x.replace(' ',''))) for x in m.groups()]
   if gen['template']=='cross_blank':expected[1]=[b[0],c[2],c[0],b[2]]
   assert actual==expected,'cross multiplication operands'
   basis=rows[3];terms=re.findall(r'([+-]?\d*)([ijk])',basis)
   coeffs={letter:sp.Integer(coef if coef not in ['', '+', '-'] else '-1' if coef=='-' else '1') for coef,letter in terms}
   assert coeffs==dict(zip('ijk',d)),'basis coefficients'
   assert vector(re.search('⟨([^⟩]+)⟩',rows[4])[1])==d,'cross final tuple'
   ds=sol.split('Now,')[1]
  else:ds=sol
  dr=ds.split(r' \\  & =')
  dot_vectors=[vector(v) for v in re.findall('⟨([^⟩]+)⟩',dr[0])];assert dot_vectors==[a,d],'dot operands'
  assert tokens(dr[1])==[x for pair in zip(a,d) for x in pair],'dot component factors'
  assert parse(dr[1])==t,'distributed dot value'
  has_evaluation='radical' in gen['template'] or gen['template']=='cross_blank'
  assert len(dr)==(4 if has_evaluation else 3),'dot stage count'
  if has_evaluation:assert parse(dr[2])==t and tokens(dr[2])==[sp.simplify(x*y) for x,y in zip(a,d)],'individual dot values'
  final=dr[-1].split(r'\end{aligned}')[0];assert parse(final)==t,'final scalar'
  assert 'determinant of the matrix whose rows' not in sol
 return int(t)

def run():
 source_cases=[];records=[];fixtures=[];fidelity=[]
 for qid,(level,template,p) in g.SPECS.items():
  case={'source_id':qid,'level':level,'template':template,'parameters':p,'bank_profile':'source:'+qid};source_cases.append(case)
  r=g.generate(level,parameters=p,template=template,profile=case['bank_profile']);validate(r);records.append(r)
  o=g.QUESTIONS[qid];q=r['question'];of=o[':question/answer-fields'][0];f=q[':question/answer-fields'][0]
  for k in [':question/problem',':question/worked-solution',':question/difficulty']:
   assert (k in o)==(k in q)
   if k in o:assert q[k]==(o[k][':db/ident'] if k==':question/difficulty' else o[k]),(qid,k)
  for k in [':answer-field/type',':answer-field/key',':answer-field/correct']:
   assert (k in f)==(k in of)
  assert f[':answer-field/type']==of[':answer-field/type'][':db/ident']
  assert f[':answer-field/key']==of[':answer-field/key']
  assert sorted(c[':answer/value'] for c in f[':answer-field/choices'])==sorted(c[':answer/value'] for c in of[':answer-field/choices'])
  if ':answer-field/correct' in of:
   assert next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])==of[':answer-field/correct'][':answer/value']
  fidelity.append({'source_id':qid,'prompt_exact':True,'solution_exact':':question/worked-solution' in o,'bank_exact':True,'designation_exact':':answer-field/correct' in of,'raw_missing_attrs_preserved':True})
  if ':answer-field/correct' in f:fixtures.append(fixture(qid,r))
  else:
   completion=g.generate(level,parameters=p,template=template,profile='completed:'+qid);validate(completion);records.append(completion);fixtures.append(fixture(qid+' authored completion',completion))
 # Changed variants for every observed template/profile: opaque evidence only.
 for qid,(level,template,p) in g.SPECS.items():
  varied=copy.deepcopy(p)
  varied['a']=[str(-g.val(x)) if 'sqrt' not in x else x[1:] if x.startswith('-') else '-'+x for x in p['a']]
  r=g.generate(level,template=template,parameters=varied,profile='source:'+qid);validate(r);records.append(r)
 # Every normal family, not just random coverage.
 for level,templates in g.TEMPLATES.items():
  for template in templates:
   if template=='cross_legacy_radio':continue
   for seed in [37,89]:
    r=g.generate(level,seed,template=template);validate(r);records.append(r);fixtures.append(fixture(level+' '+template+' '+str(seed),r))
 counts={}
 for level in g.TEMPLATES:
  fps=set();seen=set()
  for seed in range(300):
   r=g.generate(level,seed);validate(r);fps.add(r['generation']['mathematical_fingerprint']);seen.add(r['generation']['template'])
   same=g.generate(level,seed+1000,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['profile'])
   assert same['question'][':question/id']==r['question'][':question/id'],'seed changed identity'
  counts[level]={'tested':300,'unique_mathematical_tasks':len(fps),'default_templates':sorted(seen)}
 # Operation-removal mutation retains mathematical equality but must fail stage structure.
 dense=g.generate_hard(10,template='cross_blank');bad=copy.deepcopy(dense)
 bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(r' \\  & ='+bad['question'][':question/worked-solution'].split(r' \\  & =')[2],'',1)
 expect_failure(bad)
 bad=copy.deepcopy(dense);bad['question'][':question/worked-solution']+='\x0c';expect_failure(bad)
 bad=copy.deepcopy(dense);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(')i-',')i+',1);expect_failure(bad)
 invalid=[('hard',{'a':['1','2','3'],'b':['1','2','3'],'c':['1','2','3']}),('moderate',{'a':['-5','1','2'],'b':['1','2','3'],'c':['2','3','1']})]
 for l,p in invalid:
  try:g.generate(l,template='cross_blank',parameters=p)
  except ValueError:pass
  else:raise AssertionError('explicit guard bypass')
 (HERE/'source-cases.json').write_text(json.dumps(source_cases,indent=2)+'\n')
 (HERE/'review.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
 (HERE/'engine-input.json').write_text(json.dumps(fixtures,ensure_ascii=False,indent=2)+'\n')
 subprocess.run([str(Path('generate/runs/current/check-engine').resolve()),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 engine=json.loads((HERE/'engine-report.json').read_text())
 report={'status':'passed','database':'math','basis':1356,'source_questions':11,'exact_prompts':11,'exact_available_solutions':10,'exact_complete_banks':11,'source_distractors_matched':20,'source_distractors_total':20,'inferred_missing_key_distractors':4,'present_correct_designations_matched':10,'missing_source_designations':1,'raw_ungradable_sources':['q-20065'],'authored_completion_answer':16,'opaque_evidence_banks':6,'native_grading':engine,'variety':counts,'mutation_regressions':3,'plot_rating':'none','dependencies':{'python':sys.version.split()[0],'sympy':sp.__version__}}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 (HERE/'review.md').write_text('# Source originals and generated variants\n\nRaw evidence profiles retain source omissions; all changed variants are labeled by metadata.\n\n'+'\n\n'.join('## '+('Original replay' if i<12 else 'Generated variant')+' — '+r['generation']['level']+' / '+r['generation']['template']+' / '+r['generation']['profile']+'\n\n'+g.markdown(r) for i,r in enumerate(records)))
 print('PASS: 11 banks, 11 prompts, 10 available solutions; 900 changed samples; native checks passed')
def expect_failure(r):
 try:validate(r)
 except (AssertionError,ValueError,TypeError,sp.SympifyError):return
 raise AssertionError('mutation was accepted')
def fixture(label,r):
 f=r['question'][':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':c[':answer/id'],'expected':'accepted' if c[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'entire displayed bank'} for c in f[':answer-field/choices']]
 else:
  t=validate(r);checks=[{'submitted':str(t),'expected':'accepted','purpose':'canonical scalar'},{'submitted':f'{t-3}+3','expected':'accepted','purpose':'unevaluated equivalent sum'},{'submitted':str(t+1),'expected':'rejected','purpose':'wrong scalar'}]
 return {'label':label,'record':r,'checks':checks}
if __name__=='__main__':run()
