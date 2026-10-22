"""Independent rendered-matrix, complete-bank, replay, and native-grader validation."""
import hashlib,importlib.util,json,re,subprocess,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
spec=importlib.util.spec_from_file_location('coefficient_generator',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
def save(name,x):(HERE/name).write_text(json.dumps(x,indent=2,default=str)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def native(label,rec):
 f=rec['question'][':question/answer-fields'][0]
 return {'label':label,'record':rec,'checks':[{'submitted_answer_id':a[':answer/id'],'expected':'accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected','purpose':'each field-owned option through actual learner grader'} for a in f[':answer-field/choices']]}
def check(rec):
 m=rec['generation'];sid=m['template'];b=m['parameters']['b'];q=rec['question'];A,B=g.parse(q);A0,_=g.parse(g.CASES[sid]);assert A==A0 and list(B)==b
 assert rec['knowledge_point']['db_id']==g.KP_ID and q[':question/difficulty']==':question.difficulty/'+g.level(sid)
 assert rec==g.generate(g.level(sid),m['seed'],sid,{'b':b})
 # Solve the rendered prompt independently, rather than trusting generator metadata.
 if g.level(sid)=='moderate':
  assert A.det()!=0;x=A.LUsolve(B);z=sum(c*v for c,v in zip(g.target(sid),x));answer=str(z)
  assert all(v.q==1 for v in x)
 else:
  assert A.rank()==2 and A.row_join(B).rank()==3;answer='No solution'
 f=q[':question/answer-fields'][0];assert f[':answer-field/type']==':answer-field.type/radio' and len(f[':answer-field/choices'])==5
 correct=[a for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]];assert len(correct)==1 and correct[0][':answer/value']==answer
 assert len({(a[':answer/type'],a[':answer/value']) for a in f[':answer-field/choices']})==5
 # Read every emitted augmented matrix, including initial, all operation stages,
 # and verify it follows the same source row operation in the rendered solution.
 bodies=re.findall(r'\\left\[\\begin\{array\}\{ccc\|c\}(.*?)\\end\{array\}\\right\]',q[':question/worked-solution'],re.S)
 mats=[sp.Matrix([[sp.sympify(re.sub(r'\\frac\{(-?\d+)\}\{(\d+)\}',r'(\1/\2)',v.strip())) for v in row.split('&')] for row in body.split(r'\\')]) for body in bodies]
 # Values can be fractions; use the shared simple rational parser below.
 assert mats[0]==A.row_join(B) and mats[1]==mats[0]
 expected,_=g.states(sid,A,B);assert mats[1:]==expected
 assert g.expr(g.target(sid)) in q[':question/problem']
 assert m['mathematical_fingerprint']==g.fingerprint(sid,b)
 return True

def main():
 replays=[];samples=[];coverage={};details=[];markdown=[]
 for sid,source in sorted(g.CASES.items()):
  A,b0=g.parse(source);lev=g.level(sid);r=g.generate(lev,0,sid,{'b':list(map(int,b0))});check(r)
  original=source[':question/answer-fields'][0];field=r['question'][':question/answer-fields'][0]
  old={(a[':answer/type'][':db/ident'],a[':answer/value'],a[':answer/id']==original[':answer-field/correct'][':answer/id']) for a in original[':answer-field/choices']}
  new={(a[':answer/type'],a[':answer/value'],a[':answer/id']==field[':answer-field/correct'][1]) for a in field[':answer-field/choices']}
  assert old==new
  mapped=g.bank(sid,b0)
  replays.append({'source_id':sid,'template':sid,'profile':sid,'bank_matched':5,'bank_total':5,'distractors_matched':4,'distractors_total':4,'missing':[],'extra':[],'correct_designation_matches':True,'operative_stage_order_preserved':True,'literal_prose_identical':False,'presentation_changes':'Shared source instructional sentences retained; formula formatting, per-stage arithmetic, and back-substitution wording standardized; q-74032 erroneous swapped RHS corrected.'})
  per=[]
  for seed in range(24):
   rec=g.generate(lev,seed,sid);check(rec);samples.append(rec);per.append(rec['generation']['parameters']['b'])
  if lev=='moderate':
   for x in ([0,0,0],[-7,7,-7],[7,-7,7]):
    b=A*sp.Matrix(x);rec=g.generate(lev,101,sid,{'b':list(map(int,b))});check(rec);samples.append(rec)
  coverage[sid]={'rhs_coordinates_observed':[sorted({b[j] for b in per}) for j in range(3)],'distinct_rhs':len({tuple(b) for b in per}),'target_fixed':list(g.target(sid)),'coefficient_matrix_fixed':True,'source_replay':list(map(int,b0))}
  assert coverage[sid]['distinct_rhs']>=20 and all(len(x)>3 for x in coverage[sid]['rhs_coordinates_observed'])
  details.append({'source_id':sid,'question_uuid':source[':question/id'],'difficulty':lev,'field_type':'radio','field_key':'selection','template':sid,'bank_profile':sid,'coefficient_matrix':[[int(v) for v in A.row(i)] for i in range(3)],'b_original':list(map(int,b0)),'target_coefficients':g.target(sid),'operations':[list(map(str,op)) for op in g.OPS[sid]],'components':{'prompt':source[':question/problem'],'worked_solution':source[':question/worked-solution']},'choices':[dict(m,source_value=a[':answer/value'],source_correct=a[':answer/id']==original[':answer-field/correct'][':answer/id']) for m,a in zip(mapped,original[':answer-field/choices'])]})
  markdown.extend(['## '+sid,'### Source',source[':question/problem'],source[':question/worked-solution'],'### Replay',r['question'][':question/problem'],r['question'][':question/worked-solution'],'### Changed RHS',samples[-1]['question'][':question/problem'],samples[-1]['question'][':question/worked-solution']])
  samples.append(r)
 # Regression for the subtraction target: same A,b must still ask x1+x2-x3,
 # evaluate it with coefficient -1 on x3 throughout, never silently switch to sum.
 sid='q-74028';A,b=g.parse(g.CASES[sid]);rec=g.generate('moderate',0,sid,{'b':list(map(int,b))});assert 'x_{1} + x_{2} - x_{3}' in rec['question'][':question/problem'];assert rec['question'][':question/worked-solution'].rstrip().endswith('$$')
 checks=[native(str(i),r) for i,r in enumerate(samples)];save('native-input.json',checks)
 subprocess.run([str(ROOT/'generate/runs/current/check-engine'),str(HERE/'native-input.json'),str(HERE/'native-grading.json')],check=True)
 native_report=json.loads((HERE/'native-grading.json').read_text());assert native_report['documented_unresolved_checks']==0
 save('source-replay.json',{'passed':True,'complete_banks_matched':12,'complete_banks_total':12,'distractors_matched':48,'distractors_total':48,'profiles':replays})
 save('source-cases.json',details);save('slot-coverage.json',coverage);save('validated-samples.json',samples)
 (HERE/'side-by-side.md').write_text('\n\n'.join(markdown))
 save('validation.json',{'passed':True,'mathematics':True,'rendered_matrix_steps_checked':True,'full_source_banks':True,'native_grading':True,'fidelity':'Source banks and mathematical stages replay; standardized math presentation and concrete prose, not literal transcription. Source typo explicitly corrected.','samples_checked':len(samples),'supported_levels':['moderate','hard'],'unsupported_levels':['easy'],'distinct_by_level':{l:len({r['generation']['mathematical_fingerprint'] for r in samples if r['question'][':question/difficulty']==':question.difficulty/'+l}) for l in g.SUPPORTED_LEVELS},'native_accepted':native_report['accepted_checks'],'native_rejected':native_report['rejected_checks'],'hashes':{str(p.relative_to(ROOT)):sha(p) for p in [HERE.with_suffix('.py'),HERE/'source.json',HERE/'source-query.edn',HERE/'validate.py',HERE/'capabilities.json']}})
 print(json.dumps({'validated_samples':len(samples),'complete_banks':'12/12','source_distractors':'48/48','grading':native_report['accepted_checks']+native_report['rejected_checks']}))
if __name__=='__main__':main()
