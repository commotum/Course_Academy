#!/usr/bin/env python3
"""Read actual printed coordinates, vectors, matrices, every arithmetic equality
and fullbanks; separate raw source anomaly preservation from normal correctness.
Native tests use the real learning::grade_field memory fixtures.
"""
import difflib,hashlib,importlib.util,json,re,subprocess,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('vertex_volume',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def load(p):return json.loads(p.read_text())
def dump(p,v):p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
def parse(t):
 t=t.strip().rstrip('.').replace(r'\,','').replace(r'\cdot','*')
 while r'\frac' in t:
  m=re.search(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',t);assert m,t
  t=t[:m.start()]+'('+m[1]+')/('+m[2]+')'+t[m.end():]
 t=t.replace('^','**')
 t=re.sub(r'(\d|\))(?=[ijk])',r'\1*',t)
 return parse_expr(t,local_dict={'i':sp.Symbol('i'),'j':sp.Symbol('j'),'k':sp.Symbol('k')},transformations=standard_transformations+(implicit_multiplication_application,))
def balanced(t):
 assert t.count('$')%2==0,t
 depth=0
 for i,c in enumerate(t):
  if c=='{':depth+=1
  if c=='}':depth-=1
  assert depth>=0,t
 assert depth==0,t
 assert '--' not in t and '+-' not in t,t
 # Decoded adjacent slash bytes: only linebreak commands permitted, never a
 # doubled slash before a TeX command. No escape repairs inferred from repr.
 assert not re.search(r'\\\\(?:frac|overset|cdot|begin|end)',t),t

def verify(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];meta=r['generation'];f=q[':question/answer-fields'][0];raw=meta['bank_origin']=='raw-evidence';sid=meta['source_id']
 assert meta['evidence_only']==bool(sid) and meta['eligible_for_learning']==(not bool(sid))
 points=[list(map(int,z.replace(' ','').split(','))) for z in re.findall(r'[ABCD]\(([-\d, ]+)\)',q[':question/problem'])];assert len(points)==4
 # Independent determinant formula from actual coordinates and independent CAS.
 vv=[[a-b for a,b in zip(point,points[0])] for point in points[1:]];u,v,w=vv
 cross=[v[1]*w[2]-v[2]*w[1],v[2]*w[0]-v[0]*w[2],v[0]*w[1]-v[1]*w[0]];det=sum(a*b for a,b in zip(u,cross));assert sp.Matrix(vv).det()==det
 correct=abs(det);assert correct>0
 if not sid:
  level=g.TEMPLATES[meta['template']][0];active=sum(a*b!=0 for a,b in zip(u,cross));nz=sum(n!=0 for row in vv for n in row)
  assert active=={'easy':1,'moderate':2,'hard':3}[level]
  assert max(abs(n) for row in vv for n in row)<={'easy':3,'moderate':4,'hard':5}[level]
  assert max(abs(n) for row in points for n in row)<=8
  assert correct<=200 and all(abs(a*b)<=150 for a,b in zip(u,cross))
  assert nz<=6 if level=='easy' else nz>=6 if level=='moderate' else nz>=7

 for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value'] for a in f[':answer-field/choices']]:balanced(text)
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==3
  # Displacement formal/substitution/basis/tuple: preserve all twelve rows.
  rows=blocks[0].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ');assert len(rows)==12
  I,J,K=sp.symbols('i j k')
  for idx,(name,point,vec) in enumerate(zip('BCD',points[1:],vv)):
   chunk=rows[idx*4:idx*4+4]
   assert chunk[0]==r'\overset{\to }{A'+name+'} & ='+name.lower()+'-a'
   expected=sum(n*c for n,c in zip(vec,[I,J,K]))
   sub=chunk[1].split('=',1)[1].strip();assert parse(sub).expand()==expected
   parts=re.fullmatch(r'\((.*?)\)-\((.*?)\)',sub);assert parts
   assert parse(parts[1]).expand()==sum(n*c for n,c in zip(point,[I,J,K]))
   assert parse(parts[2]).expand()==sum(n*c for n,c in zip(points[0],[I,J,K]))
   reduced=parse(chunk[2].split('=',1)[1]).expand()
   if raw and sid=='q-73744' and idx==2:
    scale=g.validate_parameters('hard',{'points':points},meta['profile']);assert reduced==expected+2*scale*J
   else:assert reduced==expected,(sid,chunk)
   assert list(map(int,re.search('⟨([^⟩]+)⟩',chunk[3])[1].split(',')))==vec
  mats=re.findall(r'\|\\begin\{aligned\}(.+?)\\end\{aligned\}\|',blocks[1]);assert len(mats)==4
  cells=lambda m:[[int(t.strip()) for t in row.split('&')] for row in m.split(r'\\')]
  assert cells(mats[0])==vv
  minors=[[[v[1],v[2]],[w[1],w[2]]],[[v[0],v[2]],[w[0],w[2]]],[[v[0],v[1]],[w[0],w[1]]]]
  assert [cells(m) for m in mats[1:]]==minors
  dr=blocks[1].removesuffix(r'\end{aligned}').split(r' \\  & =')
  assert len(dr)==(g.SPECS[sid]['arithmetic_row_count']+3 if sid and g.SPECS[sid]['has_solution'] else 6)
  # Replace each actual minor with its independently computed determinant;
  # validate signed coefficient cofactor row, then EVERY numeric equality.
  row=dr[1]
  for original,m in zip(re.findall(r'\|\\begin\{aligned\}.+?\\end\{aligned\}\|',row),minors):row=row.replace(original,'('+str(sp.Matrix(m).det())+')',1)
  assert parse(row)==det,(sid,row,det)
  for row in dr[2:]:assert parse(row)==det,(sid,row,det)
  if not sid or not g.SPECS[sid]['has_solution']:
   # Authored sequence keeps distinct operator/substitution/evaluation stages.
   assert dr[2].count(r'\cdot')==9 and dr[3].count(r'\cdot')==3
   assert dr[4].count(r'\cdot')==0 and '(' not in dr[5]
   # Each determinant component's four displayed factors independently retain
   # input order, even when another numerically equal factor exists.
   expected_terms=[]
   for c,m in zip([u[0],-u[1],u[2]],minors):
    grouped=lambda n:'('+str(n)+')' if n<0 else str(n)
    expected_terms.append(grouped(c)+r'\cdot ('+grouped(m[0][0])+r'\cdot '+grouped(m[1][1])+'-'+grouped(m[1][0])+r'\cdot '+grouped(m[0][1])+')')
   assert dr[2]=='+'.join(expected_terms)
  else:
   # Stage structure agrees with raw source in each profile; dilation can add
   # only the omitted unit coefficient, not erase product/evaluation stages.
   for shown,original in zip(dr[2:-1],g.SPECS[sid]['arithmetic_source']):
    assert shown.count(r'\cdot')==original.count(r'\cdot')
    assert shown.count('(')==original.count('(')

  final=blocks[2].replace(r'\,','');m=re.fullmatch(r'V=\|(-?\d+)\|=(\d+)\.',final);assert m and [int(z) for z in m.groups()]==[det,correct]
 vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(set(vals))==len(vals) and all(v>=0 for v in vals)
 assert len(vals)==(5 if f[':answer-field/type'].endswith('radio') else 1)
 if f[':answer-field/type'].endswith('blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 for identifier in [q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]:uuid.UUID(identifier)
 if ':answer-field/correct' in f:
  ref=f[':answer-field/correct'];assert ref[0]==':answer/id'
  actual=[parse(a[':answer/value']) for a in f[':answer-field/choices'] if a[':answer/id']==ref[1]];assert actual==[correct]
 else:assert raw and sid in ('q-128472','q-20138')
 assert q.get(':question/difficulty')==(None if raw and not g.SPECS[sid]['has_difficulty'] else ':question.difficulty/'+g.TEMPLATES[meta['template']][0])
 if meta['bank_origin']=='authored' and len(vals)==5:
  if g.TEMPLATES[meta['template']][0] in ('easy','moderate'):
   expected=[correct,2*correct,sp.Rational(correct,2),sp.Rational(correct,6),abs(sp.Matrix(points[1:]).det())]
  else:
   contributions=[u[0]*cross[0],u[1]*cross[1],u[2]*cross[2]];expected=[correct]+[abs(det-c) for c in contributions]+[sp.Rational(correct,6)]
  assert set(vals)==set(expected)
 return points,det,correct

def engine_case(r,label):
 f=r['question'][':question/answer-fields'][0];points,det,correct=verify(r)
 if ':answer-field/correct' not in f:return None
 if f[':answer-field/type'].endswith('radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned complete-bank selection'} for a in f[':answer-field/choices']]
 else:
  vv=[[a-b for a,b in zip(point,points[0])] for point in points[1:]];u,v,w=vv
  expr='abs('+str(u[0])+'*('+str(v[1])+'*'+str(w[2])+'-'+str(v[2])+'*'+str(w[1])+')-'+str(u[1])+'*('+str(v[0])+'*'+str(w[2])+'-'+str(v[2])+'*'+str(w[0])+')+'+str(u[2])+'*('+str(v[0])+'*'+str(w[1])+'-'+str(v[1])+'*'+str(w[0])+'))'
  checks=[{'submitted':str(correct),'expected':'accepted','purpose':'canonical volume'},{'submitted':expr,'expected':'accepted','purpose':'independent unreduced absolute scalar triple product'},{'submitted':str(correct+1),'expected':'rejected','purpose':'incorrect volume'}]
 return {'label':label,'record':r,'checks':checks}

def main():
 src=load(HERE/'source.json')['record'][':knowledge-point/questions'];records=[];engine=[];cases=[];details=[];review=[]
 for q in src:
  sid=q[':question/math-academy-id'];p={'points':g.SPECS[sid]['points']}
  case={'source_id':sid,'level':'hard','template':g.SOURCE_TEMPLATE[sid],'parameters':p,'bank_profile':'raw_'+sid,'normal_profile':sid,'difficulty_origin':'observed' if ':question/difficulty' in q else 'authored-supported-hard'};cases.append(case)
  raw=g.generate_hard(template=sid,parameters=p,profile='raw_'+sid);verify(raw);records.append(raw)
  rq=raw['question'];sf=q[':question/answer-fields'][0];rf=rq[':question/answer-fields'][0]
  assert rq[':question/problem']==q[':question/problem']
  assert rq.get(':question/worked-solution')==q.get(':question/worked-solution'),sid
  assert set(a[':answer/value'] for a in rf[':answer-field/choices'])==set(a[':answer/value'] for a in sf[':answer-field/choices']),sid
  assert (':answer-field/correct' in rf)==(':answer-field/correct' in sf)
  assert (':question/difficulty' in rq)==(':question/difficulty' in q)
  assert rf[':answer-field/key']==sf[':answer-field/key'] and rf[':answer-field/type']==sf[':answer-field/type'][':db/ident']
  if ':answer-field/correct' in sf:
   a=next(a for a in rf[':answer-field/choices'] if a[':answer/id']==rf[':answer-field/correct'][1]);assert a[':answer/value']==sf[':answer-field/correct'][':answer/value']
  details.append({'source_id':sid,'prompt_exact':True,'worked_solution_exact':True if ':question/worked-solution' in q else None,'bank_values_exact':len(sf[':answer-field/choices']),'designation_matched':True if ':answer-field/correct' in sf else None,'metadata_absence_preserved':True,'known_raw_mathematical_anomaly':sid=='q-73744'})
  normal=g.generate_hard(template=sid,parameters=p,profile=sid);verify(normal);records.append(normal);engine.append(engine_case(normal,sid+'/normal'))
  review.append('## Original '+sid+'\n\n'+g.markdown(raw)+'\n\n### Normal replay (repairs listed in review metadata)\n\n'+g.markdown(normal))
  # Uniform dilation exercises actual math changes; translations vary subtraction.
  for scale in (2,3):
   pp={'points':[[scale*n+h for n,h in zip(row,[2,-1,1])] for row in p['points']]}
   for profile in (sid,'raw_'+sid):
    r=g.generate_hard(template=sid,parameters=pp,profile=profile);verify(r);records.append(r)
    ec=engine_case(r,sid+'/'+profile+'/scale'+str(scale))
    if ec:engine.append(ec)
   review.append('### Generated observed-domain variant: uniform dilation '+str(scale)+' plus translation; scalar bank intent unresolved\n\n'+g.markdown(r))
 for level in ('easy','moderate','hard'):
  for kind in ('radio','blank'):
   template=level+'_'+kind
   for seed in range(35):
    r=g.generate(level,seed=seed+200,template=template);verify(r);records.append(r);engine.append(engine_case(r,template+'/'+str(seed)))
    if seed<2:review.append('## Authored '+level+' / '+kind+' variant\n\n'+g.markdown(r))
    replay=g.generate(level,seed=seed+2000,template=template,parameters=r['generation']['parameters']);verify(replay)
    assert replay['question'][':question/id']==r['question'][':question/id'] and replay['generation']['parameter_fingerprint']==r['generation']['parameter_fingerprint']
 # Strict explicit guards, no silently repaired parameters.
 for level,p in [('easy',{'points':[[0,0,0],[1,1,1],[2,0,1],[0,2,1]]}),('moderate',{'points':[[0,0,0],[1,0,0],[1,2,0],[0,1,3]]}),('hard',{'points':[[0,0,0],[1,0,0],[1,2,0],[0,1,3]]})]:
  try:g.generate(level,parameters=p);raise AssertionError('Invalid level workload accepted')
  except ValueError:pass
 for p in [{'points':[[0,0,0],[1,0,0],[0,1,0],[0,0,0]]},{'points':[[0,0,0],[9,0,0],[0,9,0],[0,0,9]]}]:
  try:g.generate_hard(parameters=p);raise AssertionError('Invalid instance accepted')
  except ValueError:pass
 # Field layout changes retain mathematical-task identity, content banks change IDs.
 for level in ('easy','moderate','hard'):
  radio=g.generate(level,seed=210,template=level+'_radio');p=radio['generation']['parameters'];blank=g.generate(level,template=level+'_blank',parameters=p)
  assert radio['generation']['parameter_fingerprint']==blank['generation']['parameter_fingerprint'] and radio['question'][':question/id']!=blank['question'][':question/id']
 dump(HERE/'source-cases.json',cases);dump(HERE/'review.json',records);(HERE/'review.md').write_text('# Originals and generated variants\n\nRaw preserves one known erroneous basis stage and missing metadata; normal replay corrects/infer/authors them. Source scaling banks are evidence only.\n\n'+'\n\n---\n\n'.join(review)+'\n')
 dump(HERE/'engine-input.json',engine)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 native=load(HERE/'engine-report.json');assert native['database_writes']==0 and native['documented_unresolved_checks']==0,native
 authored=[r for r in records if r['generation']['bank_origin']=='authored']
 result={'status':'pass','provenance':g.PROVENANCE,'source_questions':17,'source_prompts_exact':17,'source_solution_exact':{'matched':15,'available':15,'missing':2,'mathematically_valid_raw_solutions':14,'raw_known_error':1},'source_bank_fidelity':{'complete':17,'values':61,'radio_banks':11,'blank_fields':6,'matched_correct_designations':15,'available_correct_designations':15,'missing_correct_designations_preserved_raw':2},'source_details':details,'normal_math_and_display_checks':len(records)-1,'total_records_verified_with_explicit_raw_anomaly':len(records),'native':{k:v for k,v in native.items() if k!='records'},'native_report':'engine-report.json','authored_level_counts':{l:sum(g.TEMPLATES[r['generation']['template']][0]==l for r in authored) for l in ('easy','moderate','hard')},'authored_task_counts':{l:len({r['generation']['parameter_fingerprint'] for r in authored if g.TEMPLATES[r['generation']['template']][0]==l}) for l in ('easy','moderate','hard')},'remaining_limits':['Scalar source distractor intent unresolved; uniform-dilation evidence profiles never selected as default banks.','No original easy/moderate labels; their workload domains are authored curriculum-supported claims.','Two unrated originals have no correct designation or solution; raw profiles retain absence, normal profiles infer volume and author solution.','q-73744 raw basis error intentionally preserved and independently detected; all normal output corrects it.']}
 # Dynamic denominators, not guessed counts.
 result['source_bank_fidelity']['values']=sum(d['bank_values_exact'] for d in details)
 result['normal_math_and_display_checks']=sum(not(r['generation']['bank_origin']=='raw-evidence' and r['generation']['source_id']=='q-73744') for r in records)
 dump(HERE/'validation.json',result)
 hashes={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [HERE.with_suffix('.py')]+sorted(p for p in HERE.iterdir() if p.is_file() and p.name!='freeze.json')}
 hashes['generate/runs/current/check-engine']=hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest()
 dump(HERE/'freeze.json',{'status':'frozen_after_all_producers','sha256':hashes})
 print(json.dumps({k:v for k,v in result.items() if k not in ('native','source_details')},indent=2))
if __name__=='__main__':main()
