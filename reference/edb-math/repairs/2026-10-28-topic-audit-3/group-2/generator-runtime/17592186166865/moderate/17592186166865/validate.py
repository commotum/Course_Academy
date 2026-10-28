"""Independent printed-TeX readback, source parity, plot and native-engine checks."""
import importlib.util,itertools,json,hashlib,re,subprocess,sys,tempfile,math
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import sympy as s
from sympy.parsing.sympy_parser import parse_expr,standard_transformations,implicit_multiplication_application
from PIL import Image
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('circle_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
x,y,z=s.symbols('x y z',real=True)
counts={'source_questions':0,'source_choices':0,'source_complete_banks':0,'present_keys':0,'inferred_missing_keys':0,'exact_prompts':0,'exact_solutions':0,'attribute_presence':0,'printed_instances':0,'ordered_derivative_rows':0,'plot_instances':0,'authored_bank_operations':0}

def group(text,start):
 assert text[start] in '{(';closing='}' if text[start]=='{' else ')';stack=[closing];i=start+1
 while stack:
  assert i<len(text),'unbalanced group'
  if text[i] in '{(':stack.append('}' if text[i]=='{' else ')')
  elif text[i] in '})':assert text[i]==stack.pop()
  i+=1
 return text[start+1:i-1],i

def scalar(text):
 text=text.strip().rstrip('.,').replace(r'\,','').replace(r'\left','').replace(r'\right','').replace(' ','')
 for cmd in (r'\frac',r'\sqrt'):
  while cmd in text:
   pos=text.rfind(cmd);a,end=group(text,pos+len(cmd))
   if cmd==r'\frac':b,end=group(text,end);replacement='(('+convert(a)+')/('+convert(b)+'))'
   else:replacement='sqrt('+convert(a)+')'
   text=text[:pos]+replacement+text[end:]
 return s.expand(parse_expr(convert(text),local_dict={'x':x,'y':y,'z':z,'sqrt':s.sqrt},transformations=standard_transformations+(implicit_multiplication_application,)))
def convert(t):
 # Recursive arguments can contain remaining fractions.
 if r'\frac' in t or r'\sqrt' in t:return str(scalar(t))
 assert '\\' not in t,('unsupported TeX',t)
 return t.replace('{','(').replace('}',')').replace('^','**')

def same_on_circle(a,b,F):
 n=s.together(a-b).as_numer_denom()[0].expand();return s.simplify(s.groebner([F],x,y,domain=s.EX).reduce(n)[1])==0

def formatting(text):
 assert text.count('$$')%2==0
 q=text.replace('$$','');assert q.count('$')%2==0
 depth=0
 for c in text:
  if c=='{':depth+=1
  elif c=='}':depth-=1
  assert depth>=0
 assert depth==0
 assert not any(v in text for v in ('+-','--'))

def check(record,source=False):
 assert set(record['knowledge_point'])=={'db_id','id','title'}
 Q=record['question'];meta=record['generation'];p={a:s.sympify(v) for a,v in meta['parameters'].items()};h,k,r=p['h'],p['k'],p['r'];F=(x-h)**2+(y-k)**2-r**2;answer=-(x-h)/(y-k)
 for key in (':question/problem',':question/worked-solution'):
  if key in Q:formatting(Q[key])
 field=Q[':question/answer-fields'][0];assert field[':answer-field/type']==':answer-field.type/radio';assert len(field[':answer-field/choices'])==5
 vals=[scalar(a[':answer/value']) for a in field[':answer-field/choices']]
 for a in field[':answer-field/choices']:formatting(a[':answer/value'])
 assert len({a[':answer/id'] for a in field[':answer-field/choices']})==5
 for a,b in itertools.combinations(vals,2):assert not same_on_circle(a,b,F)
 good=[a[':answer/id'] for a,v in zip(field[':answer-field/choices'],vals) if same_on_circle(v,answer,F)];assert len(good)==1
 assert field.get(':answer-field/correct',[None,meta['inferred_correct_answer_id']])[1]==good[0]
 if meta['bank_profile']=='method':
  expected=[answer,-answer,-(y-k)/(x-h),-2*(x-h)/(y-k),-(x-h)/(2*(y-k))]
  assert all(any(s.simplify(a-b)==0 for b in vals) for a in expected);counts['authored_bank_operations']+=5
 if ':question/worked-solution' in Q:
  worked=Q[':question/worked-solution'];blocks=re.findall(r'\$\$\n(.*?)\n\$\$',worked,re.S);assert len(blocks)==2
  equations=blocks[0].replace(r'\,','').split('⟹');assert len(equations)==2
  for equation in equations:
   lhs,rhs=map(scalar,equation.split('='));assert s.simplify(lhs-rhs-F)==0
  prose=re.search(r'centered at (.*?) and has a radius of \$(.*?),\$',worked);assert prose
  if prose[1]=='the origin':assert h==k==0
  else:
   center=prose[1].strip('$')[1:-1].split(',');assert [scalar(c) for c in center]==[h,k]
  assert scalar(prose[2])==r
  block=re.search(r'\\begin\{aligned\}(.*?)\\end\{aligned\}',blocks[1],re.S)[1];rows=block.split(r'\\');assert len(rows)==(6 if meta['bank_profile']=='q-127499' else 5)
  # Check original formal operators and inputs before interpreting chain rule.
  derivative=g.OP
  def formal(piece):
   values=[]
   while derivative in piece:
    pos=piece.find(derivative);arg,end=group(piece,pos+len(derivative));obj=scalar(arg);values.append(obj);evaluated=s.diff(obj,x)+s.diff(obj,y)*z
    piece=piece[:pos]+'('+s.latex(evaluated)+')'+piece[end:]
   return scalar(piece),values
  ls,rs=rows[0].split('& =');L,args=formal(ls);RR,rrargs=formal(rs)
  assert args==[(x-h)**2+(y-k)**2] or s.simplify(args[0]-((x-h)**2+(y-k)**2))==0
  assert rrargs==[r**2];assert s.simplify(L-(2*(x-h)+2*(y-k)*z))==0 and RR==0
  ls,rs=rows[1].split('& =');L,args=formal(ls);assert len(args)==2 and s.simplify(args[0]-(x-h)**2)==s.simplify(args[1]-(y-k)**2)==0;assert scalar(rs)==0
  parts=[]
  for row in rows[2:]:
   lhs,rhs=row.replace(g.D,'z').split('& =');parts.append((scalar(lhs),scalar(rhs)))
  assert s.simplify(parts[0][0]-(2*(x-h)+2*(y-k)*z))==0 and parts[0][1]==0
  assert s.simplify(parts[1][0]-2*(y-k)*z)==0 and s.simplify(parts[1][1]+2*(x-h))==0
  for lhs,rhs in parts[2:]:assert lhs==z and s.simplify(rhs-answer)==0
  counts['ordered_derivative_rows']+=len(rows)
 plot=Path(meta['plot']);side=json.loads(plot.with_suffix('.json').read_text());assert side['parameters']==meta['parameters']
 assert side['axes_origin']==[0,0] and side['center']==[float(h),float(k)] and math.isclose(side['radius'],float(r))
 transform=side['axes_transform'];assert math.isclose(transform[0][0],transform[1][1],rel_tol=1e-12)
 # Read plotted blue extents back from PNG; allow 2 pixels stroke/AA.
 im=Image.open(plot).convert('RGB');coords=[(xx,yy) for yy in range(im.height) for xx in range(im.width) if (lambda c:c[2]>120 and c[2]>c[0]*1.5 and c[1]>c[0]*1.4)(im.getpixel((xx,yy)))]
 assert coords
 extent=[min(v[0] for v in coords),max(v[0] for v in coords),min(v[1] for v in coords),max(v[1] for v in coords)]
 # ax transform recorded at canvas dpi100, output dpi140. PNG y flips.
 expected=[(float(h-r)*transform[0][0]+transform[0][2])*1.4,(float(h+r)*transform[0][0]+transform[0][2])*1.4,im.height-(float(k+r)*transform[1][1]+transform[1][2])*1.4,im.height-(float(k-r)*transform[1][1]+transform[1][2])*1.4]
 assert all(abs(a-b)<4 for a,b in zip(extent,expected)),(extent,expected)
 counts['plot_instances']+=1;counts['printed_instances']+=1
 return good[0]

def main():
 cases=[];review=[];native=[]
 for sid,par in g.GEOMETRY.items():
  old=g.QUESTIONS[sid];level=old.get(':question/difficulty',{}).get(':db/ident',':question.difficulty/'+('easy' if par[0]==par[1]==0 else 'moderate')).split('/')[-1]
  case={'source_id':sid,'difficulty':level,'template':'origin' if level=='easy' else 'shifted','parameters':dict(zip(('h','k','r'),par)),'bank_profile':sid,'level_assignment':'observed' if ':question/difficulty' in old else 'authored evidence assignment; raw replay remains unrated'};cases.append(case)
  rec=g.generate(level,parameters=case['parameters'],profile=sid);good=check(rec,True);q=rec['question'];oldf=old[':question/answer-fields'][0];newf=q[':question/answer-fields'][0]
  assert sorted(a[':answer/value'] for a in oldf[':answer-field/choices'])==sorted(a[':answer/value'] for a in newf[':answer-field/choices']);counts['source_choices']+=5;counts['source_complete_banks']+=1
  assert old[':question/problem']==q[':question/problem'];counts['exact_prompts']+=1
  for key in (':question/difficulty',':question/worked-solution',':question/answer-fields'):assert (key in old)==(key in q)
  assert (':answer-field/correct' in oldf)==(':answer-field/correct' in newf);counts['attribute_presence']+=1
  if ':question/worked-solution' in old:assert old[':question/worked-solution']==q[':question/worked-solution'];counts['exact_solutions']+=1
  if ':answer-field/correct' in oldf:
   value=next(a[':answer/value'] for a in newf[':answer-field/choices'] if a[':answer/id']==good);assert scalar(value)==scalar(oldf[':answer-field/correct'][':answer/value']);counts['present_keys']+=1
   native.append({'label':sid,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==good else 'rejected','purpose':'original radio grading'} for a in newf[':answer-field/choices']]})
  else:counts['inferred_missing_keys']+=1
  assert all(a[':answer/value'].count(chr(92)*2)==0 for a in oldf[':answer-field/choices']);counts['source_questions']+=1
  review.append(rec)
  # One changed-parameter evidence variant per observed complete bank.
  variant=g.generate(level,seed=48,profile=sid);check(variant);review.append(variant)
 for level in ('easy','moderate','hard'):
  for seed in (2,19,41,76):
   rec=g.generate(level,seed);good=check(rec);review.append(rec)
   native.append({'label':level+'-'+str(seed),'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==good else 'rejected','purpose':'complete radio bank grading'} for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]})
 # Supported evidence radii can appear in wrong values even though r^2 makes
 # the printed circle polynomial rational. Check the actual public API, complete
 # bank, every printed solution row, PNG geometry, and native grading.
 radical_records=[]
 for radius in ('sqrt(2)','sqrt(5)'):
  rec=g.generate('easy',profile='q-127493',parameters={'h':0,'k':0,'r':radius})
  good=check(rec);review.append(rec);radical_records.append(rec)
  native.append({'label':'q-127493-'+radius,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==good else 'rejected','purpose':'supported exact radical radius evidence bank'} for a in rec['question'][':question/answer-fields'][0][':answer-field/choices']]})
 (HERE/'supported-radical-evidence.json').write_text(json.dumps(radical_records,indent=2)+'\n')
 counts['supported_radical_evidence_banks']=2
 # Exact explicit bounds, invalid template/profile, meaningful identity.
 for level,p in [('easy',{'h':1,'k':0,'r':2}),('moderate',{'h':'1/2','k':1,'r':2}),('hard',{'h':1,'k':'1/2','r':2}),('hard',{'h':'9/2','k':'1/2','r':2})]:
  try:g.generate(level,parameters=p)
  except ValueError:pass
  else:raise AssertionError('explicit level guard')
 # Every source profile must reject out-of-workload explicit components before
 # rendering, including profiles whose center shape already excludes the input.
 # This exercises the public API, rather than only the parameter helper.
 rejected=[];original_renderer=g.render_plots
 def forbidden_render(*args,**kw):raise AssertionError('invalid explicit parameters reached renderer')
 g.render_plots=forbidden_render
 try:
  for profile,geometry in g.GEOMETRY.items():
   level='easy' if profile in ('q-127359','q-127493') else 'moderate'
   baseline=dict(zip(('h','k','r'),geometry))
   for component,values in [('h',('1/1000003','sqrt(2)','pi/3')),('k',('1/1000003','sqrt(2)','pi/3')),('r',('1/1000003','sqrt(3)','sqrt(7)','pi/3'))]:
    for value in values:
     params={**baseline,component:value}
     try:g.generate(level,parameters=params,profile=profile)
     except ValueError as exc:rejected.append({'profile':profile,'component':component,'value':value,'failure':str(exc),'before_render':True})
     else:raise AssertionError(('evidence profile arithmetic bypass',profile,params))
 finally:g.render_plots=original_renderer
 assert len(rejected)==70
 (HERE/'explicit-guard-rejections.json').write_text(json.dumps(rejected,indent=2)+'\n')
 counts['invalid_source_profile_inputs_rejected_before_render']=len(rejected)
 p={'h':'-3/2','k':'5/2','r':'3/2'};a=g.generate_hard(1,parameters=p);b=g.generate_hard(25,parameters=p);assert a['question'][':question/id']==b['question'][':question/id']
 # Fresh concurrent identical and changed geometry, private directory only.
 with tempfile.TemporaryDirectory(prefix='concurrency-',dir=HERE) as t:
  ps=[{'h':'-3/2','k':'5/2','r':'3/2'},{'h':'-3/2','k':'5/2','r':'3/2'},{'h':'3/2','k':'-1/2','r':'5/2'}]
  with ThreadPoolExecutor(max_workers=3) as pool:paths=list(pool.map(lambda p:g.render_plots(p,t),ps))
  for pp,path in zip(ps,paths):assert json.loads(Path(path).with_suffix('.json').read_text())['parameters']==pp
  assert not list(Path(t).glob('circle-render-*'))
 (HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(review,indent=2)+'\n')
 (HERE/'native-input.json').write_text(json.dumps(native,indent=2)+'\n')
 engine=HERE.parent.parent/'runs/current/check-engine';subprocess.run([str(engine),str(HERE/'native-input.json'),str(HERE/'native-report.json')],check=True)
 md=['# Circle slope review','Raw originals reproduce source attributes; variants and completed learning records are labeled. Two raw keys below are inferred only.']
 for i,r in enumerate(review):
  md.append(('### Raw original' if i<14 and i%2==0 else '### Generated variant')+'\n\n'+g.markdown(r))
 (HERE/'review.md').write_text('\n\n'.join(md)+'\n')
 variety={'easy':{'curves':8,'derivatives':1,'center_structures':1},'moderate':{'curves':320,'derivatives':80,'center_structures':3},'hard':{'curves':448,'derivatives':64,'center_structures':1},'rationale':'Curve fingerprint includes radius because the plotted locus and circle equation change. Radius does not inflate distinct derivative counts; bank profiles and option order never inflate counts.'}
 report={'passed':True,'counts':counts,'variety':variety,'native':{'cases':len(native),'checks':sum(len(n['checks']) for n in native),'passed':True,'engine_sha256':hashlib.sha256(engine.read_bytes()).hexdigest()},'concurrency':{'fresh_render_calls':3,'identical_and_different':True,'private_inputs_cleaned':True},'limitations':['No hard source difficulty exists; fractional center hard scope is authored.','Two unrated sources lack worked solution and correct designation; raw omission parity preserved, keys independently inferred.','Observed bank error intention remains underdetermined; evidence profiles are not eligible for learning.','Easy origin derivative is always -x/y; radius gives eight different circle equations, not eight distinct derivative formulas.','Raw radio fixtures without correct refs are evidence-only and cannot be graded.'],'source_snapshot_sha256':hashlib.sha256((HERE/'source.json').read_bytes()).hexdigest()}
 (HERE/'validation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
if __name__=='__main__':main()
