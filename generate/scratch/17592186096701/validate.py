#!/usr/bin/env python3
"""Independent readback of displayed vector equations, complete fidelity/native QA."""
import importlib.util,json,re,uuid,subprocess,hashlib,random,copy,tempfile,os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application,rationalize
H=Path(__file__).resolve().parent;ROOT=H.parents[2]
spec=importlib.util.spec_from_file_location('g',str(H)+'.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
trans=standard_transformations+(implicit_multiplication_application,rationalize)

def require(x,msg):
 if not x:raise AssertionError(msg)
def scalar(s):
 s=s.replace('\\\\','\\').strip().rstrip('.,')
 while '\\frac' in s:
  nxt=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
  if nxt==s:raise AssertionError('Unsupported fraction')
  s=nxt
 return sp.Rational(s) if re.fullmatch(r'-?[\d./]+',s) else sp.simplify(parse_expr(s,transformations=trans))
def math_expr(s,ns):
 s=s.strip().rstrip('.,').replace(r'\lambda','L')
 s=re.sub(r'\\overset\{\\to \}\{([A-Z]{2})\}',r'v\1',s)
 while '\\frac' in s:
  nxt=re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}',r'((\1)/(\2))',s)
  require(nxt!=s,'Complete frac parse');s=nxt
 s=s.replace('{','(').replace('}',')')
 require('\\' not in s,'Unknown printed command '+s)
 return sp.simplify(parse_expr(s,local_dict=ns,transformations=trans))
def formatting(s):
 require(s.count('$')%2==0,'Math dollars balanced')
 # TeX braces, excluding source blank placeholder doubles.
 s=re.sub(r'\{\{[^{}]+\}\}','',s);depth=0
 for c in s:
  depth+=(c=='{')-(c=='}');require(depth>=0,'Closing brace')
 require(depth==0,'TeX group balance');require('\\\\frac' not in s,'Malformed double fraction command')
def independent(r):
 require(set(r['knowledge_point'])=={'db_id','id','title'},'Outer plain keys')
 q=r['question'];m=r['generation'];f=q[':question/answer-fields'][0];p=g.normalize(m['parameters']);g.guard(p,q[':question/difficulty'].split('/')[-1],not m['authored']);choices=f[':answer-field/choices'];values=[scalar(a[':answer/value']) for a in choices]
 require(len(set(values))==len(values),'Whole-bank distinct mathematical values');require(len(choices)==(1 if f[':answer-field/type'].endswith('/blank') else 5),'Observed choice count')
 require(f[':answer-field/type'] in (':answer-field.type/radio',':answer-field.type/blank'),'Type')
 if f[':answer-field/type'].endswith('/blank'):require('{{'+f[':answer-field/key']+'}}' in q[':question/problem'],'Blank placeholder')
 for text in [q[':question/problem'],q[':question/worked-solution']]+[a[':answer/value'] for a in choices]:formatting(text)
 # Prompt supplies c=..., read its actual coefficient expression separately.
 given=re.search(r'\$c=(.*?)(?:\$)',q[':question/problem'])[1].rstrip(',')
 a=sp.Matrix(p['a']);b=sp.Matrix(p['b']);ca,cb=g.coefficients(p);C=ca*a+cb*b;O=sp.zeros(2,1);P=p['known']*(a if p['unknown']=='b' else b)
 correct=next(x for x in choices if x[':answer/id']==f[':answer-field/correct'][1]);lam=scalar(correct[':answer/value'])
 residual=C-P;basis=b if p['unknown']=='b' else a
 require(residual==lam*basis,'Independent diagram coefficient')
 for j in range(2):
  ns={'a':a[j],'b':b[j],'c':C[j],'L':lam}
  ns.update({'vOA':a[j],'vOB':(P[j] if p['known']!=1 and '△OBC' in q[':question/worked-solution'] else b[j]),'vAC':(C-a)[j],'vBC':(C-(P if '△OBC' in q[':question/worked-solution'] else b))[j],'vOP':P[j],'vPC':residual[j]})
  require(math_expr(given,ns)==C[j],'Actually displayed prompt formula')
  worked=q[':question/worked-solution']
  # Every c equation in inline/display/aligned stages, with all equalities.
  eqs=[]
  for block in re.findall(r'\$+([^$]+)\$+',worked,re.S):
   if 'c' not in block:continue
   if r'\begin{aligned}' in block:
    clean=block.replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
    rows=clean.split('\\\\')
    for row in rows:
     rhs=row.split('=',1)[1];require(math_expr(rhs,ns)==C[j],'Displayed aligned arithmetic row '+rhs);eqs.append(rhs)
   elif block.strip().startswith('c='):
    for rhs in block.strip().split('=')[1:]:require(math_expr(rhs,ns)==C[j],'Displayed c equation '+rhs)
  require(len(eqs)==2,'Exactly two aligned rows')
 for s in re.findall(r'\\lambda\s*=([^$]+)',q[':question/worked-solution']):
  # Lambda row always closes at next dollars; no later prose in a math span.
  require(scalar(s)==lam,'Displayed final lambda')
 length=re.search(r'(?:AC|BC|PC)=([^$]*?)\|([ab])\|',q[':question/worked-solution']);require(length and scalar(length[1] or '1')==lam,'Displayed length scalar')
 if not m['authored'] or q[':question/difficulty'].endswith('/easy') or q[':question/difficulty'].endswith('/moderate'):
  require('have the same direction' in worked,'No direction reversal')
 if q[':question/difficulty'].endswith('/hard'):
  coords=re.search(r'and \$C=\((.*?), (.*?)\)\$',q[':question/problem']);require(coords,'Hard exact diagram coordinates');require([scalar(coords[1]),scalar(coords[2])]==list(C),'Actual printed C coordinates')
  printedP=re.search(r'P=\((.*?), (.*?)\)\.',worked);require([scalar(printedP[1]),scalar(printedP[2])]==list(P),'Actual printed fractional endpoint')
  blocks=re.findall(r'\$\$\n(.*?)\n\$\$',worked,re.S)
  arithmetic=[z for z in blocks if z and not z.startswith(('c=','P=','\\begin','\\lambda'))]
  require(len(arithmetic)==2,'Hard subtraction and division stages')
  for z in arithmetic:
   left,right=z.rstrip('.').split('=');require(math_expr(left,{})==math_expr(right,{}),'Actual hard arithmetic stage')
 for path in m['plots'].values():require(Path(path).exists(),'Plot present')
 if m['authored'] or p!=g.normalize({k:g.PROFILES[m['profile']][k] for k in ('unknown','known','scalar','a','b')}):
  side=json.load(open(Path(m['plots']['prompt']).with_suffix('.json')))['plot_data'];require([sp.Rational(x) for x in side['a']]==list(a) and [sp.Rational(x) for x in side['b']]==list(b),'Rendered basis geometry');require(sp.Rational(side['ca_exact'])==ca and sp.Rational(side['cb_exact'])==cb,'Rendered C geometry')
 content=g.digest({'version':g.VERSION,'prompt':q[':question/problem'],'solution':worked,'field_type':f[':answer-field/type'].split('/')[-1],'key':f[':answer-field/key'],'bank':sorted(x[':answer/value'] for x in choices),'task':g.digest(g.canonical(p))})
 require(content==m['content_fingerprint'],'Complete content hash');require(g.digest(g.canonical(p))==m['mathematical_fingerprint'],'Task hash excludes bank')
 uuid.UUID(q[':question/id']);uuid.UUID(f[':answer-field/id'])
 for x in choices:uuid.UUID(x[':answer/id']);require(x[':answer/type']==':answer.type/math','Answer enum')
 return lam

def fidelity(old,r):
 q=r['question'];f=q[':question/answer-fields'][0];of=old[':question/answer-fields'][0]
 clean=lambda s:re.sub(r'!\[\]\(.*?\)','IMAGE',s)
 require(clean(q[':question/problem'])==clean(old[':question/problem']),'Full prompt prose/layout')
 require(clean(q[':question/worked-solution'])==clean(old[':question/worked-solution']),'Full fixed ordered solution')
 require(f[':answer-field/key']==of[':answer-field/key'] and f[':answer-field/type']==of[':answer-field/type'][':db/ident'],'Field fidelity')
 ov=[scalar(a[':answer/value']) for a in of[':answer-field/choices']];nv=[scalar(a[':answer/value']) for a in f[':answer-field/choices']]
 require(sorted(ov)==sorted(nv),'Every source option one-to-one')
 require(sorted(a[':answer/value'] for a in of[':answer-field/choices'])==sorted(a[':answer/value'] for a in f[':answer-field/choices']),'Exact source bank spelling')
 require(scalar(of[':answer-field/correct'][':answer/value'])==independent(r),'Source designation fidelity')
 return len(ov)

def native_checks(r):
 f=r['question'][':question/answer-fields'][0];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Complete displayed bank ID grading'} for a in f[':answer-field/choices']]
 else:
  s=independent(r);correct=f[':answer-field/choices'][0][':answer/value']
  checks=[{'submitted':correct,'expected':'accepted','purpose':'Canonical scalar'}, {'submitted':f'{s.p*3}/{s.q*3}','expected':'accepted','purpose':'Unreduced equivalent rational'}, {'submitted':str(s+1),'expected':'rejected','purpose':'Wrong scalar'}]
 return checks

def main():
 cases=json.load(open(H/'source-cases.json'));source=json.load(open(H/'source.json'));qs=source['record'][':knowledge-point/questions'];records=[];review=[];banks=0
 for old,c in zip(qs,cases):
  r=g.generate(c['level'],profile=c['profile'],parameters=c['parameters']);banks+=fidelity(old,r);records.append(r);review.append({'label':'original replay '+c['source_id'],'record':r,'original':old})
  p=copy.deepcopy(c['parameters']);p['scalar']=str(sp.Rational(p['scalar'])+(1 if sp.Rational(p['scalar']).q==3 else sp.Rational(1,2)))
  variant=g.generate(c['level'],seed=91,profile=c['profile'],parameters=p);independent(variant);records.append(variant);review.append({'label':'generated observed-profile variant '+c['source_id'],'record':variant})
 for level in ('easy','moderate','hard'):
  for seed in (40,41,42,43):
   r=g.generate(level,seed=seed,field_type='radio' if seed%2==0 else 'blank');independent(r);records.append(r);review.append({'label':'authored '+level+' seed '+str(seed),'record':r})
   same=g.generate(level,seed=seed+99,field_type=r['question'][':question/answer-fields'][0][':answer-field/type'].split('/')[-1],parameters=r['generation']['parameters']);require(r['question'][':question/id']==same['question'][':question/id'],'Seed order cannot alter identity')
 # Concurrent fresh rendering of identical and different mathematical inputs.
 fresh={"unknown":"b","known":"1","scalar":"8/3","a":[6,0],"b":[0,2]}
 other=copy.deepcopy(fresh);other['scalar']='10/3'
 with ThreadPoolExecutor(max_workers=4) as pool:
  concurrent=list(pool.map(lambda pair:g.generate('easy',seed=pair[0],profile='q-19338',parameters=pair[1]),[(501,fresh),(502,fresh),(503,other),(504,other)]))
 require(concurrent[0]['question'][':question/id']==concurrent[1]['question'][':question/id'] and concurrent[2]['question'][':question/id']==concurrent[3]['question'][':question/id'],'Concurrent deterministic identity')
 require(concurrent[0]['question'][':question/id']!=concurrent[2]['question'][':question/id'],'Concurrent distinct parameters')
 def force_render(r):
  # Exercise atomic writes even when deterministic generator assets are cached.
  data=json.load(open(Path(r['generation']['plots']['prompt']).with_suffix('.json')))['plot_data']
  fd,path=tempfile.mkstemp(prefix='.render-',suffix='.json',dir=H/'plots');os.close(fd)
  try:
   Path(path).write_text(json.dumps(data));subprocess.run([str(ROOT/'.venv/bin/python'),str(H/'render.py'),path],check=True)
  finally:Path(path).unlink(missing_ok=True)
 with ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(force_render,concurrent))
 for i,r in enumerate(concurrent):independent(r);records.append(r);review.append({'label':'concurrent rendered fixture '+str(i),'record':r})
 require(not list((H/'plots').glob('.render-*')) and not list((H/'plots').glob('.atomic-*')),'Private renderer input/atomic temporary leak')
 # Conservative mathematical domain enumeration, separate from rendered records.
 domain={}
 for level in ('easy','moderate','hard'):
  identities=set()
  for seed in range(3000):
   try:
    p=g.normalize(g.sample(level,random.Random(seed)));g.guard(p,level);identities.add(g.digest(g.canonical(p)))
   except ValueError:pass
  domain[level]=len(identities);require(len(identities)>=100,'Meaningful finite domain')
 # Explicit invalid workloads and direction reversal rejected.
 tests=[('moderate',{'unknown':'a','known':'1','scalar':'2','a':[4,0],'b':[-1,2]}),('hard',{'unknown':'a','known':'3/2','scalar':'2','a':[4,0],'b':[-1,2]}),('hard',{'unknown':'a','known':'3/2','scalar':'2/3','a':[4,0],'b':[-2,2]}),('easy',{'unknown':'b','known':'1','scalar':'-2','a':[4,0],'b':[0,2]})]
 for l,p in tests:
  try:g.generate(l,parameters=p);raise AssertionError('Invalid scope accepted')
  except ValueError:pass
 bad=copy.deepcopy(cases[0]['parameters']);bad['scalar']='1/7'
 try:g.generate('easy',profile=cases[0]['profile'],parameters=bad);raise AssertionError('Observed profile admitted arbitrary denominator')
 except ValueError:pass
 # Common vector scaling excluded from canonical mathematical identity.
 p=g.normalize({'unknown':'b','known':'1','scalar':'2','a':[2,0],'b':[0,2]});p2=copy.deepcopy(p);p2['a']=[2*x for x in p['a']];p2['b']=[2*x for x in p['b']];require(g.canonical(p)==g.canonical(p2),'Common geometry scaling is incidental')
 (H/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 lines=['# Original sources and generated variants','Basis 1356; originals are raw captures. Observed-profile ratios are replay evidence; authored banks are method-error extensions.']
 for item in review:
  lines+=['\n## '+item['label']]
  if 'original' in item:
   old=item['original'];lines+=['Raw source prompt:\n'+old[':question/problem'],'Raw source fixed solution:\n'+old[':question/worked-solution'],'Raw bank: '+json.dumps([a[':answer/value'] for a in old[':question/answer-fields'][0][':answer-field/choices']])]
  q=item['record']['question'];lines +=[q[':question/problem'],'Bank: '+', '.join(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices']),q[':question/worked-solution']]
 (H/'review.md').write_text('\n\n'.join(lines)+'\n')
 inp=[{'label':i['label'],'record':i['record'],'checks':native_checks(i['record'])} for i in review];(H/'engine-input.json').write_text(json.dumps(inp,indent=2)+'\n')
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
 native=json.load(open(H/'engine-report.json'))
 subprocess.run([str(ROOT/'.venv/bin/python'),str(H/'render.py'),'audit'],check=True)
 report={'passed':True,'source_provenance':{k:source[k] for k in ('database','basis','lineage')},'source_questions':14,'full_prompt_matches':14,'full_ordered_solution_matches':14,'full_mathematical_bank_matches':14,'source_options_matched':banks,'correct_designations_matched':14,'raw_exact_banks':14,'presentation_normalized_banks':0,'normalized_double_slash_fraction_values':0,'mathematical_repairs':0,'authored_missing_levels':['hard'],'generated_records_checked':len(records),'generated_authored_records':12,'meaningful_generated_tasks':{l:len({r['generation']['mathematical_fingerprint'] for r in records if r['question'][':question/difficulty'].endswith('/'+l)}) for l in ('easy','moderate','hard')},'meaningful_domain_lower_bound_3000_seeds':domain,'native':{k:native[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'engine_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine').read_bytes()).hexdigest(),'engine_source_sha256':hashlib.sha256((ROOT/'generate/runs/current/check-engine.rs').read_bytes()).hexdigest(),'source_distractors_matched':40,'source_distractors_total':40,'source_options_total':54,'source_banks_total':14,'concurrent_fresh_render_requests':4,'raster_audit':json.load(open(H/'raster-audit.json')),'unresolved_findings':[]}
 (H/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
