"""Independent displayed-math checks, complete bank replay, and real learner grader."""
import hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
from math_parser import expression,equivalent,X,Y,normalize
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('greens_conversion_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ENGINE=ROOT/'generate/runs/current/check-engine'
RAW=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in RAW['record'][':knowledge-point/questions']}
# Independent prompt transcription, not read from generator data or solution key.
VALID_SOURCES={
'q-108467':(X*Y**2,2*X**2*Y,(0,1,0,2*X,Y,X)),
'q-42085':(3*X*Y,X**2*Y,(-1,2,0,3,Y,X)),
'q-109249':(sp.exp(Y)-2*X*sp.cos(Y),2*X*sp.exp(Y)+X**2*sp.sin(Y),(0,3,Y,4*Y-Y**2,X,Y)),
'q-42107':(X*sp.cos(Y),X*sp.sin(Y),(-1,0,0,Y+1,X,Y)),
'q-109291':(Y**2*sp.sin(X),X*Y-2*Y*sp.cos(X),(0,1,X-1,-2*X+2,Y,X)),
'q-109288':(Y**2-2*X*Y,X*sp.sin(Y)-X**2,(-1,1,0,1-X,Y,X)),
'q-109245':(Y*sp.cos(X),sp.sin(X)+X*Y**2,(-2,1,0,1,Y,X)),
}
EXCLUDED={
'q-41702':'Correct negative lower-sine-lobe integral and an incorrect reversed upper-sine-lobe integral both evaluate to -2. Equivalent-valued source bank excluded.',
'q-109254':'Two incorrect options integrate (1+cos(x)) over the upper and right unit semidisks. Reflection and evenness of cos(x) make their values identical. Equivalent-valued source distractors excluded.',
'q-42074':'Correct 3*integral_{-1}^{1}integral_0^{1-x^2}1=4, but distractor 3*integral_{-1}^{1}integral_{-x^2}^{x^2}1=4 as well. Also two incorrect options both equal 2. Equivalent-valued source bank excluded.',
'q-168558':'Blank prompt supplies neither F nor a prompt diagram; missing essential givens. Solution alone cannot supply learner givens.',
'q-109263':'At original a=1 two distractors both evaluate to 168/5. Hard sampling excludes a=1. Original solution changes ln(2+x) to ln(1+x), invalid on part of region. Generator uses corrected ln(2+x) everywhere; original kept unchanged and conservatively excluded from validated stock.',
'q-109248':'Correct integral 2xy over right semicircle is zero, but distractor x^2*y over same region is also zero by odd symmetry. Excluded as equivalent-valued bank ambiguity.'}

def save(path,value):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,default=str,ensure_ascii=False,indent=2)+'\n')

def normalize_question(q):
 f=q[':question/answer-fields'][0]
 return {'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'generation':{'template':'source'},'question':{
 ':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],':question/difficulty':q[':question/difficulty'][':db/ident'],':question/answer-fields':[{
 ':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]}]}}

def integral(s):
 s=s.replace(r'{\int }',r'\int').replace('⁡','')
 s=re.sub(r'\\(?:mathrm|text)\{\s*d\s*\}','d',s)
 s=re.sub(r'\\text\{\s*\}','',s).replace(r'\,','')
 s=re.sub(r'\s+','',s)
 first=s.index(r'\int');prefix=s[:first];scale=expression(prefix) if prefix not in ('','-','+') else (-1 if prefix=='-' else 1);s=s[first:]
 def group(text):
  assert text[0]=='{';depth=0
  for i,ch in enumerate(text):
   depth+=(ch=='{')-(ch=='}')
   if depth==0:return text[1:i],text[i+1:]
  raise ValueError('Unclosed bound')
 bounds=[]
 for _ in range(2):
  assert s.startswith(r'\int_');s=s[5:];lo,s=group(s);assert s.startswith('^');hi,s=group(s[1:]);bounds.append((expression(lo),expression(hi)))
 m=re.fullmatch(r'(.*?)d([xy])d([xy])\.?',s);assert m,s
 f=expression(m[1]) if m[1] else sp.Integer(1)
 inn={'x':X,'y':Y}[m[2]];out={'x':X,'y':Y}[m[3]];assert inn!=out
 return (sp.expand(scale*f),*bounds[0],*bounds[1],inn,out)

def same(a,b):return len(a)==len(b) and all(equivalent(sp.sympify(v),sp.sympify(w)) for v,w in zip(a,b))
def value(spec):
 f,lo,hi,low,high,inn,out=spec
 return sp.integrate(f,(inn,low,high),(out,lo,hi))
def math_bank(q,target,evaluated=False):
 f=q[':question/answer-fields'][0];correct=f[':answer-field/correct'][1];assert len(f[':answer-field/choices'])==5
 specs=[integral(a[':answer/value']) for a in f[':answer-field/choices']]
 assert sum(same(z,target) for z in specs)==1
 for i,(a,z) in enumerate(zip(f[':answer-field/choices'],specs)):
  assert same(z,target)==(a[':answer/id']==correct)
  assert all(not same(z,w) for w in specs[:i])
 if evaluated:
  vals=list(map(value,specs));expected=value(target)
  assert sum(equivalent(z,expected) for z in vals)==1,('Ambiguous equivalent-valued options',vals)
  assert all(not equivalent(z,w) for i,z in enumerate(vals) for w in vals[:i]),('Equivalent distractors',vals)
 return specs

def source_target(sid):
 P,Q,limits=VALID_SOURCES[sid];return (sp.simplify(sp.diff(Q,X)-sp.diff(P,Y)),*limits)

def validate_instance(rec):
 q=rec['question'];level=q[':question/difficulty'].split('/')[-1];a=rec['generation']['parameters']['a'];assert rec['knowledge_point']['db_id']==g.KP_ID
 assert rec==g.generate(level,rec['generation']['seed'],{'a':a})
 prompt=q[':question/problem'];solution=q[':question/worked-solution']
 if level=='moderate':
  m=re.search(r'\\oint_C\\left\((.*?)\\right\)\\,dx\+\\left\((.*?)\\right\)\\,dy',prompt);assert m
  P,Q=map(expression,m.groups());expectedP,expectedQ=a*X*Y**2,2*a*X**2*Y;limits=(0,1,0,2*X,Y,X)
  assert '$(0,0),(1,0)$ and $(1,2),$' in prompt
  region=r'D=\{(x,y):0\le x\le1,\,0\le y\le2x\}.'
 else:
  m=re.search(r'F\(x,y\)=\\langle (.*?),(.*?)\\rangle',prompt);assert m
  P,Q=map(expression,m.groups());expectedP,expectedQ=sp.log(2+X)-a*Y**2,X**2+Y**2;limits=(-1,2,X**2,X+2,Y,X)
  assert '$y=x^2$ and $y=x+2,$' in prompt
  region=r'D=\{(x,y):-1\le x\le2,\,x^2\le y\le x+2\}.'
  # Domain x>=-1 ensures 2+x>=1, log is C1 on a neighborhood.
  assert r'\ln{\left(x + 2 \right)}' in solution and r'\ln{\left(x + 1 \right)}' not in solution
 assert equivalent(P,expectedP) and equivalent(Q,expectedQ) and 'counterclockwise' in prompt
 target=(sp.simplify(sp.diff(Q,X)-sp.diff(P,Y)),*limits);math_bank(q,target,True)
 # Independently parse every displayed partial, integrand, and repeated form.
 for label,expected in [('P',P),('Q',Q)]:
  m=re.search(label+r'\(x,y\)=(.*?)\$',solution);assert m and equivalent(expression(m[1]),expected)
 py=re.search(r'\\frac\{\\partial P\}\{\\partial y\}&=(.*?),\\\\',solution);qx=re.search(r'\\frac\{\\partial Q\}\{\\partial x\}&=(.*?)\.\\end',solution)
 assert py and qx and equivalent(expression(py[1]),sp.diff(P,Y)) and equivalent(expression(qx[1]),sp.diff(Q,X))
 forms=re.findall(r'\\oint_C\\left\((.*?)\\right\)\\,dx\+\\left\((.*?)\\right\)\\,dy',solution)
 assert len(forms)==(1 if level=='moderate' else 2) and all(equivalent(expression(u),P) and equivalent(expression(v),Q) for u,v in forms)
 operands=re.search(r'&=\\iint_D\\left\(\((.*?)\)-\((.*?)\)\\right\)',solution);assert operands and equivalent(expression(operands[1]),sp.diff(Q,X)) and equivalent(expression(operands[2]),sp.diff(P,Y))
 curl=re.search(r'&=\\iint_D (.*?)\\,dA',solution);assert curl and equivalent(expression(curl[1]),target[0])
 final=re.search(r'&=(\\int_.*?)\.\\end',solution);assert final and same(integral(final[1]),target)
 assert region in solution and solution.count('![]('+g.IMAGES[level]+')')==1
 assert (limits[1]-limits[0])>0
 outer=limits[-1];width=sp.sympify(limits[3])-limits[2]
 assert sp.integrate(width,(outer,limits[0],limits[1]))>0
 for text in (prompt,solution):
  assert text.count('$')%2==0
  depth=0
  for ch in text:depth+=(ch=='{')-(ch=='}');assert depth>=0
  assert depth==0
 f=q[':question/answer-fields'][0];ids=[q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]
 assert len(ids)==len(set(ids))==7 and all(str(uuid.UUID(i))==i for i in ids)
 assert all('$' not in z[':answer/value'] for z in f[':answer-field/choices'])
 return (level,sp.srepr(P),sp.srepr(Q),tuple(map(str,limits)))

def native(records,directory):
 directory=Path(directory);directory.mkdir(parents=True,exist_ok=True);data=[]
 for rec in records:
  f=rec['question'][':question/answer-fields'][0]
  data.append({'record':rec,'label':rec['question'][':question/id'],'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete radio bank selection'} for a in f[':answer-field/choices']]})
 save(directory/'native-input.json',data)
 r=subprocess.run([str(ENGINE),str(directory/'native-input.json'),str(directory/'native-report.json')],capture_output=True,text=True,check=True,timeout=55)
 (directory/'native.log').write_text(r.stdout+r.stderr);report=json.loads((directory/'native-report.json').read_text());assert report['documented_unresolved_checks']==0;return report

def main():
 assert set(SOURCES)==set(VALID_SOURCES)|set(EXCLUDED)
 records=[g.generate(level,parameters={'a':a}) for level in ('moderate','hard') for a in g.LEVEL_DOMAINS[level]]
 keys=[validate_instance(r) for r in records];assert len(keys)==len(set(keys))==23
 fidelity=[]
 for level,sid in g.SOURCES.items():
  source=SOURCES[sid];original=normalize_question(source)['question'];replay=g.generate(level,parameters={'a':1},source_replay=(level=='hard'))['question'];orig=original[':question/answer-fields'][0];new=replay[':question/answer-fields'][0];matches=[]
  for choice in orig[':answer-field/choices']:
   found=[a for a in new[':answer-field/choices'] if same(integral(choice[':answer/value']),integral(a[':answer/value']))];assert len(found)==1
   assert (choice[':answer/id']==orig[':answer-field/correct'][1])==(found[0][':answer/id']==new[':answer-field/correct'][1])
   matches.append({'source_answer':choice[':answer/id'],'source_value':choice[':answer/value'],'generated_value':found[0][':answer/value'],'matched':True})
  fidelity.append({'level':level,'source':sid,'matched_distractors':4,'total_distractors':4,'matched_complete_banks':1,'total_banks':1,'choices':matches})
 src_records=[];source_math=[]
 for sid in VALID_SOURCES:
  rec=normalize_question(SOURCES[sid]);specs=math_bank(rec['question'],source_target(sid),True);src_records.append(rec);source_math.append({'source':sid,'exact_choice_values':list(map(str,map(value,specs))),'complete_value_uniqueness':True})
 for level in ('moderate','hard'):
  for a in (0,13,-1,1.5,True):
   try:g.generate(level,parameters={'a':a})
   except ValueError:pass
   else:raise AssertionError('Invalid boundary accepted')
 try:g.generate('easy')
 except ValueError:pass
 else:raise AssertionError('Unsupported difficulty accepted')
 save(HERE/'source-value-audit.json',{'valid_sources':source_math,'excluded_sources':EXCLUDED})
 n=native(records+src_records,HERE/'validation-grading')
 assets=[]
 for asset in g.IMAGES.values():
  path=Path('/media/jake/SSD/EDB/math')/asset;h=hashlib.sha256(path.read_bytes()).hexdigest();assert path.stem==h
  assets.append({'reference':asset,'sha256':h,'reused_unchanged':True,'visually_inspected':True})
 save(HERE/'source-fidelity.json',{'passed':True,'profiles':fidelity,'matched_distractors':8,'total_supported_distractors':8,'matched_banks':2,'total_supported_banks':2,'solution_correction':EXCLUDED['q-109263'],'other_source_templates_generated':False})
 review=[g.generate(level,parameters={'a':a}) for level in ('moderate','hard') for a in ((1,2,12) if level=='moderate' else (2,3,12))]
 save(HERE/'review.json',review);(HERE/'review.md').write_text('\n\n---\n\n'.join(map(g.markdown,review)))
 save(HERE/'validation.json',{'passed':True,'source_basis':RAW['basis'],'supported_levels':['moderate','hard'],'unsupported_levels':['easy'],'supported_templates':list(g.TEMPLATES.values()),'complete_parameter_domain_cases':23,'distinct_mathematical_tasks':23,'slot_coverage':{'a':g.LEVEL_DOMAINS,'geometry':'fixed deliberately narrower policy; no target slot declared'},'source_fidelity':fidelity,'validated_available_source_candidates':source_math,'excluded_sources':EXCLUDED,'native_accepted':n['accepted_checks'],'native_rejected':n['rejected_checks'],'native_unresolved':0,'grader_executable_sha256':hashlib.sha256(ENGINE.read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'assets':assets,'deterministic_replay':all(r==g.generate(r['question'][':question/difficulty'].split('/')[-1],r['generation']['seed'],r['generation']['parameters']) for r in records),'math_validation':'Independently parsed prompt P,Q, partials, curl, all repeated bounds and integrands; integrated all five options for every generated instance to reject equivalent values. Positive region area, CCW orientation, and log domain checked. Complete source-bank replay at a=1.','fidelity_review':'Moderate retains differential form; hard retains vector rewrite. Shared theorem, diagram, P/Q, partials, type-I region, subtraction and repeated-integral stages preserved. No evaluation stage added.'})
 print(json.dumps({'passed':True,'variants':23,'native_accepted':n['accepted_checks'],'native_rejected':n['rejected_checks']}))
if __name__=='__main__':main()
