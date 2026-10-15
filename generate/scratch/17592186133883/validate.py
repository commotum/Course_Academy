"""Independent display parsing, exhaustive bounded-domain and actual grader checks."""
import hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
from math_parser import expression,equivalent,X,Y
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('greens_evaluation_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ENGINE=ROOT/'generate/runs/current/check-engine'
RAW=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in RAW['record'][':knowledge-point/questions']}
# P,Q and exact iterated limits, independently transcribed from prompts/regions.
VALID_SOURCES={
 'q-109147':(sp.exp(X)-2*X**2*Y,sp.exp(Y)+2*X*Y**2,(X,-Y,Y),(Y,0,2)),
 'q-41810':(sp.cos(Y),X**2-2*Y,(Y,0,sp.pi),(X,0,sp.pi)),
 'q-109115':(3*X*Y-1,3*X**2+sp.exp(Y),(Y,X**2,2*X),(X,0,2)),
 'q-109151':(sp.exp(X)-Y**2,sp.exp(Y)+X**2,(Y,-1,1),(X,-1,1)),
 'q-109160':(2*Y-X,5*X-Y,(Y,X**2-X,X),(X,0,2)),
 'q-109164':(2*X*Y,Y**2,(Y,X**2/3,sp.sqrt(3*X)),(X,0,3)),
 'q-109166':(2*X+Y**2,X**2+2*Y,(Y,0,X**2/3),(X,0,3)),
 'q-109157':(2*X+sp.exp(X)*sp.sin(Y),X+sp.exp(X)*sp.cos(Y),(Y,X-5,1),(X,0,4)),
 'q-41475':(6*X**2-X*Y+11,Y**2+1,(Y,-X/2,X/2),(X,0,2)),
 'q-109149':(X*Y,2*X**2+Y,(Y,0,2),(X,-1,3)),
 'q-109144':(2*X*Y-Y**2,X**2+2*X,(Y,0,1-X),(X,-1,1)),
}
EXCLUDED={'q-41811':'Q contains ln(y), undefined on the y=0 boundary of the supplied triangle; the line integral and stated Green hypotheses fail. Preserve source; exclude from validated stock.'}

def save(path,value):
 path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(json.dumps(value,default=str,ensure_ascii=False,indent=2)+'\n')

def normalize(q):
 f=q[':question/answer-fields'][0]
 return {'knowledge_point':{'db_id':g.KP_ID,'id':g.KP_UUID,'title':g.TITLE},'generation':{'template':'source'},'question':{
  ':question/id':str(q[':question/id']),':question/problem':q[':question/problem'],':question/worked-solution':q[':question/worked-solution'],
  ':question/difficulty':q[':question/difficulty'][':db/ident'],':question/answer-fields':[{
   ':answer-field/id':str(f[':answer-field/id']),':answer-field/key':f[':answer-field/key'],':answer-field/type':f[':answer-field/type'][':db/ident'],
   ':answer-field/correct':[':answer/id',str(f[':answer-field/correct'][':answer/id'])],
   ':answer-field/choices':[{':answer/id':str(a[':answer/id']),':answer/type':a[':answer/type'][':db/ident'],':answer/value':a[':answer/value']} for a in f[':answer-field/choices']]}]}}

def math_bank(q,answer):
 f=q[':question/answer-fields'][0];assert len(f[':answer-field/choices'])==5
 correct=f[':answer-field/correct'][1]
 vals=[expression(a[':answer/value']) for a in f[':answer-field/choices']]
 for i,a in enumerate(f[':answer-field/choices']):
  assert equivalent(vals[i],answer)==(a[':answer/id']==correct)
  assert all(not equivalent(vals[i],b) for b in vals[:i]),'Duplicate options'
 assert sum(a[':answer/id']==correct for a in f[':answer-field/choices'])==1
 return answer

def source_answer(sid):
 P,Q,inner,outer=VALID_SOURCES[sid]
 return sp.integrate(sp.diff(Q,X)-sp.diff(P,Y),inner,outer)

def validate_instance(rec):
 q=rec['question'];p=rec['generation']['parameters'];assert rec['knowledge_point']['db_id']==g.KP_ID
 assert rec==g.generate('hard',seed=rec['generation']['seed'],parameters=p)
 prompt=q[':question/problem'];solution=q[':question/worked-solution']
 m=re.search(r'F\(x,y\)=\\langle (.*?),(.*?)\\rangle',prompt);assert m
 P,Q=map(expression,m.groups());a=p['a']
 assert equivalent(P,6*X**2-a*X*Y+11) and equivalent(Q,Y**2+1)
 curl=sp.diff(Q,X)-sp.diff(P,Y)
 answer=sp.integrate(curl,(Y,-X/2,X/2),(X,0,2));math_bank(q,answer)
 # Independent direct line integral over three CCW edges, without Green's theorem.
 t=sp.symbols('t',real=True);vertices=[(0,0),(2,-1),(2,1),(0,0)];direct=0
 for (u,v),(w,z) in zip(vertices,vertices[1:]):
  px,py=u+(w-u)*t,v+(z-v)*t
  direct+=sp.integrate(P.subs({X:px,Y:py})*(w-u)+Q.subs({X:px,Y:py})*(z-v),(t,0,1))
 assert equivalent(direct,answer)
 assert '$(0,0),$ $(2,-1)$ and $(2,1),$' in prompt and 'counterclockwise' in prompt
 py=re.search(r'\\frac\{\\partial P\}\{\\partial y\}&=(.*?),\\\\',solution)
 qx=re.search(r'\\frac\{\\partial Q\}\{\\partial x\}&=(.*?)\.\\end',solution)
 assert py and qx
 assert equivalent(expression(py[1]),sp.diff(P,Y)) and equivalent(expression(qx[1]),sp.diff(Q,X))
 repeated=re.findall(r'\\oint_C \\left\((.*?)\\right\)\\,dx\+\\left\((.*?)\\right\)\\,dy',solution)
 assert len(repeated)==2 and all(equivalent(expression(z[0]),P) and equivalent(expression(z[1]),Q) for z in repeated)
 sub=re.search(r'&=\\iint_D\\left\(\((.*?)\)-\((.*?)\)\\right\)',solution);assert sub
 assert equivalent(expression(sub[1]),sp.diff(Q,X)) and equivalent(expression(sub[2]),sp.diff(P,Y))
 inner=re.search(r'&=\\int_0\^2\\int_\{-x/2\}\^\{x/2\} (.*?)\\,dy',solution);assert inner and equivalent(expression(inner[1]),curl)
 stages=re.findall(r'&=\\int_0\^2 (.*?)\\,dx',solution);assert len(stages)==3
 assert equivalent(expression(stages[-1]),sp.integrate(curl,(Y,-X/2,X/2)))
 anti=re.search(r'&=\\left\[(.*?)\\right\]_0\^2',solution);assert anti
 A=expression(anti[1]);assert equivalent(sp.diff(A,X),expression(stages[-1]))
 final=re.findall(r'&=([^&]*?)\.\\end\{aligned\}',solution);assert final and equivalent(expression(final[-1]),answer)
 assert r'D=\{(x,y):0\le x\le2,\,-x/2\le y\le x/2\}.' in solution
 assert solution.count('![]('+g.IMAGE+')')==1
 for text in (prompt,solution):
  assert text.count('$')%2==0 and '{{' not in text
  depth=0
  for char in text:
   depth+=(char=='{')-(char=='}');assert depth>=0
  assert depth==0
 f=q[':question/answer-fields'][0];ids=[q[':question/id'],f[':answer-field/id']]+[a[':answer/id'] for a in f[':answer-field/choices']]
 assert len(ids)==len(set(ids))==7 and all(str(uuid.UUID(i))==i for i in ids)
 assert all('$' not in a[':answer/value'] for a in f[':answer-field/choices'])
 return ('triangle-0-2-plus-minus-x/2',sp.srepr(sp.expand(curl)))

def native(records,directory):
 directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
 data=[]
 for rec in records:
  f=rec['question'][':question/answer-fields'][0]
  data.append({'record':rec,'label':rec['question'][':question/id'],'checks':[
   {'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'complete radio bank selection'} for a in f[':answer-field/choices']]})
 save(directory/'native-input.json',data)
 result=subprocess.run([str(ENGINE),str(directory/'native-input.json'),str(directory/'native-report.json')],capture_output=True,text=True,check=True,timeout=55)
 (directory/'native.log').write_text(result.stdout+result.stderr)
 r=json.loads((directory/'native-report.json').read_text());assert r['documented_unresolved_checks']==0
 return r

def main():
 assert set(SOURCES)==set(VALID_SOURCES)|set(EXCLUDED)
 records=[g.generate('hard',parameters={'a':a}) for a in g.DOMAIN]
 keys=[validate_instance(r) for r in records];assert len(keys)==len(set(keys))==12
 assert {r['generation']['parameters']['a'] for r in records}==set(range(1,13))
 for a in (0,13,-1,1.5,True):
  try:g.generate('hard',parameters={'a':a})
  except ValueError:pass
  else:raise AssertionError('invalid boundary accepted')
 for level in ('easy','moderate'):
  try:g.generate(level)
  except ValueError:pass
  else:raise AssertionError('unsupported level accepted')
 original=SOURCES['q-41475'];replay=g.generate('hard',parameters={'a':1});f=original[':question/answer-fields'][0]
 actual=replay['question'][':question/answer-fields'][0];matches=[]
 for a in f[':answer-field/choices']:
  matching=[b for b in actual[':answer-field/choices'] if equivalent(expression(a[':answer/value']),expression(b[':answer/value']))]
  assert len(matching)==1
  assert (a[':answer/id']==f[':answer-field/correct'][':answer/id'])==(matching[0][':answer/id']==actual[':answer-field/correct'][1])
  matches.append({'source_answer':a[':answer/id'],'source_value':a[':answer/value'],'generated_value':matching[0][':answer/value'],'matched':True})
 source_records=[];source_math=[]
 for sid in VALID_SOURCES:
  r=normalize(SOURCES[sid]);answer=source_answer(sid);math_bank(r['question'],answer);source_records.append(r)
  source_math.append({'source':sid,'computed_integral':str(answer),'correct_bank_verified':True})
 n=native(records+source_records,HERE/'validation-grading')
 asset=Path('/media/jake/SSD/EDB/math')/g.IMAGE;assert asset.is_file()
 asset_hash=hashlib.sha256(asset.read_bytes()).hexdigest();assert asset.stem==asset_hash
 save(HERE/'source-fidelity.json',{'supported_source':'q-41475','distractors_matched':4,'distractors_total':4,'banks_matched':1,'banks_total':1,'choices':matches,'other_families_supported':False,'notation_review':'Vector-field response, five scalar choices, integral rewrite, partials, type-I region, inner evaluation and cubic antiderivative preserved. Counterclockwise text makes inspected diagram orientation explicit.'})
 save(HERE/'review.json',[records[0],records[1],records[-1]])
 (HERE/'review.md').write_text('\n\n---\n\n'.join(map(g.markdown,[records[0],records[1],records[-1]])))
 save(HERE/'validation.json',{'passed':True,'source_basis':RAW['basis'],'supported_levels':['hard'],'unsupported_levels':['easy','moderate'],'supported_templates':['triangle-linear-curl'],'complete_parameter_domain_cases':12,'distinct_mathematical_tasks':12,'slot_a_values':list(range(1,13)),'source_fidelity':{'matched_distractors':4,'total_distractors':4,'matched_banks':1,'total_supported_banks':1},'validated_available_source_candidates':source_math,'excluded_sources':EXCLUDED,'native_accepted':n['accepted_checks'],'native_rejected':n['rejected_checks'],'native_unresolved':0,'grader_executable_sha256':hashlib.sha256(ENGINE.read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'asset':{'reference':g.IMAGE,'sha256':asset_hash,'reused_unchanged':True,'visually_inspected':True},'fixed_target':'Evaluate complete line integral around the same CCW triangle; no target-position slot declared.','slot_coverage':'All 12 coefficient values; negative, zero, out-of-range and noninteger rejection; prompt, both repeated integrals, partials, inner integral, antiderivative and answer independently parsed.','independent_math':'Direct parametric integration around all three oriented edges agrees with Green integration for all 12 variants.','deterministic_replay':all(r==g.generate('hard',r['generation']['seed'],r['generation']['parameters']) for r in records)})
 print(json.dumps({'passed':True,'domain':len(records),'native_accepted':n['accepted_checks'],'native_rejected':n['rejected_checks']}))
if __name__=='__main__':main()
