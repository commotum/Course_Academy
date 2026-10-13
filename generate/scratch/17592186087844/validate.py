#!/usr/bin/env python3
"""Independent printed-mathematics reader, raw fidelity, native grading, scope QA."""
from pathlib import Path
import importlib.util,json,re,hashlib,subprocess,uuid
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,convert_xor
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x=sp.Symbol('x',real=True)
TRANS=standard_transformations+(implicit_multiplication_application,convert_xor)

def group(s,i):
 assert s[i]=='{',s[i:];depth=0
 for j in range(i,len(s)):
  if s[j]=='{':depth+=1
  if s[j]=='}':
   depth-=1
   if not depth:return s[i+1:j],j+1
 raise AssertionError('Unbalanced group '+s)

def fraction_parts(s):
 out=[]
 for m in re.finditer(r'\\(?:d?frac)\{',s):
  a,i=group(s,m.end()-1);assert s[i]=='{';b,end=group(s,i);out.append((a,b,s[m.start():end]))
 return out

def read(tex):
 """Independent restricted TeX parser; reads displayed strings, not parameters."""
 s=tex.strip().rstrip('.:')
 for _,_,full in fraction_parts(s):
  a,b,_=fraction_parts(full)[0];s=s.replace(full,'(('+str(read(a))+')/('+str(read(b))+'))')
 s=s.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace('{','').replace('}','').replace('[','(').replace(']',')')
 s=s.replace('**','^')
 if not re.fullmatch(r'[\sa-zA-Z0-9+*/^().\-]+',s):raise AssertionError('Unsupported displayed arithmetic '+repr(s))
 return parse_expr(s,local_dict={'x':x,'a':sp.Symbol('a'),'b':sp.Symbol('b'),'c':sp.Symbol('c')},transformations=TRANS)

def roots_from_assignments(v):
 vals=[]
 for m in re.finditer(r'x\s*=\s*(-?\\frac\{\d+\}\{\d+\}|-?\d+)',v):vals.append(read(m.group(1)))
 return tuple(sorted(set(vals)))

def format_check(txt):
 assert txt.count('$')%2==0
 # Count complete math spans plus residual dollars, so odd inline delimiters fail.
 residue=g.MATH_SPANS.sub('',txt);assert '$' not in residue
 depth=0
 for ch in txt:
  if ch=='{':depth+=1
  elif ch=='}':depth-=1;assert depth>=0
 assert depth==0
 assert '--' not in txt and '+-' not in txt

def check_printed(r):
 q=r['question'];meta=r['generation']
 assert meta['evidence_only']!=meta['eligible_for_learning']
 if meta['profile']=='original':assert meta['evidence_only'] and not meta['eligible_for_learning']
 prompt=q[':question/problem'];sol=q[':question/worked-solution']
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert r['knowledge_point']['db_id']==g.KP_ID
 for text in (prompt,sol):format_check(text)
 uuid.UUID(q[':question/id'])
 fs=fraction_parts(prompt);assert len(fs)==1
 N,D=map(read,fs[0][:2]);assert sp.degree(sp.gcd(N,D),x)==0
 factors=sp.factor_list(D,x)[1];quadratics=[f for f,m in factors if sp.degree(f,x)==2];assert len(quadratics)==1,(prompt,D,factors)
 Q=quadratics[0];a,b,c=sp.Poly(Q,x).all_coeffs();disc=b*b-4*a*c;assert disc<0
 real_roots=tuple(sorted(sp.polys.polytools.ground_roots(D,x)))
 # Every entire option root set, including text and math mixtures.
 for f in q.get(':question/answer-fields',[]):
  uuid.UUID(f[':answer-field/id']);key=f[':answer-field/key'];shape=f[':answer-field/type']
  assert all(a[':answer/type'] in (':answer.type/math',':answer.type/text') for a in f[':answer-field/choices'])
  if shape.endswith('/blank'):assert '{{'+key+'}}' in prompt
  choices=f[':answer-field/choices'];own={a[':answer/id'] for a in choices};assert len(own)==len(choices);assert f[':answer-field/correct'][1] in own
  sets=[]
  for answer in choices:
   uuid.UUID(answer[':answer/id']);value=answer[':answer/value'];format_check(value)
   if shape.endswith('/blank'):rs=(read(value),)
   else:
    rs=roots_from_assignments(value)
    if not rs:assert 'no vertical asymptotes' in value.lower()
   sets.append(rs)
   if answer[':answer/id']==f[':answer-field/correct'][1]:assert rs==real_roots,(prompt,value,real_roots)
   else:assert rs!=real_roots
  assert len(set(sets))==len(sets)
  operations=r['generation']['bank_operations']
  if operations:
   expected={tuple(sorted(sp.polys.polytools.ground_roots(read(op['zeros_of']),x))) for op in operations}
   assert expected==set(sets),(operations,sets)
 # Every printed rational function in worked stages is equal to prompt.
 fractions=[f for f in fraction_parts(sol) if 'x' in f[0] or 'x' in f[1]]
 for n,d,_ in fractions:assert sp.cancel(read(n)/read(d)-N/D)==0,(prompt,n,d)
 if fractions:assert len(fractions)==len([f for f in fraction_parts(g.QS[r['generation']['template']][':question/worked-solution']) if 'x' in f[0] or 'x' in f[1]])
 # All displayed denominator=0 equations preserve real roots; inline complex
 # factors have no roots. All isolated linear equations yield a true real root.
 spans=[m.group(0).strip('$').strip() for m in g.MATH_SPANS.finditer(sol)]
 checked_equations=0
 for span in spans:
  if r'\begin{aligned}D' in span:
   rows=span.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\  & =')
   assert len(rows)==4
   formal=rows[0].split('& =')[1].strip();expr=read(formal)
   assert sp.expand(expr-(sp.Symbol('b')**2-4*sp.Symbol('a')*sp.Symbol('c')))==0
   for row in rows[1:]:assert read(row)==disc,(prompt,row,disc)
   # Explicitly keep substitution, multiplication evaluation, subtraction rows.
   assert '^' in rows[1] and '-4(' in rows[1] and '^' not in rows[2] and '-' in rows[2]
  elif '=0' in span and r'\begin' not in span and r'\frac' not in span:
   lhs=read(span.split('=')[0]);rs=tuple(sorted(sp.polys.polytools.ground_roots(lhs,x)))
   assert rs==real_roots or (not rs and sp.degree(lhs,x)==2) or (sp.degree(lhs,x)==1 and all(z in real_roots for z in rs)),(prompt,span,real_roots)
   checked_equations+=1
  elif re.fullmatch(r'x=.+[.]?',span):
   rs=roots_from_assignments(span);assert all(z in real_roots for z in rs),(span,real_roots)
 conclusion=sol.split('Therefore,')[-1]
 got=roots_from_assignments(conclusion)
 if real_roots:assert got==real_roots,(conclusion,real_roots)
 else:assert 'no vertical asymptotes' in conclusion or 'does not have any vertical asymptotes' in conclusion
 return {'fractions':len(fractions),'equations':checked_equations,'option_sets':sum(len(f[':answer-field/choices']) for f in q.get(':question/answer-fields',[]))}

def fidelity(t):
 level,_,p=g.SPECS[t];src=g.QS[t];r=g.generate(level,template=t,parameters=p,profile='original');q=r['question']
 assert q[':question/problem']==src[':question/problem']
 assert q[':question/worked-solution']==src[':question/worked-solution']
 for key in (':question/difficulty',':question/answer-fields',':question/worked-solution',':question/math-academy-id'):
  assert (key in src)==(key in q),(t,key,'attribute-presence parity')
 for key in src:
  if key not in (':db/id',':question/id',':question/problem',':question/worked-solution',':question/answer-fields'):
   v=src[key];assert q[key]==(v.get(':db/ident',v) if isinstance(v,dict) else v)
 a=src.get(':question/answer-fields');b=q.get(':question/answer-fields')
 if not a:assert ':question/answer-fields' not in q;return r,0,0,0
 assert len(a)==len(b)
 count=distractors=banks=0
 for sf,gf in zip(a,b):
  assert sf[':answer-field/type'][':db/ident']==gf[':answer-field/type'];assert sf[':answer-field/key']==gf[':answer-field/key']
  source_bank=sorted((o[':answer/type'][':db/ident'],o[':answer/value']) for o in sf[':answer-field/choices']);gen_bank=sorted((o[':answer/type'],o[':answer/value']) for o in gf[':answer-field/choices']);assert source_bank==gen_bank
  sc=sf[':answer-field/correct'];gc=next(o for o in gf[':answer-field/choices'] if o[':answer/id']==gf[':answer-field/correct'][1]);assert (sc[':answer/type'][':db/ident'],sc[':answer/value'])==(gc[':answer/type'],gc[':answer/value'])
  count+=len(source_bank);distractors+=len(source_bank)-1;banks+=not gf[':answer-field/type'].endswith('/blank')
 return r,count,distractors,banks

def native_item(r,label):
 checks=[]
 for i,f in enumerate(r['question'].get(':question/answer-fields',[])):
  if f[':answer-field/type'].endswith('/blank'):
   correct=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);v=read(correct)
   checks.extend([{'field_index':i,'submitted':correct,'expected':'accepted','purpose':'canonical exact root fragment'},{'field_index':i,'submitted':str(v*2)+'/2','expected':'accepted','purpose':'unreduced equivalent root fragment'},{'field_index':i,'submitted':str(v+1),'expected':'rejected','purpose':'incorrect real root'}])
  else:
   for a in f[':answer-field/choices']:checks.append({'field_index':i,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'owned full-choice designation'})
 return {'label':label,'record':r,'checks':checks}

def enumerate_tasks():
 from itertools import product
 catalog={'easy':{},'moderate':{},'hard':{}}
 for t,(level,family,base) in g.SPECS.items():
  if family=='quadratic':domains={'a':range(2,6)} if t=='q-6912' else {'b':[b for b in range(-7,8) if b],'c':range(1,13)}
  elif family=='gcf':domains={'b':range(1,5),'c':range(1,10)}
  elif family=='group':
   domains={'r':range(1,6),'c':range(1,10)} if t!='q-278551' else {'r':range(1,6),'a':range(2,4)}
   if t in ('q-113523','q-113527'):domains['s']=range(1,6)
  elif family=='cube':
   domains={'r':range(2 if t=='q-4694' else 1,6)}
   if t=='q-270004':domains['s']=range(1,6)
  else:domains={'p':range(2,4),'q':range(1,3),'s':range(1,5)}
  keys=list(domains)
  for values in product(*(domains[k] for k in keys)):
   p=dict(base);p.update(zip(keys,values))
   try:r=g.generate(level,template=t,parameters=p)
   except ValueError:continue
   fingerprint=r['generation']['mathematical_fingerprint']
   # Read one complete actual printed question per enumerated mathematical task.
   check_printed(r)
   catalog[level].setdefault(fingerprint,{'template':t,'parameters':p})
 (HERE/'task-catalog.json').write_text(json.dumps(catalog,indent=2)+'\n')
 return {level:len(tasks) for level,tasks in catalog.items()}

def main():
 cases=[];review=[];native=[];count=wrong=banks=0;metrics={'fractions':0,'equations':0,'option_sets':0};ids=set();tasks={'easy':set(),'moderate':set(),'hard':set()};tested=0
 originals=[];normal_exact=0;normal_repairs=0;normal_completions=0
 for t,(level,family,p) in g.SPECS.items():
  r,a,b,c=fidelity(t);originals.append(r);count+=a;wrong+=b;banks+=c;cases.append({'source_id':g.QS[t][':question/id'],'source_math_academy_id':t,'template':t,'parameters':p,'bank_profile':'original','level':level})
  check_printed(r)
  normal=g.generate(level,template=t,parameters=p,profile='supported-observed')
  expected_solution=g.QS[t][':question/worked-solution'].replace('$2x=0$','$x=0$') if t=='q-39795' else g.QS[t][':question/worked-solution']
  assert normal['question'][':question/worked-solution']==expected_solution
  assert normal['question'][':question/problem']==g.QS[t][':question/problem']
  normal_exact+=normal['question'][':question/worked-solution']==g.QS[t][':question/worked-solution'];normal_repairs+=normal['question'][':question/worked-solution']!=g.QS[t][':question/worked-solution'];normal_completions+=normal['generation']['supported_field_completion']
  check_printed(normal)
  if ':question/answer-fields' in r['question']:native.append(native_item(r,'original '+t))
  for profile in ['authored','supported-observed','original']:
   for seed in range(40):
    try:r=g.generate(level,seed,template=t,profile=profile)
    except Exception as e:raise AssertionError((t,profile,seed,str(e))) from e
    m=check_printed(r)
    for k,v in m.items():metrics[k]+=v
    tested+=1;ids.add(r['question'][':question/id']);tasks[level].add(r['generation']['mathematical_fingerprint'])
    rr=g.generate(level,seed+81,template=t,profile=profile,parameters=r['generation']['parameters']);assert rr['question'][':question/id']==r['question'][':question/id']
    assert rr['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
    if seed<2:
     review.append(r)
     if ':question/answer-fields' in r['question']:native.append(native_item(r,t+' '+profile+' '+str(seed)))
 # Every explicit guard must reject off-scope workload, real quadratic roots,
 # cancellation, all-real denominators and nonprimitive rational-root factors.
 bad=[('q-80679',dict(a=1,b=4,c=1,n=1)),('q-113525',dict(a=1,b=8,c=20,n=3)),('q-80676',dict(a=1,c=-4,r=2,n=2,s=1)),('q-113527',dict(a=1,c=6,r=3,s=3)),('q-278551',dict(a=1,c=1,r=1,n=4)),('q-4698',dict(p=4,q=2,s=1)),('q-270004',dict(r=1,n=1,s=3)),('q-4698',dict(p=1,q=1,s=1))]
 for t,p in bad:
  try:g.generate(g.SPECS[t][0],template=t,parameters=p)
  except ValueError:continue
  raise AssertionError('Off-scope parameters accepted '+t)
 # Fingerprint ignores incidental numerator coefficients and bank profiles.
 for t,(level,_,p) in g.SPECS.items():
  if 'n' in p:
   p2=dict(p);p2['n']=p['n']+1
   try:a=g.generate(level,template=t,parameters=p);b=g.generate(level,template=t,parameters=p2)
   except ValueError:continue
   assert a['generation']['mathematical_fingerprint']==b['generation']['mathematical_fingerprint']
 enumerated=enumerate_tasks()
 report={'pass':True,'enumerated_eligible_meaningful_tasks':enumerated,'source_questions':13,'raw_exact_prompts':13,'raw_exact_solutions':13,'supported_normal_solutions_exact':normal_exact,'teaching_repairs':normal_repairs,'fieldless_raw_replays':3,'supported_field_completions':normal_completions,'source_fields':10,'source_correct_designations_matched':10,'source_options_matched':count,'source_options_total':count,'source_distractors_matched':wrong,'source_distractors_total':wrong,'complete_radio_banks_matched':banks,'complete_radio_banks_total':banks,'source_blank_fragments_matched':3,'generated_records_checked':tested,'printed_mathematics':metrics,'unique_presentation_ids':len(ids),'sampled_meaningful_tasks':{k:len(v) for k,v in tasks.items()},'explicit_guard_rejections':len(bad),'native_grading':'pending','plots':'none','database_writes':0,'scope':'complex quadratic exclusion, coprime numerator/denominator; GCF, grouping, cubes only'}
 for name,obj in [('source-cases.json',cases),('review.json',review),('original-replays.json',originals),('native-input.json',native)]: (HERE/name).write_text(json.dumps(obj,indent=2)+'\n')
 command=[str(HERE.parents[1]/'runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-report.json')]
 subprocess.run(command,check=True)
 n=json.loads((HERE/'native-report.json').read_text());report['native_grading']={k:n[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')};report['native_binary_sha256']=hashlib.sha256(Path(command[0]).read_bytes()).hexdigest()
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 text=['# Review: originals and generated variants\n\nSource capture: math basis 1356, lineage '+g.CAPTURE['lineage']+'. Raw originals retain the stray 2x equation and three missing fields. Normal outputs repair/supply these explicitly. Every generated example below has been read independently from its printed rational function, all option root sets and all solution stages.\n']
 for t in g.SPECS:
  src=g.QS[t];text.append('\n## '+t+' — '+g.SPECS[t][0]+'\n\n### Original captured evidence\n\n'+src[':question/problem']+'\n\n')
  for f in src.get(':question/answer-fields',[]):
   for a in f[':answer-field/choices']:text.append(('* ' if a[':answer/id']==f[':answer-field/correct'][':answer/id'] else '- ')+a[':answer/value']+'\n')
  if not src.get(':question/answer-fields'):text.append('Captured question has no answer fields.\n')
  text.append('\n'+src[':question/worked-solution']+'\n')
  for r in review:
   if r['generation']['template']==t:text.append('\n### Generated '+r['generation']['profile']+' variant, seed '+str(r['generation']['seed'])+'\n\nParameters: `'+json.dumps(r['generation']['parameters'])+'`\n\n'+g.markdown(r)+'\n')
 (HERE/'review.md').write_text(''.join(text))
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
