"""Exact source/generated mathematics, task deduplication and native grading."""
from db_support import *
import copy,re,sympy as sp

def normalize(q):
 def enum(x):return str(x[':db/ident']) if isinstance(x,dict) else str(x)
 return {':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':enum(q[':question/difficulty']),':question/answer-fields':sorted([{':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':enum(f[':answer-field/type']),':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])] if isinstance(f[':answer-field/correct'],dict) else f[':answer-field/correct'],':answer-field/choices':sorted([{':answer/id':str(a[':answer/id']),':answer/type':enum(a[':answer/type']),':answer/value':a[':answer/value']} for a in f[':answer-field/choices']],key=lambda a:a[':answer/id'])} for f in q[':question/answer-fields']],key=lambda f:f[':answer-field/key'])}
def ordered(q):
 q=copy.deepcopy(q)
 q[':question/answer-fields'].sort(key=lambda f:f[':answer-field/key'])
 for f in q[':question/answer-fields']:f[':answer-field/choices'].sort(key=lambda a:a[':answer/id'])
 return q

def parse(t):
 t=t.replace(r'\:', '')
 t=t.replace(r'\operatorname{cos}',r'\cos').replace(r'\operatorname{sin}',r'\sin')
 t=re.sub(r'(?<=[a-zA-Z0-9)}])(?=\\(?:sin|cos)|(?:\{e\}|e)\^)', '*',t)
 e=v.parse_math(t)
 return e.subs({s:g.__dict__[str(s)] for s in e.free_symbols if str(s) in ('x','y','z','u','v')})
def printed(q):
 text=q[':question/problem'];vectors=re.findall('⟨(.*?)⟩|'+re.escape(r'\left\langle')+'(.*?)'+re.escape(r'\right\rangle'),text,re.S)
 assert len(vectors)>=2
 F,r=[sp.Matrix([parse(t.strip()) for t in re.split(r'\\,|,',a or b) if t.strip()]) for a,b in vectors[:2]]
 assert len(F)==len(r)==3
 return F,r

def fingerprint(q):
 F,r=printed(q);N=r.diff(g.u).cross(r.diff(g.v))
 # Ignore inactive components, option banks, seed, identity, difficulty and hint.
 values=list(r)+[F[i] if sp.simplify(N[i])!=0 else sp.Integer(0) for i in range(3)]
 return hashlib.sha256(json.dumps([sp.srepr(sp.expand(t)) for t in values]).encode()).hexdigest()

def source_check(q):
 F,r=printed(q);N=r.diff(g.u).cross(r.diff(g.v));P=F.subs(dict(zip((g.x,g.y,g.z),r)),simultaneous=True)
 G=sp.trigsimp(sp.expand(sum(P[i]*N[i] for i in range(3))))
 f=q[':question/answer-fields'][0];assert len(q[':question/answer-fields'])==1 and str(f[':answer-field/type'][':db/ident'])==':answer-field.type/radio'
 if 'what is the value of $a+b' in q[':question/problem']:
  expected=sp.simplify(G.subs({g.u:1,g.v:0 if q.get(':question/math-academy-id')=='q-161306' else 1}))
 else:expected=G
 values=[parse(a[':answer/value']) for a in f[':answer-field/choices']];assert len(values)==5
 assert all(not v.eq(a,b) for i,a in enumerate(values) for b in values[:i])
 assert [str(a[':answer/id']) for a,val in zip(f[':answer-field/choices'],values) if v.eq(val,expected)]==[str(f[':answer-field/correct'][':answer/id'])]
 hints=re.findall(r'\times.*?=⟨(.*?)⟩',q[':question/problem'])
 if hints:
  shown=sp.Matrix([parse(t) for t in hints[0].split(r'\,')]);assert all(v.eq(a,b) for a,b in zip(shown,N))
 return {'source_id':q.get(':question/math-academy-id'),'integrand':str(G),'correct':str(expected),'choices_checked':5,'fingerprint':fingerprint(q)}

def validate(r):
 assert r['knowledge_point']=={'db_id':KP,'id':g.KP_UUID,'title':g.TITLE}
 m=r['generation'];l=r['question'][':question/difficulty'].split('/')[-1];assert l in LEVELS
 replay=g.generate(l,seed=m['seed'],template=m['template'],parameters=m['parameters'],profile=m['bank_profile'])
 assert ordered(replay['question'])==ordered(r['question']) and replay['generation']==m
 v.check(r)
 F,R=printed(r['question']);M=m['mathematics']
 assert all(v.eq(a,sp.sympify(b,locals={**g.LOCALS,'x':g.x,'y':g.y,'z':g.z})) for a,b in zip(list(F)+list(R),M['F']+M['r']))
 return fingerprint(r['question'])

def native(records,path):
 path.mkdir(parents=True,exist_ok=True);items=[]
 for r in records:
  f=r['question'][':question/answer-fields'][0]
  items.append({'label':r['question'][':question/id'],'record':r,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'Every field-owned radio option'} for a in f[':answer-field/choices']]})
 save(path/'input.json',items)
 subprocess.run([str(OUT/'check-engine'),str(path/'input.json'),str(path/'report.json')],check=True,capture_output=True,text=True,timeout=55)
 assert json.loads((path/'report.json').read_text())['documented_unresolved_checks']==0

USAGE='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/items ?i] [?i :task-item/content ?q]]'''
RESERVED='''[:find ?q :in $ ?kp ?learner :where [?l :learner/id ?learner] [?kp :knowledge-point/questions ?q] [?l :learner/activity ?t] [?t :learner-task/status ?status] (or [?status :db/ident :learner-task.status/started] [?status :db/ident :learner-task.status/paused] [?status :db/ident :learner-task.status/unlocked]) [?t :learner-task/activity ?a] [?a :activity/steps ?s] [?s :step/content ?q]]'''
def counts(kp,b,path):
 shown={x[0] for x in DB.query(USAGE,[KP,LEARNER],path,'ever-shown',b,history=True)}
 reserved={x[0] for x in DB.query(RESERVED,[KP,LEARNER],path,'reserved',b)}
 examples={x[0] for x in DB.query('[:find ?q :in $ ?kp :where [?kp :knowledge-point/questions ?q] [_ :knowledge-point/canonical-example ?q]]',[KP],path,'examples',b)}
 known={r['question'][':question/id']:r for p in OUT.glob('basis-*/generated.json') for r in json.loads(p.read_text())};levels={l:set() for l in LEVELS};records=[];excluded=[];source=[]
 for q in kp[':knowledge-point/questions']:
  level=str(q.get(':question/difficulty',{}).get(':db/ident','')).split('/')[-1]
  if ':question/math-academy-id' in q:source.append(source_check(q))
  if q[':db/id'] in shown|reserved|examples or level not in LEVELS or not q.get(':question/worked-solution'):
   excluded.append({'question':str(q[':question/id']),'reason':'shown/reserved/canonical/unrated/incomplete'});continue
  if ':question/math-academy-id' not in q:validate(known[str(q[':question/id'])]);assert normalize(q)==ordered(known[str(q[':question/id'])]['question'])
  levels[level].add(fingerprint(q));records.append({'knowledge_point':{'title':g.TITLE},'question':normalize(q)})
 native(records,path/'native');result={'basis':b,'distinct_available':{l:len(x) for l,x in levels.items()},'source_mathematics':source,'excluded':excluded,'ever_shown':sorted(shown),'reserved':sorted(reserved),'validated_available_ids':[r['question'][':question/id'] for r in records]};save(path/'counts.json',result);return result
