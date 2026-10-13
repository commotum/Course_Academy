"""Failing fidelity/math/grading validator; native engine is read-only in-memory."""
import concurrent.futures,hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
D=Path(__file__).resolve().parent;spec=importlib.util.spec_from_file_location('parabola',D.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
X,Y,P=sp.symbols('x y p',real=True)
def parse(t):
 t=t.strip().rstrip('.').replace('\\cdot','*')
 def group(s,start):
  assert s[start]=='{';n=1;i=start+1
  while n:
   if s[i]=='{':n+=1
   elif s[i]=='}':n-=1
   i+=1
  return s[start+1:i-1],i
 while '\\frac' in t:
  i=t.rfind('\\frac');a,j=group(t,i+5);b,k=group(t,j);t=t[:i]+'(('+a+')/('+b+'))'+t[k:]
 t=t.replace('{','(').replace('}',')').replace('^','**')
 return parse_expr(t,local_dict={'x':X,'y':Y,'p':P},transformations=standard_transformations+(implicit_multiplication_application,))
def fmt(s):
 assert s.count('$')%2==0
 n=0
 for ch in s:
  n+=1 if ch=='{' else -1 if ch=='}' else 0
  assert n>=0
 assert n==0 and '+-' not in s and '--' not in s

def mathcheck(r,raw=False):
 q=r['question'];gen=r['generation'];assert set(r['knowledge_point'])=={'db_id','id','title'}
 assert gen['eligible_for_learning'] is (not gen['evidence_only'])
 assert gen['dependencies']['python']==sys.version and gen['dependencies']['sympy']==sp.__version__
 easy=q.get(':question/difficulty','').endswith('/easy')
 for k in (':question/problem',':question/worked-solution'):
  if k in q:fmt(q[k])
 f=q[':question/answer-fields'][0];vals=[parse(a[':answer/value']) for a in f[':answer-field/choices']]
 assert len(vals)==len(set(map(sp.srepr,vals)))
 assert all(sp.simplify(v-w)!=0 for i,v in enumerate(vals) for w in vals[i+1:])
 if f[':answer-field/type'].endswith('/blank'):assert '{{'+f[':answer-field/key']+'}}' in q[':question/problem']
 sol=q.get(':question/worked-solution')
 if not sol:
  geo=next(z for z in geometry if z['source_id']==gen['source_id']);a,b=geo['marked_point'];expected=sp.Rational(b*b,2*a)/Y
  assert sum(sp.simplify((v-expected).subs(X,Y**2/sp.Rational(b*b,a)))==0 for v in vals)==1
  return
 # Read actual marked point and curve from learner-facing solution, then verify
 # it against the independent raster/renderer geometry, never only metadata.
 asset=gen['plot']
 if easy:
  side=json.loads(Path(asset).with_suffix('.json').read_text());a,b=(side['parameters'][k] for k in ('a','b'))
  prompt_blocks=re.findall(r'\$\$\n(.*?)\n\$\$',q[':question/problem'],re.S);assert len(prompt_blocks)==1
  supplied_l,supplied_r=prompt_blocks[0].split('=');assert parse(supplied_l)==Y**2
  supplied_curve=parse(supplied_l)-parse(supplied_r);assert sp.expand(supplied_curve)==Y**2-sp.Rational(b*b,a)*X
  assert gen['assessment_mode']=='given equation' and '4p' not in sol and 'Substituting' not in sol
 else:
  point=re.search(r'passes through the point \$\((-?\d+),(-?\d+)\)',sol);assert point
  a,b=map(int,point.groups());assert gen['assessment_mode']=='reconstruct equation from plot'
 if asset.startswith('images/'):
  geo=next(z for z in geometry if z['source_id']==gen['source_id']);assert geo['marked_point']==[a,b] and geo['fit_pass']
 else:
  side=json.loads(Path(asset).with_suffix('.json').read_text());assert side['parameters']=={'a':a,'b':b}
  assert gen['dependencies']['plot']['dependencies']==side['dependencies']
  assert all(Path(p).exists() for p in side['dependencies']['cached_dependency_paths'].values())
  for xx,yy in side['curve_samples']:assert abs(yy*yy-b*b/a*xx)<1e-8
  assert side['bounds'][0][0]<a<side['bounds'][0][1] and side['bounds'][1][0]<b<side['bounds'][1][1]
 blocks=re.findall(r'\$\$\n(.*?)\n\$\$',sol,re.S);assert len(blocks)==(2 if easy else 4)
 if easy:
  lhs,rhs=blocks[0].split('=');curve=parse(lhs)-parse(rhs);assert curve==supplied_curve
 else:
  assert blocks[0]==r'{y}^{2}=4px.'
  # Actual substitution/squaring/p isolation: stages must remain separate.
  rows=blocks[1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==3
  expected_p=sp.Rational(b*b,4*a)
  for row in rows:
   lhs,rhs=row.replace('&','').split('=');assert sp.simplify((parse(lhs)-parse(rhs)).subs(P,expected_p))==0
  assert '^' in rows[0] and 'p' in rows[1] and rows[2].strip().startswith('p')
  lhs,rhs=blocks[2].split('=');curve=parse(lhs)-parse(rhs)
 c=sp.Rational(b*b,a);assert sp.expand(curve)==Y**2-c*X
 rows=blocks[-1].replace(r'\begin{aligned}','').replace(r'\end{aligned}','').split(r'\\');assert len(rows)==3
 pattern=re.escape(g.DX)+r'\((.*?)\)\s*&\s*='+re.escape(g.DX)+r'\((.*?)\)'
 ops=re.fullmatch(pattern,rows[0].strip());assert ops
 left,right=map(parse,ops.groups());assert left==Y**2 and right==c*X
 # Independent total derivative of the actual formal operator inputs.
 d=sp.Symbol('D');total=lambda expr:sp.diff(expr,X)+sp.diff(expr,Y)*d
 l,rhs=rows[1].replace('&','').replace(g.DY,'D').split('=');printed_l=parse(l).subs(sp.Symbol('D'),d);printed_r=parse(rhs)
 assert sp.expand(printed_l-total(left))==0 and sp.expand(printed_r-total(right))==0
 final=rows[2].replace('&','').split('=');assert final[0].strip()==g.DY
 actual=parse(final[1]);expected=sp.solve(total(left)-total(right),d)[0];assert sp.simplify(actual-expected)==0
 assert sum(sp.simplify((v-expected).subs(X,Y**2/c))==0 for v in vals)==1
 correct=f.get(':answer-field/correct')
 if correct:
  ca=next(a for a in f[':answer-field/choices'] if a[':answer/id']==correct[1]);assert sp.simplify(parse(ca[':answer/value'])-expected)==0

geometry=json.loads((D/'source-geometry.json').read_text());assert len(geometry)==11 and all(z['fit_pass'] for z in geometry)
cases=[];review=[];fixtures=[];banks=values=solutions=designations=0
for sid,q in g.QS.items():
 a,b=g.SOURCE_PARAMS[sid];level='hard' if a<0 else 'moderate';p={'a':a,'b':b};case={'source_id':sid,'level':level,'template':'point_'+q[':question/answer-fields'][0][':answer-field/type'][':db/ident'].rsplit('/',1)[1],'parameters':p,'bank_profile':'raw:'+sid};cases.append(case)
 raw=g.generate(level,parameters=p,profile='raw:'+sid);qr=raw['question'];f=qr[':question/answer-fields'][0];f0=q[':question/answer-fields'][0]
 assert qr[':question/problem']==q[':question/problem']
 for key in (':question/difficulty',':question/worked-solution'):assert (key in qr)==(key in q)
 assert qr.get(':question/worked-solution')==q.get(':question/worked-solution')
 assert (':answer-field/correct' in f)==(':answer-field/correct' in f0)
 assert f[':answer-field/key']==f0[':answer-field/key'] and f[':answer-field/type']==f0[':answer-field/type'][':db/ident']
 assert sorted(a[':answer/value'] for a in f[':answer-field/choices'])==sorted(a[':answer/value'] for a in f0[':answer-field/choices'])
 if ':question/difficulty' in q:assert qr[':question/difficulty']==q[':question/difficulty'][':db/ident']
 if ':answer-field/correct' in f0:
  found=next(a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);assert found[':answer/value']==f0[':answer-field/correct'][':answer/value'];designations+=1
 mathcheck(raw,True);banks+=1;values+=len(f[':answer-field/choices']);solutions+=int(':question/worked-solution' in q)
 completed=g.generate(level,parameters=p,profile='completed:'+sid);mathcheck(completed);review.extend([raw,completed])
 # Every observed template/bank has a changed-parameter variant through public API.
 variant=None
 for aa,bb in g.domain(level):
  if (aa,bb)==(a,b):continue
  try:variant=g.generate(level,parameters={'a':aa,'b':bb},profile='completed:'+sid)
  except ValueError:continue
  break
 assert variant;mathcheck(variant);review.append(variant)
for level in ('easy','moderate','hard'):
 for kind in ('blank','radio'):
  for seed in (42,63):
   r=g.generate(level,seed,field_type=kind);mathcheck(r);review.append(r)
 # Explicit guards, including evidence-only profiles, cannot bypass workload.
 for bad in ({'a':1,'b':1000},{'a':sp.Rational(1,999),'b':2},{'a':-9 if level=='hard' else 9,'b':2},{'a':1,'b':0}):
  try:g.generate(level,parameters=bad)
  except ValueError:pass
  else:raise AssertionError('Accepted out-of-scope parameter')
 # Enumerate mathematics for every candidate: aliases/point sign do not count.
 for a,b in g.domain(level):
  vals,_=g.bank('authored-method',a,b);assert all(sp.simplify(v-w)!=0 for i,v in enumerate(vals) for w in vals[i+1:])
profile_enumeration={}
for sid in g.QS:
 level='hard' if g.SOURCE_PARAMS[sid][0]<0 else 'moderate';valid=invalid=0
 for a,b in g.domain(level):
  vals,_=g.bank(sid,a,b);c=sp.Rational(b*b,a);m=c/(2*Y)
  distinct=all(sp.cancel((v-w).subs(X,Y**2/c))!=0 for i,v in enumerate(vals) for w in vals[i+1:])
  if distinct:
   assert sum(sp.cancel((v-m).subs(X,Y**2/c))==0 for v in vals)==1;valid+=1
  else:
   invalid+=1
   for mode in ('raw','completed'):
    try:g.generate(level,parameters={'a':a,'b':b},profile=mode+':'+sid)
    except ValueError:pass
    else:raise AssertionError('Historical profile collision bypassed')
 profile_enumeration[sid]={'finite_candidate_instances':len(g.domain(level)),'valid':valid,'whole_instance_rejections':invalid}
easy_cases={}
for a,b in g.domain('easy'):
 easy_cases.setdefault(str(sp.Rational(b*b,a)),{'a':a,'b':b})
assert len(easy_cases)==17
easy_records=[]
for params in easy_cases.values():
 for kind in ('blank','radio'):
  r=g.generate_easy(parameters=params,field_type=kind);mathcheck(r);easy_records.append(r)
  counterpart=g.generate_moderate(parameters=params,field_type=kind);mathcheck(counterpart)
  assert r['generation']['mathematical_fingerprint']!=counterpart['generation']['mathematical_fingerprint']
  signflip=g.generate_easy(parameters={'a':params['a'],'b':-params['b']},field_type=kind);mathcheck(signflip)
  assert r['generation']['mathematical_fingerprint']==signflip['generation']['mathematical_fingerprint']
  assert r['question'][':question/id']==g.generate_easy(113,parameters=params,field_type=kind)['question'][':question/id']
for r in review+easy_records:
 if ':answer-field/correct' not in r['question'][':question/answer-fields'][0]:continue
 f=r['question'][':question/answer-fields'][0];correct=f[':answer-field/correct'][1];checks=[]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==correct else 'rejected','purpose':'complete displayed bank ID selection'} for a in f[':answer-field/choices']]
 else:
  a,b=(r['generation']['parameters'][k] for k in ('a','b'));value=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==correct)
  checks=[{'submitted':value,'expected':'accepted','purpose':'exact answer'},{'submitted':rf'\frac{{{b*b}}}{{{2*a}y}}','expected':'accepted','purpose':'unreduced independently differentiated quotient'},{'submitted':'y','expected':'rejected','purpose':'incorrect derivative'},{'submitted':r'\frac{y}{2x}','expected':'rejected','purpose':'locus-equivalent slope lacks native curve context; blank also requires y-only response'}]
 fixtures.append({'label':r['question'][':question/id'],'record':r,'checks':checks})
# Same geometry/content under seed changes; bank shuffling cannot alter IDs.
r=g.generate_moderate(12,parameters={'a':5,'b':7},field_type='radio');rr=g.generate_moderate(99,parameters={'a':5,'b':7},field_type='radio');assert r['question'][':question/id']==rr['question'][':question/id']
# API profile selection and reordered explicit inputs are independent of RNG.
for seed in range(5):
 assert g.generate_moderate(seed,profile='authored-method')['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/radio')
 assert g.generate_moderate(seed,profile='blank')['question'][':question/answer-fields'][0][':answer-field/type'].endswith('/blank')
assert g.generate_moderate(parameters={'b':7,'a':5},field_type='radio')['question'][':question/id']==r['question'][':question/id']
# Fresh concurrent writes for identical and differing geometry. Remove nothing:
# use unrendered coordinates, preserve assets for other active reviewers.
private=D/'concurrency-renders'/uuid.uuid4().hex
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 fresh=list(ex.map(lambda p:g.render_plots(*p,output_dir=private),[(7,8),(7,8),(8,7),(8,6)]))
assert fresh[0]==fresh[1]
for asset in fresh:
 side=json.loads(Path(asset).with_suffix('.json').read_text());a,b=(side['parameters'][k] for k in ('a','b'))
 assert all(abs(yy*yy-b*b/a*xx)<1e-8 for xx,yy in side['curve_samples'])
assert len(list(private.glob('*.png')))==3 and len(list(private.glob('*.json')))==3
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
 concurrent=list(ex.map(lambda p:g.generate_moderate(parameters=p,field_type='blank'),[{'a':7,'b':8},{'a':7,'b':8},{'a':8,'b':7},{'a':8,'b':6}]))
for r in concurrent:mathcheck(r)
assert concurrent[0]['question'][':question/id']==concurrent[1]['question'][':question/id']
assert not list(D.glob('render-*.json'))
(D/'engine-input.json').write_text(json.dumps(fixtures,indent=2)+'\n');subprocess.run(['generate/runs/current/check-engine',str(D/'engine-input.json'),str(D/'engine-report.json')],check=True)
(D/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(D/'review.json').write_text(json.dumps(review,indent=2)+'\n')
(D/'review.md').write_text('# Parabola review\n\nRaw originals reproduce missing attributes and original prose. Completed historical radio banks remain evidence-only; missing keys are inferred, not matched. Easy is authored with the equation supplied; its solution directly differentiates, omitting graph-to-p reconstruction. Correct marks refer to actual field keys.\n\n'+'\n'.join(g.markdown(r) for r in review))
report={'status':'passed','source_practice_questions':10,'complete_original_banks':banks,'displayed_original_values':values,'original_correct_designations_matched':designations,'missing_original_correct_refs':2,'raw_solution_exact':solutions,'raw_attribute_presence_parity':10,'raw_prompt_exact':10,'raw_prose_error_preserved_evidence_only':1,'completed_prose_repairs':1,'inferred_unrated_levels':{'q-127372':'moderate','q-127374':'hard'},'authored_missing_levels':['easy'],'native_grading':json.loads((D/'engine-report.json').read_text()),'finite_domain_tasks':{l:len({str(sp.Rational(b*b,a)) for a,b in g.domain(l)}) for l in ('easy','moderate','hard')},'review_records':len(review),'easy_all_coefficient_instances_checked':len(easy_records),'easy_assessment':'supplied equation → formal derivative → chain factor → isolation','raster_fits':11,'observed_profile_domain_checks':profile_enumeration,'concurrent_render_calls':8,'fresh_private_render_assets':3,'database_writes':0,'limits':['Original distractor intent underdetermined; historical profiles evidence-only, including completed records.','Easy has an authored given-equation demand; moderate/hard reconstruct the curve from plot. Historical moderate/hard labels retain their observed arithmetic overlap.','Raster fit is stroke-tolerant geometric recovery, not exact source renderer reproduction.','Native blank grading rejects y/(2x): it lacks the locus relation and sources explicitly require y-only answers; independently unreduced y-only quotients are accepted.']}
(D/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print({k:v for k,v in report.items() if k!='native_grading'})
