"""Prepare formatting-only CAS forms from the captured immutable database value."""
import collections,hashlib,json,re,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3];sys.path.insert(0,str(ROOT/'scripts'));sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import normalize_math_boundaries,validate_math_boundaries
from migrate_learner_history import dumps,kw
ATTRS={'question/problem','question/worked-solution','tutorial/content','multistep/context','answer/feedback','answer-field/feedback','assigned-problem/instructions'}

def main():
 snapshot=ROOT/'.local/edb/tex-boundary-current.jsonl';manifest=json.loads(snapshot.with_suffix('.manifest.json').read_text());values={};qfields=collections.defaultdict(set);fields=collections.defaultdict(dict);idents={};refs=collections.defaultdict(set);gens={};owners={}
 for r in map(json.loads,snapshot.open()):
  e,a,v=r['e'],r['a'],r['v']
  if a in ATTRS:values[e,a]=r
  if a=='question/answer-fields':qfields[e].add(v)
  if a in ('answer-field/key','answer-field/type'):fields[e][a]=v
  if a=='db/ident':idents[e]=v
  if a=='answer-field/choices':refs[e].add(v)
  if a=='question-generator/script':gens[e]=v
  if a=='knowledge-point/question-generator':owners[e]=v
 out=[];unresolved=[];actions=collections.Counter()
 for (e,a),r in values.items():
  before=r['v'];after=normalize_math_boundaries(before);special=[]
  if e==17592186124792 and a=='question/problem':
   # Source asks for a missing radio word; $$ is an empty captured formula,
   # and the ordinary TeX group around its equivalence array lacks its close.
   after=before.replace('is a $$ $','is a ? $').replace(r'\end{aligned}$',r'\end{aligned}}$');after=normalize_math_boundaries(after);special=['restore-visible-unknown-and-close-equivalence-group']
  try:validate_math_boundaries(after)
  except ValueError as ex:unresolved.append({'entity':e,'attribute':a,'error':str(ex),'after':after})
  if after==before:continue
  assert normalize_math_boundaries(after)==after,(e,a,'not idempotent')
  reasons=[]
  if re.search(r'\\begin\{(?:align\*?|eqnarray\*?)\}',before):reasons.append('protect-multiline-environment')
  if '[math]' in before or '[/math]' in before:reasons.append('recover-legacy-math-or-currency-marker')
  if re.search(r'\d%',before):reasons.append('escape-numeric-percentage')
  if re.search(r'(?m)^[ \t]{4,}(?:\$|\\\[)',before):reasons.append('deindent-math-opener')
  if '$$' in before and '$$' in after and before.count('$')!=after.count('$'):reasons.append('repair-empty-or-duplicated-delimiter')
  if r'\$' in after and r'\$' not in before:reasons.append('restore-literal-currency')
  if '<br>' in after and '<br>' not in before:reasons.append('separate-table-formula-row-break')
  if not reasons:reasons.append('repair-math-boundary-or-spacing')
  reasons+=special;actions.update(reasons)
  fs=[{'key':fields[f]['answer-field/key'],'type':idents[fields[f]['answer-field/type']]} for f in qfields[e]]
  out.append({'entity':e,'attribute':a,'before':before,'after':after,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest(),'reasons':reasons,'fields':fs,'old_t':r['t'],'old_source':r['source']})
 (HERE/'unresolved.json').write_text(json.dumps(unresolved,indent=2,ensure_ascii=False)+'\n');assert not unresolved,[(u['entity'],u['attribute'],u['error']) for u in unresolved[:10]]
 (HERE/'fields.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n');batches=[]
 for i in range(0,len(out),300):
  chunk=out[i:i+300];name=f'batch-{i//300+1:02}';folder=HERE/name;folder.mkdir(exist_ok=True);payload=dumps([[kw('db/cas'),f['entity'],kw(f['attribute']),f['before'],f['after']] for f in chunk])+'\n';assert len(payload.encode())<3_500_000;(folder/'transaction.edn').write_text(payload)
  (folder/'read-query.edn').write_text('[:find ?e ?a ?v :in $ [[?e ?a]] :where [?e ?a ?v]]\n');(folder/'read-inputs.edn').write_text(dumps([[[f['entity'],kw(f['attribute'])] for f in chunk]])+'\n');batches.append({'name':name,'fields':len(chunk),'sha256':hashlib.sha256(payload.encode()).hexdigest(),'field_keys':[[f['entity'],f['attribute']] for f in chunk]})
 (HERE/'batches.json').write_text(json.dumps(batches,indent=2)+'\n');report={'database':'math','basis_t':manifest['basis_t'],'prose_fields_scanned':len(values),'fields':len(out),'entities':len({f['entity'] for f in out}),'batches':len(batches),'attributes':dict(collections.Counter(f['attribute'] for f in out)),'actions':dict(actions),'unresolved':len(unresolved)};(HERE/'preparation.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))
 (HERE/'active-generators.json').write_text(json.dumps([{'kp':kp,'generator':g,'script':gens[g]} for kp,g in owners.items()],indent=2)+'\n')
if __name__=='__main__':main()
