"""Regression 9a89e94337b098d0aba5: visible-bank witnesses, no service writes.

For each quotient family/profile and fixed independent factor, change only n.
Every choice bank must be identical and four different equations must become
correct. Thus no deterministic function of that visible bank can identify the
correct equation for all four prompts. Mathematical validity is checked by the
independent visible TeX reader, not generation metadata.
"""
import collections,importlib.util,json,pathlib,sys
sys.dont_write_bytecode=True
from repair_regression import ROOT,g,probe
from visible_math import check_record,resolved,same
E=ROOT/'evidence/revision-2';E.mkdir(exist_ok=True)
spec=importlib.util.spec_from_file_location('review_bank_attack',E/'before/bank_shortcut.py')
a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
def choices(r):return r['question'][':question/answer-fields'][0][':answer-field/choices']
def correct(r):
 f=r['question'][':question/answer-fields'][0]
 return next(c[':answer/value'] for c in choices(r) if c[':answer/id']==f[':answer-field/correct'][1])
def visible_bank(r):return sorted(c[':answer/value'] for c in choices(r))
def attack(r,method):
 cs=choices(r);idx=method(cs)
 return idx is not None and cs[idx][':answer/value']==correct(r)
def check_group(rs):
 banks=[visible_bank(r) for r in rs]
 assert all(b==banks[0] for b in banks), 'correct power leaks into visible bank construction'
 keys=[correct(r) for r in rs]
 assert len(set(keys))==4, 'controlled prompt change must change correct equation in the same bank'
 assert all(check_record(r)['passed'] for r in rs), 'visible equation or solution is incorrect'
 # Each reported attack is held to its real output, including arbitrary mode ties.
 # Since bank ordering is also fixed here, it can succeed on at most one prompt.
 stats={name:sum(attack(r,method) for r in rs) for name,method in [('review_modal',a.choose),('review_repeated_lhs_shortest',a.power_sign_shortest)]}
 assert all(n<=1 for n in stats.values()), 'reported prompt-blind strategy remains reliable'
 # No repeated-LHS subset of size three, and no unique fractionless key.
 for r in rs:
  assert not probe(r)['shortcut_success']
  left=collections.Counter(c[':answer/value'].split('=')[0] for c in choices(r))
  assert 3 not in left.values(), 'reported shortest repeated-LHS subset persists'
 return {'same_bank':True,'correct_equations':keys,'records':len(rs),'attack_successes':stats,'prompt_blind_ceiling':1/4}
def main():
 records=[];groups=[]
 for t,base in [('simple_quotient',{}),('exp_quotient',{'base':2,'a':1}),('exp_quotient',{'base':5,'a':5})]:
  for seed in (0,1):
   rs=[g.generate_easy(seed,t,parameters={**base,'n':n}) for n in range(1,5)]
   groups.append({'template':t,'seed':seed,'parameters_held_fixed':base,**check_group(rs)})
   records+=rs
 exact=[g.generate_easy(17,'simple_quotient',parameters={'n':1}),g.generate_easy(2404317989,'exp_quotient',parameters={'base':4,'a':4,'n':4})]
 exact_results=[{'question_id':r['question'][':question/id'],'modal_correct':attack(r,a.choose),'repeated_lhs_shortest_correct':attack(r,a.power_sign_shortest),'math':check_record(r)} for r in exact]
 # The exact historical attack must now fail, not just change IDs or parameters.
 assert all(not v['modal_correct'] and not v['repeated_lhs_shortest_correct'] and v['math']['passed'] for v in exact_results), 'latest exact counterexample persists'
 records+=exact
 (E/'regression-records.json').write_text(json.dumps(records,indent=2,ensure_ascii=False)+'\n')
 (E/'bank-signature-regression.json').write_text(json.dumps({'finding':'9a89e94337b098d0aba5','passed':True,'groups':groups,'exact_counterexamples':exact_results,'records':len(records),'interpretation':'Identical banks with four different keys disprove deterministic inference of the key from answer strings. Chance hits remain possible; no claim of zero chance hits.'},indent=2,ensure_ascii=False)+'\n')
 print('bank-signature regression:',len(groups),'same-bank groups;',len(records),'independent math cases; both exact historical attacks fail')
if __name__=='__main__':main()
