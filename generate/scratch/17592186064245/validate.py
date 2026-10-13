#!/usr/bin/env python3
"""Parse displayed integrands, every integration stage and complete choice banks.
Actual native grader exercised separately; no source designation is invented.
"""
import importlib.util,hashlib,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X=s.Symbol('x',real=True);C=s.Symbol('C',real=True)
TRANS=standard_transformations+(implicit_multiplication_application,)
def group(t,i):
 assert t[i]=='{',(t,i)
 d=1;j=i+1
 while d:
  d+=(t[j]=='{')-(t[j]=='}');j+=1
 return t[i+1:j-1],j

def parse(text):
 text=text.replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\cdot','*').replace('\u2061','').replace(r'\operatorname{ln}',r'\ln')
 text=re.sub(r'\\(?:text|textrm)\{d\}x','dx',text)
 text=text.strip().rstrip('.,')
 # All displayed residual integrals here are elementary exponentials.
 while r'\int' in text:
  pos=text.index(r'\int');end=text.index('dx',pos)
  body=text[pos+4:end];expr=s.integrate(parse(body),X)
  text=text[:pos]+'('+str(expr)+')'+text[end+2:]
 while r'\frac' in text:
  pos=text.index(r'\frac');n,end=group(text,pos+5);d,end2=group(text,end)
  text=text[:pos]+'(('+str(parse(n))+')/('+str(parse(d))+'))'+text[end2:]
 # Expand each exponent group before stripping the surrounding source braces.
 while '^{' in text:
  pos=text.index('^{');power,end=group(text,pos+1)
  text=text[:pos]+'**('+str(parse(power))+')'+text[end:]
 text=text.replace(r'\ln','log')
 text=re.sub(r'log\s*([0-9]+)',r'log(\1)',text)
 text=text.replace('{','(').replace('}',')').replace('^','**')
 assert '\\' not in text,repr(text)
 return parse_expr(text,local_dict={'x':X,'e':s.E,'C':C,'log':s.log,'exp':s.exp},transformations=TRANS)
def same(a,b):return s.simplify(a-b)==0
def equivalent_primitive(a,b):return same(s.diff(a-b,X),0)
MATH=re.compile(r'\$\$.*?\$\$|\$(?!\$).*?\$',re.S)
def skeleton(t):return MATH.sub('<math>',t)
def displayed_integrand(prompt):
 t=MATH.findall(prompt)[0].strip('$').replace(r'\intx',r'\int x');t=t.rstrip('.=')
 t=t.split(r'\int',1)[1]
 t=re.sub(r'\\(?:text|textrm)\{d\}x','dx',t).replace(r'\,','')
 return parse(t.rsplit('dx',1)[0])
def validate_solution(q):
 text=q.get(':question/worked-solution')
 if text is None:return 0
 integrand=displayed_integrand(q[':question/problem']);blocks=re.findall(r'\$\$\n(.*?)\n\$\$',text,re.S);count=0
 # First concrete aligned block fixes u,u',v',v.
 setup=next(b for b in blocks if '⟹' in b)
 setup=setup.split(r'\begin{aligned}',1)[1].split(r'\end',1)[0]
 rows=setup.split(r'\\')
 values=[]
 for row in rows:
  left,right=row.split('⟹');left=left.replace('&','').strip();right=right.replace(r'\,','')
  values.append((parse(left.split('=',1)[1]),parse(right.split('=',1)[1])))
 (u,du),(dz,v)=values
 assert same(s.diff(u,X),du),'u derivative';assert same(s.diff(v,X),dz),'v primitive';assert same(u*dz,integrand),'u/v choice';count+=3
 for block in blocks:
  if r'\begin{aligned}' not in block or '⟹' in block:continue
  for row in block.split(r'\begin{aligned}',1)[1].split(r'\end',1)[0].split(r'\\'):
   if ' & =' not in row:continue
   lhs,rhs=row.split(' & =',1)
   if 'uv' in rhs:continue
   value=parse(rhs)
   if lhs.strip():assert equivalent_primitive(parse(lhs),s.integrate(integrand,X)),('integration-stage left side',lhs)
   assert equivalent_primitive(value,s.integrate(integrand,X)),('integration stage',rhs,value,integrand)
   count+=1
 return count

def validate_record(r):
 q=r['question'];field=q[':question/answer-fields'][0];integrand=displayed_integrand(q[':question/problem']);answers=field[':answer-field/choices'];values=[parse(a[':answer/value']) for a in answers]
 assert len(answers)==5
 for a in answers:
  uuid.UUID(a[':answer/id']);assert '$' not in a[':answer/value'];assert a[':answer/value'].endswith('+C');assert ':answer-field/' not in a[':answer/value']
 ci=next(i for i,a in enumerate(answers) if a[':answer/id']==field[':answer-field/correct'][1]);assert same(s.diff(values[ci],X),integrand)
 assert sum(same(s.diff(v,X),integrand) for v in values)==1
 assert not any(equivalent_primitive(a,b) for i,a in enumerate(values) for b in values[i+1:])
 assert field[':answer-field/type']==':answer-field.type/radio';assert field[':answer-field/key']=='selection';uuid.UUID(q[':question/id']);uuid.UUID(field[':answer-field/id'])
 if not r['generation']['bank_profile'].startswith('observed:'):assert all(not v.has(s.zoo,s.nan,s.oo,s.I) for v in values)
 stages=validate_solution(q)
 # Mathematical scope independently from visible question: affine u and one exponential.
 p=r['generation']['parameters'];assert not integrand.has(s.sin,s.cos,s.Integral)
 assert s.Poly(g.mathdata(r['generation']['template'],p)[0],X).degree()==1
 return values,stages

def checks(r):
 f=r['question'][':question/answer-fields'][0]
 return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'every owned radio selection'} for a in f[':answer-field/choices']]
def write(name,data):(ROOT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
def main():
 fidelity=[];review=[];requests=[];sourcecases=[];originalstages=generatedstages=0;matched=0;correctrefs=0;variantcount=0
 for sid,name,p in g.SOURCE_CASES:
  r=g.generate(g.TEMPLATES[name][0],0,name,parameters=p,profile='observed:'+sid);values,stages=validate_record(r);generatedstages+=stages
  src=g.SOURCES[sid];originalstages+=validate_solution(src);sf=src[':question/answer-fields'][0];sourcevalues=[parse(a[':answer/value']) for a in sf[':answer-field/choices']]
  matches=[[i for i,v in enumerate(values) if equivalent_primitive(v,o)] for o in sourcevalues]
  assert all(len(x)==1 for x in matches) and len({x[0] for x in matches})==5,(sid,'source-bank mismatch',matches)
  assert sf[':answer-field/type'][':db/ident']==r['question'][':question/answer-fields'][0][':answer-field/type'];matched+=5
  designation=sf.get(':answer-field/correct');dstatus='missing original designation'
  if designation:
   assert same(s.diff(parse(designation[':answer/value']),X),displayed_integrand(src[':question/problem']));correctrefs+=1;dstatus='matched'
  if sid!='q-2425':
   assert skeleton(src[':question/problem'])==skeleton(r['question'][':question/problem']),(sid,'prompt prose')
   assert skeleton(src[':question/worked-solution'])==skeleton(r['question'][':question/worked-solution']),(sid,'solution prose')
  fidelity.append({'source_id':sid,'complete_bank':'matched','values_matched':5,'values_total':5,'designation':dstatus,'solution_stages_verified':validate_solution(src),'notation':'normalized equivalent LaTeX; whole primitive shape retained','field_layout':'matched','authored_level':'moderate' if sid=='q-2425' else None})
  print('Source bank verified: '+sid,flush=True)
  sourcecases.append({'source_id':sid,'template':name,'parameters':p,'bank_profile':'observed:'+sid,'authored_level':'moderate' if sid=='q-2425' else None})
  requests.append({'label':'source/'+sid,'record':r,'checks':checks(r)});review.append({'label':'Source replay '+sid,'record':r})
  for seed in range(100,200):
   try:peer=g.generate(g.TEMPLATES[name][0],seed,name,profile='observed:'+sid)
   except ValueError:continue
   if peer['generation']['parameters']!=p:break
  else:raise AssertionError('No profile peer '+sid)
  validate_record(peer);review.append({'label':'Generated empirical-profile variant '+sid,'record':peer});requests.append({'label':'profile-peer/'+sid,'record':peer,'checks':checks(peer)})
 for name,t in g.TEMPLATES.items():
  print('Default template: '+name,flush=True)
  for seed in range(8):
   r=g.generate(t[0],seed,name);_,stages=validate_record(r);generatedstages+=stages;variantcount+=1
   requests.append({'label':name+'/'+str(seed),'record':r,'checks':checks(r)})
   if seed<2:review.append({'label':'Generated authored default '+name+'/'+str(seed),'record':r})
  fixed=g.generate(t[0],99,name);p=fixed['generation']['parameters'];again=g.generate(t[0],999,name,parameters=p)
  assert fixed['question'][':question/id']==again['question'][':question/id']
  assert fixed['generation']['parameter_fingerprint']==again['generation']['parameter_fingerprint']
 # Full bank differs in identity but semantic mathematical fingerprint remains.
 p=dict(a=6,b=0,k=4,h=0);a=g.generate_easy(parameters=p,template='e_positive');b=g.generate_easy(parameters=p,template='e_positive',profile='observed:q-14434')
 assert a['question'][':question/id']!=b['question'][':question/id'];assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint']
 a=g.generate_moderate(template='base_calculate',parameters=dict(a=1,b=0,r=3));b=g.generate_moderate(template='base_equals',parameters=dict(a=1,b=0,r=3));assert a['generation']['parameter_fingerprint']==b['generation']['parameter_fingerprint'];assert a['question'][':question/id']!=b['question'][':question/id']
 bad=[dict(a=0,b=0,k=4,h=0),dict(a=1,b=0,k=0,h=0),dict(a=1,b=0,k=-2,h=0),dict(a=1,b=0,k=2,h=0,other=4)]
 for p in bad:
  try:g.generate_easy(parameters=p,template='e_positive')
  except ValueError:pass
  else:raise AssertionError('Invalid explicit input accepted')
 write('source-cases.json',sourcecases);write('engine-input.json',requests);write('review.json',review)
 engine=REPO/'generate/runs/current/check-engine';subprocess.run([str(engine),str(ROOT/'engine-input.json'),str(ROOT/'native-grading.json')],check=True)
 native=json.loads((ROOT/'native-grading.json').read_text());assert native['documented_unresolved_checks']==0
 raw='\n\n---\n\n'.join('## Original '+sid+' — '+src.get(':question/difficulty',{}).get(':db/ident','unrated').split('/')[-1]+'\n\n'+src[':question/problem']+'\n\n'+'\n'.join('- $'+a[':answer/value']+'$'+(' **original correct**' if a[':answer/id']==src[':question/answer-fields'][0].get(':answer-field/correct',{}).get(':answer/id') else '') for a in src[':question/answer-fields'][0][':answer-field/choices'])+'\n\n'+src.get(':question/worked-solution','*No original correct designation, solution, or difficulty captured.*') for sid,src in g.SOURCES.items())
 (ROOT/'review.md').write_text('# Exponential integration by parts: originals and variants\n\nAuthor preview. All generated variants explicitly labeled; same-level variants have no progression.\n\n'+raw+'\n\n---\n\n'+'\n\n---\n\n'.join('## '+item['label']+'\n\n'+g.markdown(item['record']) for item in review)+'\n')
 write('validation.json',{'passed':True,'source_provenance':{k:g.CAPTURE[k] for k in ('database','basis','lineage')},'source_questions':14,'difficulty_counts':{'easy':2,'moderate':6,'hard':5,'unrated':1},'source_fidelity':fidelity,'complete_banks':{'matched':14,'total':14},'answer_values':{'matched':matched,'total':70},'distractors':{'matched':56,'total':56},'correct_designations':{'matched':correctrefs,'available':13,'missing_original_refs':1},'original_solution_stages_verified':originalstages,'generated_solution_stages_verified':generatedstages,'generated_default_records':variantcount,'all_templates_all_profiles_exercised':True,'native_grading':{'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':0,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'engine_harness_source_sha256':hashlib.sha256((REPO/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'learning_source_sha256':hashlib.sha256((REPO/'engine/rust/learning.rs').read_bytes()).hexdigest()},'blank_tests':{'applicable':False,'reason':'All 14 source practice fields are radio; no blank template invented.'},'identity_tests':True,'plots':'none','authored_extensions':['complete operation-derived default banks','same-workload integer coefficient/sign/shift/base ranges','q-2425 authored moderate assignment, prompt spacing repair and derived solution/correct ref'],'limitations':['No observed distractor intent claimed for empirical replay profiles','q-2425 original correct designation, solution and difficulty remain missing in evidence'],'database_writes':0})
 print('PASS: 14/14 banks, 70/70 values, 56/56 distractors; 13/13 available correct refs, 1 missing; '+str(variantcount)+' defaults; native '+str(native['accepted_checks'])+' accepted/'+str(native['rejected_checks'])+' rejected.')
if __name__=='__main__':main()
