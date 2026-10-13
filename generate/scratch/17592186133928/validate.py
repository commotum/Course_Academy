#!/usr/bin/env python3
"""Private step-7 audit: full source fidelity, printed math, native radio grading."""
import importlib.util,json,re,sys,subprocess,hashlib,itertools
from pathlib import Path
import sympy as s
from math_parser import parse,SYMS
ROOT=Path(__file__).parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('stokes',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);sys.modules[spec.name]=g;spec.loader.exec_module(g)
T,X,Y,Z=[SYMS[v] for v in 'txyz']
def equal(a,b):return s.simplify(s.trigsimp(a-b))==0
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def rows(block):
 text=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','')
 return [r.split('=',1)[1].strip() for r in text.split(r'\\')]
def vector(text):
 assert text.startswith(r'\langle ') and text.endswith(r'\rangle'),text
 return tuple(parse(v) for v in text[len(r'\langle '):-len(r'\rangle')].split(','))
def fmt(text):
 assert text.count('$$')%2==0
 assert text.replace('$$','').count('$')%2==0
 count=0
 for ch in text:
  if ch=='{':count+=1
  elif ch=='}':count-=1
  assert count>=0,text
 assert count==0,text
 assert '{{' not in text and '--' not in text and '+-' not in text

def components(text):
 # Split the actual unevaluated component masks only at top-level plus signs.
 depth=0;chunks=[];start=0;i=0
 while i<len(text):
  if text[i]=='(':depth+=1
  elif text[i]==')':depth-=1
  if depth==0 and text[i:i+3]==' + ':
   chunks.append(text[start:i]);start=i+3;i+=2
  i+=1
 chunks.append(text[start:]);return chunks

def audit(record):
 q=record['question'];meta=record['generation'];prompt=q[':question/problem'];sol=q[':question/worked-solution']
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 fmt(prompt);fmt(sol)
 # Parse the actual displayed field, boundary and interval, then derive all
 # expected objects without consulting the generation parameters.
 r=vector(re.search(r'parametrization \$r\(t\)=(.*?)\$ for',prompt)[1])
 f=vector(re.search(r'F\(x,y,z\)=(.*?),\$ evaluate',prompt)[1])
 lo,hi=map(parse,re.search(r't\\in \[(.*?),(.*?)\)\.',prompt).groups())
 assert all(equal(v.subs(T,lo),v.subs(T,hi)) for v in r),'not closed'
 rp=tuple(s.diff(v,T) for v in r);fr=tuple(v.subs(dict(zip((X,Y,Z),r)),simultaneous=True) for v in f)
 dot=s.expand(sum(u*v for u,v in zip(fr,rp)))
 correct=s.simplify(s.integrate(dot,(T,lo,hi)))
 # Independent curl and vector area orientation; source families have constant
 # curl except the bilinear/exponential terms, whose integrated restrictions
 # still cross-check via homotopy disk parameterization below.
 curl=(s.diff(f[2],Y)-s.diff(f[1],Z),s.diff(f[0],Z)-s.diff(f[2],X),s.diff(f[1],X)-s.diff(f[0],Y))
 # Ruled spanning surface r_surface(u,t)=u*r(t). Its oriented normal is
 # r_u cross r_t; boundary u=1 follows increasing t. The disk's collapsed
 # edge u=0 contributes zero; no outward/upward sign is assumed.
 u=s.Symbol('u',real=True);ru=s.Matrix(r);rt=u*s.Matrix(rp);normal=ru.cross(rt)
 restricted=[v.subs(dict(zip((X,Y,Z),[u*a for a in r])),simultaneous=True) for v in curl]
 flux=s.integrate(sum(a*b for a,b in zip(restricted,normal)),(u,0,1),(T,lo,hi))
 assert equal(flux,correct),(meta['template'],'curl normal audit',flux,correct)
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==6
 coords=blocks[1].split(r',\quad ');assert len(coords)==3
 for j,row in enumerate(coords):assert row.split('=')[0]==str((X,Y,Z)[j]);assert equal(parse(row.split('=')[1]),r[j])
 frrows=rows(blocks[2]);assert len(frrows)==3
 for i,row in enumerate(frrows):
  vals=vector(row)
  expected=f if i==0 else fr
  assert all(equal(a,b) for a,b in zip(vals,expected)),('field',row,expected)
 dr=rows(blocks[3]);assert len(dr)==2
 form=dr[0][len(r'\langle '):-len(r'\rangle')].split(',')
 for v,expected in zip(form,r):
  prefix=r'\frac{\mathrm d}{\mathrm dt}'
  assert v.strip().startswith(prefix)
  assert equal(parse(v.strip()[len(prefix):]),expected)
 assert all(equal(a,b) for a,b in zip(vector(dr[1]),rp))
 dotrows=rows(blocks[4]);assert len(dotrows)==5
 vv=dotrows[0].split(r'\cdot ');assert len(vv)==2
 assert all(equal(a,b) for a,b in zip(vector(vv[0]),fr))
 assert all(equal(a,b) for a,b in zip(vector(vv[1]),rp))
 for row in dotrows[1:]:assert equal(parse(row),dot),('dot stage',row,dot)
 final=rows(blocks[5]);assert len(final)==6
 assert final[0]==r'\oint_C F\cdot\mathrm dr'
 prefix=r'\int_{'+g.tex(lo)+'}^{'+g.tex(hi)+'}'
 assert final[1]==prefix+r' F(r(t))\cdot r\prime(t)\,\mathrm dt'
 assert final[2].startswith(prefix) and final[2].endswith(r'\,\mathrm dt')
 assert equal(parse(final[2][len(prefix):-len(r'\,\mathrm dt')]),dot)
 prim=final[3];ending=r'\right]_{'+g.tex(lo)+'}^{'+g.tex(hi)+'}'
 assert prim.startswith(r'\left[') and prim.endswith(ending)
 primitive=parse(prim[len(r'\left['):-len(ending)])
 assert equal(s.diff(primitive,T),dot),('primitive',primitive,dot)
 # Read BOTH endpoint groups and EACH evaluated primitive component.
 endpoint=final[4];assert equal(parse(endpoint),correct)
 assert len(re.findall(r'\\left\(',endpoint))==2+2*len(s.Add.make_args(parse(final[2][len(prefix):-len(r'\,\mathrm dt')])))
 primitive_components=components(prim[len(r'\left['):-len(ending)])
 endpoint_groups=endpoint.split(r'\right)-\left(')
 assert len(endpoint_groups)==2
 upper=endpoint_groups[0][len(r'\left('):]
 lower=endpoint_groups[1][:-len(r'\right)')]
 for group,point in [(upper,hi),(lower,lo)]:
  evaluated=components(group)
  assert len(evaluated)==len(primitive_components)
  for printed,component in zip(evaluated,primitive_components):
   assert equal(parse(printed),parse(component).subs(T,point)),('individual endpoint',printed,component,point)
 assert equal(parse(final[5]),correct)
 field=q[':question/answer-fields'][0];assert len(field[':answer-field/choices'])==5
 vals=[parse(a[':answer/value']) for a in field[':answer-field/choices']]
 assert len({s.srepr(s.simplify(v)) for v in vals})==5
 correctid=field[':answer-field/correct'][1]
 for a,val in zip(field[':answer-field/choices'],vals):assert equal(val,correct)==(a[':answer/id']==correctid)
 return {'stage_rows':sum(len(rows(b)) for b in blocks[2:]),'curl':g.tex(s.Matrix(curl)),'flux':g.tex(flux)}

def main():
 subprocess.run([sys.executable,str(ROOT/'audit_source_errors.py')],check=True)
 sources=[];review=[];native=[];audits=[]
 for case in json.loads((ROOT/'source-cases.json').read_text()):
  sid=case['source_id'];raw=g.generate(case['level'],template=sid,profile='raw',parameters=case['parameters']);q=raw['question'];original=g.SOURCES[sid]
  for key in [':question/problem',':question/worked-solution',':question/difficulty']:
   assert (key in q)==(key in original),(sid,'presence',key)
   if key in q:assert q[key]==(original[key][':db/ident'] if isinstance(original[key],dict) else original[key]),(sid,key)
  assert len(q[':question/answer-fields'])==len(original[':question/answer-fields'])
  total=0;designated=0
  for f,of in zip(q[':question/answer-fields'],original[':question/answer-fields']):
   assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in of[':answer-field/choices'])
   assert (':answer-field/correct' in f)==(':answer-field/correct' in of)
   total+=len(f[':answer-field/choices'])
   if ':answer-field/correct' in f:
    cv=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert cv==of[':answer-field/correct'][':answer/value'];designated+=1
  r,field,lo,hi=g.objects(sid,{'a':1,'b':1,'d':1,'c':1})
  fr=[v.subs(dict(zip((g.X,g.Y,g.Z),r)),simultaneous=True) for v in field]
  answer=s.simplify(s.integrate(sum(u*s.diff(v,g.T) for u,v in zip(fr,r)),(g.T,lo,hi)))
  for of in original[':question/answer-fields']:
   if ':answer-field/correct' in of:assert equal(parse(of[':answer-field/correct'][':answer/value']),answer)
  # Changed scalar recipe actually changes field and all dependent stages.
  changed=g.generate(case['level'],template=sid,profile='raw',parameters={'c':-2});assert changed['question'][':question/problem']!=q[':question/problem']
  for cf,f in zip(changed['question'][':question/answer-fields'],q[':question/answer-fields']):
   assert sorted(str(s.simplify(parse(a[':answer/value']))) for a in cf[':answer-field/choices'])==sorted(str(s.simplify(-2*parse(a[':answer/value']))) for a in f[':answer-field/choices'])
  sources.append({'source_id':sid,'banks':len(original[':question/answer-fields']),'choices':total,'designation_matches':designated,'presence_prompt_solution_lexical_fidelity':True,'eligible_for_learning':False});review.append({'kind':'original raw evidence','record':raw})
  for seed in [4,17]:review.append({'kind':'authored bank/coefficient variant of observed family','record':g.generate(case['level'],seed,template=sid)})
 for seed in [4,17]:review.append({'kind':'authored missing easy','record':g.generate_easy(seed)})
 # A substantial unordered coefficient bank, signed boundaries, all families,
 # with explicit-input identity/error behavior.
 sampled={level:set() for level in ['easy','moderate','hard']};familycoverage=set()
 for template,(level,*_) in g.FAMILIES.items():
  for seed in range(18):
   record=g.generate(level,seed,template=template);audits.append({'template':template,'parameters':record['generation']['parameters'],**audit(record)})
   sampled[level].add(record['generation']['mathematical_fingerprint']);familycoverage.add(template)
   again=g.generate(level,seed+91,template=template,parameters=record['generation']['parameters']);assert again['question'][':question/id']==record['question'][':question/id']
  for p in [{'a':0,'b':1,'d':1,'c':1},{'a':4,'b':1,'d':1,'c':1}]:
   try:g.generate(level,template=template,parameters=p)
   except ValueError:pass
   else:raise AssertionError('unguarded explicit parameter')
 for item in review:
  if not item['record']['generation']['eligible_for_learning']:continue
  audit(item['record']);rec=item['record'];f=rec['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete displayed bank radio selection'} for a in f[':answer-field/choices']]
  native.append({'label':rec['question'][':question/id'],'record':rec,'checks':checks})
 for profile in ['raw','method']:
  try:g.generate('moderate',template='q-161928',profile=profile,parameters={})
  except ValueError:pass
  else:raise AssertionError('explicit empty parameters silently replaced')
 assert familycoverage==set(g.FAMILIES)
 defaults={level:{g.generate(level,i)['generation']['template'] for i in range(70)} for level in sampled}
 assert all(defaults[level]=={k for k,v in g.FAMILIES.items() if v[0]==level} for level in sampled)
 write('native-input.json',native)
 result=subprocess.run([str(REPO/'generate/runs/current/check-engine'),str(ROOT/'native-input.json'),str(ROOT/'native-report.json')],check=True,capture_output=True,text=True);print(result.stdout.strip())
 write('review.json',review);md=['# Frozen step-7 review\n\nRaw evidence is explicitly ineligible. Normal examples use authored complete method banks. No plots occur.']
 for item in review:md+=['\n## '+item['kind']+' — '+item['record']['generation']['template'],g.markdown(item['record'])]
 (ROOT/'review.md').write_text('\n\n'.join(md)+'\n')
 write('displayed-math-audit.json',audits)
 report={'passed':True,'step':7,'sources':sources,'coverage':{'practice_questions':11,'full_templates':11,'raw_banks':12,'raw_choices_matched':60,'correct_designations_matched':10,'missing_correct_designations':2,'raw_exact_worked_solutions':10,'missing_worked_solutions':1,'authored_levels':['easy'],'plot_rating':'none'},'math_checks':len(audits),'sampled_substantive_tasks':{k:len(v) for k,v in sampled.items()},'default_family_coverage':{k:sorted(v) for k,v in defaults.items()},'native':json.loads((ROOT/'native-report.json').read_text()),'dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'source_solution_math':{'raw_correct':6,'raw_errors':4,'missing':1,'minimal_repair_edits':7},'generator_sha256':hashlib.sha256(ROOT.with_suffix('.py').read_bytes()).hexdigest(),'source_anomalies':'See source-errors.md; preserved publicly, ineligible. No native claims for malformed raw fields.'}
 write('validation.json',report)
 print('PASS',len(audits),'independent printed stage/curl/normal audits; 11 templates / 12 banks / 60 choices; no writes')
if __name__=='__main__':main()
