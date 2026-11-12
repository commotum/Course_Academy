"""Exercise retained checker rejection and retired replay guards without EDB."""
import copy,importlib.util,json,subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[4];results=[]
for kp in [17592186092384,17592186092385]:
 D=H/str(kp);P=D/'package';sys.path.insert(0,str(P));spec=importlib.util.spec_from_file_location('checker_'+str(kp),P/'check_refill.py');checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
 for band in ['easy','moderate','hard']:
  record=json.loads((D/'verification'/f'{band}.json').read_text())[0];checker.check(record)
  for kind in ['supplied-work','radio-bank','wrong-key','retired-source']:
   bad=copy.deepcopy(record);q=bad['question'];field=q[':question/answer-fields'][0]
   if kind=='supplied-work':q[':question/problem']+='\n\nUse the negative reciprocal of the derivative.'
   elif kind=='radio-bank':field[':answer-field/type']=':answer-field.type/radio'
   elif kind=='wrong-key':field[':answer-field/choices'][0][':answer/value']='123456789'
   else:bad['generation']['source_refs' if kp==17592186092384 else 'source_references']=['q-47407' if kp==17592186092384 else 'q-10870']
   try:checker.check(bad)
   except (AssertionError,ValueError,KeyError):results.append(dict(kp=kp,band=band,mutation=kind,rejected=True))
   else:raise AssertionError((kp,band,kind,'regression not rejected'))
 if kp==17592186092385:
  rows=json.loads(subprocess.check_output([sys.executable,str(P/'generator.py'),'--replay-sources']));prov=json.loads((P/'source-provenance.json').read_text());assert all(not set(r['generation']['source_references'])&set(prov['forbidden_source_refs']) for r in rows);results.append(dict(kp=kp,replay_records=len(rows),retired_replays_absent=True,historical_source_file_preserved=True))
 sys.path.remove(str(P))
(H/'checker-regressions.json').write_text(json.dumps(dict(passed=True,checks=results,database_writes=0),indent=2)+'\n');print(len(results),'regressions passed')
