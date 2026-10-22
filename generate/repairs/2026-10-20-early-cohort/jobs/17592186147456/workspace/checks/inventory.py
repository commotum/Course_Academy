"""Read-only reconstruction of captured non-source inventory records."""
import copy
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import validate as v

inventory=v.json.loads((v.H.parent/'source/inventory.json').read_text())
records=[];affected=[];tested=[]
for q in inventory['questions']:
    if q.get(':question/math-academy-id'):
        tested.append({'id':q[':question/id'],'status':'source record; not relabeled as generated'})
        continue
    rows=[f[':answer-field/key'].strip('$') for f in q[':question/answer-fields'] if '=' in f[':answer-field/key']]
    if len(rows)!=3:
        tested.append({'id':q[':question/id'],'status':'untested: could not reconstruct three equations'})
        continue
    triples=[]
    for row in rows:
        lhs,rhs=row.split('=');left=v.parse(lhs);right=v.parse(rhs)
        triples.append((v.sp.diff(left,v.g.D),left.subs(v.g.D,0),right))
    candidates=[]
    for template,(level,base) in v.g.CASES.items():
        assignment=[]
        for m,a,b in triples:
            found=[]
            for j,(mm,aa,bb) in enumerate(base):
                ls=v.sp.simplify(a/aa);rs=v.sp.simplify(b/bb)
                if v.sp.simplify(m-mm)==0 and ls.is_Integer and rs.is_Integer and 1<=ls<=5 and 1<=rs<=5:
                    found.append((j,int(ls),int(rs)))
            if len(found)!=1:break
            assignment.append(found[0])
        if len(assignment)==3 and {a[0] for a in assignment}=={0,1,2}:
            candidates.append((template,level,assignment))
    assert len(candidates)==1,(q[':question/id'],candidates)
    t,level,assignment=candidates[0]
    p={'left_scales':[0]*3,'right_scales':[0]*3}
    for j,l,r in assignment:p['left_scales'][j]=l;p['right_scales'][j]=r
    reproduced=v.g.generate(level,0,t,p)
    eqs=v.prompt_equations(reproduced['question'][':question/problem'])
    truths=[v.independent_truth(m*v.g.D+a-b) for m,a,b in triples]
    assert truths==[v.correct_value(f)=='true' for f in q[':question/answer-fields']]
    assert all(v.sp.simplify(v.normalized(m*v.g.D+a-b)-v.normalized(eqs[j]))==0 for (m,a,b),(j,_,_) in zip(triples,assignment))
    # Complete stored record, with captured IDs and choices unchanged. Metadata
    # states exactly what was recovered; no seed or historical provenance is invented.
    rec={'knowledge_point':reproduced['knowledge_point'],'question':copy.deepcopy(q),
         'generation':{'evidence_only':True,'eligible_for_learning':False,
                       'inventory_basis':inventory['basis'],'template':t,
                       'parameters':p,'row_assignment':[a[0] for a in assignment],
                       'original_generation_metadata':None,
                       'reproduction':'Visible mathematical equations match current generator at these explicit original-power parameters; original runtime seed/version not supplied.'}}
    records.append(rec)
    item={'id':q[':question/id'],'template':t,'parameters':p,'truths':truths,'semantically_reproduced':True}
    tested.append(item)
    # Every inferred legacy template freezes these outcomes under scalar changes.
    # The stronger item-level defect in the two all-false stored records is also retained.
    finding='Recognizable legacy x-function/power family has a fixed qualifying subset under every coefficient-only variation; mathematical reconstruction matches this stored item.'
    if not any(truths):finding+=' All three checkbox keys are false and there is no visible None option, so no correct selectable option exists.'
    affected.append({'question_id':q[':question/id'],'entity_id':q[':db/id'],'finding':finding,
                     'reproduction':f'{sys.executable} checks/inventory.py (template {t}, parameters {v.json.dumps(p,sort_keys=True)})',
                     'evidence_path':'../workspace/evidence/generated-records.json'})
assert len(records)==7
v.save(v.E/'generated-records.json',records)
v.save(v.H/'affected-inventory.json',{'affected_questions':affected})
v.save(v.E/'inventory-report.json',{'basis':inventory['basis'],'inspected':len(inventory['questions']),'non_source_records_reconstructed':len(records),'empty_correct_subsets':sum(not any(x['truths']) for x in tested if 'truths' in x),'items':tested,'limits':'Inventory has no generation metadata. Mathematical parameters and row assignment were recovered, not historical seeds/version. Original source questions were not marked generated. No database writes.'})
print(f'Inspected {len(inventory["questions"])} inventory records; reconstructed {len(records)} non-source records; two lack a correct selectable option')
