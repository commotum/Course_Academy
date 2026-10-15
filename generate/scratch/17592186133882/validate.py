"""Independent display parsing, exhaustive bounded-domain and actual grader checks."""
import hashlib,importlib.util,json,re,subprocess,sys,uuid
from pathlib import Path
import sympy as sp
from math_parser import expression,equivalent,X,Y
HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('greens_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
ENGINE=ROOT/'generate/runs/current/check-engine'
RAW=json.loads((HERE/'source.json').read_text())
SOURCES={q[':question/math-academy-id']:q for q in RAW['record'][':knowledge-point/questions']}
VALID_SOURCES={
 'q-109161':(sp.exp(X)*sp.cos(2*Y),sp.exp(X)*sp.sin(2*Y)),
 'q-109112':(Y*sp.sin(Y)-X**2*Y,X*sp.sin(Y)+X*Y*sp.cos(Y)),
 'q-109114':(Y**2*sp.exp(X*Y),2*X*Y*sp.exp(X*Y)),
 'q-109196':(X**2-Y**2,-2*sp.sin(X*Y)),
 'q-109199':(sp.cos(2*X*Y),2*sp.sin(X*Y)**2),
 'q-109129':(X*sp.exp(-Y**2),X**2*Y*sp.exp(-Y**2)),
}
EXCLUDED={
 'q-108588':'Two distinct distractor IDs have equal value (x^3+y^3)/3. Complete valid five-choice bank cannot be replayed without an authored repair; excluded.',
 'q-109111':'Source solution repeats integral with xy instead of supplied 3xy. Generator corrects the displayed integral; original is preserved and conservatively excluded from validated stock.',
 'q-109130':'arctan(y/x) is undefined at the triangle vertex (0,2); stated open-neighborhood Green hypothesis fails. No automatic source repair.',
 'q-169203':'Prompt references missing diagram, vector field and previous part. Cannot derive answer from captured prompt.',
 'q-109120':'sqrt(y) is not defined on an open real neighborhood of the boundary point y=0. Stated Green hypotheses require a domain correction, not an automatic coefficient variant.',
 'q-108830':'Solution identifies Q as x^3*y+y although prompt supplies x^3*y+sin(y). Correct curl agrees but source solution mismatch remains unchanged.',
}

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

def math_bank(q,P,Q):
 f=q[':question/answer-fields'][0];assert len(f[':answer-field/choices'])==5
 correct=f[':answer-field/correct'][1];curl=sp.simplify(sp.diff(Q,X)-sp.diff(P,Y))
 vals=[expression(a[':answer/value']) for a in f[':answer-field/choices']]
 for i,a in enumerate(f[':answer-field/choices']):
  assert equivalent(vals[i],curl)==(a[':answer/id']==correct)
  assert all(not equivalent(vals[i],b) for b in vals[:i]),'Duplicate options'
 assert sum(a[':answer/id']==correct for a in f[':answer-field/choices'])==1
 return curl

def validate_instance(rec):
 q=rec['question'];p=rec['generation']['parameters'];assert rec['knowledge_point']['db_id']==g.KP_ID
 assert rec==g.generate('easy',seed=rec['generation']['seed'],parameters=p)
 prompt=q[':question/problem'];solution=q[':question/worked-solution']
 match=re.search(r'\\oint_C \\left\((.*?)\\right\)\\,dx\+\\left\((.*?)\\right\)\\,dy',prompt,re.S);assert match
 P,Q=map(expression,match.groups());curl=math_bank(q,P,Q)
 assert equivalent(P,p['a']*Y**2) and equivalent(Q,p['b']*X*Y)
 assert '$(-1,0),(1,0)$ and $(0,1),$' in prompt and 'counterclockwise' in prompt
 py=re.search(r'\\frac\{\\partial P\}\{\\partial y\}&=(.*?),\\\\',solution)
 qx=re.search(r'\\frac\{\\partial Q\}\{\\partial x\}&=(.*?)\.\\end',solution)
 assert py and qx
 assert equivalent(expression(py[1]),sp.diff(P,Y)) and equivalent(expression(qx[1]),sp.diff(Q,X))
 final=re.search(r'Hence, \$f\(x,y\)=(.*?)\.\$',solution);assert final and equivalent(expression(final[1]),curl)
 # Check the actual repeated integral and the two concrete subtraction operands.
 repeated=re.search(r'\\begin\{aligned\}(\\oint_C .*?)&=',solution);assert repeated and repeated[1]==match[0]
 sub=re.search(r'&=\\iint_D\\left\(\((.*?)\)-\((.*?)\)\\right\)',solution);assert sub
 assert equivalent(expression(sub[1]),sp.diff(Q,X)) and equivalent(expression(sub[2]),sp.diff(P,Y))
 simplified=re.search(r'&=\\iint_D\\left\(([^&]*?)\\right\)\\,dA\.\\end',solution);assert simplified and equivalent(expression(simplified[1]),curl)
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
 return tuple(sp.srepr(sp.expand(v)) for v in (P,Q))

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
 records=[g.generate('easy',parameters={'a':a,'b':b}) for a,b in g.DOMAIN]
 keys=[validate_instance(r) for r in records];assert len(keys)==len(set(keys))==41
 # Every slot value and the full bounded parameter domain are exercised.
 assert {r['generation']['parameters']['a'] for r in records}==set(range(1,6))
 assert {r['generation']['parameters']['b'] for r in records}==set(range(1,10))
 original=SOURCES['q-109111'];replay=g.generate('easy',parameters={'a':1,'b':3});f=original[':question/answer-fields'][0]
 actual=replay['question'][':question/answer-fields'][0]
 matches=[]
 for a in f[':answer-field/choices']:
  matching=[b for b in actual[':answer-field/choices'] if equivalent(expression(a[':answer/value']),expression(b[':answer/value']))]
  assert len(matching)==1
  assert (a[':answer/id']==f[':answer-field/correct'][':answer/id'])==(matching[0][':answer/id']==actual[':answer-field/correct'][1])
  matches.append({'source_answer':a[':answer/id'],'source_value':a[':answer/value'],'generated_value':matching[0][':answer/value'],'matched':True})
 source_records=[]
 for sid,(P,Q) in VALID_SOURCES.items():
  r=normalize(SOURCES[sid]);math_bank(r['question'],P,Q);source_records.append(r)
 n=native(records+source_records,HERE/'validation-grading')
 asset=Path('/media/jake/SSD/EDB/math')/g.IMAGE;assert asset.is_file()
 asset_hash=hashlib.sha256(asset.read_bytes()).hexdigest();assert asset.stem==asset_hash
 save(HERE/'source-fidelity.json',{'supported_source':'q-109111','distractors_matched':4,'distractors_total':4,'banks_matched':1,'banks_total':1,'choices':matches,'source_solution_correction':'Repeated integral xy corrected to 3xy; orientation made explicit following diagram. Source facts are never modified.','other_families_supported':False})
 save(HERE/'review.json',records[:2]+[records[-1]])
 (HERE/'review.md').write_text('\n\n---\n\n'.join(map(g.markdown,records[:2]+[records[-1]])))
 save(HERE/'validation.json',{'passed':True,'source_basis':RAW['basis'],'supported_levels':['easy'],'unsupported_levels':['moderate','hard'],'supported_templates':['triangle-polynomial'],'complete_parameter_domain_cases':len(records),'distinct_mathematical_tasks':len(set(keys)),'slot_a_values':list(range(1,6)),'slot_b_values':list(range(1,10)),'deterministic_replay':all(r==g.generate('easy',r['generation']['seed'],r['generation']['parameters']) for r in records),'source_fidelity':{'matched_distractors':4,'total_distractors':4,'matched_banks':1,'total_supported_banks':1},'validated_available_source_candidates':list(VALID_SOURCES),'excluded_sources':EXCLUDED,'native_accepted':n['accepted_checks'],'native_rejected':n['rejected_checks'],'native_unresolved':0,'grader_executable_sha256':hashlib.sha256(ENGINE.read_bytes()).hexdigest(),'generator_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'asset':{'reference':g.IMAGE,'sha256':asset_hash,'reused_unchanged':True,'visually_inspected':True},'fixed_target':'scalar curl Q_x-P_y; same variable roles on a fixed positively oriented triangle','changed_target_case':'Not applicable: target is fixed by method; both coefficient slots exhaustively exercised.'})
 print(json.dumps({'passed':True,'domain':len(records),'native_accepted':n['accepted_checks'],'native_rejected':n['rejected_checks']}))
if __name__=='__main__':main()
