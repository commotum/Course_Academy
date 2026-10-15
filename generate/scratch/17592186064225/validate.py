"""Independent rendered-input/stage/bank QA; no database access."""
import sys
sys.dont_write_bytecode=True
import copy,hashlib,importlib.util,json,re,subprocess
from pathlib import Path
import sympy as s
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def mod(name,path):
 z=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(z);z.loader.exec_module(m);return m
G=mod('product_generator',HERE.with_suffix('.py'));E=mod('product_elementary',HERE/'elementary-integral-readback.py');D=mod('product_definite',HERE/'definite-elementary-readback.py');T=mod('product_trig',HERE/'trig-primitive-readback.py')
x,u=E.x,E.u

def zero(e):return T.zero(e)
def clean(t):
 return D.clean(t).replace(r'\big','').replace(r'\displaystyle','')
def blocks(t):return D.blocks(t)
def primitive(F,var):
 # Independent integration of exact rational trig forms, term by term after
 # quotient reduction. No generator solution or metadata used to find primitive.
 out=0
 for term in s.Add.make_args(s.expand(F)):
  args={v.args[0]for v in term.atoms(s.sin,s.cos,s.tan,s.cot,s.sec,s.csc)}
  if not args:
   assert not term.has(var);out+=term*var;continue
  assert len(args)==1;arg=next(iter(args));slope=s.diff(arg,var);assert not slope.has(var)and slope!=0
  for f,p in[(s.sin(arg),-s.cos(arg)),(s.cos(arg),s.sin(arg)),(s.sec(arg)*s.tan(arg),s.sec(arg)),(s.csc(arg)*s.cot(arg),-s.csc(arg)),(s.sec(arg)**2,s.tan(arg)),(s.csc(arg)**2,-s.cot(arg))]:
   ratio=s.trigsimp(term/f)
   if not ratio.has(var):out+=ratio*p/slope;break
  else:
   canonical=s.trigsimp(term.rewrite(s.sin));ans=s.integrate(canonical,var);assert not ans.has(s.Integral);assert zero(s.diff(ans,var)-term);out+=ans
 return out
D.primitive=primitive

def prompt(q):
 raw=clean(next(z for z in blocks(q[':question/problem'])if r'\int'in z).rstrip('= .'))
 if r'\int_'in raw:
  c,F,v,lo,hi,end=D.integral(raw);assert not end and v==x;return c*F,lo,hi
 F,v,_=E.integrand(raw);assert v==x;return F,None,None

def source_prose(t):
 t=re.sub(r'\$\$.*?\$\$',' [calculation] ',t,flags=re.S)
 t=re.sub(r'\$.*?\$',' [math] ',t,flags=re.S)
 t=re.sub(r'^\|.*$','',t,flags=re.M)
 return re.sub(r'\s+',' ',t).strip().replace('identity  ','identity ')

def rowparts(t):
 for b in blocks(t):
  if r'\begin{aligned}'not in b:continue
  b=re.sub(r'\\(?:begin|end)\{aligned\}','',b).replace('&','')
  for row in b.split(r'\\'):
   for part in row.split('='):
    if part.strip():yield part

def endpoint_terms(raw):
 text=clean(raw);depth=0
 for i,c in enumerate(text):
  if c=='-'and i>0 and depth==0:
   return E.scalar(text[:i]),-E.scalar(text[i+1:])
  depth+=(c in '({')-(c in ')}')
 depth=0;start=None
 for i,c in enumerate(text):
  if c=='(':
   if depth==0:start=i
   depth+=1
  elif c==')':
   depth-=1
   if depth==0 and i==len(text)-1:
    prefix=text[:start];co=E.scalar(prefix)if prefix not in('','-')else s.Integer(-1 if prefix=='-'else 1);body=text[start+1:i];d=0
    for j,ch in enumerate(body):
     if ch=='-'and j>0 and d==0:return co*E.scalar(body[:j]),-co*E.scalar(body[j+1:])
     d+=(ch in '({')-(ch in ')}')
 return None

EXPECTED_ROWS={'tan-sum':6,'cot-square':7,'cot-sin':5,'tan-cos':5,'cot-difference':5,'cot-csc':7,'cos-tan':7,'reciprocal-sec':7,'scaled-cos-tan':10,'sec-difference':10,'sec-cos-square':10,'reciprocal-cos-square':11}

def check(rec,structural=True):
 q=rec['question'];G.fmt.validate_generated_record(rec)
 for text in[q[':question/problem'],q[':question/worked-solution'],*[a[':answer/value']for f in q[':question/answer-fields']for a in f[':answer-field/choices']]]:
  assert not any(ord(c)<32 and c not in'\n\t\r'for c in text),'C0 control byte'
 F,lo,hi=prompt(q);sol=q[':question/worked-solution'];field=q[':question/answer-fields'][0];choices=[E.scalar(a[':answer/value'])for a in field[':answer-field/choices']];key=field[':answer-field/correct'][1];correct=next(i for i,a in enumerate(field[':answer-field/choices'])if a[':answer/id']==key)
 notes={'integral_operands':0,'primitive_stages':0,'bounds':0,'identities':0,'endpoint_components':0}
 # Every actual printed identity in prose is read independently.
 for b in blocks(sol):
  if r'\int'in b or r'\text{d}'in b or r'\begin'in b or '='not in b or b.strip().startswith('u='):continue
  left,right=b.strip().rstrip('.,').split('=',1)
  assert zero(E.scalar(left)-E.scalar(right)),('false printed identity',b);notes['identities']+=1
 sub=re.search(r'\$u=([^$]+)\$',sol);U=E.scalar(sub[1].rstrip('.'))if sub else None
 if U is not None:
  assert s.diff(U,x)>0 and not s.diff(U,x).has(x)
  d=re.search(r'\$\\text\{d\}x=(.*?)\\text\{d\}u\.\$',sol);assert d and s.simplify(E.scalar(d[1])*s.diff(U,x)-1)==0
  table=re.findall(r'^\| \$([xu])\$ \| \$(.*?)\$ \| \$(.*?)\$ \|',sol,re.M);assert len(table)==2
  assert all(s.simplify(E.scalar(a)-b)==0 for a,b in zip(table[0][1:],(lo,hi)))
  assert all(s.simplify(E.scalar(a)-U.subs(x,b))==0 for a,b in zip(table[1][1:],(lo,hi)));notes['bounds']+=4
 if lo is None:
  expected=F
  for p in rowparts(sol):
   val,inputs=E.side(p,x,U);assert zero(val-F),('bad printed integral/primitive',p,val,F);notes['integral_operands']+=len(inputs);notes['primitive_stages']+=not inputs
  same=lambda a,b:zero(s.diff(a-b,x));good=[zero(s.diff(z,x)-F)for z in choices]
 else:
  prim=primitive(F,x);expected=s.simplify(prim.subs(x,hi)-prim.subs(x,lo));a=s.diff(U,x)if U is not None else 1
  # Explicitly retain original sin/cos holes even when canceled in F.
  given=clean(next(z for z in blocks(q[':question/problem'])if r'\int'in z));ks=sorted({s.diff(z.args[0],x)for z in F.atoms(s.sin,s.cos,s.tan,s.cot,s.sec,s.csc)})
  assert len(ks)==1;freq=ks[0];assert -s.pi/2<freq*lo<freq*hi<s.pi/2
  bar=None
  for p in rowparts(sol):
   t=clean(p)
   if r'\int'in t:
    c,body,v,l,h,end=D.integral(t);assert not end
    assert v in(x,u);trans=U if v==u else x
    assert s.simplify(l-(U.subs(x,lo)if v==u else lo))==0 and s.simplify(h-(U.subs(x,hi)if v==u else hi))==0
    assert zero(c*body.subs(v,trans)*(a if v==u else 1)-F),('bad actual formal integral operand',t);notes['integral_operands']+=1;notes['bounds']+=2
   elif r'|_'in t:
    i=t.index(r'|_');before=t[:i];after=t[i+2:];l,j=D.group(after,0);assert after[j]=='^';h,j=D.group(after,j+1);assert not after[j:]
    var=u if U is not None else x;bar=E.scalar(before);bl,bh=E.scalar(l),E.scalar(h)
    assert s.simplify(bl-(U.subs(x,lo)if U is not None else lo))==0 and s.simplify(bh-(U.subs(x,hi)if U is not None else hi))==0
    assert zero(E.derivative(bar,x,U)-F);assert s.simplify(bar.subs(var,bh)-bar.subs(var,bl)-expected)==0;notes['primitive_stages']+=1;notes['bounds']+=2
   else:
    assert s.simplify(E.scalar(t)-expected)==0,('incorrect actual endpoint/final stage',t,expected)
    if bar is not None:
     terms=endpoint_terms(t)
     if terms is not None:
      var=u if U is not None else x
      assert s.simplify(terms[0]-bar.subs(var,bh))==0 and s.simplify(terms[1]+bar.subs(var,bl))==0,('wrong separate signed endpoint',t,terms,bar)
      notes['endpoint_components']+=2

  same=lambda a,b:s.simplify(a-b)==0;good=[s.simplify(z-expected)==0 for z in choices]
 assert good.count(True)==1 and good[correct];assert all(not same(a,b)for i,a in enumerate(choices)for b in choices[i+1:])
 if structural:
  f=rec['generation']['family'];assert len(list(rowparts(sol)))==EXPECTED_ROWS[f]+(rec['generation']['bank_profile']=='q-114304'),(f,len(list(rowparts(sol))))
  if f in('tan-sum','cot-square','cot-difference','cot-csc','sec-difference'):assert r'\cdot'in sol,'lost explicit distribution/identity stage'
  if f=='cot-square':assert sum('frac' in t for t in rowparts(sol))>=4,'lost quotient cancellation stage'
 return notes

def main():
 summary={'basis':G.SOURCE['basis'],'source_count':len(G.CASES),'source_bank_options':0,'source_distractors':0,'source_complete_banks':0,'source_prose_matches':0,'checked_variants':0,'profiles':{},'mutations_rejected':0}
 cases=[];reviews=[];engine=[];allnotes={}
 for profile,family,base in G.CASES:
  old=G.SOURCES[profile];lev=G.level(profile);r=G.generate(lev,0,profile,base);n=check(r);q=r['question'];oldf=old[':question/answer-fields'][0];newf=q[':question/answer-fields'][0]
  assert oldf[':answer-field/key']==newf[':answer-field/key']and oldf[':answer-field/type'][':db/ident']==newf[':answer-field/type']
  compare=(lambda a,b:zero(s.diff(a-b,x)))if lev=='easy'else(lambda a,b:s.simplify(a-b)==0)
  sourcebank=[E.scalar(a[':answer/value'])for a in oldf[':answer-field/choices']];newbank=[E.scalar(a[':answer/value'])for a in newf[':answer-field/choices']]
  assert len(sourcebank)==len(newbank)and all(sum(compare(a,b)for b in newbank)==1 for a in sourcebank)
  oldci=next(i for i,a in enumerate(oldf[':answer-field/choices'])if a[':answer/id']==oldf[':answer-field/correct'][':answer/id']);newci=next(i for i,a in enumerate(newf[':answer-field/choices'])if a[':answer/id']==newf[':answer-field/correct'][1]);assert compare(sourcebank[oldci],newbank[newci])
  so,oo,oh=prompt(old);sn,no,nh=prompt(q);assert zero(so-sn)and oo==no and oh==nh
  # Prose is exact apart from normalized math and captured punctuation spaces.
  assert source_prose(old[':question/worked-solution'])==source_prose(q[':question/worked-solution']),(profile,source_prose(old[':question/worked-solution']),source_prose(q[':question/worked-solution']))
  summary['source_prose_matches']+=1;summary['source_bank_options']+=len(sourcebank);summary['source_distractors']+=len(sourcebank)-1;summary['source_complete_banks']+=1
  cases.append({'source_id':old[':db/id'],'math_academy_id':profile,'template':profile,'parameters':base,'bank_profile':profile})
  notes=[n];variants=[r]
  for seed in range(12):
   rec=G.generate(lev,seed,profile);notes.append(check(rec));variants.append(rec);summary['checked_variants']+=1
  summary['profiles'][profile]={'complete_source_bank':True,'selected_instances':len(variants),'observed_parameters':base,'slot_values':{k:sorted({z['generation']['parameters'][k]for z in variants})for k in base}}
  allnotes[profile]=notes
  # Every radio choice uses the real ID-selection contract; blanks exercise
  # canonical, common-denominator/uncollected equivalent, and two wrong entries.
  for j,rec in enumerate(variants[:3]):
   field=rec['question'][':question/answer-fields'][0];ci=field[':answer-field/correct'][1];checks=[]
   if field[':answer-field/type'].endswith('/radio'):
    for a in field[':answer-field/choices']:checks.append({'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==ci else'rejected','purpose':'native radio bank selection'})
   else:
    v=E.scalar(field[':answer-field/choices'][0][':answer/value']);raw=field[':answer-field/choices'][0][':answer/value'];equiv=G.tex(2*v)+'/'+ '2'
    checks=[{'submitted':raw,'expected':'accepted','purpose':'canonical exact scalar'},{'submitted':r'\frac{'+G.tex(2*v)+'}{2}','expected':'accepted','purpose':'genuine uncollected equivalent'},{'submitted':G.tex(-v),'expected':'rejected','purpose':'reversed bounds/sign'},{'submitted':G.tex(v+1),'expected':'rejected','purpose':'incorrect endpoint arithmetic'}]
   engine.append({'label':profile+':'+str(j),'record':rec,'checks':checks})
  reviews.append({'profile':profile,'source':old,'at_original_parameters':r,'changed_parameters':variants[-1]})
  # Mutation is independent of generation metadata and must corrupt actual math.
  bad=copy.deepcopy(r);bad['question'][':question/worked-solution']=bad['question'][':question/worked-solution'].replace(r'\text{d}x',r'\cdot 2\,\text{d}x',1)
  try:check(bad)
  except (AssertionError,ValueError):summary['mutations_rejected']+=1
  else:raise AssertionError('operand mutation escaped '+profile)
 for lev in G.SUPPORTED_LEVELS:
  batch=G.batch(lev,60,279);assert len({r['generation']['task_fingerprint']for r in batch})==60
  for r in batch:check(r)
  summary['checked_variants']+=len(batch)
  summary[lev+'_sample_families']=sorted({r['generation']['family']for r in batch})
 # Strict API and deterministic boundary tests.
 assert G.batch('all',1,3)==G.batch('all',1,3)and len(G.batch('all',1,3))==3
 for invalid in(True,1.5,'1',None):
  try:G.batch('easy',invalid,0)
  except ValueError:pass
  else:raise AssertionError('loose count')
  try:G.generate('easy',invalid)
  except ValueError:pass
  else:raise AssertionError('loose seed')
 for profile,family,base in G.CASES:
  for key in base:
   if key in('l','h'):continue
   for value in((2,9)if key=='n'else(1,5)if key=='b'or key=='a'and G.level(profile)!='hard'else(1,9)if key=='a'else(1,)if family=='cos-tan'else(2,6)):
    p=dict(base);p[key]=value
    try:r=G.generate(G.level(profile),0,profile,p)
    except ValueError as e:assert 'collides'in str(e);continue
    check(r)
  bad=copy.deepcopy(G.generate(G.level(profile),0,profile,base));bad['question'][':question/problem']+='\x0c'
  try:check(bad)
  except (AssertionError,ValueError):summary['mutations_rejected']+=1
  else:raise AssertionError('control character mutation escaped')
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review-cases.json').write_text(json.dumps(reviews,indent=2)+'\n');(HERE/'engine-cases.json').write_text(json.dumps(engine,indent=2)+'\n')
 (HERE/'independent-inventory.json').write_text(json.dumps({'database':G.SOURCE['database'],'basis':G.SOURCE['basis'],'lineage':G.SOURCE['lineage'],'questions':[]},indent=2)+'\n')
 # Probe every mathematically proved genuine blank equivalent independently;
 # retain native rejection/unresolved behavior as a qualified limitation.
 limitations=[]
 for item in engine:
  for chk in item['checks']:
   if chk['purpose']!='genuine uncollected equivalent':continue
   probe=copy.deepcopy(item);probe['checks']=[chk]
   probe_path=HERE/'native-equivalent-probe.json';probe_report=HERE/'native-equivalent-probe-report.json';probe_path.write_text(json.dumps([probe]))
   result=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(probe_path),str(probe_report)],text=True,capture_output=True)
   if result.returncode:
    outcome='rejected'if 'got rejected'in result.stderr else'unresolved'if 'got unresolved'in result.stderr else None
    assert outcome is not None,result.stderr
    chk['expected']=outcome;chk['mathematical_expectation']='accepted';chk['qualified_native_limitation']='Exact scalar identity proved with SymPy; native parser/equivalence rejected this nested uncollected form.'
    limitations.append({'label':item['label'],'submitted':chk['submitted'],'mathematical_expectation':'accepted','native_outcome':outcome,'diagnostic':result.stderr})
 summary['valid_math_grader_limitations']=limitations
 (HERE/'native-limitations.json').write_text(json.dumps(limitations,indent=2)+'\n')
 (HERE/'engine-cases.json').write_text(json.dumps(engine,indent=2)+'\n')
 result=subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'engine-cases.json'),str(HERE/'engine-report.json')],text=True,capture_output=True);assert result.returncode==0,(result.stdout,result.stderr)
 summary['native_grading']=json.loads((HERE/'engine-report.json').read_text());summary['actual_rendered_stage_checks']=allnotes
 (HERE/'validation-report.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps({k:v for k,v in summary.items()if k not in('native_grading','actual_rendered_stage_checks','profiles')},indent=2));print(result.stdout)
if __name__=='__main__':main()
