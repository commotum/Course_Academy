#!/usr/bin/env python3
"""Independent displayed-math, every choice, original fidelity and native grading checks."""
import copy,importlib.util,json,re,subprocess,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
ROOT=Path(__file__).resolve().parent;PROJECT=ROOT.parents[2]
spec=importlib.util.spec_from_file_location('g98392',ROOT.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
L={**{n:sp.Function(n) for n in ('g','h','k','f','s','w')},**g.SYMBOLS,**{s:sp.Symbol(s) for s in ('Dg','Dh','Dk','Df','Ds','Dw','Dx','Dy','Dz','DP','DQ','DR')}}

def latex(s):
 s=s.strip().rstrip('.').replace(r'\,','').replace(r'\cdot','*').replace(r'\left','').replace(r'\right','').replace(r'\end{aligned}','').replace('$','')
 s=re.sub(r'∂([A-Za-z])',r'D\1',s)
 while r'\frac' in s:
  i=s.rfind(r'\frac');j=i+5
  def brace(start):
   assert s[start]=='{';depth=1;end=start+1
   while depth:
    if s[end]=='{':depth+=1
    elif s[end]=='}':depth-=1
    end+=1
   return s[start+1:end-1],end
  num,j=brace(j);den,j=brace(j);s=s[:i]+'(('+num+')/('+den+'))'+s[j:]
 s=re.sub(r'\^\{([^{}]+)\}',r'**(\1)',s).replace('^','**').replace('{','(').replace('}',')').strip().rstrip('.')
 return parse_expr(s,local_dict=L,transformations=standard_transformations+(implicit_multiplication_application,))

def tokens(s):
 s=re.sub(r'\\text\{[^}]*\}','',s).replace('$','')
 s=re.sub(r'\\+,','',s);s=s.replace(' and ', ',');s=s.strip().strip(',')
 return [latex(t) for t in s.split(',') if t.strip()]

def independent(r):
 q=r['question'];a=r['generation'];name=a['template'];d=g.DATA[name];axis=d['axis']
 # Read graph from actual displayed prompt, never from generation metadata.
 match=re.search(r'given by \$([xyz])=([^$]+)\$',q[':question/problem']);assert match and match[1]==axis
 u,v={'x':(g.y,g.z),'y':(g.x,g.z),'z':(g.x,g.y)}[axis]
 graphtext=match[2]
 if d['kind']=='monomial':graph=latex(graphtext);du=sp.diff(graph,u);dv=sp.diff(graph,v)
 else:
  fm=re.fullmatch(r'([ghkfsw])\('+str(u)+','+str(v)+r'\)',graphtext);assert fm
  dg=L['D'+fm[1]];du=dg/L['D'+str(u)];dv=dg/L['D'+str(v)]
 rr=[graphtext if t.name==axis else str(t) for t in (g.x,g.y,g.z)]
 ru={'x':[du,1,0],'y':[1,du,0],'z':[1,0,du]}[axis];rv={'x':[dv,0,1],'y':[0,dv,1],'z':[0,1,dv]}[axis]
 N=[ru[1]*rv[2]-ru[2]*rv[1],ru[2]*rv[0]-ru[0]*rv[2],ru[0]*rv[1]-ru[1]*rv[0]];cross=list(N)
 if axis=='y':N=[-t for t in N]
 full=sp.expand(sum(a*b for a,b in zip((g.P,g.Q,g.R),N)))
 return u,v,du,dv,ru,rv,cross,N,full

def verify(r):
 q=r['question'];a=r['generation'];name=a['template'];d=g.DATA[name];u,v,du,dv,ru,rv,cross,N,full=independent(r)
 assert r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['title']==g.TITLE
 assert q[':question/difficulty']==':question.difficulty/'+d['level']
 assert a['source_analysis']['basis']==1356 and a['plot_assets']=={} and a['plot_rating']=='none'
 assert q[':question/problem'].count('$$')%2==0 and q[':question/worked-solution'].count('$$')%2==0
 assert '<<' not in q[':question/problem']+q[':question/worked-solution']
 solution=q[':question/worked-solution'];expected=[ru,rv,cross,N,[g.P,g.Q,g.R]]
 # Fixed source teaching prose must survive every permitted numerical parameter.
 raw=next(t for t in g.RAW['record'][':knowledge-point/questions'] if t[':question/id']==d['source_id'])
 def prose(text):
  text=re.sub(r'\$\$.*?\$\$', '',text,flags=re.S)
  return re.sub(r'\$[^$]*\$', '',text)
 assert prose(solution)==prose(raw[':question/worked-solution'])
 # Read the actual displayed parametrization, protecting the comma inside g(x,y).
 first=solution.split('We now compute the tangent vectors to the grid curves:')[0]
 displayed=re.findall('⟨([^⟨⟩]+)⟩',first)[0].replace(r'\,','')
 terms=[];depth=0;start=0
 for i,ch in enumerate(displayed):
  depth+=ch=='(';depth-=ch==')'
  if ch==',' and depth==0:terms.append(displayed[start:i]);start=i+1
 terms.append(displayed[start:]);assert len(terms)==3
 graphtext=re.search(r'given by \$[xyz]=([^$]+)\$',q[':question/problem'])[1]
 graph=latex(graphtext)
 params=a['parameters']
 if d['kind']=='monomial':assert sp.simplify(graph-(params['c']*(u-params.get('a',0))**params['m']*(v-params.get('b',0))**params['n']+params.get('h',0)))==0
 else:assert graph==sp.Function(params['function'])(u,v)
 canonical=str(graph).replace(params.get('function','!')+'(', 'f(') if d['kind']=='symbolic' else str(sp.expand(graph))
 fp=g.digest({'axis':d['axis'],'graph':canonical,'orientation':'positive_'+d['axis'],'assessed':'Cartesian flux formula'})
 assert fp==a['parameter_fingerprint'] and a['orientation']=='positive_'+d['axis']
 expected_r=[graph if t.name==d['axis'] else t for t in (g.x,g.y,g.z)]
 assert all(sp.simplify(latex(t)-e)==0 for t,e in zip(terms,expected_r))
 # Read both rows of the printed determinant, not only its computed vector.
 det=solution.split(r'|\begin{aligned}i & j & k ')[1].split(r'\end{aligned}|')[0]
 rows=[r.strip() for r in det.split(r'\\') if r.strip()]
 assert len(rows)==2
 assert all(all(sp.simplify(latex(t)-e)==0 for t,e in zip(row.split(' & '),expect)) for row,expect in zip(rows,(ru,rv)))

 # Check each displayed tangent, cross-product and field vector independently.
 for vec in re.findall('⟨([^⟨⟩]+)⟩',solution.split('We now compute the tangent vectors to the grid curves:')[1]):
  ss=[latex(t) for t in vec.replace(r'\,','').split(',')];assert len(ss)==3,(name,vec)
  assert any(all(sp.simplify(a-b)==0 for a,b in zip(ss,old)) for old in expected),(name,ss,expected)
 # Final distributed formula is independently parsed, catching incorrect slot assignment.
 tail=solution.split('Therefore, the surface integral can be written as')[1];last=tail.rsplit(' & =',1)[1]
 scalar=last.split('{∬}_{D}(',1)[1].rsplit(r')\,\text{d}A',1)[0]
 assert sp.simplify(latex(scalar)-full)==0,(name,scalar,full)
 if d['axis']=='y':assert '({r}_{z}^{′}\\times {r}_{x}^{′})' in tail
 if d['axis']=='x':assert 'F(r(y,z))' in tail
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and f[':answer-field/key']=='selection' and f[':answer-field/type']==':answer-field.type/radio'
 assert f[':answer-field/correct'][0]==':answer/id';choices=f[':answer-field/choices'];assert len(choices)==5
 seen=[];right=0
 for choice in choices:
  assert choice[':answer/type']==d['answer_type'];uuid.UUID(choice[':answer/id']);tt=tokens(choice[':answer/value'])
  if d['kind']=='monomial':
   assert len(tt)==2
   graph=latex(re.search(r'given by \$[xyz]=([^$]+)\$',q[':question/problem'])[1])
   # Read bases from actual prompt formula and substitute its missing coefficients.
   formula=q[':question/problem'].split('$$')[1].split('{∬}_{D}(',1)[1].split(r')\,\text{d}A')[0]
   formula=formula.replace(g.BOX,'@')
   if name in ('q-161453','q-161456') and '@' not in formula:formula=formula.replace(r'\,',r'@\,')
   for t in tt:formula=formula.replace('@','('+sp.sstr(t)+')',1)
   assert '@' not in formula and formula.count('P')+formula.count('Q')+formula.count('R')>=1
   assessed=latex(formula)
  else:
   formula=q[':question/problem'].split('$$')[1].split('{∬}_{D}(',1)[1].split(r')\,\text{d}A')[0]
   formula=formula.replace(g.BOX,'@').replace(r'\boxed{}','@')
   if '@' not in formula:
    if name=='q-161189':formula=formula.replace(r'(\frac',r'(@\frac').replace(r'+\frac',r'+@\frac') if formula.startswith('(') else '@'+formula.replace(r'+\frac',r'+@\frac')
    elif name=='q-161166':formula=formula.replace(r'\frac{}',r'@\frac{@}',1);formula=re.sub(r'\\frac\{(∂[A-Za-z])\}\{\}',lambda m:r'\frac{'+m[1]+'}{@}',formula)
    elif name=='q-161446':formula=formula.replace(r'P+\frac',r'P+@\frac');formula=re.sub(r'\\frac\{(∂[A-Za-z])\}\{\}',lambda m:r'\frac{'+m[1]+'}{@}',formula)
    elif name=='q-161460':formula=formula.replace(r'\,+','@@+').replace(r'-R\,',r'-R@\,')
   assert formula.count('@')==len(tt),(name,formula,tt)
   for t in tt:formula=formula.replace('@','('+sp.sstr(t)+')',1)
   assessed=latex(formula)

  equal=sp.simplify(assessed-full)==0;iscorrect=choice[':answer/id']==f[':answer-field/correct'][1];assert equal==iscorrect,(name,choice[':answer/value'],assessed,full)
  right+=equal;seen.append(tuple(tt))
 assert right==1 and len(set(seen))==5
 content=g.digest({'version':g.VERSION,'problem':q[':question/problem'],'solution':solution,'bank':sorted(c[':answer/value'] for c in choices),'parameters':a['parameter_fingerprint']});assert content==a['content_fingerprint']
 qid=uuid.uuid5(uuid.NAMESPACE_URL,f'{g.KP_UUID}/{content}');assert q[':question/id']==str(qid) and f[':answer-field/id']==str(uuid.uuid5(qid,'selection'))
 return True

def write(name,obj):(ROOT/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def main():
 cases=json.loads((ROOT/'source-cases.json').read_text());sources={q[':question/id']:q for q in g.RAW['record'][':knowledge-point/questions']};assert len(cases)==len(sources)==12
 coverage=[];records=[]
 for c in cases:
  r=g.generate(c['level'],template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);verify(r);old=sources[c['source_id']];q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
  assert q[':question/problem']==old[':question/problem']
  nb=sorted((aa[':answer/value'],aa[':answer/id']==f[':answer-field/correct'][1]) for aa in f[':answer-field/choices']);ob=sorted((aa[':answer/value'],aa[':answer/id']==of[':answer-field/correct'][':answer/id']) for aa in of[':answer-field/choices']);assert nb==ob
  exact=q[':question/worked-solution']==old[':question/worked-solution'];assert exact==(not g.DATA[c['template']]['repairs'])
  coverage.append({'source_id':c['source_id'],'template':c['template'],'complete_bank':True,'values_matched':5,'distractors_matched':4,'designation_matched':True,'prompt_exact':True,'solution_exact':exact,'solution_repaired':not exact})
  records.append({'label':'Original replay '+c['template']+' (supported solution repair)' if not exact else 'Original replay '+c['template'],'record':r,'raw_original':old})
  for seed in range(2):
   rr=g.generate(c['level'],seed+77,template=c['template'],profile=c['bank_profile']);verify(rr);records.append({'label':'Generated observed profile '+c['template']+' '+str(seed),'record':rr})
 for name,d in g.DATA.items():
  if d['kind']=='symbolic':
   for function in ('g','h','k','f','s','w'):
    for origin in ('observed:','authored:'):
     verify(g.generate(d['level'],template=name,parameters={'function':function},profile=origin+name))
 profile_checks=[];unique={l:set() for l in ('easy','moderate','hard')}
 for name,level in g.TEMPLATES.items():
  for origin in ('observed:','authored:'):
   for seed in range(12):
    r=g.generate(level,seed,template=name,profile=origin+name);verify(r)
    again=g.generate(level,seed+700,template=name,profile=origin+name,parameters=r['generation']['parameters']);assert r['question'][':question/id']==again['question'][':question/id']
    if seed<2 and origin=='authored:':records.append({'label':'Generated authored variant '+name+' '+str(seed),'record':r})
   profile_checks.append({'template':name,'profile':origin+name,'checks':12})
 # Enumerate the narrow but complete coefficient/exponent domain. Symbol renaming is NOT counted.
 for name in g.MONOMIALS:
  d=g.DATA[name]
  for m,n in [(d['original_parameters']['m'],d['original_parameters']['n']),(d['original_parameters']['n'],d['original_parameters']['m'])]:
   for c in range(-9,10):
    if c==0:continue
    try:r=g.generate(d['level'],template=name,parameters={'c':c,'m':m,'n':n});verify(r)
    except ValueError:continue
    unique[d['level']].add(r['generation']['parameter_fingerprint'])
 assert all(len(unique[l])>=16 for l in unique)
 shifted_normals=set()
 for ca in (-4,-2,2,4):
  for aa in range(-2,3):
   for bb in range(-2,3):
    rr=g.generate_moderate(template='q-161456',parameters={'c':ca,'m':1,'n':1,'a':aa,'b':bb,'h':0},profile='authored_shifted_bilinear:q-161456');verify(rr)
    shifted_normals.add(tuple(rr['generation']['math']['normal']))
    unique['moderate'].add(rr['generation']['parameter_fingerprint'])
 for seed in range(12):
  rr=g.generate_moderate(seed,template='q-161456',profile='authored_shifted_bilinear:q-161456');verify(rr)
  if seed<2:records.append({'label':'Generated authored shifted bilinear '+str(seed),'record':rr})
 profile_checks.append({'template':'q-161456','profile':'authored_shifted_bilinear:q-161456','checks':112,'distinct_oriented_normals':len(shifted_normals)})
 assert len(shifted_normals)==100
 # Invalid explicit instances and independent corruption detection.
 invalid=[('easy',{'template':'q-161453'}),('easy',{'template':'q-161449','parameters':{'c':0,'m':2,'n':1}}),('moderate',{'template':'q-161456','parameters':{'c':-1,'m':1,'n':1}}),('moderate',{'template':'q-161456','parameters':{'c':2,'m':1,'n':1,'a':1,'b':0,'h':0},'profile':'observed:q-161456'}),('easy',{'field_type':'blank'}),('hard',{'profile':'observed:q-161449'})]
 for level,kwargs in invalid:
  try:g.generate(level,**kwargs)
  except ValueError:pass
  else:raise AssertionError('Invalid input accepted')
 mutants=[];base=g.generate_easy(3)
 for kind in ('choice','solution','prompt','identity','scope'):
  r=copy.deepcopy(base)
  if kind=='choice':r['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']='$999P$ and $Q$'
  if kind=='solution':r['question'][':question/worked-solution']=r['question'][':question/worked-solution'].replace('6xy','7xy')
  if kind=='prompt':r['question'][':question/problem']=r['question'][':question/problem'].replace('3{x}','4{x}')
  if kind=='identity':r['question'][':question/id']=str(uuid.uuid4())
  if kind=='scope':r['question'][':question/difficulty']=':question.difficulty/hard'
  try:verify(r)
  except (AssertionError,ValueError):mutants.append(kind)
  else:raise AssertionError('Mutation escaped '+kind)
 engine=[]
 for item in records:
  f=item['record']['question'][':question/answer-fields'][0];engine.append({**item,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every owned radio choice'} for a in f[':answer-field/choices']]})
 write('engine-input.json',engine);subprocess.run([str(PROJECT/'generate/runs/current/check-engine'),str(ROOT/'engine-input.json'),str(ROOT/'engine-validation.json')],check=True);native=json.loads((ROOT/'engine-validation.json').read_text());assert native['documented_unresolved_checks']==0
 write('review.json',records)
 blocks=[]
 for item in records:
  if 'raw_original' in item:
   old=item['raw_original'];of=old[':question/answer-fields'][0]
   blocks.append('## Raw original '+old[':question/math-academy-id']+'\n\n'+old[':question/problem']+'\n\n'+'\n'.join('- '+('$'+aa[':answer/value']+'$' if aa[':answer/type'][':db/ident']==':answer.type/math' else aa[':answer/value'])+(' (correct)' if aa[':answer/id']==of[':answer-field/correct'][':answer/id'] else '') for aa in of[':answer-field/choices'])+'\n\n'+old[':question/worked-solution'])
  label=item['label']
  if label.startswith('Generated') and g.DATA[item['record']['generation']['template']]['kind']=='symbolic':label+=' (notation alias; finite same formula mask)'
  blocks.append('## '+label+'\n\n'+g.markdown(item['record']))
 (ROOT/'review.md').write_text('# Original and generated Cartesian flux formula review\n\nRaw originals and their normal generator replays appear below. Four replays repair documented teaching errors. Generated labels distinguish variants from originals and label symbolic notation aliases honestly. No plots occur.\n\n'+'\n\n'.join(blocks))
 write('validation.json',{'passed':True,'source_provenance':{k:g.RAW[k] for k in ('database','basis','lineage')},'source_coverage':coverage,'complete_source_banks':12,'displayed_values_matched':60,'distractors_matched':48,'correct_designations_matched':12,'prompts_exact':12,'solutions_exact':8,'solutions_repaired':4,'profile_checks':profile_checks,'unique_mathematical_defaults':{k:len(v) for k,v in unique.items()},'native_grading':{'entry_point':native['entry_point'],'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':0},'independent_math':'Displayed graph, parametrization, determinant rows, tangents and oriented normals parsed and checked; every answer reinserted into actual displayed formula; final scalar parsed independently; fixed prose checked', 'symbolic_name_profile_cases':96,'authored_shifted_bilinear_cases':112,'shifted_bilinear_distinct_oriented_normals':100,'validator_mutations_rejected':mutants,'invalid_inputs_rejected':len(invalid),'database_writes':0,'unresolved_findings':[],'interpretation_limits':['Observed algebraic distractor operation is reproducible; no claim that an individual learner error intent is identified.','Symbolic layout masks are finite categorical variants; function renaming is not counted as mathematical variety.']})
 print('PASS: 12 banks, 60 values, 48 distractors; 12 exact prompts, 8 exact + 4 repaired solutions; native '+str(native['accepted_checks'])+' accepted / '+str(native['rejected_checks'])+' rejected; unique defaults '+str({k:len(v) for k,v in unique.items()}))
if __name__=='__main__':
 try:main()
 except Exception as exc:write('validation.json',{'passed':False,'failure':str(exc)});raise
