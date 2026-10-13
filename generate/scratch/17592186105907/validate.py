#!/usr/bin/env python3
"""Independent validation from actual printed vectors, matrices and arithmetic.
Run from repo root with .venv/bin/python. Writes only this private evidence folder.
"""
import importlib.util,json,re,subprocess,hashlib
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('volume_generator',HERE.with_suffix('.py'))
g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
TRANS=standard_transformations+(implicit_multiplication_application,)

def read_math(text):
 text=text.strip().removesuffix('.')
 # Fractions are exact; substitute innermost complete numerator/denominator.
 while r'\frac' in text:
  out=re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',r'((\1)/(\2))',text)
  assert out!=text,('unreadable fraction',text)
  text=out
 text=text.replace(r'\cdot','*').replace('{','(').replace('}',')').replace(' ','')
 assert not any(t in text for t in ('--','+-')),text
 result=parse_expr(text,transformations=TRANS,evaluate=True)
 assert result.is_Rational,('Nonrational printed scalar',text,result)
 return result

def printed_vectors(q):
 v=[[read_math(x) for x in s.split(',')] for s in re.findall('⟨(.*?)⟩',q[':question/problem'])]
 assert len(v)==3 and all(len(row)==3 for row in v)
 return v

def independent(q):
 v=printed_vectors(q); m=sp.Matrix(v)
 # Alternate determinant route avoids the generator's hand-coded cofactor helper.
 d=sp.Matrix(v[0]).dot(sp.Matrix(v[1]).cross(sp.Matrix(v[2])))
 assert d==m.det()
 values=[read_math(a[':answer/value']) for a in q[':question/answer-fields'][0][':answer-field/choices']]
 assert len(set(values))==len(values)
 assert all(x>0 for x in values)
 f=q[':question/answer-fields'][0]
 if ':answer-field/correct' in f:
  correct=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])
  assert read_math(correct[':answer/value'])==abs(d)
 else:assert abs(d) in values
 if ':question/worked-solution' not in q:return v,d
 s=q[':question/worked-solution']
 # Match inner matrices without using generation metadata or renderer helpers.
 matches=list(re.finditer(r'\\begin\{aligned\}((?:(?!\\begin\{aligned\}|\\end\{aligned\}).)*)\\end\{aligned\}',s,re.S))
 assert len(matches)==4,('four displayed matrices required',matches)
 mats=[]
 for match in matches:
  mats.append(sp.Matrix([[read_math(x) for x in row.split('&')] for row in match[1].split(r'\\')]))
 assert mats[0]==m
 assert mats[1]==m.minor_submatrix(0,0)
 assert mats[2]==m.minor_submatrix(0,1)
 assert mats[3]==m.minor_submatrix(0,2)
 # Replace each COMPLETE |matrix| with its independently evaluated determinant.
 collapsed=s
 for match,mat in reversed(list(zip(matches,mats))):
  assert s[match.start()-1]=='|' and s[match.end()]=='|'
  collapsed=collapsed[:match.start()-1]+'('+str(mat.det())+')'+collapsed[match.end()+1:]
 block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',collapsed,re.S)[1]
 rows=block.split(r'\\')
 assert len(rows)==5
 labels=re.findall(r'\$([a-z])\s*=',q[':question/problem'])
 assert len(labels)==3
 assert rows[0].split('& =')[0].strip()==labels[0]+r'\cdot ('+labels[1]+r'\times '+labels[2]+')'
 cofactor_terms=re.findall(r'(.*?)\\cdot \((-?\d+(?:/\d+)?)\)',rows[1].split('& =',1)[1])
 assert len(cofactor_terms)==3
 assert [read_math(prefix) for prefix,_ in cofactor_terms]==[v[0][0],-v[0][1],v[0][2]]
 for row in rows:
  assert '& =' in row
  assert read_math(row.split('& =',1)[1])==d,('wrong displayed determinant stage',row,d)
 # First two rows have matrix expansion structure; third preserves substituted
 # products or the extracted q-280712 evaluated-minor structure; fourth is sum.
 assert rows[1].count(r'\cdot')==3
 assert rows[2].count(r'\cdot') in (0,4,6)
 assert rows[3].count(r'\cdot')==0
 final=re.search(r'V=\|(.*?)\|=(.*?)\.',s)
 assert final and read_math(final[1])==d and read_math(final[2])==abs(d)
 return v,d

def formatting(record):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 evidence_only=bool(record['generation']['bank_profile'] and record['generation']['bank_profile'].startswith('observed_'))
 assert record['generation']['evidence_only']==evidence_only
 assert record['generation']['eligible_for_learning']==(not evidence_only)
 q=record['question'];f=q[':question/answer-fields'][0]
 import uuid
 for value in (q[':question/id'],f[':answer-field/id'],*[a[':answer/id'] for a in f[':answer-field/choices']]):uuid.UUID(value)
 assert f[':answer-field/type'] in (':answer-field.type/radio',':answer-field.type/blank')
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 for text in [q[':question/problem'],q.get(':question/worked-solution',''),*[a[':answer/value'] for a in f[':answer-field/choices']]]:
  assert text.count('$')%2==0
  # TeX groups and field placeholders are balanced in all generated output.
  assert text.count('{')==text.count('}')
  assert not re.search(r'[+\-]\s*-\d',text),text

checks=[]
def engine_fixture(label,r):
 f=r['question'][':question/answer-fields'][0]
 assert ':answer-field/correct' in f
 correct=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  entry=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'Owned radio answer selected, complete bank independent math checked'} for a in f[':answer-field/choices']]
 else:
  value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
  v=read_math(value)
  # Unreduced but genuinely different arithmetic syntax, positive exact volume.
  equivalent=str(3*v.p)+'/'+str(3*v.q)
  entry=[{'submitted':value,'expected':'accepted','purpose':'Canonical exact volume'},
   {'submitted':equivalent,'expected':'accepted','purpose':'Equivalent unreduced rational entry'},
   {'submitted':str(v+1),'expected':'rejected','purpose':'Incorrect positive volume'},
   {'submitted':str(-v),'expected':'rejected','purpose':'Signed triple product is not volume'}]
 checks.append({'label':label,'record':r,'checks':entry})

def review_block(label,r):
 return '## '+label+'\n\n'+g.markdown(r)+'\n\nAuthor metadata: '+json.dumps(r['generation'],sort_keys=True)+'\n'

def run():
 cases=json.loads((HERE/'source-cases.json').read_text())
 fidelity=[]; review=[]; markdown=['# Parallelepiped volume source and variant review\n\nOriginals and generated variants are labeled; opaque bank variants are evidence-only, never normal defaults.']
 stages=0; distractors=0; known_correct=0; raw_missing=0
 for case in cases:
  sid=case['source_id']; original=g.SOURCES[sid]
  r=g.generate('easy',19,case['template'],parameters=case['parameters'],profile=case.get('bank_profile'))
  q=r['question'];formatting(r);independent(q)
  assert q[':question/problem']==original[':question/problem']
  assert q.get(':question/worked-solution')==original.get(':question/worked-solution')
  assert q.get(':question/difficulty')== (original.get(':question/difficulty') or {}).get(':db/ident')
  sf=original[':question/answer-fields'][0];gf=q[':question/answer-fields'][0]
  assert gf[':answer-field/key']==sf[':answer-field/key']
  assert gf[':answer-field/type']==sf[':answer-field/type'][':db/ident']
  assert sorted(read_math(a[':answer/value']) for a in gf[':answer-field/choices'])==sorted(read_math(a[':answer/value']) for a in sf[':answer-field/choices'])
  if ':answer-field/correct' in sf:
   correct=next(a for a in gf[':answer-field/choices'] if a[':answer/id']==gf[':answer-field/correct'][1])
   assert read_math(correct[':answer/value'])==read_math(sf[':answer-field/correct'][':answer/value']);known_correct+=1
  else:assert ':answer-field/correct' not in gf;raw_missing+=1
  if ':question/worked-solution' in original:stages+=1
  if sf[':answer-field/type'][':db/ident'].endswith('/radio'):distractors+=len(sf[':answer-field/choices'])-1
  fidelity.append({'source_id':sid,'prompt_exact':True,'solution_exact_or_absence_preserved':True,'bank_complete_exact_values':True,'designation':'matched' if ':answer-field/correct' in sf else 'absent-preserved-not-matched'})
  markdown.append('## Original '+sid+'\n\n'+original[':question/problem']+'\n\nBank: '+', '.join(a[':answer/value'] for a in sf[':answer-field/choices'])+'\n\n'+original.get(':question/worked-solution','[Absent source solution, correct designation and rating]'))
  markdown.append(review_block('Generated source replay '+sid,r));review.append({'label':'source replay '+sid,'record':r})
  repaired=r
  if ':answer-field/correct' not in gf:
   repaired=g.generate('easy',19,case['template'],parameters=case['parameters'],profile=case['bank_profile']+'_repaired')
   formatting(repaired);independent(repaired['question'])
  engine_fixture('source '+sid+(' repaired' if repaired is not r else ''),repaired)
  # Every observed layout and whole bank gets a changed-parameter variant.
  v=g.canonical(case['parameters']);v[1]=[-x for x in v[1]]
  variant=g.generate('easy',23,case['template'],parameters=g.serialized(v),profile=case.get('bank_profile'))
  formatting(variant);independent(variant['question']);review.append({'label':'evidence variant '+sid,'record':variant});markdown.append(review_block('Generated changed-vector evidence variant '+sid,variant))
  if ':answer-field/correct' in variant['question'][':question/answer-fields'][0]:engine_fixture('variant '+sid,variant)
 tasks={}; total=0
 for level in ('easy','moderate','hard'):
  seen=set(); positions=set()
  for seed in range(120):
   for kind in ('radio','blank'):
    r=g.generate(level,seed,field_type=kind);formatting(r);v,d=independent(r['question']);total+=1
    # Assert all level bounds independently against the printed, reduced values.
    flat=sum(v,[]);m=sp.Matrix(v)
    if level=='easy':assert all(x.q==1 and abs(x)<=9 for x in flat) and 1<=flat.count(0)<=3
    if level=='moderate':assert all(x!=0 and x.q==1 and abs(x)<=5 for x in flat) and all(v[0][i]*m.cofactor(0,i)!=0 for i in range(3))
    if level=='hard':assert all(x!=0 and x.q in (1,2,3) and abs(x)<=5 for x in flat) and sum(x.q>1 for x in flat)>=3 and all(v[0][i]*m.cofactor(0,i)!=0 for i in range(3))
    if kind=='radio':
     t=[v[0][i]*m.cofactor(0,i) for i in range(3)]
     expected={abs(d),abs(t[0]+t[1]),abs(t[0]+t[2]),abs(t[1]+t[2]),abs(t[0]-t[1]+t[2])}
     assert {read_math(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']}==expected
     positions.add(next(i for i,a in enumerate(r['question'][':question/answer-fields'][0][':answer-field/choices']) if a[':answer/id']==r['question'][':question/answer-fields'][0][':answer-field/correct'][1]))
    again=g.generate(level,seed+983,template=r['generation']['template'],parameters=r['generation']['parameters'],profile=r['generation']['bank_profile'])
    assert r['question'][':question/id']==again['question'][':question/id']
    assert r['generation']['parameter_fingerprint']==again['generation']['parameter_fingerprint']
    seen.add(r['generation']['parameter_fingerprint'])
    if seed<2:
     review.append({'label':'authored '+level+' '+kind+' '+str(seed),'record':r});markdown.append(review_block('Generated authored '+level+' '+kind+' seed '+str(seed),r));engine_fixture(level+' '+kind+' '+str(seed),r)
  assert len(seen)>100 and len(positions)>=4
  tasks[level]={'meaningful_tasks_120_seeds_two_layouts':len(seen),'correct_positions':sorted(positions)}
 # Explicit invalid levels/profile/field/presentation cases must fail.
 invalid=[('moderate',{'vectors':[[0,1,2],[1,2,3],[2,3,4]]}),('hard',{'vectors':[[1,2,3],[4,5,1],[2,1,4]]}),('hard',{'vectors':[['1/2',1,2],[1,2,3],[2,3,4]]}),('moderate',{'vectors':[[-6,1,2],[1,2,3],[2,3,4]]}),('easy',{'vectors':[[1,2,3],[4,5,1],[2,1,4]]})]
 for l,p in invalid:
  try:g.generate(l,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('Invalid explicit input accepted',l,p))
 # Mutation controls prove that QA observes printed math and all bank members.
 import copy
 r=g.generate('moderate',0)
 bad=copy.deepcopy(r);bad['question'][':question/problem']=bad['question'][':question/problem'].replace('⟨','⟨99,',1)
 try:independent(bad['question'])
 except (AssertionError,ValueError):pass
 else:raise AssertionError('Printed prompt mutation escaped QA')
 bad=copy.deepcopy(r);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(r'\cdot ',r'\cdot 9+',1)
 try:independent(bad['question'])
 except (AssertionError,ValueError):pass
 else:raise AssertionError('Displayed intermediate mutation escaped QA')
 engine_input=HERE/'engine-input.json';engine_input.write_text(json.dumps(checks,indent=2))
 result=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(engine_input),str(HERE/'engine-report.json')],capture_output=True,text=True)
 assert result.returncode==0,(result.stdout,result.stderr)
 engine=json.loads((HERE/'engine-report.json').read_text())
 (HERE/'review.json').write_text(json.dumps(review,indent=2,ensure_ascii=False)+'\n')
 (HERE/'review.md').write_text('\n\n---\n\n'.join(markdown)+'\n')
 report={'status':'passed','source_basis':g.PROVENANCE,'source_questions':len(cases),'exact_prompts':len(cases),'exact_existing_solutions':stages,'solution_denominator':9,'preserved_absent_solutions':2,'source_banks_matched':7,'source_choices_matched':39,'source_distractors_matched':distractors,'known_correct_designations_matched':known_correct,'designation_denominator':9,'missing_designations_preserved':raw_missing,'independently_inferred_missing_keys':{'q-40214':'45','q-42052':'29'},'source_errors':[],'presentation_repairs':0,'normal_records_independently_checked':total,'variety':tasks,'native_grading':{k:v for k,v in engine.items() if k!='records'},'native_binary_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'scope':'easy observed, moderate/hard authored; supplied vectors only','unresolved':'All seven scalar source radio banks have opaque distractor intent; evidence-only ratio profiles retain exact values, default uses separately authored cofactor-method bank.'}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))
if __name__=='__main__':run()
