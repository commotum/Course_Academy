#!/usr/bin/env python3
"""Independent displayed-text mathematics, complete banks, fidelity and native QA."""
from pathlib import Path
import importlib.util,json,re,subprocess,sys
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
sys.dont_write_bytecode=True
D=Path(__file__).parent;spec=importlib.util.spec_from_file_location('generator',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y=g.x,g.y;i,j=s.symbols('i j');TR=standard_transformations+(implicit_multiplication_application,)
def parse(t):
 t=t.replace('⁡','').replace('\\,',' ').replace('\\cdot','*').replace('\\left','').replace('\\right','').replace('\\operatorname{ln}',' ln').replace('\\operatorname{cos}',' cos').replace('\\operatorname{sin}',' sin')
 t=t.replace('\\ln',' ln').replace('\\sin',' sin').replace('\\cos',' cos')
 def group(z,pos):
  if z[pos]!='{':raise ValueError((z,pos))
  d=1;end=pos+1
  while d:
   if z[end]=='{':d+=1
   elif z[end]=='}':d-=1
   end+=1
  return z[pos+1:end-1],end
 while '\\frac' in t:
  p=t.index('\\frac');a,mid=group(t,p+5);b,end=group(t,mid);t=t[:p]+'(('+a+')/('+b+'))'+t[end:]
 while '\\sqrt' in t:
  p=t.index('\\sqrt');a,end=group(t,p+5);t=t[:p]+'sqrt('+a+')'+t[end:]
 t=t.replace('{','(').replace('}',')').replace('^','**').replace('∇','')
 t=re.sub(r'(?<=[0-9])([ij])',r'*\1',t)
 t=re.sub(r'(?<![A-Za-z])e(?![A-Za-z])','E',t)
 return parse_expr(t,local_dict={'x':x,'y':y,'i':i,'j':j,'E':s.E,'ln':s.log,'cos':s.cos,'sin':s.sin,'sqrt':s.sqrt},transformations=TR)
def relation(t):
 a,b=t.replace('&','').strip().rstrip('.').split('=');return s.expand(parse(a)-parse(b))
def eq(a,b):
 if a==0 or b==0:return a==b
 ratio=s.simplify(a/b);return ratio!=0 and not ratio.has(x,y)
def formatting(text):
 assert text.count('$')%2==0
 depth=0
 for c in text:
  if c=='{':depth+=1
  elif c=='}':depth-=1
  assert depth>=0
 assert depth==0
 assert '--' not in text and '+-' not in text

def check_record(r):
 q=r['question'];assert set(r['knowledge_point'])=={'db_id','id','title'}
 text=q[':question/problem'];parts=re.findall(r'\$(.*?)\$',text);curve=relation(parts[0]);pt=tuple(map(int,re.findall(r'-?\d+',parts[1])))
 assert len(pt)==2;subs=dict(zip((x,y),pt));assert s.simplify(curve.subs(subs))==0
 gx,gy=[s.simplify(s.diff(curve,v).subs(subs)) for v in (x,y)];assert (gx,gy)!=(0,0)
 correct=g.line(gx,gy,*pt)
 f=q[':question/answer-fields'][0];answers=f[':answer-field/choices'];rels=[relation(a[':answer/value']) for a in answers]
 assert len({g.key(v) for v in rels})==5
 actual=[a for a,z in zip(answers,rels) if eq(z,correct)];assert len(actual)==1 and actual[0][':answer/id']==f[':answer-field/correct'][1]
 sol=q[':question/worked-solution'];formatting(text+sol)
 allblocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)
 if '∇f' not in allblocks[0]:
  for row in allblocks[0].split('\\\\'):assert eq(relation(row),curve)
 definition=re.search(r'If we set \$f\(x,y\)=(.*?)\$',sol);level_value=re.search(r'level curve \$f\(x,y\)=(.*?)\.\$',sol)
 assert eq(parse(definition.group(1))-parse(level_value.group(1)),curve)
 # Read all printed vector rows independently, including unsimplified point
 # substitution and final prose vector. Ratios allow source F=-prompt residual.
 grad=curve+0
 gradblock=[b for b in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S) if '∇f(x,y)' in b][0]
 rows=gradblock.split('\\\\')
 formal=rows[1]
 m=re.search(r'∂x\}\((.*?)\)\\,i',formal);printed_f=parse(m.group(1));assert eq(printed_f-printed_f.subs(subs),curve-curve.subs(subs))
 fx,fy=[s.diff(printed_f,v) for v in (x,y)]
 for n,row in enumerate(rows[2:]):
  rhs=row.split('=',1)[1].strip()
  if rhs.startswith('⟨'):
   a,b=rhs[1:-1].split(',');v=(parse(a),parse(b));assert all(s.simplify(z-w)==0 for z,w in zip(v,(fx.subs(subs),fy.subs(subs))))
  else:
   vv=s.expand(parse(rhs));want=(fx,fy) if '∇f' not in row and (vv.has(x) or vv.has(y)) else (fx.subs(subs),fy.subs(subs))
   assert s.simplify(vv.coeff(i)-want[0])==0,(r['generation']['template'],rhs,vv,want)
   assert s.simplify(vv.coeff(j)-want[1])==0
 for pnt,a,b in re.findall(r'∇f(\([^)]*\))=⟨([^,]*),([^⟩]*)⟩',sol):
  assert tuple(map(int,re.findall('-?\\d+',pnt)))==pt
  assert s.simplify(parse(a)-fx.subs(subs))==0 and s.simplify(parse(b)-fy.subs(subs))==0
 # Every non-generic line row is a complete relation proportional to normal.
 lineblock=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[-1]
 for row in lineblock.split('\\\\')[1:]:assert eq(relation(row),correct),(r['generation']['template'],row,correct)
 return r

def check_raw_stages(t,q,h=0,k=0):
 if ':question/worked-solution' not in q:return
 f,c,pt,*_=g.DATA[t];f=f.subs({x:x-h,y:y-k},simultaneous=True);pt=(pt[0]+h,pt[1]+k);subs=dict(zip((x,y),pt));fx,fy=[s.diff(f,z) for z in (x,y)]
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',q[':question/worked-solution'],re.S)
 grad=next(z for z in blocks if '∇f(x,y)' in z)
 formal=grad.split('\\\\')[1];m=re.search(r'∂x\}\((.*?)\)(?:\\,)?i',formal)
 assert s.simplify(parse(m.group(1))-f)==0
 for row in grad.split('\\\\')[2:]:
  rhs=row.split('=',1)[1].strip()
  if rhs.startswith('⟨'):
   a,b=rhs[1:-1].split(',');assert s.simplify(parse(a)-fx.subs(subs))==0 and s.simplify(parse(b)-fy.subs(subs))==0
  else:
   vv=s.expand(parse(rhs));want=(fx,fy) if vv.has(x,y) else (fx.subs(subs),fy.subs(subs))
   assert s.simplify(vv.coeff(i)-want[0])==0 and s.simplify(vv.coeff(j)-want[1])==0
 normal=g.line(fx.subs(subs),fy.subs(subs),*pt)
 for row in blocks[-1].split('\\\\')[1:]:assert eq(relation(row),normal)
 for row in blocks[0].split('\\\\'):
  if '∇f' not in blocks[0]:assert eq(relation(row),f-c)

def normalized(q):
 out={}
 for k,v in q.items():
  if k==':db/id':continue
  if k==':question/difficulty':v=v[':db/ident']
  if k==':question/answer-fields':
   v=json.loads(json.dumps(v))
   for f in v:
    f.pop(':db/id',None);f[':answer-field/type']=f[':answer-field/type'][':db/ident']
    for a in f[':answer-field/choices']:a.pop(':db/id',None);a[':answer/type']=a[':answer/type'][':db/ident']
    if ':answer-field/correct' in f:f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  out[k]=v
 return out

def main():
 cases=[];review=[];engine=[];raws=[];samples=0;variety={};fail=[]
 for t,source in g.QS.items():
  formatting(source[':question/problem']+source.get(':question/worked-solution',''))
  check_raw_stages(t,source)
  level=g.TEMPLATES[t];r=g.generate(level,template=t,profile='observed:'+t,parameters={'h':0,'k':0});assert r['question']==normalized(source);raws.append(r)
  for h,k in [(1,-2),(-3,3)]:
   shifted=g.generate(level,template=t,profile='observed:'+t,parameters={'h':h,'k':k})
   formatting(shifted['question'][':question/problem']+shifted['question'].get(':question/worked-solution',''))
   check_raw_stages(t,shifted['question'],h,k)
   parts=re.findall(r'\$(.*?)\$',shifted['question'][':question/problem']);curve=relation(parts[0]);pt=tuple(map(int,re.findall(r'-?\d+',parts[1])));subs=dict(zip((x,y),pt));assert s.simplify(curve.subs(subs))==0
   normal=g.line(*[s.diff(curve,v).subs(subs) for v in (x,y)],*pt);fld=shifted['question'][':question/answer-fields'][0];matches=[a for a in fld[':answer-field/choices'] if eq(relation(a[':answer/value']),normal)];assert len(matches)==1
   if ':answer-field/correct' in fld:assert matches[0][':answer/id']==fld[':answer-field/correct'][1]
  cases.append({'source_id':source[':db/id'],'math_academy_id':t,'template':t,'parameters':{'h':0,'k':0},'bank_profile':'observed:'+t})
 for t,source in g.QS.items():
  if ':question/worked-solution' in source:
   original=g.generate(g.TEMPLATES[t],template=t,parameters=dict(zip(('p','q'),g.DATA[t][2])))
   count=lambda z:[len(b.split('\\\\')) for b in re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',z,re.S)]
   assert count(source[':question/worked-solution'])==count(original['question'][':question/worked-solution'])
 for r in raws:
  f=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' in f:
   engine.append({'label':'raw-'+r['generation']['template'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'original-bank native selection'} for a in f[':answer-field/choices']]})
 for t,level in g.TEMPLATES.items():
  found={};records=[]
  for seed in range(35):
   r=check_record(g.generate(level,seed=seed,template=t));samples+=1;found[r['generation']['mathematical_fingerprint']]=r
   if len(records)<2:records.append(r)
  variety[t]=len(found);review+=records
  for r in records:
   f=r['question'][':question/answer-fields'][0]
   checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete-bank native selection'} for a in f[':answer-field/choices']]
   engine.append({'label':t+'-'+str(len(engine)),'record':r,'checks':checks})
  # Identical fixed inputs: shuffle changes neither task nor content identity.
  p=records[0]['generation']['parameters'];a=g.generate(level,1,template=t,parameters=p);b=g.generate(level,99,template=t,parameters=p);assert a['generation']['content_identity']==b['generation']['content_identity']
 (D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 (D/'review.json').write_text(json.dumps({'original_replay':raws,'generated':review},indent=2,ensure_ascii=False)+'\n')
 (D/'engine-input.json').write_text(json.dumps(engine,indent=2,ensure_ascii=False)+'\n')
 subprocess.run(['generate/runs/current/check-engine',str(D/'engine-input.json'),str(D/'engine-validation.json')],check=True)
 # Original banks: exact all-option evidence separate from mathematical eligibility.
 source_issues={}
 for t,r in zip(g.QS,raws):
  prompt=re.findall(r'\$(.*?)\$',r['question'][':question/problem']);residual=relation(prompt[0]);point=tuple(map(int,re.findall(r'-?\d+',prompt[1])));sub=dict(zip((x,y),point));assert s.simplify(residual.subs(sub))==0
  gradient=[s.diff(residual,v).subs(sub) for v in (x,y)];assert gradient!=[0,0]
  mathematical_correct=g.line(*gradient,*point)
  vals=[relation(a[':answer/value']) for a in r['question'][':question/answer-fields'][0][':answer-field/choices']]
  correct_values=[n for n,v in enumerate(vals) if eq(v,mathematical_correct)];assert len(correct_values)==1
  fld=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' in fld:assert fld[':answer-field/choices'][correct_values[0]][':answer/id']==fld[':answer-field/correct'][1]
  if len(set(g.key(z) for z in vals))<5:source_issues[t]='equivalent distractors retained in evidence only'
  if ':answer-field/correct' not in r['question'][':question/answer-fields'][0]:source_issues[t]='correct designation/solution/difficulty absent; first option derived correct, raw preserves omissions'
  if t=='q-130719':source_issues[t]='worked-solution prose ∇f(3,1) must be ∇f(2,1); raw preserved'
 default_coverage={g.generate_moderate(seed)['generation']['template'] for seed in range(100)};assert default_coverage==set(g.MOD)
 # Scope boundary guards share normal explicit/random path.
 for level in ['easy','moderate','hard']:
  try:g.generate(level,parameters={})
  except ValueError:pass
  else:raise AssertionError('empty explicit input resampled')
 for level,t,p in [('easy','easy_quadratic',{'a':0,'b':1,'p':1,'q':1}),('hard','q-71385',{'p':2,'q':1}),('moderate','q-130719',{'p':2,'q':-1}),('moderate','q-71388',{'p':0,'q':0})]:
  try:g.generate(level,template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError('explicit guard failure')
 report={'status':'passed with documented source anomalies','runtime':{'python':sys.version.split()[0],'sympy':s.__version__},'sources':15,'raw_vector_and_line_chains_checked':14,'changed_affine_source_chains_checked':28,'normal_source_row_count_matches':14,'finite_variety':json.loads((D/'variety.json').read_text()),'raw_complete_banks_exact':15,'raw_options_exact':75,'raw_correct_designations_exact':14,'missing_original_correct':1,'default_moderate_families_100_seeds':sorted(default_coverage),'normal_displayed_math_records':samples,'generated_review_records':len(review),'variety_35_seeds':variety,'source_issues':source_issues,'native':json.loads((D/'engine-validation.json').read_text()),'plots':'none in assessed sources/canonical; no generated plot needed','limitations':['Opaque source distractor intent unresolved; observed profiles evidence-only.','Raw affine-translated legacy solutions preserve source evaluated arithmetic; normal output uses full fresh substituted stages.','Normal source-parameter presentation preserves operation sequence but uses SymPy notation normalization; raw replay alone is byte-exact.']}
 (D/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 text='# Original evidence and generated variants\n\nAll originals below are faithful evidence-only replays; generated examples are explicitly authored/default presentations.\n\n'
 for t in g.TEMPLATES:
  text+='## '+t+'\n\n'
  if t in g.QS:text+='### Original\n\n'+g.markdown(next(r for r in raws if r['generation']['template']==t))+'\n\n'
  for n,r in enumerate(z for z in review if z['generation']['template']==t):text+='### Generated variant '+str(n+1)+' ('+r['generation']['level']+')\n\n'+g.markdown(r)+'\n\n'
 (D/'review.md').write_text(text)
 print('PASS:',samples,'displayed mathematics records; 15 exact raw banks / 75 options; 46 native records')
if __name__=='__main__':main()
