"""Fail-fast printed mathematics, fidelity, whole-bank, identity and native QA."""
import copy, hashlib, importlib.util, itertools, json, re, subprocess, sys
from pathlib import Path
import sympy as s
import math_parser as mp
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
T,X,Y=mp.T,mp.X,mp.Y

def eq(a,b):return s.simplify(s.trigsimp(a-b))==0

def balanced(text):
 assert text.count('$$')%2==0 and text.replace('$$','').count('$')%2==0
 depth=0
 for ch in text:
  depth+=(ch=='{')-(ch=='}');assert depth>=0
 assert depth==0 and '+-' not in text and '--' not in text

def group(text,start,opening='{',closing='}'):
 assert text[start]==opening
 depth=1;end=start+1
 while depth:
  depth+=(text[end]==opening)-(text[end]==closing);end+=1
 return text[start+1:end-1],end

def prompt(q):
 text=q[':question/problem']
 f=re.search(r'f\(x,y\)=(.*?)\$',text).group(1)
 curve=re.search(r'r\(t\)=⟨(.*?)⟩',text).group(1).split(r',\,')
 limits=re.search(r't\\in \[(.*?),(.*?)\]',text)
 return mp.expr(f),*(mp.expr(e) for e in curve),mp.expr(limits[1]),mp.expr(limits[2])

def source_prompt(q):
 text=q[':question/problem']
 fm=re.search(r'f\(x,\s*y\)\s*=\s*(.*?)\$',text)
 if fm:field=fm[1]
 else:
  field=text.split('_{C}',1)[1].split(r'\,\text{d}s',1)[0] if '_{C}' in text else text.split('_(C)',1)[1].split('ds',1)[0]
 curve=re.search(r'r\(t\)\s*=\s*(.*?)\$',text)[1].rstrip(',')
 if '⟨' in curve:
  x,y=curve.split('⟨',1)[1].split('⟩',1)[0].replace(r'\,','').split(',')
  x,y=mp.expr(x),mp.expr(y)
 else:x,y=mp.vector(curve)
 interval=re.search(r't(?:\\in| ∈)\s*\[(.*?),(.*?)\]',text)
 if interval:lo,hi=mp.expr(interval[1]),mp.expr(interval[2])
 else:
  limits=re.search(r'0\\le t\\le (.*?)\.\$',text.replace(' ',''))
  if limits is None:limits=re.search(r'0\\let\\le(.*?)\$',text.replace(' ',''))
  assert limits,text
  lo,hi=s.Integer(0),mp.expr(limits[1])
 return mp.expr(field),x,y,lo,hi

def printed_value(q,raw=False):
 F,x,y,lo,hi=(source_prompt(q) if raw else prompt(q))
 square=s.factor(s.trigsimp(s.diff(x,T)**2+s.diff(y,T)**2));v=s.sqrt(square)
 if float(lo)>=0:v=v.xreplace({s.Abs(T):T,s.Abs(T+1):T+1})
 I=s.trigsimp(s.expand(F.subs({X:x,Y:y}))*v)
 return s.simplify(s.integrate(I,(T,lo,hi)))

def rows(block):return [r.strip().rstrip('.') for r in block.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')]
def rhs(row):return row.split('&=',1)[1]

def integral_expr(raw):
 norm=mp.normalize(raw);i=norm.index(r'\int_');coef=mp.expr(norm[:i]) if i else 1
 lo,j=group(norm,i+len(r'\int_'));assert norm[j]=='^';hi,j=group(norm,j+1)
 assert norm.endswith('dt')
 return coef*mp.expr(norm[j:-2]),mp.expr(lo),mp.expr(hi)

def primitive(raw):
 norm=mp.normalize(raw);a=norm.index('[');b=norm.index(']');coef=mp.expr(norm[:a]) if a else 1
 body=mp.expr(norm[a+1:b]);assert norm[b+1]=='_'
 lo,pos=group(norm,b+2);assert norm[pos]=='^';hi,pos=group(norm,pos+1);assert pos==len(norm)
 return coef*body,mp.expr(lo),mp.expr(hi)

def additive_components(text):
 text=mp.normalize(text);out=[];depth=0;begin=0
 for i,ch in enumerate(text):
  depth+=(ch in '({')-(ch in ')}')
  if ch=='+' and depth==0:out.append(text[begin:i]);begin=i+1
 out.append(text[begin:]);return [mp.expr(v) for v in out]

def endpoint_sides(raw):
 raw=mp.normalize(raw);left,pos=group(raw,0,'(',')');assert raw[pos:pos+2]=='-(';right,end=group(raw,pos+1,'(',')');assert end==len(raw)
 return additive_components(left),additive_components(right)

def derivative_args(raw):
 out=[]
 for m in re.finditer(re.escape(r'\frac{\text{d}}{\text{d}t}'),raw):
  value,end=group(raw,m.end(),'(',')');out.append(mp.expr(value))
 return out

def mathcheck(r):
 q=r['question'];F,x,y,lo,hi=(source_prompt(q) if r['generation']['bank_profile'].startswith('completed_') else prompt(q));du,dv=s.diff(x,T),s.diff(y,T);square=s.factor(s.trigsimp(du*du+dv*dv))
 # Derive nonnegative speed from printed geometry and the actual interval.
 v=s.sqrt(square)
 for expr in (s.Abs(T),s.Abs(T+1)):
  if float(lo)>=0:v=v.xreplace({expr:(T if expr==s.Abs(T) else T+1)})
 if v.has(s.Abs):raise AssertionError('Unsupported sign domain')
 sub=s.trigsimp(s.expand(F.subs({X:x,Y:y})));I=s.trigsimp(sub*v)
 fingerprint={'curve':[s.srepr(s.expand_trig(x)),s.srepr(s.expand_trig(y))],'field':s.srepr(s.cancel(s.expand(F))),'integrand':s.srepr(s.trigsimp(s.expand(I))),'bounds':[str(lo),str(hi)],'assessed_response':'evaluate_scalar_ds'}
 assert g.digest(fingerprint)==r['generation']['mathematical_fingerprint']
 P=s.integrate(I,T);value=s.simplify(P.subs(T,hi)-P.subs(T,lo))
 bs=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S);assert len(bs)==4 and bs[0]==g.FORMULA
 dr=rows(bs[1]);assert derivative_args(rhs(dr[1]))==[x,y]
 marker=next(i for i,row in enumerate(dr) if row.startswith(r'\|r'))
 for row in dr[2:marker]:
  a,b=mp.vector(rhs(row));assert eq(a,du) and eq(b,dv),('vector',row)
 for row in dr[marker+1:]:
  e=rhs(row)
  if '|' in e:
   e=re.sub(r'\|([^|]+)\|',lambda m:r'\sqrt{('+m[1]+')^2}',e)
  vrow=mp.expr(e);assert eq(vrow*vrow,square),('speed row',row)
  assert all(float(vrow.subs(T,z))>=0 for z in (lo,(lo+hi)/2,hi))
 sr=rows(bs[2]);assert all(eq(mp.expr(rhs(row)),sub) for row in sr),('substitution',sr)
 ir=rows(bs[3]);lhs=ir[0].split('&=',1)[0];assert eq(mp.expr(lhs.removeprefix(r'\int_C ').removesuffix(r'\,\text{d}s')),F)
 symbolic=rhs(ir[0]);assert r'f(r(t))\|r^{\prime}(t)\|' in symbolic
 _,al,ah=integral_expr(symbolic.replace(r'f(r(t))\|r^{\prime}(t)\|',g.G(sub)+g.G(v)));assert eq(al,lo) and eq(ah,hi)
 for row in ir[1:-3]:
  text=rhs(row)
  if r'\int_' in text:
   e,a,b=integral_expr(text);assert eq(e,I) and eq(a,lo) and eq(b,hi),('integrand',row)
  else:
   e,a,b=primitive(text);assert eq(s.diff(e,T),I) and eq(a,lo) and eq(b,hi),('primitive',row)
 # Read and compare every individual component before and after evaluation.
 components=additive_components(mp.normalize(rhs(ir[-4])).split('[',1)[1].split(']',1)[0])
 assert eq(s.diff(sum(components),T),I)
 for row in ir[-3:-1]:
  sides=endpoint_sides(rhs(row));assert len(sides[0])==len(components)==len(sides[1])
  for z,parts in zip((hi,lo),sides):
   for expr,part in zip(components,parts):assert eq(expr.subs(T,z),part),('individual endpoint',row,z)
 assert eq(mp.expr(rhs(ir[-1])),value)
 family=r['generation']['template']
 # Distinct source operative structures cannot be replaced by equal CAS rows.
 if family.startswith('circle'):
  assert r'(\sin^2t+\cos^2t)' in bs[1]
 if family=='circle_cos':assert r'(2\cos^2t-1)' in bs[2] and r'\frac{1}{2}\sin 2t' in bs[3]
 if family=='circle_sin':assert r'\frac{1-\cos 2t}{2}' in bs[3] and r't-\frac{\sin 2t}{2}' in bs[3]
 if family=='cubic':assert 't^6-' in bs[2] and r'|t|' in bs[1] and r'\frac{t^8}{8}' in bs[3]
 if family in ('fractional','mixed_fractional'):assert '(t^2+2t+1)' in bs[1] and 't^{3/2}(t+1)' in bs[3]
 if family=='involute':assert '-\\sin t+\\sin t+t\\cos t' in bs[1] and '2t\\sin t\\cos t' in bs[2]
 f=q[':question/answer-fields'][0];vals=[]
 for a in f[':answer-field/choices']:
  e=mp.expr(a[':answer/value']);vals.append(e)
  assert eq(e,value)==(a[':answer/id']==f[':answer-field/correct'][1])
 assert not any(eq(a,b) for i,a in enumerate(vals) for b in vals[:i])
 return value

def contract(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'} and r['knowledge_point']['db_id']==g.KP_ID
 q=r['question'];f=q[':question/answer-fields'][0]
 correct=f.get(':answer-field/correct');correct_text=None if correct is None else next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct[1])
 identity=g.digest({'version':g.VERSION,'prompt':q[':question/problem'],'solution':q.get(':question/worked-solution'),'bank':sorted(a[':answer/value'] for a in f[':answer-field/choices']),'difficulty':q.get(':question/difficulty'),'field_type':':answer-field.type/radio','correct':correct_text})
 assert identity==r['generation']['content_fingerprint'] and g.uid(identity)==q[':question/id']
 assert f[':answer-field/type']==':answer-field.type/radio' and len(f[':answer-field/choices'])==5
 assert len({a[':answer/id'] for a in f[':answer-field/choices']})==5
 for a in f[':answer-field/choices']:assert a[':answer/type']==':answer.type/math' and '$' not in a[':answer/value']
 for text in (q[':question/problem'],q.get(':question/worked-solution','')):balanced(text)
 assert r['generation']['eligible_for_learning']!=r['generation']['evidence_only']

def source_expected(f,c=1):
 # Independently transcribed original mathematics, checked against source strings
 # in the bank-map evidence. Missing source keys are not counted as designations.
 base={'sum':2*s.sqrt(2),'reciprocal':-s.sqrt(2),'circle_cos':32,'circle_sin':s.pi-2,'cubic':s.Rational(25,2),'fractional':s.Rational(96,35),'involute':54*s.pi**2*(1+2*s.pi**2)}
 return c*base[f]

def main():
 replays=[];variants=[];checks=[];fidelity=[];bankmap=[];cases=[];tested=[]
 for f,sid in g.FAMILY_SOURCE.items():
  level=g.TEMPLATES[f];old=g.SOURCES[sid];r=g.generate(level,template=f,parameters={'c':1},profile='raw_'+f);contract(r)
  q=r['question'];of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem'] and q.get(':question/worked-solution')==old.get(':question/worked-solution')
  for key in (':question/worked-solution',':question/difficulty',':question/answer-fields'):assert (key in q)==(key in old)
  assert (':answer-field/correct' in of)==(':answer-field/correct' in nf)
  assert {a[':answer/value'] for a in of[':answer-field/choices']}=={a[':answer/value'] for a in nf[':answer-field/choices']}
  assert eq(printed_value(q,raw=True),source_expected(f))
  vals=[mp.expr(a[':answer/value']) for a in of[':answer-field/choices']];assert sum(eq(a,source_expected(f)) for a in vals)==1
  assert g.generate(level,901,template=f,parameters={'c':1},profile='raw_'+f)['question'][':question/id']==q[':question/id']
  if ':answer-field/correct' in of:
   designated=next(a[':answer/value'] for a in nf[':answer-field/choices'] if a[':answer/id']==nf[':answer-field/correct'][1]);assert designated==of[':answer-field/correct'][':answer/value'];assert eq(mp.expr(designated),source_expected(f))
  for c in (-3,2):
   changed=g.generate(level,template=f,profile='raw_'+f,parameters={'c':c});contract(changed)
   assert eq(printed_value(changed['question'],raw=True),c*source_expected(f))
   assert {s.srepr(mp.expr(a[':answer/value'])) for a in changed['question'][':question/answer-fields'][0][':answer-field/choices']}=={s.srepr(c*v) for v in vals}
  entry={'source_id':sid,'template':f,'parameters':{'c':1},'bank_profile':'raw_'+f,'difficulty':level,'source_difficulty':old.get(':question/difficulty',{}).get(':db/ident'),'api_level_provenance':'observed' if ':question/difficulty' in old else 'authored wrapper assignment; raw question retains omission','evidence_only':True,'eligible_for_learning':False};cases.append(entry);replays.append(r)
  fidelity.append({'source_id':sid,'prompt_exact':True,'solution_presence_exact':True,'solution_raw_exact':':question/worked-solution' in old,'difficulty_presence_exact':True,'bank_values_exact':5,'designation_exact':':answer-field/correct' in of})
  bankmap.append({'source_id':sid,'profile':'raw_'+f,'scale_parameter':'c times entire source scalar field','choices':[{'original':a[':answer/value'],'parameterized_pattern':'c*('+str(mp.expr(a[':answer/value']))+')','source_correct':a.get(':answer/id')==of.get(':answer-field/correct',{}).get(':answer/id'),'interpretation':'opaque historical scalar pattern; error intent unresolved; evidence-only'} for a in of[':answer-field/choices']]})
  variants.append(g.generate(level,31,template=f,profile='raw_'+f,parameters={'c':2}))
  if f in ('fractional','involute'):
   completed=g.generate(level,template=f,profile='completed_'+f);cf=completed['question'][':question/answer-fields'][0];cv=next(a[':answer/value'] for a in cf[':answer-field/choices'] if a[':answer/id']==cf[':answer-field/correct'][1]);assert eq(mp.expr(cv),source_expected(f));mathcheck(completed);variants.append(completed)
 # Canonical tasks deduplicate observed and normal presentation/bank aliases.
 for fam in ('sum','reciprocal','circle_cos','circle_sin','cubic','fractional'):
  p={k:str(v) for k,v in g.source_parameters(fam,1).items()}
  normal=g.generate(g.TEMPLATES[fam],template=fam,parameters=p)
  observed=g.generate(g.TEMPLATES[fam],template=fam,profile='raw_'+fam)
  mathcheck(normal)
  assert normal['generation']['mathematical_fingerprint']==observed['generation']['mathematical_fingerprint']
  assert normal['question'][':question/id']!=observed['question'][':question/id']
 # Confirm observed source errors against actual decoded rows, not serialization.
 src=g.SOURCES['q-76434'][':question/worked-solution']
 bad=re.search(r'f\(r\(t\)\) & =(.*?)=',src)[1]
 assert not eq(mp.expr(bad),-s.Rational(1,4))
 cubic=g.SOURCES['q-76447'][':question/worked-solution']
 badlhs=re.search(r'\\begin\{aligned\}\{\\int \}_\{C\}(.*?)\\,\\text\{d\}s',cubic)[1]
 assert not eq(mp.expr(badlhs),X**3-2*Y**3)
 assert r'100[\frac{{1}^{8}}{8}+\frac{{0}^{8}}{8}]' in cubic
 for family,level in g.TEMPLATES.items():
  for seed in range(8):
   r=g.generate(level,seed,template=family);contract(r);mathcheck(r);tested.append(r)
   if seed<2:variants.append(r)
  p=tested[-1]['generation']['parameters'];assert g.generate(level,901,template=family,parameters=p)['question'][':question/id']==tested[-1]['question'][':question/id']
 # Real structural-regression check: replace half-angle operation with equal CAS
 # integrand; row count and mathematics are unchanged, structure must fail.
 mutant=copy.deepcopy(next(r for r in tested if r['generation']['template']=='circle_sin'));mutant['question'][':question/worked-solution']=mutant['question'][':question/worked-solution'].replace(r'\frac{1-\cos 2t}{2}',r'\sin^2t')
 try:mathcheck(mutant)
 except AssertionError:pass
 else:raise AssertionError('Operative structure mutation passed')
 for level in ('easy','moderate','hard'):
  assert {g.generate(level,z)['generation']['template'] for z in range(40)}=={f for f,l in g.TEMPLATES.items() if l==level}
 invalid=[('easy','sum',{'a':5,'b':1,'c':1,'lower':0,'upper':1}),('moderate','cubic',{'a':8,'b':6,'c':1,'k':2,'lower':0,'upper':1}),('moderate','circle_cos',{'R':4,'c':1,'orientation':1,'lower':0,'upper':'pi/3'}),('hard','involute',{'A':3,'c':1,'d':0,'lower':0,'upper':1}),('hard','mixed_fractional',{'s':1,'c':1,'d':0,'lower':0,'upper':1})]
 for level,f,p in invalid:
  try:g.generate(level,template=f,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit workload accepted')
 for r in replays+variants:
  f=r['question'][':question/answer-fields'][0]
  if ':answer-field/correct' not in f:continue
  correct=f[':answer-field/correct'][1]
  checks.append({'label':r['generation']['bank_profile']+':'+r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'owned radio choice; full scalar equivalence independently checked'} for a in f[':answer-field/choices']]})
 (HERE/'native-input.json').write_text(json.dumps(checks,indent=2));engine=HERE.parents[1]/'runs/current/check-engine';subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 for name,data in [('source-cases',cases),('bank-map',bankmap),('review',replays+variants)]: (HERE/(name+'.json')).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
 review=['# Scalar ds evaluation review','Raw evidence replays preserve original omissions and teaching errors. Completed profiles infer missing keys and author solutions. Normal method profiles are learner-eligible.']
 for r in replays+variants:
  label='ORIGINAL PARAMETERIZED REPLAY' if r in replays else 'GENERATED / '+r['generation']['difficulty_provenance']
  review += ['## '+label+' '+r['generation']['template']+' / '+r['generation']['bank_profile'],g.markdown(r)]
 (HERE/'review.md').write_text('\n\n'.join(review)+'\n')
 report={'status':'pass; retained source errors and omissions documented separately','source':g.SOURCE,'source_questions':7,'complete_source_banks_exact':7,'source_answer_values_exact':35,'source_designations_exact':5,'source_designations_absent':2,'raw_native_ungradable_missing_key_records':2,'source_solutions_raw_exact':5,'source_solutions_absent':2,'missing_keys_independently_inferred':2,'finite_domain_variety':'variety.json','raw_known_math_errors':{'q-167609':'derivative labeled r rather than r prime (also in q-76434)','q-76434':'1/[t-(4-t)] is not 1/[(t-4)-t]','q-76447':'integral lhs drops coefficient2; endpoint subtraction printed plus; strict t>0 includes t=0 endpoint'},'normal_math_records_tested':len(tested),'structural_mutation_rejected':1,'default_family_coverage':'all eight templates covered','source_fidelity':fidelity,'explicit_invalid_inputs_rejected':len(invalid),'native_report':'native-report.json','native_scope':'all owned radio choices; no blank source fields or invented blank layouts; raw missing-key originals cannot be graded and are explicitly evidence-only; completed fixtures are separate','plots':'none: no plot in any assigned prompt, bank, or solution; sibling/tutorial diagrams are not assessment assets','dependencies':{'python':sys.version.split()[0],'sympy':s.__version__},'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'database_operations':0,'frozen_after_step':7}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
