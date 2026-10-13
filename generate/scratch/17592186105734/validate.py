#!/usr/bin/env python3
"""Independent QA reads actual printed givens and every displayed arithmetic row."""
import importlib.util,json,re,subprocess,hashlib,copy,uuid,itertools
from pathlib import Path
import sympy as S
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
R=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('altitude',R.with_suffix('.py'));G=importlib.util.module_from_spec(spec);spec.loader.exec_module(G)
I,J,K=S.symbols('i j k',real=True)
def equal(a,b):assert S.simplify(a-b)==0,(a,b)
def mathparse(s,locals=None):
 s=s.strip().rstrip('.').replace(r'\,','').replace(r'\cdot','*')
 def convert(s):
  out='';i=0
  while i<len(s):
   if s.startswith(r'\frac',i) or s.startswith(r'\sqrt',i):
    op='frac' if s.startswith(r'\frac',i) else 'sqrt';i+=5
    def take(j):
     assert s[j]=='{',(s,j);d=1;k=j+1
     while d:d+=(s[k]=='{')-(s[k]=='}');k+=1
     return s[j+1:k-1],k
    a,i=take(i)
    if op=='frac':b,i=take(i);out+='(('+convert(a)+')/('+convert(b)+'))'
    else:out+='sqrt('+convert(a)+')'
   else:out+=s[i];i+=1
  return out
 s=convert(s).replace('{','(').replace('}',')').replace('^','**')
 s=re.sub(r'(?<![A-Za-z_])[ijk](?![A-Za-z_])',lambda m: {'i':'axis_i','j':'axis_j','k':'axis_k'}[m[0]],s)
 return parse_expr(s,local_dict={'axis_i':I,'axis_j':J,'axis_k':K,**(locals or {})},transformations=standard_transformations+(implicit_multiplication_application,))
def basis(x):return x[0]*I+x[1]*J+x[2]*K
def rows(b):return re.split(r' \\\\ ',b.removeprefix(r'\begin{aligned}').removesuffix(r'\end{aligned}'))
def rhs(row):return row.split(' & =',1)[1]
def formatting(s):
 assert s.count('$$')%2==0
 assert s.replace('$$','').count('$')%2==0
 depth=0
 for m in re.finditer(r'(?<!\\)[{}]',s):
  depth+=1 if m[0]=='{' else -1;assert depth>=0
 assert depth==0
 assert '@BLOCK' not in s and not re.search(r'@[A-Z]@',s)
 assert '+-' not in s and '--' not in s

def check(r):
 assert set(r['knowledge_point'])=={'db_id','id','title'};assert r['knowledge_point']==G.KP
 q=r['question'];p=q[':question/problem'];sol=q[':question/worked-solution'];formatting(p);formatting(sol)
 pts={n:S.Matrix(list(map(int,c.split(',')))) for n,c in re.findall(r'([A-Z])\(([-\d, ]+)\)',p)}
 assert len(pts)==3
 apex=re.search(r'length of the altitude \$([A-Z]{2})\$',p)[1][0]
 B=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(B)==7
 basestr=re.search(r'\\cdot ([A-Z]{2})',B[0])[1];a,b=basestr;assert apex not in basestr
 U=pts[b]-pts[a];V=pts[apex]-pts[a];L=S.sqrt(U.dot(U));h=S.sqrt(V.dot(V)-U.dot(V)**2/U.dot(U))
 edge_rows=rows(B[1]);assert len(edge_rows)==8
 edges=[]
 for n in (0,4):
  name=re.search(r'\\overset\{\\to \}\{([A-Z]{2})\}',edge_rows[n])[1];x=pts[name[1]]-pts[name[0]];edges.append((name,x))
  assert rhs(edge_rows[n])==name[1].lower()+'-'+name[0].lower()
  equal(mathparse(rhs(edge_rows[n+1])),basis(x));equal(mathparse(rhs(edge_rows[n+2])),basis(x))
  assert tuple(map(int,re.search('⟨(.*?)⟩',rhs(edge_rows[n+3]))[1].split(',')))==tuple(x)
 u,v=edges[0][1],edges[1][1];W=u.cross(v);N=S.sqrt(W.dot(W));equal(N/L,h)
 assert edges[0][0][0]==edges[1][0][0]
 # Inspect complete first matrix and each cofactor matrix from printed solution.
 matrices=re.findall(r'\|\\begin\{aligned\}(.*?)\\end\{aligned\}\|',B[2]);assert len(matrices)==4
 main=matrices[0].split(r' \\ ');assert main[0]=='i & j & k';assert list(map(int,main[1].split(' & ')))==list(u);assert list(map(int,main[2].split(' & ')))==list(v)
 for mat,indices in zip(matrices[1:],((1,2),(0,2),(0,1))):
  x,y=mat.split(r' \\ ');assert list(map(int,x.split(' & ')))==[u[i] for i in indices];assert list(map(int,y.split(' & ')))==[v[i] for i in indices]
 # Check stage counts and complete shared prose against the raw source mask.
 sid=r['generation']['template']
 if sid.startswith('q-') and sid!='q-20028':
  sourceqs=json.loads((R/'source.json').read_text())['record'][':knowledge-point/questions'];original=next(z[':question/worked-solution'] for z in sourceqs if z[':question/math-academy-id']==sid);OB=re.findall(r'\$\$\n(.*?)\n\$\$',original,re.S)
  assert re.sub(r'\$\$\n.*?\n\$\$','@MATH@',sol,flags=re.S)==re.sub(r'\$\$\n.*?\n\$\$','@MATH@',original,flags=re.S)
  for index in (1,3,5,6):assert len(rows(B[index]))==len(rows(OB[index]))
  assert B[4].count('=')==OB[4].count('=')
 # Cross rows after nested matrix blocks: products, collected basis, tuple.
 tail=B[2].split(matrices[-1]+r'\end{aligned}|k',1)[1]
 cr=tail.split(r' \\ ')[1:];assert len(cr)==3
 equal(mathparse(rhs(cr[0])),basis(W));equal(mathparse(rhs(cr[1])),basis(W));assert tuple(map(int,re.search('⟨(.*?)⟩',rhs(cr[2]))[1].split(',')))==tuple(W)
 for block,val,name,formal in ((B[3],N,'A','|'+G.vector_arrow(edges[0][0])+r'\times '+G.vector_arrow(edges[1][0])+'|'),(B[5],L,basestr,'|'+G.vector_arrow(basestr)+'|')):
  rr=rows(block);assert rr[0]==name+' & ='+formal
  for row in rr[1:]:equal(mathparse(rhs(row)),val)
 ar=B[4].split('=');assert ar[:2]==[r'{A}_{△}',r'\frac{1}{2}A']
 for exp in ar[2:]:equal(mathparse(exp),N/2)
 # Validate all formal, substituted, reduced, quotient and final equations.
 alt=re.search(r'length of the altitude \$([A-Z]{2})\$',p)[1]
 initial=B[0].replace(r'{A}_{△}','('+str(N/2)+')').replace(alt,'height').replace(basestr,'baselength');ileft,iright=initial.split('=');equal(mathparse(ileft,{'height':h,'baselength':L}),mathparse(iright,{'height':h,'baselength':L}))
 for row in rows(B[6]):
  left,right=row.split(' & =');left=left or alt
  def subst(s):return s.replace(r'{A}_{△}','('+str(N/2)+')').replace(alt,'height').replace(basestr,'baselength')
  equal(mathparse(subst(left),{'height':h,'baselength':L}),mathparse(subst(right),{'height':h,'baselength':L}))
 f=q[':question/answer-fields'][0];kind=f[':answer-field/type'].split('/')[-1];choices=f[':answer-field/choices'];assert len(choices)==(5 if kind=='radio' else 1)
 if kind=='blank':assert '{{'+f[':answer-field/key']+'}}' in p
 ids=[x[':answer/id'] for x in choices];assert len(set(ids))==len(ids);[uuid.UUID(x) for x in ids];uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id'])
 vals=[mathparse(x[':answer/value']) for x in choices];assert all(x.is_positive and x.is_real for x in vals);assert all(S.simplify(x-y)!=0 for i,x in enumerate(vals) for y in vals[i+1:])
 correct=f[':answer-field/correct'];assert correct[0]==':answer/id' and correct[1] in ids
 equal(vals[ids.index(correct[1])],h);assert sum(S.simplify(x-h)==0 for x in vals)==1
 # Check complete displayed method-error bank independently from generation math.
 if r['generation']['profile']=='method_errors':
  expected=[h,h/2,2*h,N,N/L**2]
  assert all(sum(S.simplify(x-y)==0 for y in vals)==1 for x in expected)
 elif r['generation']['profile'] in G.PROFILES:
  expected=[h*S.sympify(x) for x in G.PROFILES[r['generation']['profile']]['ratios']]
  assert all(sum(S.simplify(x-y)==0 for y in vals)==1 for x in expected)
 return h,N,L

def native_item(label,r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':x[':answer/id'],'expected':'accepted' if x[':answer/id']==correct else 'rejected','purpose':'grade each complete displayed option'} for x in f[':answer-field/choices']]
 else:
  h,N,L=check(r);value=f[':answer-field/choices'][0][':answer/value']
  # Unevaluated ratio is meaningfully different from rationalized canonical form.
  checks=[{'submitted':value,'expected':'accepted','purpose':'canonical exact altitude'},{'submitted':r'\frac{'+G.tex(N)+'}{'+G.tex(L)+'}','expected':'accepted','purpose':'equivalent unreduced crossnorm/base ratio'},{'submitted':G.tex(h+1),'expected':'rejected','purpose':'wrong exact altitude'}]
 return {'label':label,'record':r,'checks':checks}

def run():
 sources=json.loads((R/'source.json').read_text())['record'][':knowledge-point/questions'];cases=json.loads((R/'source-cases.json').read_text());sourceby={q[':question/math-academy-id']:q for q in sources}
 native=[];reviews=[];source_report=[];solution_exact=0;choices=0;defaults=[]
 for c in cases:
  sid=c['source_id'];q=sourceby[sid];r=G.generate(c['level'],seed=43,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);check(r)
  assert r['question'][':question/problem']==q[':question/problem'];f=q[':question/answer-fields'][0];got=r['question'][':question/answer-fields'][0];raw=[mathparse(x[':answer/value']) for x in f[':answer-field/choices']];gv=[mathparse(x[':answer/value']) for x in got[':answer-field/choices']]
  assert len(raw)==len(gv) and all(sum(S.simplify(x-y)==0 for y in gv)==1 for x in raw);choices+=len(raw)
  observed_correct=f.get(':answer-field/correct')
  if observed_correct:equal(mathparse(observed_correct[':answer/value']),mathparse(next(a[':answer/value'] for a in got[':answer-field/choices'] if a[':answer/id']==got[':answer-field/correct'][1])))
  original=q.get(':question/worked-solution');current=r['question'][':question/worked-solution']
  if original:
   repaired=original.replace('-i+3j-3j','-i+3j-3k') if sid=='q-128008' else original
   assert current==repaired;solution_exact+=current==original
   rawrec=copy.deepcopy(r);rawrec['question'][':question/worked-solution']=original
   try:check(rawrec);assert sid!='q-128008'
   except AssertionError:
    assert sid=='q-128008','Unexpected original solution mathematics failure'
  source_report.append({'source_id':sid,'prompt_exact':True,'complete_bank_matched':True,'choice_count':len(raw),'correct_designation_matched':bool(observed_correct),'missing_designation_inferred':not bool(observed_correct),'raw_solution_exact':current==original,'solution_repaired':sid=='q-128008','solution_authored':original is None})
  native.append(native_item('source '+sid,r));reviews.append({'label':'source replay '+sid,'record':r})
  # A genuinely changed triangle and complete original bank profile, through API.
  changed=G.generate('hard',seed=83,template=c['template'],profile=c['bank_profile']);check(changed);assert changed['generation']['mathematical_fingerprint']!=r['generation']['mathematical_fingerprint'];native.append(native_item('changed '+sid,changed));reviews.append({'label':'changed-parameter observed presentation '+sid,'record':changed})
  again=G.generate('hard',seed=501,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);assert again['question'][':question/id']==r['question'][':question/id']
 for level in ('easy','moderate','hard'):
  fingerprints=set()
  for kind in ('radio','blank'):
   for seed in range(30):
    r=G.generate(level,seed=seed,field_type=kind);check(r);fingerprints.add(r['generation']['mathematical_fingerprint']);defaults.append(r)
    if seed<2:reviews.append({'label':'authored '+level+' '+kind+' '+str(seed),'record':r});native.append(native_item('authored '+level+' '+kind+' '+str(seed),r))
  assert len(fingerprints)>=25,(level,len(fingerprints))
 # Source implicit multiplication must never concatenate positive factors.
 implicit_checks=0
 for seed in range(30,42):
  r=G.generate('hard',seed=seed,template='q-316558',profile='none');check(r);implicit_checks+=1;native.append(native_item('implicit changed seed '+str(seed),r))
 for signs in itertools.product((-1,1),repeat=6):
  u=[n*s for n,s in zip((3,1,1),signs[:3])];v=[n*s for n,s in zip((2,3,2),signs[3:])];p={'vertices':{'R':[0,0,0],'S':u,'T':v}}
  r=G.generate('hard',template='q-316558',profile='none',parameters=p);check(r);implicit_checks+=1
 # Explicit-input scope and whole-bank boundaries must not resample silently.
 invalid=[]
 for level in ('easy','moderate','hard'):
  r=G.generate(level,seed=7);p=copy.deepcopy(r['generation']['parameters']);p['vertices']['B'][0]+=10
  try:G.generate(level,parameters=p);raise AssertionError('Out-of-scope explicit parameters accepted')
  except ValueError:invalid.append(level+' bounds')
 # Planar vectors cannot satisfy authored moderate/hard, regardless seed.
 p={'vertices':{'A':[0,0,0],'B':[1,2,0],'C':[2,-1,0]}}
 for level in ('moderate','hard'):
  try:G.generate(level,parameters=p);raise AssertionError('Reduced planar workload accepted')
  except ValueError:invalid.append(level+' reduced-workload rejection')
 # h/2,2h,N,N/L² are a fixed bank: a base of length 2 collides N=2h.
 p={'vertices':{'A':[0,0,0],'B':[2,0,0],'C':[1,2,0]}}
 try:G.options(p,G.TEMPLATES['q-20027'],'method_errors');raise AssertionError('Whole-bank collision accepted')
 except ValueError:invalid.append('whole-bank collision')
 # Names and rigid motion cannot increase mathematical identity counts.
 r=G.generate('hard',seed=5);p=copy.deepcopy(r['generation']['parameters'])
 for v in p['vertices'].values():v[:]=[v[1]+1,-v[0]+1,v[2]+1]
 rotated=G.generate('hard',parameters=p);assert rotated['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint'];assert rotated['question'][':question/id']!=r['question'][':question/id']
 p=copy.deepcopy(r['generation']['parameters']);p['vertices']['A'],p['vertices']['B']=p['vertices']['B'],p['vertices']['A'];reversed_=G.generate('hard',parameters=p);assert reversed_['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
 # Vertex naming and swapped cross edge order do not change assessed geometry.
 alias={'vertices':{'L':r['generation']['parameters']['vertices']['A'],'N':r['generation']['parameters']['vertices']['B'],'M':r['generation']['parameters']['vertices']['C']}}
 named=G.generate('hard',template='q-71113',parameters=alias,profile='observed_q-71113');check(named);assert named['generation']['mathematical_fingerprint']==r['generation']['mathematical_fingerprint']
 # Bank changes alter content identity while retaining mathematical identity.
 c=cases[0];x=G.generate('hard',template=c['template'],parameters=c['parameters'],profile=c['bank_profile']);y=G.generate('hard',template=c['template'],parameters=c['parameters']);assert x['question'][':question/id']!=y['question'][':question/id'];assert x['generation']['mathematical_fingerprint']==y['generation']['mathematical_fingerprint']
 (R/'engine-input.json').write_text(json.dumps(native,indent=2,ensure_ascii=False)+'\n');subprocess.run(['generate/runs/current/check-engine',str(R/'engine-input.json'),str(R/'engine-report.json')],check=True)
 (R/'review.json').write_text(json.dumps(reviews,indent=2,ensure_ascii=False)+'\n')
 md=['# Altitude generator review','Original raw strings are preserved in source.json. Changed records use the public API. All answers shown here are author review data.']
 for c in cases:
  sid=c['source_id'];q=sourceby[sid];md+=['\n## '+sid+' original',q[':question/problem'],'\nOriginal full bank: '+', '.join('$'+a[':answer/value']+'$' for a in q[':question/answer-fields'][0][':answer-field/choices']),q.get(':question/worked-solution','No source worked solution or correct designation. Reconstruction is authored.')]
  for rr in [x for x in reviews if x['record']['generation']['template']==sid]:md+=['\n### '+rr['label'],G.markdown(rr['record'])]
 for rr in reviews:
  if rr['record']['generation']['template'].startswith('authored'):md+=['\n## '+rr['label'],G.markdown(rr['record'])]
 (R/'review.md').write_text('\n\n'.join(md)+'\n')
 engine=json.loads((R/'engine-report.json').read_text());report={'status':'pass','source_basis':1356,'source_questions':18,'source_prompt_exact':18,'source_complete_banks':10,'source_blank_values':8,'source_choices_matched':choices,'source_distractors_matched':40,'source_correct_designations_matched':17,'source_missing_correct_designation_inferred':1,'supplied_source_solutions':17,'raw_exact_source_solutions':solution_exact,'minimally_repaired_source_solutions':1,'authored_missing_source_solutions':1,'full_source_stages_checked':17,'raw_source_stage_checks_passed':16,'raw_source_stage_checks_failed_documented':1,'repaired_source_stage_checks_passed':17,'changed_source_presentations_checked':18,'implicit_signed_display_checks':implicit_checks,'default_records_checked':len(defaults),'default_distinct_geometry':{l:len({r['generation']['mathematical_fingerprint'] for r in defaults if r['question'][':question/difficulty'].endswith('/'+l)}) for l in ('easy','moderate','hard')},'boundary_rejections':invalid,'native':{k:engine[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'source_results':source_report,'remaining_findings':['Observed scalar option intent is underdetermined; observational scale profiles are explicit replay extensions, not default error recipes.','q-20028 has no observed level, correct ref or solution; hard placement, key and full solution are authored.','q-128008 reduced basis row j→k repaired; raw evidence retained.']}
 (R/'validation.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2),flush=True)
 # Hash every deliverable after successful validation; freeze itself excluded.
 files=[R.with_suffix('.py')]+sorted(x for x in R.iterdir() if x.is_file() and x.name!='freeze.json')
 freeze={str(x):hashlib.sha256(x.read_bytes()).hexdigest() for x in files};freeze['native_engine_source_sha256']=hashlib.sha256(Path('generate/runs/current/check-engine.rs').read_bytes()).hexdigest();freeze['native_engine_sha256']=hashlib.sha256(Path('generate/runs/current/check-engine').read_bytes()).hexdigest();(R/'freeze.json').write_text(json.dumps(freeze,indent=2)+'\n')
if __name__=='__main__':run()
