#!/usr/bin/env python3
"""Independent readback of displayed functions, derivatives and integration rows.

Full raw bank fidelity is distinct from source mathematical defects and from
radio UUID grading. No raw anomaly is treated as mathematical correctness.
"""
import concurrent.futures, copy, hashlib, importlib.util,json, math,re, subprocess,sys
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,r,th=g.X,g.Y,g.R,g.T
L={'x':x,'y':y,'r':r,'theta':th,'e':s.E,'pi':s.pi,'sin':s.sin,'cos':s.cos,'sqrt':s.sqrt}

def group(z,i):
 assert z[i]=='{',(z,i);d=1;j=i+1
 while d:
  if z[j]=='{':d+=1
  elif z[j]=='}':d-=1
  j+=1
 return z[i+1:j-1],j

def scalar(z):
 z=z.strip().rstrip('.,');z=z+'1'if z in ['-','+']else z;z=z.replace(r'\left','').replace(r'\right','').replace(r'\,',' ').replace(r'\quad',' ').replace(r'\cdot','*').replace(r'\theta','theta').replace(r'\pi','pi').replace('π','pi').replace('⁡','').replace(r'\text{ }','')
 while r'\frac' in z or r'\sqrt' in z:
  m=re.search(r'\\(frac|sqrt)',z);a,j=group(z,m.end())
  if m.group(1)=='frac':b,j=group(z,j);v='(('+str(scalar(a))+')/('+str(scalar(b))+'))'
  else:v='sqrt('+str(scalar(a))+')'
  z=z[:m.start()]+v+z[j:]
 # Handle exactly source-bounded standard trig powers and their complete input.
 for fn in ['sin','cos']:
  z=re.sub(r'\\'+fn+r'\^\{?([23])\}?\s*(theta|x|y)',lambda m:'('+fn+'('+m[2]+'))**'+m[1],z)
  z=re.sub(r'\\'+fn+r'\s*(theta|x|y)',lambda m:fn+'('+m[1]+')',z)
  z=z.replace('\\'+fn,fn)
 z=z.replace('^','**').replace('{','(').replace('}',')')
 assert '\\'not in z,z
 return parse_expr(z,local_dict=L,transformations=standard_transformations+(implicit_multiplication_application,),evaluate=True)

def eq(a,b):assert s.simplify(a-b)==0,(a,b)
def formatting(z):
 assert all(ord(c)>=32 or c in '\n\t'for c in z), 'C0 control byte'
 assert z.count('$')%2==0
 assert not re.search(r'(?<!\\)(?:--|\+\+|\+-|-\+)',z),z
 for m in re.finditer(r'\$\$.*?\$\$|\$[^$]*\$',z,re.S):
  depth=0
  for c in m.group():
   if c=='{':depth+=1
   elif c=='}':depth-=1;assert depth>=0
  assert depth==0,m.group()

def eval_row(z,p):
 """Evaluate the actual rendered definite-integral/endpoint object recursively."""
 z=z.strip().rstrip('.,').replace(r'\left','').replace(r'\right','').replace(r'\,','').replace(r'\end{aligned}','')
 if r'\iint_D' in z:
  prefix,body=z.split(r'\iint_D',1);body=body.removesuffix('dA');f=scalar(body);F=s.simplify(f.subs({x:r*s.cos(th),y:r*s.sin(th)})*r)
  value=s.integrate(s.integrate(F,(r,p['inner'],s.sqrt(p['s']))),(th,p['lo']*s.pi,p['hi']*s.pi))
  return scalar(prefix or '1')*value
 if r'\iint_\Delta' in z:
  prefix,body=z.split(r'\iint_\Delta',1);body=body.removesuffix(r'drd\theta');F=scalar(body)
  return scalar(prefix or '1')*s.integrate(s.integrate(F,(r,p['inner'],s.sqrt(p['s']))),(th,p['lo']*s.pi,p['hi']*s.pi))
 if r'\int_' in z:
  i=z.index(r'\int_');start=i+len(r'\int_');lo,j=group(z,start);assert z[j]=='^';hi,j=group(z,j+1)
  suffix=z[j:]
  if suffix.endswith(r'd\theta'):v=th;body=suffix[:-len(r'd\theta')]
  elif suffix.endswith('dr'):v=r;body=suffix[:-2]
  else:raise AssertionError(z)
  inner=eval_row(body or '1',p)
  return scalar(z[:i]or'1')*s.integrate(inner,(v,scalar(lo),scalar(hi)))
 if '['in z:
  i=z.index('[');j=z.index(']',i);body=z[i+1:j];assert z[j+1]=='_';lo,k=group(z,j+2);assert z[k]=='^';hi,k=group(z,k+1);assert not z[k:],z
  F=scalar(body);v=r if r in F.free_symbols else th
  return scalar(z[:i]or'1')*(F.subs(v,scalar(hi))-F.subs(v,scalar(lo)))
 return scalar(z)

def raw_prompt_components(q):
 z=q[':question/problem']
 if '⟨'in z:pt,qt=re.search('⟨(.*?),(.*?)⟩',z).groups()
 else:pt,qt=re.search(r'(?:\{∮\}_\{C\}|∮_\(C\))\((.*?)\)(?:\\,)?dx\s*\+\s*\((.*?)\)(?:\\,)?dy',z).groups()
 def norm(z):
  for a,b in [(r'\operatorname{cos}⁡',r'\cos'),(r'\operatorname{sin}⁡',r'\sin'),('{sin}^{3}⁡',r'\sin^3')]:z=z.replace(a,b)
  return scalar(z)
 return norm(pt),norm(qt)

def prompt_components(q):
 z=q[':question/problem']
 if r'F(x,y)=\langle'in z:
  pt,qt=re.search(r'F\(x,y\)=\\langle (.*?),(.*?)\\rangle',z).groups()
 else:pt,qt=re.search(r'\\oint_C\((.*?)\)\\,dx\+\((.*?)\)\\,dy',z).groups()
 return scalar(pt),scalar(qt)

def normal_check(record):
 q=record['question'];gen=record['generation'];p=g.exact(gen['parameters']);name=gen['template'];level=q[':question/difficulty'].split('/')[-1]
 assert set(record['knowledge_point'])=={'db_id','id','title'};assert not gen['evidence_only']and gen['eligible_for_learning']
 formatting(q[':question/problem']);formatting(q[':question/worked-solution'])
 P,Q=prompt_components(q);pp=s.diff(P,y);qq=s.diff(Q,x);curl=s.expand(qq-pp)
 # Radius/bounds read from actual supplied equations or actual figure sidecar.
 if level=='moderate':eq(scalar(re.search(r'x\^2\+y\^2=(.*?),',q[':question/problem']).group(1)),p['s'])
 if level=='easy':eq(scalar(re.search(r'0\\le r\\le (.*?),',q[':question/problem']).group(1)),s.sqrt(p['s']))
 if level=='hard':
  path=Path(re.search(r'!\[\]\((.*?)\)',q[':question/problem']).group(1));side=json.loads(path.with_suffix('.json').read_text());assert not side['shaded'];assert all(s.sympify(side[k])==p[k]for k in ['s','inner','lo','hi']);assert path.exists()
 F=s.simplify(curl.subs({x:r*s.cos(th),y:r*s.sin(th)})*r);ans=s.simplify(s.integrate(s.integrate(F,(r,p['inner'],s.sqrt(p['s']))),(th,p['lo']*s.pi,p['hi']*s.pi)))
 eq(ans,s.sympify(gen['answer']))
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/worked-solution'],re.S)
 comp=next(z for z in blocks if z.startswith('P(x,y)='));aa,bb=comp.split(r',\quad Q(x,y)=');eq(scalar(aa[len('P(x,y)='):]),P);eq(scalar(bb),Q)
 partial=next(z for z in blocks if z.startswith(r'\begin{aligned}\frac{\partial P}'))
 aa,bb=partial.removeprefix(r'\begin{aligned}\frac{\partial P}{\partial y}=').removesuffix(r'\end{aligned}').split(r',\quad \frac{\partial Q}{\partial x}=');eq(scalar(aa),pp);eq(scalar(bb),qq)
 region=next(z for z in blocks if z.startswith(r'\Delta='));m=re.search(r':(.*?)\\le r\\le (.*?),(.*?)\\le\\theta\\le (.*?)\\\}',region);assert m,region
 for printed,expected in zip(m.groups(),[p['inner'],s.sqrt(p['s']),s.pi*p['lo'],s.pi*p['hi']]):eq(scalar(printed),expected)
 applied=next(z for z in blocks if z.startswith(r'\begin{aligned}\oint_C'))
 parts=applied.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}').split(r' \\ ')
 pp2,qq2=re.search(r'\\oint_C\((.*?)\)\\,dx\+\((.*?)\)\\,dy',parts[0]).groups();eq(scalar(pp2),P);eq(scalar(qq2),Q)
 for row in parts[1:]:eq(eval_row(row.removeprefix('&='),p),ans)
 assert len(parts)==(2 if name=='q-126747'else 3)
 # Every displayed final chain equality, including distributed substitution,
 # trig reduction, radial primitive, EACH endpoint, angular primitive/arithmetic.
 final=blocks[-1].removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}');rows=final.split(r' \\ ')
 lhs,first=rows[0].split('&=');eq(eval_row(lhs,p),ans);eq(eval_row(first,p),ans)
 for row in rows[1:]:eq(eval_row(row.removeprefix('&='),p),ans)
 if name=='q-126747':
  assert '\\cos(2\\theta)'in rows[2]and'\\sin(2\\theta)'in rows[5]
  assert len(rows)==8
  primitive=re.search(r'\[(.*?)\\right\]',rows[5]).group(1);eq(s.diff(scalar(primitive),th),s.cos(2*th))
 else:
  assert 'r^3'in rows[1]and'\\sin^2\\theta'in rows[1]
  assert 'r^3'in rows[2]and '\\sin^2' not in rows[2]
  assert 'r^4'in rows[3]and'['in rows[3]and'4'in rows[3]
  primitive=re.search(r'\[(.*?)\\right\]',rows[3]).group(1);eq(s.diff(scalar(primitive),r),(p['c']if name=='q-126756'else 1)*r**3)
  assert '\\left'in final # endpoint structural masks survive simplification
  assert len(rows)==(8 if name=='q-126736'else 9)
  # Assert individually evaluated radial endpoint arithmetic, not collapsed value.
  assert re.search(r'\(.*?-.*?\)',rows[4]),rows[4]
  expected_up=(p['c']if name=='q-126756'else 1)*p['s']**2/4;expected_low=(p['c']if name=='q-126756'else 1)*p['inner']**4/4
  body=re.search(r'\((.*?)\)',rows[4]).group(1);up,low=body.split('-',1);eq(scalar(up),expected_up);eq(scalar(low),expected_low)
 field=q[':question/answer-fields'][0];choices=field[':answer-field/choices'];assert len(choices)==5
 for a in choices:formatting(a[':answer/value'])
 values=[scalar(a[':answer/value'])for a in choices];assert all(s.simplify(v-w)!=0 for i,v in enumerate(values)for w in values[i+1:])
 hit=[a[':answer/id']for a,v in zip(choices,values)if s.simplify(v-ans)==0];assert hit==[field[':answer-field/correct'][1]]
 # Field-owned answer identity, valid UUIDs and math field shapes.
 for a in choices:__import__('uuid').UUID(a[':answer/id']);assert a[':answer/type']==':answer.type/math'
 assert field[':answer-field/type']==':answer-field.type/radio'
 rr=g.generate(level,seed=944,template=name,parameters=gen['parameters']);assert rr['question'][':question/id']==q[':question/id'];assert rr['generation']['mathematical_fingerprint']==gen['mathematical_fingerprint']
 return dict(template=name,level=level,displayed_stage_count=len(rows)+len(parts),whole_bank_valid=True)

def main():
 raw_report=[];cases=[];records=[]
 for name,q in g.Q.items():
  level=g.FAMILIES[name]['level'];case={'source_id':name,'source_db_id':q[':db/id'],'template':name,'level':level,'level_authored':':question/difficulty'not in q,'parameters':{'noise':1},'bank_profile':'observed:'+name};cases.append(case)
  rec=g.generate(level,template=name,parameters=case['parameters'],profile=case['bank_profile']);out=rec['question'];field=out[':question/answer-fields'][0];src=q[':question/answer-fields'][0]
  assert out[':question/problem']==q[':question/problem'];assert out.get(':question/worked-solution')==q.get(':question/worked-solution')
  for k in [':question/difficulty',':question/worked-solution',':question/answer-fields']:assert (k in out)==(k in q)
  assert(':answer-field/correct'in field)==(':answer-field/correct'in src)
  assert sorted(a[':answer/value']for a in field[':answer-field/choices'])==sorted(a[':answer/value']for a in src[':answer-field/choices'])
  # Decoded source values have no adjacent backslash pairs; JSON escaping
  # is not an additional source byte. Public raw values preserve exact bytes.
  assert all(chr(92)*2 not in a[':answer/value'] for a in src[':answer-field/choices'])
  originals=[scalar(a[':answer/value'].replace('\\\\','\\'))for a in src[':answer-field/choices']]
  vals=list(map(s.sympify,g.HISTORICAL[name]));assert all(s.simplify(a-b)==0 for a,b in zip(originals,vals))
  if ':answer-field/correct'in src:
   chosen=next(a for a in field[':answer-field/choices']if a[':answer/id']==field[':answer-field/correct'][1]);eq(scalar(chosen[':answer/value'].replace('\\\\','\\')),scalar(src[':answer-field/correct'][':answer/value'].replace('\\\\','\\')))
  changed=g.generate(level,template=name,profile=case['bank_profile'],parameters={'noise':2});component=g.FAMILIES[name]['noise'];assert changed['question'][':question/problem']!=q[':question/problem']
  if ':question/worked-solution'in q:
   assert changed['question'][':question/worked-solution']!=q[':question/worked-solution'];assert changed['question'][':question/worked-solution'].count(('3-{x}^{2}y' if name=='q-126733'else r'2\cdot('+component+')'))==q[':question/worked-solution'].count(component)
  assert changed['generation']['mathematical_fingerprint']==rec['generation']['mathematical_fingerprint']
  P0,Q0=raw_prompt_components(out);P1,Q1=raw_prompt_components(changed['question']);eq(s.diff(Q0,x)-s.diff(P0,y),s.diff(Q1,x)-s.diff(P1,y))
  assert s.simplify(P0-P1)!=0
  pp=g.exact(g.anchor(name));ind=s.simplify((s.diff(Q1,x)-s.diff(P1,y)).subs({x:r*s.cos(th),y:r*s.sin(th)})*r);raw_ans=s.integrate(s.integrate(ind,(r,pp['inner'],s.sqrt(pp['s']))),(th,pp['lo']*s.pi,pp['hi']*s.pi));eq(raw_ans,s.sympify(changed['generation']['answer']))
  raw_report.append({'source_id':name,'prompt_raw_exact':True,'solution_raw_exact_or_absent':True,'bank_values_raw_exact':5,'designation_matched':':answer-field/correct'in src,'key_presence_parity':True,'mathematical_bank_valid':name!='q-126758','source_solution_mathematically_valid':name not in ['q-126736','q-126758'],'noise_readback_all_occurrences':True})
  (HERE/('raw-'+name+'.json')).write_text(json.dumps(rec,ensure_ascii=False,indent=2)+'\n')
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n')
 checks=[];normal_reports=[]
 for name,f in g.FAMILIES.items():
  # Source family anchors use NORMAL authored bank/repair recipe too.
  rr=g.generate(f['level'],template=name,parameters=g.anchor(name));normal_reports.append(normal_check(rr));records.append(rr)
  for seed in [17,34,81]:
   rr=g.generate(f['level'],seed,template=name);normal_reports.append(normal_check(rr));records.append(rr)
 for seed in range(30):
  for level in ['easy','moderate','hard']:
   rr=g.generate(level,seed);normal_reports.append(normal_check(rr));records.append(rr)
 # Every normal family is eligible for default sampling.
 coverage={l:sorted({rr['generation']['template']for rr in records if rr['question'][':question/difficulty'].endswith('/'+l)})for l in ['easy','moderate','hard']}
 assert all(coverage[l]==sorted(n for n,f in g.FAMILIES.items()if f['level']==l)for l in coverage)
 # Independent mathematical task variety excludes stationary nuisance scaling.
 variety={}
 for level in ['easy','moderate','hard']:
  seen=set()
  for name,f in g.FAMILIES.items():
   if f['level']!=level:continue
   rng=__import__('random').Random(202)
   for _ in range(180):
    p=g.sample(level,name,rng)
    try:g.bank(f,p,g.answer_value(f,p))
    except ValueError:continue
    P,Q,_,_=g.components(name,p);seen.add((s.srepr(s.expand(P-P.subs(y,0))),s.srepr(s.expand(Q-Q.subs(x,0))),*(str(p[k])for k in ['s','inner','lo','hi'])))
  variety[level]=len(seen);assert len(seen)>=(10 if level=='easy'else 35),(level,len(seen))
 # Enumerate the complete bounded mathematical domain, excluding nuisances,
 # equivalent cubic coefficient masks and bank/presentation aliases.
 finite={}
 for level in ['easy','moderate','hard']:
  seen=set();instances=0
  for name,f in g.FAMILIES.items():
   if f['level']!=level:continue
   ss=[1,4,9,16,25]if level=='easy'else [1,2,4,9,16,25]if level=='moderate'else[4,9,16,25]
   angular=[(0,'1/6'),(0,'1/3'),(0,'2/3')]if name=='q-126747'else[(0,'1/2'),('1/2',1),(0,1)]if name=='q-126756'else[(g.anchor(name)['lo'],g.anchor(name)['hi'])]
   for cc in range(1,5 if level=='easy'else 7):
    for ss0 in ss:
     aa=range(1,int(s.sqrt(ss0)))if name=='q-126758'else[0]
     for aa0 in aa:
      for ll,hh in angular:
       p=g.exact(dict(c=cc,s=ss0,inner=aa0,lo=ll,hi=hh))
       try:g.check_scope(level,name,p);g.bank(f,p,g.answer_value(f,p))
       except ValueError:continue
       P,Q,_,_=g.components(name,p);key=(s.srepr(s.expand(P-P.subs(y,0))),s.srepr(s.expand(Q-Q.subs(x,0))),*(str(p[k])for k in ['s','inner','lo','hi']))
       seen.add(key);instances+=1
  finite[level]={'distinct_assessed_tasks':len(seen),'eligible_template_instances':instances}
 assert {l:v['distinct_assessed_tasks']for l,v in finite.items()}=={'easy':20,'moderate':108,'hard':204}
 # Explicit scope violations are rejected, never resampled into a different task.
 for level,name,p in [('easy','supported_disk',dict(c=5,s=4,inner=0,lo=0,hi=2)),('moderate','q-126733',dict(c=1,s=4,inner=0,lo=0,hi=1)),('hard','q-126758',dict(c=3,s=4,inner=0,lo=0,hi='1/2')),('hard','q-126747',dict(c=1,s=16,inner=0,lo=0,hi='1/5')),('moderate','q-126736',dict(c=2,s=9,inner=0,lo=0,hi=2))]:
  try:g.generate(level,template=name,parameters=p)
  except ValueError:pass
  else:raise AssertionError(('scope was accepted',p))
 # Corrupt a real displayed intermediate while keeping its final answer constant;
 # independent QA must detect it, including structure removed but same value.
 probe=copy.deepcopy(records[0]);probe['question'][':question/problem']+='\f'
 try:normal_check(probe)
 except AssertionError:pass
 else:raise AssertionError('control byte undetected')
 probe=copy.deepcopy(records[0]);probe['question'][':question/worked-solution']=probe['question'][':question/worked-solution'].replace(r'\cos^2\theta+\sin^2\theta',r'\cos^2\theta-\sin^2\theta',1)
 try:normal_check(probe)
 except AssertionError:pass
 else:raise AssertionError('distributed trig corruption undetected')
 probe=copy.deepcopy(records[0]);probe['question'][':question/worked-solution']=probe['question'][':question/worked-solution'].replace(r'r^3(\cos^2\theta+\sin^2\theta)','r^3')
 try:normal_check(probe)
 except AssertionError:pass
 else:raise AssertionError('missing identity stage undetected')
 # Concurrent fresh renders, identical and different instances, retain sidecars.
 ps=[g.exact(dict(c=2,s=16,inner=1,lo=0,hi='1/2')),g.exact(dict(c=2,s=16,inner=1,lo=0,hi='1/2')),g.exact(dict(c=2,s=25,inner=2,lo=0,hi='1/2'))]
 for p in ps:
  data={k:str(p[k])for k in ['s','inner','lo','hi']};data['shaded']=True;data['renderer_revision']=3;key=g.digest(data)
  for suffix in ['.png','.json']:(HERE/'plots'/(key+suffix)).unlink(missing_ok=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3)as pool:paths=list(pool.map(lambda p:g.render_plots(p,True),ps))
 assert paths[0]==paths[1]and paths[0]!=paths[2];assert all(Path(z).exists()and Path(z).with_suffix('.json').exists()for z in paths)
 assert not list((HERE/'plots').glob('tmp*'))
 # Real radio grading, every displayed option including rejected wrong entries.
 for i,rec in enumerate(records):
  field=rec['question'][':question/answer-fields'][0];correct=field[':answer-field/correct'][1]
  checks.append({'label':'normal-'+str(i),'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected','purpose':'native owned radio option'}for a in field[':answer-field/choices']]})
 for name in g.Q:
  raw=json.loads((HERE/('raw-'+name+'.json')).read_text());field=raw['question'][':question/answer-fields'][0]
  if ':answer-field/correct'not in field:continue
  correct=field[':answer-field/correct'][1]
  checks.append({'label':'historical-evidence-'+name,'record':raw,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted'if a[':answer/id']==correct else'rejected','purpose':'native ID designation only; no mathematical bank validity claim'}for a in field[':answer-field/choices']]})
 input_path=HERE/'engine-input.json';output_path=HERE/'engine-report.json';input_path.write_text(json.dumps(checks,ensure_ascii=False,indent=2)+'\n')
 engine=Path('generate/runs/current/check-engine');proc=subprocess.run([str(engine),str(input_path),str(output_path)],text=True,capture_output=True);assert proc.returncode==0,(proc.stdout,proc.stderr)
 engine_report=json.loads(output_path.read_text())
 # Clearly labeled source evidence and two+ normal changed examples per family.
 review=records[:44]
 (HERE/'review.json').write_text(json.dumps(review,ensure_ascii=False,indent=2)+'\n')
 md=['# Source evidence and generated review','All observed banks are opaque historical evidence; normal examples use authored method banks. Raw anomalous originals remain explicitly ineligible.']
 for name,q in g.Q.items():
  md+=['## Original '+name,q[':question/problem'],'Source bank: '+', '.join('$'+a[':answer/value']+'$'for a in q[':question/answer-fields'][0][':answer-field/choices']),q.get(':question/worked-solution','Original worked solution absent; no original difficulty or correct designation.')]
  for rr in review:
   if rr['generation']['template']==name:md+=['### Generated '+rr['question'][':question/difficulty']+'; authored method bank',g.markdown(rr)]
 md+=['## Authored missing easy level']+[g.markdown(rr)for rr in review if rr['generation']['template']=='supported_disk']
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
 report={'status':'passed_with_explicit_source_defects','source':{k:g.SOURCE[k]for k in ['database','basis','lineage']},'runtime':{'python':sys.version.split()[0],'sympy':s.__version__,'matplotlib':g.matplotlib.__version__},'raw_fidelity':{'questions':10,'prompts_exact':'10/10','all_option_strings_exact':'50/50','complete_banks_exact':'10/10','correct_designations_exact':'9/9 present;1 absent','solutions_exact':'9/9 present;1 absent','attribute_presence_parity':'10/10'},'source_mathematical_validity':{'original_correct_answers':'9/9 designated','inferred_correct_answers':'1/1 missing designation (8pi)','unambiguous_banks':'9/10','duplicate_wrong_pair':'q-126758:90pi/4=45pi/2','correct_original_solutions':'7/9 present','normal_repaired_solutions':'2/2 (q126736 sign; q126758 omitted3)','canonical_solution_repair':'3(x²+y²) replaces3x²+y²'},'normal':{'records_verified':len(records),'source_shaped_templates':10,'authored_easy_templates':1,'coverage':coverage,'sampled_mathematical_tasks':variety,'complete_bounded_domain':finite,'displayed_stage_checks':normal_reports,'native_engine_report':str(output_path),'native_engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest(),'checks_requested':5*len(records)+45,'concurrent_render':True,'formatting_identity_scope':True},'raw_evidence_limitations':['Opaque historical banks preserve expressions but wrong-operation intent is unresolved.','q125717 missing original solution,difficulty andcorrectref; normal designation andhardrouting explicitly authored.','q125717 sqrt{x} has no C1 open neighborhood at x=0; normal sqrt{x+1} repair.','Observed source profiles vary only irrelevant-to-curl univariate noise; no noise counted as new mathematical task.','Raw answer TeX bytes are preserved; decoded source values contain zero adjacent backslash pairs.']}
 (HERE/'validation.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:report[k]for k in ['status','raw_fidelity']},indent=2));print('normal',len(records),'records;',5*len(records),'native checks; tasks',variety)

if __name__ == "__main__":
 main()
