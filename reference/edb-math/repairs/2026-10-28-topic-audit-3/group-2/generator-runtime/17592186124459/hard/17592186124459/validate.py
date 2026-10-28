#!/usr/bin/env python3
"""Independent prompt/choice/stage/prose, raw fidelity, guard and native QA."""
import copy,hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).parent;REPO=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('generator',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z=S.symbols('x y z',real=True);ivs=S.symbols('IB JB KB')
def group(t,i):
 assert t[i]=='{',(t,i);depth=1;j=i+1
 while depth:depth+=(t[j]=='{')-(t[j]=='}');j+=1
 return t[i+1:j-1],j

def math(t):
 t=t.strip().rstrip('.').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace('⁡','').replace(r'\cdot','*')
 t=re.sub(r'\\text\{[^}]*\}','',t)
 for op in ('ln','sin','cos'):t=t.replace(r'\operatorname{'+op+'}', '\\'+op)
 for cmd in (r'\frac',r'\sqrt'):
  while cmd in t:
   i=t.index(cmd);a,j=group(t,i+len(cmd))
   if cmd==r'\frac':b,j=group(t,j);v='('+str(math(a))+')/('+str(math(b))+')'
   else:v='sqrt('+str(math(a))+')'
   t=t[:i]+v+t[j:]
 t=t.replace(r'\ln',' log ').replace(r'\sin',' sin ').replace(r'\cos',' cos ').replace(r'\pi','pi').replace('^','**').replace('{','(').replace('}',')')
 for a,b in [('i','IB'),('j','JB'),('k','KB')]:t=re.sub((r'(?<![A-Za-z])' if a=='i' else '')+a+r'(?![A-Za-z])','('+b+')',t)
 return parse_expr(t,local_dict={'x':x,'y':y,'z':z,'e':S.E,'pi':S.pi,'sin':S.sin,'cos':S.cos,'log':S.log,'sqrt':S.sqrt,**dict(zip(['IB','JB','KB'],ivs))},transformations=standard_transformations+(implicit_multiplication_application,))
def vector(t):
 t=t.strip().rstrip('.')
 if t.startswith('⟨'):return [math(v)for v in t[1:t.index('⟩')].replace(r'\,','').split(',')]
 e=S.expand(math(t));return[e.coeff(v)for v in ivs[:2]]
def equal(a,b):return S.simplify(a-b)==0
def veq(a,b):return len(a)==len(b)and all(equal(v,w)for v,w in zip(a,b))
def parallel(a,b):
 if all(equal(e,0)for e in a)or all(equal(e,0)for e in b):return False
 j=next(i for i,e in enumerate(b)if not equal(e,0))
 if not all(equal(u*b[j],v*a[j])for u,v in zip(a,b)):return False
 r=S.simplify(a[j]/b[j]);assert r.is_positive is not None,'unresolved parallel sign';return bool(r.is_positive)
def formatting(t):
 assert all(ord(c)>=32 or c in '\n\t'for c in t),'C0'
 assert t.count('$')%2==0,'dollars'
 d=0
 for i,c in enumerate(t):
  if c=='{'and(i==0 or t[i-1]!='\\'):d+=1
  elif c=='}'and(i==0 or t[i-1]!='\\'):d-=1
  assert d>=0,'braces'
 assert d==0,'braces'
 assert '+-'not in t and '--'not in t,'signed operands'
def prompt(r):
 q=r['question'];text=q[':question/problem'];m=re.search(r'[fg]\(x,\s*y(?:,\s*z)?\)\s*=([^$]+)',text);assert m,text
 F=math(m[1]);pm=re.search(r'point \$\(([^)]+)\)',text);assert pm,text
 P=[math(e)for e in pm[1].split(',')];vs=[x,y,z][:len(P)];d=[S.diff(F,v)for v in vs];E=[S.simplify(v.subs(dict(zip(vs,P))))for v in d]
 sign=-1 if 'decrease most rapidly'in text else 1;target=[sign*v for v in E];unit='unit direction'in text
 if unit:N=S.sqrt(sum(e*e for e in E));target=[v/N for v in target]
 return F,vs,P,d,E,target,unit

def formal_args(t):
 out=[]
 for m in re.finditer(r'\\frac\{∂\}\{∂([xyz])\}\(',t):
  i=m.end();start=i;d=1
  while d:d+=(t[i]=='(')-(t[i]==')');i+=1
  out.append((m[1],math(t[start:i-1])))
 return out

def check(r,raw=False):
 assert set(r['knowledge_point'])=={'db_id','id','title'}
 q=r['question'];F,vs,P,d,E,target,unit=prompt(r)
 fld=q[':question/answer-fields'][0];vals=[vector(a[':answer/value'])for a in fld[':answer-field/choices']]
 for text in [q[':question/problem'],q.get(':question/worked-solution','')]+[a[':answer/value']for a in fld[':answer-field/choices']]:formatting(text)
 ids=[a[':answer/id']for a in fld[':answer-field/choices']];assert len(set(ids))==5
 eligibility=[parallel(v,target)and(not unit or equal(sum(e*e for e in v),1))for v in vals]
 assert sum(eligibility)==1,'direction ambiguity'
 if ':answer-field/correct'in fld:assert ids[eligibility.index(True)]==fld[':answer-field/correct'][1]
 for i,v in enumerate(vals):
  assert not all(equal(e,0)for e in v),'zero choice'
  for w in vals[i+1:]:assert not (veq(v,w) if unit else parallel(v,w)),'duplicate requested directions'
 sol=q.get(':question/worked-solution')
 if sol is None:assert raw;return
 blocks=re.findall(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S);assert blocks
 rows=blocks[0].split(r'\\');arguments=formal_args(rows[0]);assert[v for v,e in arguments]==list(map(str,vs));assert all(equal(e,F)for v,e in arguments),'held-partial operands'
 t=r['generation']['template'];derivative_count=2 if t=='log_unit'else 1
 assert len(rows)==(5 if t in ('linear_sin','mixed_sin','log_unit') else 4),'source stage sequence'
 if t in ('linear_sin','mixed_sin'):
  assert rows[2].count(r'\operatorname{cos}⁡')==2 and rows[2].count(r'\cdot')>=3,'component substitution structure'
  assert rows[3].count(r'\operatorname{cos}⁡')==2 and r'\cdot' not in rows[3],'trig-phase reduction structure'
 elif t=='quadratic':assert rows[2].count('(')>=6,'individual polynomial component products'
 elif t=='exp':assert r'\operatorname{ln}⁡1' in rows[2] and r'\frac{' in rows[2] and r'\cdot' in rows[2],'exp component structure'
 elif t=='trig_product':assert rows[2].count(r'\operatorname{sin}⁡')==2 and rows[2].count(r'\operatorname{cos}⁡')==2,'trig zero-factor components retained'
 elif t=='log_unit':assert rows[1].count(r'\frac{1}{')==3 and rows[1].count(r'\cdot')==3 and rows[3].count(r'\frac{')==3,'log chain and substitution structure'
 for row in rows[1:1+derivative_count]:assert veq(vector(row.split(' & =')[1]),d),'symbolic partials/chain'
 for row in rows[1+derivative_count:]:assert veq(vector(row.split(' & =')[1]),E),'evaluated gradient'
 # The evaluated LHS must refer to the actual displayed point. Only the known
 # raw exp error is exempt; its substituted operands remain checked above.
 point='('+','.join(str(v)for v in P)+')';labels=re.findall(r'∇[fg](\([^xyz)]*\))\s*&',blocks[0])
 if not(raw and t=='exp'):assert labels==[point],('gradient point label',labels,point)
 fm=re.search(r'Therefore,.*?direction of \$(.*?)\.\$',sol,re.S);assert fm,sol
 conclusion=vector(fm[1]);assert veq(conclusion,target),'final prose vector'
 if unit:
  assert len(blocks)==2;norm_rows=blocks[1].split(r'\\');assert len(norm_rows)==3
  sg=-1 if 'decrease most rapidly'in q[':question/problem']else 1
  expected=(('-'if sg<0 else '')+r'\frac{∇f'+point+r'}{‖∇f'+point+r'‖}')
  assert norm_rows[0].split(' & =')[1].strip()==expected,'normalization formal operands'
  row=norm_rows[1].split(' & =')[1];start=row.index(r'\frac');n,j=group(row,start+len(r'\frac'));den,j=group(row,j)
  assert equal(math(n),sg)and equal(math(den),S.sqrt(sum(e*e for e in E))),'normalization operands'
  assert veq(vector(row[j:]),E),'normalization gradient operand'
  assert veq(vector(norm_rows[2].split(' & =')[1]),target),'normalized final'
 else:assert len(blocks)==1
 return

def source_fidelity():
 cases=[];report=[]
 for t,(level,i,p)in g.FAMILIES.items():
  if i is None:continue
  r=g.generate(level,template=t,parameters=p,profile='source');q=r['question'];old=g.QUESTIONS[i];check(r,True)
  for k in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert(k in q)==(k in old),'presence parity'
  assert q[':question/problem']==old[':question/problem'];assert q.get(':question/worked-solution')==old.get(':question/worked-solution')
  of=old[':question/answer-fields'][0];nf=q[':question/answer-fields'][0];assert(':answer-field/correct'in of)==(':answer-field/correct'in nf)
  assert of[':answer-field/key']==nf[':answer-field/key'];assert nf[':answer-field/type']==of[':answer-field/type'][':db/ident']
  assert sorted(a[':answer/value']for a in of[':answer-field/choices'])==sorted(a[':answer/value']for a in nf[':answer-field/choices'])
  if ':answer-field/correct'in of:
   got=next(a[':answer/value']for a in nf[':answer-field/choices']if a[':answer/id']==nf[':answer-field/correct'][1]);assert got==of[':answer-field/correct'][':answer/value']
  cases.append({'source_id':i,'template':t,'parameters':p,'bank_profile':'source','level':level,'observed_level':None if ':question/difficulty'not in old else level})
  report.append({'source_id':i,'prompt_exact':True,'solution_exact':':question/worked-solution'in old,'bank_exact':True,'correct_ref_exact':':answer-field/correct'in of,'raw_attribute_presence':True})
 (ROOT/'source-cases.json').write_text(json.dumps(cases,indent=2));return report

def mutate_failure(r,edit,label):
 bad=copy.deepcopy(r);edit(bad)
 try:check(bad)
 except (AssertionError,ValueError,S.SympifyError,IndexError,TypeError):return label
 raise AssertionError('Mutation survived '+label)

def main():
 source=source_fidelity();records=[];coverage={};fps={l:set()for l in ('easy','moderate','hard')}
 for t,(lv,i,p)in g.FAMILIES.items():
  coverage[t]=0
  for seed in range(16):
   r=g.generate(lv,seed,template=t);check(r);records.append(r);coverage[t]+=1;fps[lv].add(r['generation']['mathematical_fingerprint'])
   r2=g.generate(lv,seed+91,template=t,parameters=r['generation']['parameters']);assert r['question'][':question/id']==r2['question'][':question/id']
  # Normal anchor retains its full source stage chain, with documented label repair.
  if i:
   r=g.generate(lv,template=t,parameters=p);check(r);records.append(r)
   varied=dict(p);varied['c'if t=='exp'else'b'if t=='quadratic'else'a']+=1
   rr=g.generate(lv,template=t,parameters=varied,profile='source');check(rr,True)
 # Default sampler must serve all source families without explicit selection.
 default={lv:set()for lv in ('easy','moderate','hard')}
 for lv in default:
  for seed in range(20):
   r=g.generate(lv,seed)
   if r['generation']['template'] not in default[lv]:check(r)
   default[lv].add(r['generation']['template'])
  assert default[lv]=={t for t,(v,_,_)in g.FAMILIES.items()if v==lv}
 # Whole-instance guard on reduced workload, not only initial integer spelling.
 invalid=[('log_unit',dict(a=6,b=6,c=6,u=1,v=1,w=1)),('log_unit',dict(a=6,b=1,c=1,u=1,v=1,w=1)),('log_unit',dict(a=6,b=6,c=1,u=3,v=3,w=3)),('mixed_sin',dict(a=4,b=3,u=3,v=0,w=1)),('exp',dict(a=1,b=1,c=1,u=1,v=2)),('linear_sin',dict(a=1,b=2,c=2,u=1,v=1,w=1))]
 for t,p in invalid:
  try:g.generate(g.FAMILIES[t][0],template=t,parameters=p)
  except ValueError:pass
  else:raise AssertionError('explicit guard '+t)
 base=next(r for r in records if r['generation']['template']=='quadratic')
 mutations=[mutate_failure(base,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace(r'\frac{∂}{∂x}',r'\frac{∂}{∂y}',1)),'held partial mutation'),mutate_failure(base,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].replace('Therefore,','Therefore,\f')),'C0 mutation'),mutate_failure(base,lambda r:r['question'].__setitem__(':question/worked-solution',r['question'][':question/worked-solution'].rsplit('direction of $',1)[0]+'direction of $i+j.$'),'stale prose vector')]
 # Incidental common magnitude cannot create another canonical direction.
 for template,p1,p2 in [('quadratic',dict(a=1,b=1,c=2,u=1,v=2),dict(a=2,b=2,c=4,u=1,v=2)),('log_unit',dict(a=2,b=1,c=1,u=1,v=1,w=1),dict(a=4,b=2,c=2,u=1,v=1,w=1)),('trig_product',dict(a=3,b=1,u=0,v=1),dict(a=4,b=1,u=0,v=-1))]:
  r1=g.generate(g.FAMILIES[template][0],template=template,parameters=p1);r2=g.generate(g.FAMILIES[template][0],template=template,parameters=p2)
  assert r1['generation']['mathematical_fingerprint']==r2['generation']['mathematical_fingerprint'],'common direction magnitude'
  assert r1['question'][':question/id']!=r2['question'][':question/id'],'presentation identity'
 def erase_operation(r):
  t=r['question'][':question/worked-solution'];block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',t,re.S)[1];rows=block.split(r'\\');r['question'][':question/worked-solution']=t.replace(rows[1],rows[2],1)
 h=next(r for r in records if r['generation']['template']=='log_unit');mutations.append(mutate_failure(h,erase_operation,'algebraically equal but erased log chain operation'))
 axis=g.generate_easy(template='trig_product',parameters=dict(a=3,b=1,u=0,v=1),profile='axis_method');check(axis)
 def duplicate_axis_direction(r):
  f=r['question'][':question/answer-fields'][0];wrong=next(a for a in f[':answer-field/choices'] if a[':answer/value'].startswith('-i'))
  wrong[':answer/value']=r'(3\cos(1)-1)j'
 mutations.append(mutate_failure(axis,duplicate_axis_direction,'duplicate wrong positive-parallel axis directions'))
 old_g=g.data('trig_product',dict(a=3,b=1,u=0,v=1))[4]
 try:g.validate_bank([old_g,[-e for e in old_g],[6*S.sin(1),-1],[0,3*S.cos(1)-1],[-1,0]],0,False)
 except ValueError:pass
 else:raise AssertionError('generator accepted duplicate axis directions')
 # Both complete trig banks remain normally eligible and observable.
 assert {g.generate_easy(seed,template='trig_product')['generation']['profile'] for seed in range(16)}=={'axis_method','nonaxis_method'}
 checks=[]
 native_records=list(records)
 for t,(lv,i,p) in g.FAMILIES.items():
  if i is not None and ':answer-field/correct' in g.QUESTIONS[i][':question/answer-fields'][0]:native_records.append(g.generate(lv,template=t,parameters=p,profile='source'))
 for r in native_records:
  f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
  checks.append({'label':r['generation']['template']+'/'+str(r['generation']['seed']),'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected','purpose':'all owned radio choices'}for a in f[':answer-field/choices']]})
 native_in=ROOT/'engine-input.json';native_out=ROOT/'engine-report.json';native_in.write_text(json.dumps(checks,ensure_ascii=False,indent=2));engine=REPO/'generate/runs/current/check-engine';subprocess.run([str(engine),str(native_in),str(native_out)],check=True)
 byte_evidence=[]
 for q in g.QUESTIONS.values():
  for a in q[':question/answer-fields'][0][':answer-field/choices']:
   text=a[':answer/value'];i=text.find(chr(92));byte_evidence.append({'source_id':q[':db/id'],'answer_id':a[':answer/id'],'adjacent_backslash_pairs':text.count(chr(92)*2),'first_command_ord':[]if i<0 else[ord(c)for c in text[i:i+5]]})
 (ROOT/'decoded-source-bytes.json').write_text(json.dumps(byte_evidence,indent=2))
 result={'passed':True,'runtime':{'python':sys.version.split()[0],'sympy':S.__version__},'source_fidelity':source,'source_counts':{'questions':6,'banks':6,'choices':30,'correct_designations':5,'worked_solutions':5,'unrated_missing_correct':1},'generated_independent_checks':len(records),'family_coverage':coverage,'default_family_coverage':{k:sorted(v)for k,v in default.items()},'sampled_math_tasks':{k:len(v)for k,v in fps.items()},'mutations_rejected':mutations,'native':{'report':'engine-report.json','records':len(checks),'checks':len(checks)*5,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'limitations':['Unrated source has no captured correct designation; inferred normal key verified mathematically, excluded from source matched-designation denominator.','Raw exponential solution retains wrong point label; only normal presentation repairs it.','Historical quadratic/trig-axis banks have unresolved error intent and remain evidence-only; normal generation uses method-derived banks.','All native fields are radio: selection checks do not establish vector-expression free-entry support.']}
 (ROOT/'validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
 build_review()

def build_review():
 # Review has every observed original/profile, two changed method variants each,
 # plus six authored hard variants. Originals use captured records unmodified.
 review=[];md=['# Direction generator review','Frozen source: math basis 1356. Raw originals retain omissions and known label error. Changed variants use authored complete banks.']
 for t,(lv,i,p)in g.FAMILIES.items():
  if i:
   md+=['## '+t+' — original',g.QUESTIONS[i][':question/problem'],'\n'.join('- $'+a[':answer/value']+'$'for a in g.QUESTIONS[i][':question/answer-fields'][0][':answer-field/choices']),g.QUESTIONS[i].get(':question/worked-solution','[Source omits difficulty, solution and correct ref.]')]
  if i:
   varied=dict(p);varied['c' if t=='exp' else 'b' if t=='quadratic' else 'a']+=1
   r=g.generate(lv,172,template=t,parameters=varied,profile='source');check(r,True);review.append(r);md+=['## '+t+' — generated raw source bank variant (evidence only)',g.markdown(r)]
  for seed in (170,171):
   r=g.generate(lv,seed,template=t);check(r);review.append(r);md+=['## '+t+' — generated '+lv+' seed '+str(seed),g.markdown(r)]
 (ROOT/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2));(ROOT/'review.md').write_text('\n\n'.join(md))
if __name__=='__main__':main()
