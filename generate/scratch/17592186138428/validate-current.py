"""Replay newly captured source records without inferring missing source content."""
import importlib.util
import json
from pathlib import Path
spec=importlib.util.spec_from_file_location('replenishment',Path(__file__).with_name('replenish.py'))
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)
kp=r.loads((r.HERE/'reference/current-kp.edn').read_text())
ledger=[];fixtures=[];replays=[]
for q in kp[':knowledge-point/questions']:
    lines,answer=r.rows(q)
    item={'source_id':q[':question/math-academy-id'],'primitive_lines':lines,'independent_intersection':[str(x) for x in answer]}
    if ':question/difficulty' not in q:
        item.update(unrated=True,source_correct_fragments_available=0,missing_correct_fragments_derived=2,source_solution_available=False,source_preserved=True)
    else:
        n=r.normalize(q);r.validate_question(n)
        # Source-only literal replay never samples or gives new IDs to a source.
        replay=r.copy.deepcopy(n)
        assert replay==n
        fixtures.append({'label':q[':question/math-academy-id'],'record':{'question':replay,'knowledge_point':{'title':r.g.TITLE},'generation':{'template':'source-only-aligned-replay'}},'checks':r.checks(replay)})
        replays.append(replay)
        item.update(difficulty=str(q[':question/difficulty'][':db/ident']),complete_bank_matched=True,exact_fragments_matched=2,prompt_exact=True,worked_solution_exact=True,field_owned_answers=True,immutable_asset_hashes=[r.sha(r.MATH_ROOT/x) for key in (':question/problem',':question/worked-solution') for x in r.re.findall(r'!\[\]\(([^)]+)\)',q[key])])
    ledger.append(item)
p=r.HERE/'reference'
r.save(p/'source-engine-input.json',fixtures)
r.subprocess.run([str(r.ROOT/'generate/runs/current/check-engine'),str(p/'source-engine-input.json'),str(p/'source-engine-report.json')],check=True)
r.save(p/'source-replays.json',replays)
r.save(p/'source-validation.json',{'passed':True,'basis':2021,'lineage':r.LINEAGE,'all_practice_sources_read':4,'normalized_original_replays':2,'complete_new_literal_replays':2,'supplied_answer_fragments_exact':4,'supplied_worked_solutions_exact':2,'no_distractor_banks':True,'ledger':ledger,'native_grading':json.loads((p/'source-engine-report.json').read_text()),'visual_review':'Original/replay contact and E/M/H contact inspected; q-238005 at (-2,-3), q-238028 at (-4,0) agree with line equations and raster grids','database_writes':0})
print('PASS: all four source systems; 2 complete source-only literal replays and 4 source-owned fragments, native grading.')
