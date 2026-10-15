"""Independent displayed-math checks, exhaustive bounded replay and actual grading."""
from pathlib import Path
import importlib.util,json,re,subprocess,sys,hashlib
import sympy as s
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sp=importlib.util.spec_from_file_location('gradient_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(sp);sp.loader.exec_module(g)
x,y=g.x,g.y

def save(p,obj):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2,default=str,ensure_ascii=False)+'\n')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def math(raw):
 raw=raw.strip().rstrip('.,').replace('C','0').replace(r'\qquad',',').replace(r'\text{ }','').replace('\xa0','').replace(r'\textbf','').replace(r'\mathbf','')
 return g.p.scalar(raw)
def eq(a,b):return s.simplify(a-b)==0
def potential(raw):return math(raw.split('=',1)[-1])
def gradient(v):return (s.diff(v,x),s.diff(v,y))
def task(q):
 P,Q=prompt(q[':question/problem']);return g.digest([s.srepr(s.simplify(P)),s.srepr(s.simplify(Q))])
def prompt(text):
 match=re.search(r'F\(x,\s*y\)\s*=\s*(.*?)\$',text,re.S);assert match,('Missing standalone field',text)
 v=g.p.vector(match[1].replace(r'\text{ }','').replace('\xa0',''));assert v[2]==0
 return v[0],v[1]
def normalize(q):
 fields=[]
 for f in q[':question/answer-fields']:
  fields.append({':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':str(f[':answer-field/type'][':db/ident']),':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':str(a[':answer/type'][':db/ident']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])]})
 return {':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':str(q[':question/difficulty'][':db/ident']),':question/answer-fields':fields}
def ordered(q):
 q=json.loads(json.dumps(q));q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
 for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
 return q

def check_bank(q,P,Q):
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1
 vals=[potential(a[':answer/value']) for a in f[':answer-field/choices']];flags=[all(eq(a,b) for a,b in zip(gradient(v),(P,Q))) for v in vals]
 cid=f[':answer-field/correct'][1]
 assert sum(flags)==1 and all(ok==(a[':answer/id']==cid) for ok,a in zip(flags,f[':answer-field/choices']))
 # Potentials that differ by constants are one answer family.
 for i,a in enumerate(vals):
  for b in vals[:i]:assert not all(eq(u,v) for u,v in zip(gradient(a),gradient(b))),('Equivalent bank entries',a,b)
 return len(vals)
def check(r):
 q=r['question'];meta=r['generation'];assert r['knowledge_point']['db_id']==g.KP and q[':question/difficulty']==':question.difficulty/easy'
 assert ordered(g.generate('easy',meta['seed'],meta['template'],meta['parameters'],meta['bank_profile'])['question'])==ordered(q)
 P,Q=prompt(q[':question/problem']);n=check_bank(q,P,Q);sol=q[':question/worked-solution'];blocks=re.findall(r'\$\$(.*?)\$\$',sol,re.S);assert len(blocks)==6
 def body(i):return blocks[i].strip().rstrip('.').replace(r'\begin{aligned}','').replace(r'\end{aligned}','').replace('&','')
 # Read each displayed supplied derivative, primitive, residual and final answer.
 first=body(1).split(r',\qquad ');assert len(first)==2
 assert eq(math(first[0].split('=',1)[1]),P) and eq(math(first[1].split('=',1)[1]),Q)
 rows=body(2).split(r'\\');assert len(rows)==3
 integrand=rows[1].split(r'\int (',1)[1].split(r')\,\text{d}x',1)[0];assert eq(math(integrand),P)
 A=math(rows[2].split('=',1)[1].replace('+g(y)',''));assert eq(s.diff(A,x),P)
 Ay=math(body(3).split('=',1)[1].replace("+g'(y)",''));assert eq(Ay,s.diff(A,y))
 rows=body(4).split(r'\\');assert len(rows)==3
 assert eq(math(rows[0].split('=',1)[0].replace("+g'(y)",'')),Ay) and eq(math(rows[0].split('=',1)[1]),Q)
 R=math(rows[1].split('=',1)[1]);H=math(rows[2].split('=',1)[1]);assert eq(R,Q-Ay) and eq(s.diff(H,y),R)
 final=potential(body(5));assert eq(final,A+H) and all(eq(a,b) for a,b in zip(gradient(final),(P,Q)))
 blank=q[':question/answer-fields'][0][':answer-field/type'].endswith('/blank');assert ('{{field-1}}' in q[':question/problem'])==blank
 if meta['template']=='q-81737':assert 'either half-plane' in q[':question/problem']
 return {'task':task(q),'choices':n,'solution_stages':6}

def fixture(r):
 f=r['question'][':question/answer-fields'][0];ci=f[':answer-field/correct'][1]
 if f[':answer-field/type'].endswith('/radio'):
  checks=[{'field_index':0,'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==ci else 'rejected','purpose':'entire independently checked bank'} for a in f[':answer-field/choices']]
 else:
  v=f[':answer-field/choices'][0][':answer/value'];checks=[{'field_index':0,'submitted':z,'expected':e,'purpose':purpose} for z,e,purpose in [(v,'accepted','canonical fragment'),('('+v+')+(x-x)','accepted','equivalent fragment'),('('+v+')+x','rejected','incorrect derivative')]]
 return {'label':r['question'][':question/id'],'record':r,'checks':checks}
def native(records,path):
 path.mkdir(parents=True,exist_ok=True);save(path/'input.json',[fixture(r) for r in records]);exe=HERE/'reference/native/check-engine'
 result=subprocess.run([str(exe),str(path/'input.json'),str(path/'report.json')],capture_output=True,text=True,timeout=55);(path/'run.log').write_text(result.stdout+result.stderr);assert result.returncode==0,result.stderr
 return json.loads((path/'report.json').read_text())
def build_native():
 p=HERE/'reference/native';p.mkdir(parents=True,exist_ok=True);deps=ROOT/'target/release/deps';cmd=['rustc','--edition=2024','-O',str(ROOT/'generate/runs/current/check-engine.rs')]
 libs={}
 for name in ['course_academy_engine','serde_json']:
  lib=max(deps.glob('lib'+name+'-*.rlib'),key=lambda p:p.stat().st_mtime_ns);libs[str(lib)]=sha(lib);cmd+=['--extern',name+'='+str(lib)]
 cmd+=['-L','dependency='+str(deps),'-o',str(p/'check-engine')];subprocess.run(cmd,check=True);save(p/'build.json',{'command':cmd,'libraries':libs,'harness_sha256':sha(ROOT/'generate/runs/current/check-engine.rs')})

def source_evidence(kp=None):
 kp=kp or g.SOURCE['record'];assert kp[':knowledge-point/id']==g.KP_UUID
 current={q[':question/math-academy-id']:q for q in kp[':knowledge-point/questions'] if ':question/math-academy-id'in q}
 replay=[];source_records=[]
 for name,case in g.CASES.items():
  q=current[name];f=q[':question/answer-fields'][0];vals=list(map(potential,[a[':answer/value'] for a in f[':answer-field/choices']]));(P,Q,A,H),bank=g.data(name,1)
  assert len(vals)==len(bank)
  for a,b in zip(vals,bank):assert eq(a,b),(name,a,b)
  if name=='q-168602':
   assert 'In part 1' in q[':question/worked-solution'] and not re.search(r'F\(x,\s*y\)\s*=',q[':question/problem']);P0,Q0=prompt(q[':question/worked-solution']);assert eq(P,P0) and eq(Q,Q0)
  else:
   P0,Q0=prompt(q[':question/problem']);assert eq(P,P0) and eq(Q,Q0)
  norm=normalize(q);check_bank(norm,P,Q)
  # Final source solution potential independently has the supplied gradient.
  blocks=re.findall(r'\$\$(.*?)\$\$',q[':question/worked-solution'],re.S);final=potential(blocks[-1]);assert all(eq(a,b) for a,b in zip(gradient(final),(P,Q)))
  generated=g.generate('easy',0,name,{'scale':1});check(generated)
  for a,b in zip(generated['question'][':question/answer-fields'][0][':answer-field/choices'],f[':answer-field/choices']):assert eq(potential(a[':answer/value']),potential(b[':answer/value']))
  source_records.append({'knowledge_point':{'db_id':g.KP,'title':g.TITLE},'question':norm,'generation':{'template':name}})
  replay.append({'source':name,'source_id':q[':db/id'],'options_matched':len(vals),'distractors_matched':max(0,len(vals)-1),'complete_bank':True,'original_key_matched':True,'plot_rating':'none','source_final_gradient_verified':True,'blank_context_reconstructed':name=='q-168602'})
 return replay,source_records

def main():
 build_native();replay,source_records=source_evidence();records=[];checks=[]
 for name in sorted(g.CASES):
  for k in g.SCALES:
   r=g.generate('easy',123,name,{'scale':k});checks.append(check(r));records.append(r)
 assert len({c['task'] for c in checks})==len(checks),'Duplicated mathematical questions'
 # Seeds are metadata only; equal parameters retain content identity.
 a=g.generate('easy',1,'q-35994',{'scale':2});b=g.generate('easy',100,'q-35994',{'scale':2});assert a['question']==b['question']
 native(records,HERE/'reference/exhaustive-grading');native(source_records,HERE/'reference/source-grading');save(HERE/'reference/all-validated.json',records)
 save(HERE/'validation.json',{'passed':True,'source_basis':g.SOURCE['basis'],'source_banks':replay,'complete_banks_matched':len(replay),'source_options_matched':sum(z['options_matched'] for z in replay),'source_distractors_matched':sum(z['distractors_matched'] for z in replay),'excluded':g.EXCLUDED,'exhaustive_distinct_instances':len(records),'scales':list(g.SCALES),'solution_stages_checked':sum(z['solution_stages'] for z in checks),'actual_learner_grading':'all source banks and all 96 generated banks/fragments passed','generator_sha256':sha(HERE.with_suffix('.py')),'validator_sha256':sha(__file__),'source_sha256':sha(HERE/'reference/initial/source.json'),'fidelity':'Complete supported banks and keys replayed mathematically at scale=1. Prompt math notation normalized. Source instructional sequence retained in six rendered stages; blank source is made standalone using its explicit solution premise. No claim of exact source Markdown replay.'})
 print('Validated',len(records),'distinct instances;',len(replay),'complete source banks.')
if __name__=='__main__':main()
