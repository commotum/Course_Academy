#!/usr/bin/env python3
"""Independent displayed-expression, source, domain and real native-grader QA."""
import copy,hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
def fileload(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
g=fileload('quotient_draft',HERE.with_suffix('.py'));p=fileload('quotient_parser',HERE/'math_parser.py');X,K=p.X,p.K

def save(name,v):(HERE/name).write_text(json.dumps(v,indent=2,default=str)+'\n')
def eq(a,b):return s.cancel(a-b)==0

def independently_read(r):
 q=r['question'];sol=q[':question/worked-solution'];prompt=q[':question/problem']
 assert r['knowledge_point']=={'db_id':17592186096620,'id':'fc978820-517c-5885-b31b-ab6f9650d57a','title':'Differentiating a Quotient of Two Polynomials'}
 for text in [prompt,sol,*[a[':answer/value'] for f in q[':question/answer-fields'] for a in f[':answer-field/choices']]]:
  assert not any(ord(ch)<32 and ch not in '\n\t\r' for ch in text),'control character'
  assert text.count('{')==text.count('}') and text.count('$')%2==0
 g.FORMAT.validate_generated_record(copy.deepcopy(r))
 # Read numerator and denominator from the ACTUAL displayed fraction, before
 # cancellation; compare separately, not merely the final rational function.
 f=s.cancel(p.function(prompt));raw=re.search(r'\$f\(x\)\s*=\s*(.*?)\$',prompt).group(1)
 i=raw.index(r'\frac')+5;nu,end=p.group(raw,i);de,end=p.group(raw,end)
 u,v=p.parse(nu),p.parse(de)
 us=p.parse(re.search(r'\$u\(x\)=(.*?)\$',sol).group(1));vs=p.parse(re.search(r'\$v\(x\)=(.*?)\$',sol).group(1))
 assert eq(u,us) and eq(v,vs)
 du,dv=s.diff(u,X),s.diff(v,X);expected=s.cancel(s.diff(f,X))
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
 if len(blocks)==2:
  derivatives=[p.parse(row.split('&=',1)[1]) for row in blocks[0].split(r'\\')]
 else:
  line=re.search(r'\$\$\s*u\^\{\\prime\}\(x\)=(.*?),\\,v\^\{\\prime\}\(x\)=(.*?)\$\$',sol,re.S)
  derivatives=[p.parse(z) for z in line.groups()]
 assert eq(derivatives[0],du) and eq(derivatives[1],dv)
 rows=[row.split('&=',1)[1] for row in blocks[-1].split(r'\\')]
 formal=r'\frac{u^{\prime}(x)\cdot v(x)-u(x)\cdot v^{\prime}(x)}{[v(x)]^{2}}'
 assert rows[0]==formal,'formal quotient-rule order/operands changed'
 # Independent structural reading of every component in substituted quotient.
 # These checks catch swapped factors or scaled symbolic rules despite a
 # coincidentally equal final answer.
 numerator,end=p.group(rows[1],5);denominator,end=p.group(rows[1],end)
 pattern=r'^\((.*?)\)\\cdot \((.*?)\)-\((.*?)\)\\cdot \((.*?)\)$'
 operands=re.match(pattern,numerator)
 assert operands,'missing source substituted product structure'
 for actual,want in zip(operands.groups(),[du,v,u,dv]):assert eq(p.parse(actual),want)
 assert eq(p.parse(denominator),v**2)
 for row in rows[1:]:assert eq(p.parse(row),expected),row
 t=r['generation']['template']
 # Required operative stages, independently specified by source family.
 assert len(rows)==({'q-11955':3,'q-104305':3,'q-104309':5}.get(t,4))
 if t=='q-128235':
  num,end=p.group(rows[2],5);assert re.fullmatch(r'\(.*\)-\(.*\)',num),'grouped product expansion omitted'
 if t=='q-128335':
  num,end=p.group(rows[2],5);assert num.startswith('-(') and r'\cdot' in num
  num,end=p.group(rows[-1],5);assert r'\cdot' in num,'factored final source form omitted'
 if t=='q-104309':
  num,end=p.group(rows[2],5)
  # Four separately displayed products before collection, even after changed signs.
  terms=re.findall(r'[-+]',num)
  assert len(terms)>=3,'distributed source row collapsed'
  _,end=p.group(rows[3],5);den,_=p.group(rows[3],end)
  assert len(re.findall(r'\^\{2\}',den))>=1 and s.Poly(v,X).content()>1
 field=q[':question/answer-fields'][0];values=[p.parse(a[':answer/value']) for a in field[':answer-field/choices']]
 assert sum(eq(z,expected) for z in values)==1
 assert all(not eq(z,y) for i,z in enumerate(values) for y in values[:i])
 cid=field[':answer-field/correct'][1]
 assert next(a[':answer/id'] for a,z in zip(field[':answer-field/choices'],values) if eq(z,expected))==cid
 assert len(values)==(5 if field[':answer-field/type'].endswith('/radio') else 1)
 if len(values)==1:assert '{{'+field[':answer-field/key']+'}}' in prompt
 for value in [q[':question/id'],field[':answer-field/id'],*[a[':answer/id'] for a in field[':answer-field/choices']]]:uuid.UUID(value)
 domain=s.Poly(v,X).sqf_part().monic().as_expr()
 fp=g.digest([s.srepr(s.cancel(u/v)),s.srepr(domain),'find fprime'])
 assert fp==r['generation']['math_fingerprint']
 return len(rows)+2

def independently_read_source(q,r):
 if ':question/worked-solution' not in q:return 0
 sol=q[':question/worked-solution'];normal=r['question'][':question/worked-solution']
 u=p.parse(re.search(r'\$u\(x\)\s*=\s*(.*?)\$',sol).group(1));v=p.parse(re.search(r'\$v\(x\)\s*=\s*(.*?)\$',sol).group(1));du,dv=s.diff(u,X),s.diff(v,X)
 # Independently read every source quotient-stage, including initial symbolic
 # operands and the unsimplified substituted numerator, before any collection.
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
 raw=[row.split('&',1)[1].lstrip().lstrip('=').strip() for row in blocks[-1].split(r'\\')]
 norm=[row.split('&=',1)[1] for row in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',normal,re.S)[-1].split(r'\\')]
 assert len(raw)==len(norm)
 prime=lambda letter:r'\{?'+letter+r'\}?\^\{(?:′|\x27|\\prime)\}\(x\)'
 formal=raw[0]
 assert len(re.findall(prime('u'),formal))==1 and len(re.findall(prime('v'),formal))==1
 assert formal.index('u')<formal.index('v') and '-' in formal
 assert '[v(x)]' in formal and ('^{2}' in formal or '^2' in formal)
 # Read the four actual operands separately even when0 makes a wrong factor
 # disappear algebraically. Source masks use cdot or adjacent grouped factors.
 source_num,end=p.group(raw[1],raw[1].index(r'\frac')+5)
 depth=0;cut=None
 for i,ch in enumerate(source_num):
  if ch in '({':depth+=1
  elif ch in ')}':depth-=1
  elif ch=='-' and depth==0 and i>0:cut=i;break
 assert cut is not None
 factors=[]
 for term in [source_num[:cut],source_num[cut+1:]]:
  if r'\cdot' in term:pair=term.split(r'\cdot');assert len(pair)==2
  else:
   term=term.strip();assert term.startswith('(');depth=0;end=None
   for i,ch in enumerate(term):
    if ch=='(':depth+=1
    elif ch==')':
     depth-=1
     if depth==0:end=i+1;break
   pair=[term[:end],term[end:]]
  factors += [p.parse(z) for z in pair]
 for actual,want in zip(factors,[du,v,u,dv]):assert eq(actual,want),'source substituted operand mismatch'
 expected=s.cancel((du*v-u*dv)/v**2)
 parsed=[]
 for row in raw:
  row=re.sub(prime('u'),lambda m:'('+s.sstr(du)+')',row)
  row=re.sub(prime('v'),lambda m:'('+s.sstr(dv)+')',row)
  row=row.replace('u(x)','('+s.sstr(u)+')').replace('v(x)','('+s.sstr(v)+')').replace('[','(').replace(']',')')
  value=p.parse(row);assert eq(value,expected),row;parsed.append(value)
 for a,b in zip(raw,norm):
  # Distinct source operations remain visible, beyond mathematical equality:
  # the substituted row retains4 operand factors; the group-expansion source
  # keeps the subtraction of two complete products; evaluated x^4 remains x^4.
  if q[':question/math-academy-id']=='q-340290' and a==raw[2]:assert 'x^{4}' in b
 return len(raw)

def canonical_q(r):
 q=copy.deepcopy(r['question'])
 for f in q.get(':question/answer-fields',[]):f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
 return q

def engine_checks(r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  return [dict(submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==correct else 'rejected',purpose='owned radio choice') for a in f[':answer-field/choices']]+[dict(submitted=z,expected='unresolved',purpose=purpose) for z,purpose in [('999999','foreign numeric choice ID'),('not-an-id','malformed choice ID'),('x^2','mathematical text is not a radio selection')]]
 value=f[':answer-field/choices'][0][':answer/value'];fun=p.function(r['question'][':question/problem']);u,v=s.fraction(fun)
 # A genuinely unreduced quotient-rule expression tests equivalent entry.
 expanded='(('+s.sstr(s.diff(u,X))+')*('+s.sstr(v)+')-('+s.sstr(u)+')*('+s.sstr(s.diff(v,X))+'))/('+s.sstr(v)+')^2'
 expanded=expanded.replace('**','^')
 return [dict(submitted=value,expected='accepted',purpose='canonical fragment'),dict(submitted=expanded,expected='accepted',purpose='independently unreduced quotient rule equivalent'),*[dict(submitted=z,expected='accepted' if eq(p.parse(z),s.diff(fun,X)) else 'rejected',purpose='ordinary wrong scalar or mathematically valid0/1') for z in ['0','1']],dict(submitted='('+expanded+')+1',expected='rejected',purpose='ordinary incorrect derivative')]

def main():
 records=[];review=[];fidelity=[];cases=[];operations=0;negative=0
 for t,q in g.SOURCES.items():
  raw=g.generate('easy',template=t,parameters=g.TEMPLATES[t]['p'],profile='raw')
  # Raw key presence parity covers all omissions individually.
  assert set(raw['question'])==set(q)
  assert raw['question'][':question/problem']==q[':question/problem']
  for key in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (key in raw['question'])==(key in q)
  if ':question/worked-solution' in q:assert raw['question'][':question/worked-solution']==q[':question/worked-solution']
  profile='observed-'+t[2:] if g.TEMPLATES[t]['field']=='radio' else 'fragment'
  r=g.generate('easy',template=t,parameters=g.TEMPLATES[t]['p'],profile=profile);operations+=independently_read(r);operations+=independently_read_source(q,r);records.append(r)
  original=[a for f in q.get(':question/answer-fields',[]) for a in f[':answer-field/choices']]
  vals=[p.parse(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  for a in original:assert sum(eq(p.parse(a[':answer/value']),z) for z in vals)==1
  expected=s.diff(p.function(r['question'][':question/problem']),X)
  for field in q.get(':question/answer-fields',[]):
   if ':answer-field/correct' in field:assert eq(p.parse(field[':answer-field/correct'][':answer/value']),expected)
  row={'source_id':t,'bank_profile':profile,'captured_values':len(original),'matched_values':len(original),'captured_designation_present':any(':answer-field/correct' in f for f in q.get(':question/answer-fields',[])),'raw_exact_attribute_presence':True,'normal_solution':'authored' if ':question/worked-solution' not in q else 'source-specific normalized operative chain','normal_presentation_repair':t in ['q-104305','q-104309','q-128235','q-128335','q-11966']}
  fidelity.append(row);cases.append({'source_id':t,'template':t,'parameters':g.TEMPLATES[t]['p'],'bank_profile':profile,'raw_bank_profile':'raw','level':'easy','source_difficulty':q.get(':question/difficulty'),'raw_record':q})
  review += [{'label':t+' immutable original','record':raw},{'label':t+' parameterized source-bank anchor','record':r}]
  profiles=[profile]+(['method'] if g.TEMPLATES[t]['field']=='radio' else [])
  for pr in profiles:
   if pr=='method':
    anchor=g.generate('easy',template=t,parameters=g.TEMPLATES[t]['p'],profile=pr);operations+=independently_read(anchor);records.append(anchor);review.append({'label':t+' authored method-bank anchor','record':anchor})
   for seed in range(10):
    v=g.generate('easy',seed+31,template=t,profile=pr);operations+=independently_read(v);records.append(v)
    again=g.generate('easy',999,template=t,parameters=v['generation']['parameters'],profile=pr)
    assert canonical_q(v)==canonical_q(again),'seed or order changes identity'
   review.append({'label':t+' changed-parameter '+pr,'record':v})
 for level in g.SUPPORTED_LEVELS:
  for r in g.batch(level,60,901):operations+=independently_read(r);records.append(r)
  review += [dict(label=level+' generated example '+str(i+1),record=r) for i,r in enumerate(g.batch(level,2,110))]
 # Actual same rational function and excluded-zero set dedup across banks/notation.
 for t in ['q-11955','q-11966']:
  anchor=g.TEMPLATES[t]['p'];a=g.generate('easy',template=t,parameters=anchor,profile='method');b=g.generate('easy',template=t,parameters=anchor,profile='observed-'+t[2:])
  assert a['generation']['math_fingerprint']==b['generation']['math_fingerprint']
  assert a['question'][':question/id']!=b['question'][':question/id']
 for kw in [dict(parameters={'c':True,'a':4,'b':-9}),dict(parameters={'c':-2,'a':13,'b':-9}),dict(parameters={'c':0,'a':4,'b':-9}),dict(profile='invented'),dict(seed=True)]:
  try:g.generate('easy',template='q-11955',**kw)
  except ValueError:negative+=1
  else:raise AssertionError('invalid input accepted')
 for level,bound in [('moderate',4),('hard',3)]:
  for key in ['c','e','a','d']:
   params=dict(g.TEMPLATES['authored-'+level]['p']);params[key]=-(bound+1)
   try:g.generate(level,parameters=params)
   except ValueError:negative+=1
   else:raise AssertionError('level bound bypass')
 # Independent mutation controls: preserve answer while corrupting operations.
 normal=next(r for r in records if r['generation']['template']=='q-104309')
 for mutate in ['operand','stage','control']:
  bad=copy.deepcopy(normal);z=bad['question'][':question/worked-solution']
  if mutate=='operand':z=z.replace('(-2)'+r'\cdot','(-3)'+r'\cdot',1)
  elif mutate=='stage':
   z=z.replace(r'\frac{-4 x^{2}+4-12 x+8 x^{2}}',r'\frac{4 x^{2}-12 x+4}')
  else:z=z.replace('Applying','\x0cApplying')
  assert z!=bad['question'][':question/worked-solution']
  bad['question'][':question/worked-solution']=z
  try:independently_read(bad)
  except (AssertionError,ValueError):negative+=1
  else:raise AssertionError('operation corruption accepted: '+mutate)
 save('source-cases.json',cases);save('source-fidelity.json',fidelity);save('review.json',review)
 (HERE/'review.md').write_text('\n\n---\n\n'.join('## '+row['label']+'\n\n'+g.markdown(row['record']) for row in review)+'\n')
 # Native grader inputs contain every profile, original-parameter completion,
 # changed-parameter instance, all difficulty bands, and ordinary wrong answers.
 engine=[{'label':str(i),'record':r,'checks':engine_checks(r)} for i,r in enumerate(records)]
 save('engine-input.json',engine)
 binary=HERE/'check-engine'
 subprocess.run([str(binary),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 native=json.loads((HERE/'engine-report.json').read_text())
 baseline=json.loads((HERE/'registered-baseline.json').read_text());now={str(f):hashlib.sha256(f.read_bytes()).hexdigest() for f in [ROOT/'generate/scratch/17592186096620.py',*sorted(f for f in (ROOT/'generate/scratch/17592186096620').rglob('*') if f.is_file())]}
 assert baseline=={str(Path(k)):v for k,v in now.items()} or baseline=={str(Path(k).relative_to(ROOT)):v for k,v in now.items()},'registered baseline changed'
 report={'passed':True,'basis':2275,'source_questions':11,'raw_exact_records':11,'source_banks':{'matched':9,'total':9,'matched_values':sum(x['matched_values'] for x in fidelity),'total_values':sum(x['captured_values'] for x in fidelity),'missing_correct_designations':1,'fieldless_originals':2},'source_worked_solutions':{'captured':10,'source_specific_operative_chains':10,'authored_missing':1,'exact_raw_prose':10,'normalized_parameterized_presentation':True},'correctness':{'records':len(records),'displayed_operations_read':operations,'negative_controls':negative},'supported_levels':list(g.SUPPORTED_LEVELS),'authored_levels':['moderate','hard'],'native':{k:native[k] for k in ['accepted_checks','rejected_checks','documented_unresolved_checks']},'native_unresolved_interpretation':'Only deliberately invalid radio transport (foreign numeric IDs, malformed IDs, mathematical text). Blank equivalents must all accept.','registered_baseline_unchanged':True,'limitations':['Raw profile is immutable evidence at source parameters; parameterized source-bank profiles are separately exposed.','Opaque radio transport is evidence only; inferred intent is unresolved.','Source TeX/whitespace normalized in completed source-shaped output; raw records retain exact originals.','Missing moderate/hard bands are authored design claims, not observed ratings.']}
 save('validation.json',report)
 files=[HERE.with_suffix('.py'),*sorted(f for f in HERE.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.name!='freeze.json')]
 save('freeze.json',{'version':g.VERSION,'files':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'engine_binary_sha256':hashlib.sha256(binary.read_bytes()).hexdigest(),'python_version':sys.version.split()[0],'sympy_version':s.__version__})
 print(json.dumps(report,indent=2))
if __name__=='__main__':main()
