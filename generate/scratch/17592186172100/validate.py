"""Read displayed mathematics independently of the sampled parameters."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('flux_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
sp=g.sp;x,y=g.x,g.y
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import validate_generated_record

def save(p,v):p.write_text(json.dumps(v,indent=2,default=str)+'\n')
def read_field(problem):
 match=re.search(r'\$F\(x,y\)=(.*?)\$',problem,re.S);assert match
 s=match[1]
 if s.startswith('⟨'):
  s=s[1:-1];p,q=s.split(r',\,')
 elif s.startswith(r'\langle'):
  p,q=s[len(r'\langle'):].removesuffix(r'\rangle').split(',')
 else:
  p,tail=s.split(r'\,i');q=tail.removesuffix(r'\,j').lstrip('+')
 return g.parse_poly(p),g.parse_poly(q)
def read_vertices(problem):
 part=problem.split('vertices ')[1].split('traversed')[0].split('can be represented')[0]
 return [(int(a),int(b)) for a,b in re.findall(r'\((-?\d+),(-?\d+)\)',part)]
def normalized(q):
 import copy
 q=json.loads(json.dumps(q,default=str))
 if isinstance(q[':question/difficulty'],dict):q[':question/difficulty']=q[':question/difficulty'][':db/ident']
 for f in q[':question/answer-fields']:
  if isinstance(f[':answer-field/type'],dict):f[':answer-field/type']=f[':answer-field/type'][':db/ident']
  if isinstance(f[':answer-field/correct'],dict):f[':answer-field/correct']=[':answer/id',f[':answer-field/correct'][':answer/id']]
  for a in f[':answer-field/choices']:
   if isinstance(a[':answer/type'],dict):a[':answer/type']=a[':answer/type'][':db/ident']
 return q

def check_question(question,generated=False):
 q=normalized(question);p,v=read_field(q[':question/problem']);div=sp.expand(sp.diff(p,x)+sp.diff(v,y));level=q[':question/difficulty'].split('/')[-1]
 verts=read_vertices(q[':question/problem']);assert len(verts)==(4 if level=='moderate' or 'rectangle' in q[':question/problem'] else 3)
 assert sum(verts[i][0]*verts[(i+1)%len(verts)][1]-verts[(i+1)%len(verts)][0]*verts[i][1] for i in range(len(verts)))>0
 if level=='moderate':
  a,b=min(t[0] for t in verts),max(t[0] for t in verts);c,d=min(t[1] for t in verts),max(t[1] for t in verts)
  expected=sp.Integral(div,(y,c,d),(x,a,b))
 else:assert level=='easy';expected=div
 fields=q[':question/answer-fields'];assert len(fields)==1
 f=fields[0];assert f[':answer-field/type']==':answer-field.type/radio' and f[':answer-field/key']=='selection'
 choices=f[':answer-field/choices'];assert len(choices)==5 and len({a[':answer/id'] for a in choices})==5
 values=[g.parse_value(a[':answer/value']) for a in choices]
 assert all(not g.equivalent(a,b) for i,a in enumerate(values) for b in values[i+1:])
 correct=[i for i,val in enumerate(values) if g.equivalent(val,expected)];assert len(correct)==1
 assert choices[correct[0]][':answer/id']==f[':answer-field/correct'][1]
 # Read concrete derivatives and final requested object from rendered output.
 if generated:
  validate_generated_record({'question':q})
  sol=q[':question/worked-solution']
  derivative=re.search(r'\\frac\{\\partial P\}\{\\partial x\}=(.*?),\\qquad \\frac\{\\partial Q\}\{\\partial y\}=(.*?) \.',sol)
  assert derivative
  assert sp.expand(g.parse_poly(derivative[1])-sp.diff(p,x))==0
  assert sp.expand(g.parse_poly(derivative[2])-sp.diff(v,y))==0
  if level=='easy':
   final=re.search(r'Hence, \$f\(x,y\)=(.*?)\.\$',sol);assert final
   assert g.equivalent(g.parse_poly(final[1]),div)
  else:
   final=sol.rsplit(r'\\ &=',1)[1].split(r'.\end{aligned}')[0]
   assert g.equivalent(g.parse_value(final),expected)
   assert r'D=\{(x,y):'+str(a)+r'\le x\le '+str(b)+r',\ '+str(c)+r'\le y\le '+str(d)+r'\}' in sol
 return {'level':level,'divergence':str(div),'bounds':list(expected.limits) if isinstance(expected,sp.Integral) else None,'signature':g.digest([level,str(div),[a,b,c,d] if level=='moderate' else None])}

def engine_checks(q):
 q=normalized(q);f=q[':question/answer-fields'][0]
 return [{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each complete radio bank option through actual application grader'} for a in f[':answer-field/choices']]

def main():
 source_results=[];fixtures=[];slots={};seen=set();examples=[]
 for sid,source in g.SOURCES.items():
  read=check_question(source);level=read['level'];replay=g.generate(level,0,sid,{'scale':1});check_question(replay['question'],True)
  f=source[':question/answer-fields'][0];rf=replay['question'][':question/answer-fields'][0]
  src=[g.parse_value(a[':answer/value']) for a in f[':answer-field/choices']];new=[g.parse_value(a[':answer/value']) for a in rf[':answer-field/choices']]
  mapping=[[j for j,b in enumerate(new) if g.equivalent(a,b)] for a in src];assert all(len(m)==1 for m in mapping)
  assert len({m[0] for m in mapping})==5
  p,q=read_field(source[':question/problem']);rp,rq=read_field(replay['question'][':question/problem']);assert sp.expand(p-rp)==sp.expand(q-rq)==0
  source_results.append({'source':sid,'template':sid,'profile':sid,'matched_options':5,'total_options':5,'matched_distractors':4,'total_distractors':4,'complete_bank':True,'missing':[],'extra':[],'prompt_geometry_and_components':True,'presentation':'source wording and solution stages retained; TeX and polynomial factorization normalized; concrete derivative equations and region recomputed'})
  fixtures.append({'label':'source-'+sid,'record':{'knowledge_point':{'title':g.TITLE},'question':normalized(source),'generation':{'template':sid}},'checks':engine_checks(source)})
  slots[sid]=[]
  for scale in range(1,13):
   r=g.generate(level,123,sid,{'scale':scale});checked=check_question(r['question'],True)
   assert checked['signature']==r['generation']['mathematical_fingerprint']
   assert checked['signature'] not in seen;seen.add(checked['signature']);slots[sid].append(scale)
   other=g.generate(level,456,sid,{'scale':scale})
   assert r['question']==other['question'],'Seed alone must not change identity or content'
   fixtures.append({'label':sid+'-'+str(scale),'record':r,'checks':engine_checks(r['question'])})
   if scale in (1,7):examples.append({'source':sid,'original':source,'variant':r})
  assert not g.equivalent(g.parse_value(g.generate(level,0,sid,{'scale':1})['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value']),g.parse_value(g.generate(level,0,sid,{'scale':7})['question'][':question/answer-fields'][0][':answer-field/choices'][0][':answer/value'])) or src[0]==0
 # Forbidden level, invalid scale and mismatched profile checks.
 for call in (lambda:g.generate('hard'),lambda:g.generate('easy',template='q-127070',parameters={'scale':0}),lambda:g.generate('moderate',template='q-127072',profile='q-127229')):
  try:call()
  except (ValueError,AssertionError):pass
  else:raise AssertionError('Invalid request accepted')
 save(HERE/'source-replay.json',{'pass':True,'banks':source_results,'matched_complete_banks':10,'total_complete_banks':10,'matched_distractors':40,'total_distractors':40})
 save(HERE/'side-by-side.json',examples)
 save(HERE/'engine-input.json',fixtures)
 assets=[]
 for q in g.SOURCES.values():
  for ref in re.findall(r'!\[.*?\]\((.*?)\)',q[':question/worked-solution']):
   file=Path('/media/jake/SSD/EDB/math')/ref
   sha=hashlib.sha256(file.read_bytes()).hexdigest();assert Path(ref).stem==sha
   assets.append({'source':q[':question/math-academy-id'],'path':ref,'sha256':sha,'reused_unchanged':True})
 save(HERE/'asset-verification.json',assets)
 native_source=ROOT/'generate/runs/current/check-engine.rs';libs={name:max((ROOT/'target/release/deps').glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns) for name in ('course_academy_engine','serde_json')}
 subprocess.run(['rustc','--edition=2024','-O',str(native_source),*[v for name,p in libs.items() for v in ('--extern',name+'='+str(p))],'-L','dependency='+str(ROOT/'target/release/deps'),'-o',str(HERE/'check-engine')],check=True)
 subprocess.run([str(HERE/'check-engine'),str(HERE/'engine-input.json'),str(HERE/'engine-report.json')],check=True)
 native=json.loads((HERE/'engine-report.json').read_text());assert native['documented_unresolved_checks']==0
 result={'pass':True,'source_basis':g.SOURCE['basis'],'source_banks':10,'source_distractors':40,'source_fidelity':'10/10 complete banks, source component mathematics and geometry; operative solution stages retained with normalized presentation','correctness':'independent rendered-field differentiation, rectangle readback, all option keys, exact polynomial and unevaluated integral comparisons','grading':{'entry_point':native['entry_point'],'accepted':native['accepted_checks'],'rejected':native['rejected_checks'],'unresolved':0},'unique_catalog_tasks':len(seen),'slot_coverage':slots,'fixed_geometry_reason':'bounded conservative policy: source region diagrams can be reused; coefficients alone vary the assessed divergence without introducing domain-setting skills','changed_target_test':'not applicable: target is always divergence (easy) or dy dx integral (moderate); no target-location slot declared','source_errors':[],'dependencies':{'sympy':sp.__version__},'finite_limit':{'easy':60,'moderate':60},'native_build':{name:{'path':str(p.relative_to(ROOT)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for name,p in libs.items()}}
 save(HERE/'validation.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
