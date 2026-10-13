#!/usr/bin/env python3
"""Read displayed TeX independently, replay every source, invoke real grader.

Run with --write-evidence only before manifest freeze. No transactions.
"""
import argparse,concurrent.futures,hashlib,importlib.util,json,re,subprocess,sys,tempfile
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
from PIL import Image
H=Path(__file__).resolve().parent
S=importlib.util.spec_from_file_location('tall_ellipse',H.with_suffix('.py'));g=importlib.util.module_from_spec(S);S.loader.exec_module(g)
X,Y,A,B=sp.symbols('x y a b')

def fail(assertion,message):
 if not assertion:raise AssertionError(message)

def parse(s):
 """Recursive fraction/group reader of actual displayed source/generated math."""
 s=s.strip().rstrip('.')
 def convert(t):
  result='';i=0
  def group(j):
   fail(j<len(t) and t[j]=='{','Expected TeX group '+t)
   depth=1;k=j+1
   while k<len(t) and depth:
    if t[k]=='{':depth+=1
    if t[k]=='}':depth-=1
    k+=1
   fail(depth==0,'Unbalanced TeX');return t[j+1:k-1],k
  while i<len(t):
   if t.startswith('\\frac',i):
    n,j=group(i+5);d,i=group(j);result+='(('+convert(n)+')/('+convert(d)+'))'
   elif t[i]=='{':
    z,i=group(i);result+='('+convert(z)+')'
   elif t[i]=='^':result+='**';i+=1
   else:result+=t[i];i+=1
  return result
 return parse_expr(convert(s),local_dict={'x':X,'y':Y,'a':A,'b':B},transformations=standard_transformations+(implicit_multiplication_application,))

def residual(s):
 parts=s.replace('&','').strip().rstrip('.').split('=')
 fail(len(parts)==2,'Full displayed equation required '+s)
 return sp.expand(parse(parts[0])-parse(parts[1]))

def same_equation(e,target):
 ratio=sp.cancel(e/target)
 return not ratio.has(X,Y) and ratio!=0

def formatting(s):
 fail(s.count('$')%2==0,'Unbalanced math delimiter')
 n=0
 for c in s:
  if c=='{':n+=1
  elif c=='}':n-=1
  fail(n>=0,'Unbalanced TeX groups')
 fail(n==0,'Unbalanced TeX groups')
 fail('--' not in s and '+-' not in s,'Ungrouped sign')

def displayed_math(r):
 q=r['question'];m=r['generation'];fail(m['evidence_only']==(m['source_id'] is not None),'Evidence eligibility separation');fail(m['eligible_for_learning']==(m['source_id'] is None),'Opaque/source learning eligibility');f=q[':question/answer-fields'][0];a,b=map(sp.Rational,(m['parameters']['a'],m['parameters']['b']))
 fail(set(r['knowledge_point'])=={'db_id','id','title'},'Outer knowledge_point shape')
 fail(r['knowledge_point']['db_id']==g.KP_ID and r['knowledge_point']['id']==g.KP_UUID,'KP identity')
 fail(a<b and (a,b) in g.domain(q.get(':question/difficulty',':question.difficulty/easy').split('/')[-1]),'Workload scope')
 for s in [q[':question/problem'],q.get(':question/worked-solution','')]+[v[':answer/value'] for v in f[':answer-field/choices']]:formatting(s)
 if f[':answer-field/type'].endswith('/blank'):fail('{{'+f[':answer-field/key']+'}}' in q[':question/problem'],'Missing supplied blank fragment')
 target=X**2/a**2+Y**2/b**2-1
 equations=[]
 for ans in f[':answer-field/choices']:
  s=ans[':answer/value'];e=residual(s) if '=' in s else parse(s)-1
  equations.append((ans[':answer/id'],e))
 for i,(_,e) in enumerate(equations):
  for _,other in equations[i+1:]:fail(not same_equation(e,other),'Equivalent displayed options')
 correct=[uid for uid,e in equations if same_equation(e,target)]
 fail(len(correct)==1,'Exactly one geometrically correct displayed option')
 if ':answer-field/correct' in f:fail(f[':answer-field/correct']==[':answer/id',correct[0]],'Incorrect correct lookup ref')
 if ':question/worked-solution' in q:
  sol=q[':question/worked-solution'];am=re.search(r'length \$a=(.*?)\$',sol)[1];bm=re.search(r'length \$b=(.*?)\.\$',sol)[1]
  fail(parse(am)==a and parse(bm)==b,'Stale solution radius prose')
  aligned=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',sol,re.S)[1];rows=aligned.split(r'\\')
  fail(len(rows)==(3 if a.q==1 and b.q==1 else 4),'Mathematical stage count')
  fail('a' in rows[0] and 'b' in rows[0] and rows[0].count('^{2}')==4,'Missing formal stage')
  fail(rows[1].count('^{2}')==4,'Substitution must retain radius powers')
  if len(rows)==4:fail(rows[2].count('^{2}')==2 and rows[2]!=rows[-1],'Keep fractional square evaluation separately')
  for row in rows:
   fail(same_equation(residual(row).subs({A:a,B:b}),target),'Wrong displayed solution equation '+row)
  for p in [(a,0),(-a,0),(0,b),(0,-b)]:fail(sp.simplify(target.subs({X:p[0],Y:p[1]}))==0,'Geometry check')
 asset=m['plot']
 if not asset['original']:
  side=json.loads(Path(asset['sidecar']).read_text());fail(side['a']==str(a) and side['b']==str(b),'Plot sidecar mismatch')
  im=Image.open(asset['path']).convert('RGB');blue=[]
  for y in range(im.height):
   for x in range(im.width):
    rr,gg,bb=im.getpixel((x,y))
    if bb>rr*1.6 and gg>rr*1.5 and rr<100:blue.append((x,y))
  fail(len(blue)>150,'Curve raster missing')
  # Independent pixel extents recover ellipse ratio despite arrow/label styles.
  xmin,xmax=min(x for x,y in blue),max(x for x,y in blue);ymin,ymax=min(y for x,y in blue),max(y for x,y in blue)
  fail(abs((xmax-xmin)/(ymax-ymin)-float(a/b))<.025,'Raster ellipse scales do not match displayed answer')
 return True

def checks(r):
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  return [{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'full mathematically independently checked option selection'} for a in f[':answer-field/choices']]
 a,b=map(sp.Rational,(r['generation']['parameters']['a'],r['generation']['parameters']['b']))
 return [{'submitted':next(z[':answer/value'] for z in f[':answer-field/choices'] if z[':answer/id']==correct),'expected':'accepted','purpose':'canonical source fragment'},
 {'submitted':f'x*x/({a*a})+y*y/({b*b})','expected':'accepted','purpose':'actual repeated-product equivalent fragment'},
 {'submitted':f'x*x/({b*b})+y*y/({a*a})','expected':'rejected','purpose':'swapped radius fragment'}]

def run(write=False):
 cases=[];replays=[];native=[];detail=[];banks=options=designations=solutions=0
 for sid,q in g.RECORDS.items():
  level=q.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/easy').split('/')[-1];params=dict(zip(('a','b'),map(str,g.SOURCE_GEOMETRY[sid])))
  r=g.generate(level,parameters=params,profile=sid);z=r['question'];displayed_math(r)
  vals=lambda w:sorted(a[':answer/value'] for a in w[':question/answer-fields'][0][':answer-field/choices'])
  fail(vals(q)==vals(z),'Source bank string mismatch '+sid)
  fail(q[':question/problem']==z[':question/problem'],'Source prompt mismatch '+sid)
  fail(q.get(':question/worked-solution')==z.get(':question/worked-solution'),'Full source prose/stage mismatch '+sid)
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):fail((key in q)==(key in z),'Source attribute presence mismatch '+sid+key)
  sf=q[':question/answer-fields'][0];zf=z[':question/answer-fields'][0]
  for key in (':answer-field/correct',':answer-field/type',':answer-field/key',':answer-field/choices'):fail((key in sf)==(key in zf),'Source field attribute presence mismatch '+sid+key)
  fail(sf[':answer-field/key']==zf[':answer-field/key'] and sf[':answer-field/type'][':db/ident']==zf[':answer-field/type'],'Source field shape')
  if ':answer-field/correct' in sf:
   cv=sf[':answer-field/correct'][':answer/value'];zcv=next(x[':answer/value'] for x in zf[':answer-field/choices'] if x[':answer/id']==zf[':answer-field/correct'][1]);fail(cv==zcv,'Source correct designation mismatch');designations+=1
   native.append({'label':'Original '+sid,'record':r,'checks':checks(r)})
  banks+=1;options+=len(vals(q));solutions+=(':question/worked-solution' in q)
  cases.append({'source_id':sid,'source_db_id':q[':db/id'],'template':r['generation']['template'],'level':level,'difficulty_assignment':'authored easy inference' if sid=='q-7605' else 'observed','parameters':params,'bank_profile':sid,'raw_omissions':[k for k in (':question/difficulty',':question/worked-solution') if k not in q]})
  replays.append(r);detail.append({'source_id':sid,'bank_count':len(vals(q)),'exact_prompt':True,'exact_solution':q.get(':question/worked-solution')==z.get(':question/worked-solution'),'correct_designation_present':':answer-field/correct' in sf,'attribute_presence_parity':True})
 # Every observed bank gets a genuinely changed public parameter instance.
 changed=[]
 for case in cases:
  pair=None
  for a,b in g.domain(case['level']):
   if (a,b)==tuple(map(sp.Rational,case['parameters'].values())):continue
   try:r=g.generate(case['level'],seed=41,profile=case['source_id'],parameters={'a':str(a),'b':str(b)})
   except ValueError:continue
   pair=(a,b);break
  fail(pair is not None,'No changed profile instance');displayed_math(r);changed.append(r)
 generated=[]
 for l in ('easy','moderate','hard'):
  for i in (2,13):
   r=g.generate(l,seed=i);displayed_math(r);generated.append(r);native.append({'label':'Generated '+l+' '+str(i),'record':r,'checks':checks(r)})
 repair=g.generate('easy',parameters={'a':3,'b':4},profile='repair-q-7605');displayed_math(repair);generated.append(repair);native.append({'label':'Supported repair q-7605','record':repair,'checks':checks(repair)})
 # Deterministic identity independent of seed; same displayed bank = same identity.
 for l in ('easy','moderate','hard'):
  for t,(tl,_) in g.TEMPLATES.items():
   if tl!=l:continue
   p={'a':str(g.domain(l)[-1][0]),'b':str(g.domain(l)[-1][1])};rs=[g.generate(l,seed=s,template=t,parameters=p) for s in (0,1,22)]
   fail(len({r['question'][':question/id'] for r in rs})==1,'Seed changes content identity')
   for r in rs:displayed_math(r)
 positions=[]
 for seed in range(12):
  rr=g.generate('easy',seed=seed,template='integer_radio',parameters={'a':3,'b':7});ff=rr['question'][':question/answer-fields'][0];positions.append(next(i for i,z in enumerate(ff[':answer-field/choices']) if z[':answer/id']==ff[':answer-field/correct'][1]))
 fail(len(set(positions))>2,'Choice shuffling does not move correct option')
 rradio=g.generate('easy',template='integer_radio',parameters={'a':3,'b':7});rblank=g.generate('easy',template='integer_blank',parameters={'a':3,'b':7})
 fail(rradio['generation']['mathematical_fingerprint']==rblank['generation']['mathematical_fingerprint'],'Layouts inflated mathematical task counts')
 fail(rradio['question'][':question/id']!=rblank['question'][':question/id'],'Different displayed field/bank identity collapsed')
 # Enumerate finite exact math domains without rendering hundreds of figures.
 for level in ('easy','moderate','hard'):
  pairs=g.domain(level);fail(len(pairs)==len(set(pairs)),'Rational alias overcount')
  if level=='easy':
   for a,b in pairs:g.bank_pairs('authored',a,b)
 for level,p in [('easy',{'a':0,'b':3}),('easy',{'a':2,'b':2}),('moderate',{'a':2,'b':4}),('hard',{'a':'3/2','b':'7/2'}),('hard',{'a':'100/3','b':'103/3'})]:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('Invalid explicit workload accepted '+level+str(p))
 # Fresh concurrent calls: unique inputs and atomic writes for identical and
 # different figures; private QA directory assets are retained, never pruned.
 rp=H/'plots';qa=H/'concurrency';qa.mkdir(exist_ok=True)
 inputs=[]
 for i,(a,b) in enumerate([('7/3','17/4'),('7/3','17/4'),('5/4','13/3')]):
  spec={'a':a,'b':b,'renderer_version':3,'equal_scale':True,'width':480,'height':400,'origin':[0,0],'intercepts':[[a,'0'],['-'+a,'0'],['0',b],['0','-'+b]],'bounds':[-float(sp.Rational(b))*1.2,float(sp.Rational(b))*1.2,-float(sp.Rational(b))*1.2,float(sp.Rational(b))*1.2]}
  stem='same' if i<2 else 'different';path=qa/f'input-{i}.json';path.write_text(json.dumps({'spec':spec,'png':str(qa/(stem+'.png')),'sidecar':str(qa/(stem+'.json'))}));inputs.append(path)
 def render(p):subprocess.run([sys.executable,str(H/'render.py'),str(p)],check=True,capture_output=True)
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(render,inputs))
 for p in inputs:p.unlink()
 fail(not list(qa.glob('atomic-*')),'Atomic render temporary leak')
 for stem,a in [('same','7/3'),('different','5/4')]:fail(json.loads((qa/(stem+'.json')).read_text())['a']==a,'Concurrent renderer crossed parameters')
 engine=H.parents[1]/'runs/current/check-engine';fail(engine.exists(),'Native engine unavailable')
 with tempfile.TemporaryDirectory(prefix='ellipse-grade-') as temp:
  inp=Path(temp)/'input.json';out=Path(temp)/'report.json';inp.write_text(json.dumps(native));p=subprocess.run([str(engine),str(inp),str(out)],check=True,capture_output=True,text=True);report=json.loads(out.read_text())
  if write:(H/'native-grading-input.json').write_text(json.dumps(native,indent=2)+'\n');(H/'native-grading.json').write_text(json.dumps(report,indent=2)+'\n')
 result={'passed':True,'source_provenance':g.PROVENANCE,'source_questions':len(cases),'source_banks':{'matched':banks,'total':len(cases)},'source_options':{'matched':options,'total':options},'source_correct_designations':{'matched':designations,'total_present':designations,'missing':1},'source_worked_solutions':{'exact':solutions,'total_present':solutions,'missing':1},'raw_source_attribute_presence_matches':len(cases),'source_repairs':{'q-7605':'infer easy/correct/solution and replace incorrect bottom +4 label by -4; raw original remains publicly replayable'},'changed_parameter_source_profiles_checked':len(changed),'generated_examples':len(generated),'finite_mathematical_tasks':{l:len(g.domain(l)) for l in ('easy','moderate','hard')},'native_grading':{k:report[k] for k in ('accepted_checks','rejected_checks','documented_unresolved_checks')},'plot_concurrency':'fresh same/different parameter atomic writes passed','findings':['q-7605 raw source lacks difficulty, correct designation, and solution; bottom plot label is +4','q-73627 and q-7605 contain opaque distractor operations; q-73631 decrement-radius interpretation remains uncertain; these banks are evidence-only by default','No observed hard source; thirds/quarters hard workload is authored, not recovered'],'source_details':detail}
 if write:
  (H/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(H/'validation.json').write_text(json.dumps(result,indent=2)+'\n');(H/'review.json').write_text(json.dumps({'original_replays':replays,'changed_parameter_observed_profiles':changed,'authored_generated':generated},indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='source_details'},indent=2))
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--write-evidence',action='store_true');args=p.parse_args();run(args.write_evidence)
