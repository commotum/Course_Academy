"""Bind sampled records to native whole-question checks and player fixtures."""
import copy
import itertools
import json
from pathlib import Path
import subprocess

H=Path(__file__).resolve().parent
ROOT=H.parents[3]
engine=[];visual=[]
for kp in [17592186119924,17592186119925]:
    for band in ['easy','moderate','hard']:
        records=json.loads((H/'verification'/str(kp)/(band+'.json')).read_text())
        empty=[]
        for index,r in enumerate(records):
            q=r['question'];checks=[];fields=q[':question/answer-fields']
            assert len(fields)==3
            if all(next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])=='false' for f in fields):empty.append(index)
            for j,f in enumerate(fields):
                assert f[':answer-field/type']==':answer-field.type/checkbox'
                assert f[':answer-field/key'] not in ('I','II','III','None','None of the above')
                assert {a[':answer/value'] for a in f[':answer-field/choices']}=={'true','false'}
                for a in f[':answer-field/choices']:
                    checks.append(dict(field_index=j,submitted_answer_id=a[':answer/id'],expected='accepted' if a[':answer/id']==f[':answer-field/correct'][1] else 'rejected',purpose='Exact generated owned Boolean answer'))
            mapped=[]
            for bits in itertools.product((False,True),repeat=3):
                answers=[next(a[':answer/id'] for a in f[':answer-field/choices'] if a[':answer/value']==str(b).lower()) for f,b in zip(fields,bits)]
                mapped.append(dict(old_answer=list(bits),answer_ids=answers,expected=all(a==f[':answer-field/correct'][1] for a,f in zip(answers,fields))))
            contextual=copy.deepcopy(r)
            contextual['knowledge_point']={'db_id':kp,'title':'Linear Dependence and Independence'}
            contextual['generation'].setdefault('template',str(contextual['generation'].get('version','checkbox')))
            engine.append(dict(label=f'{kp}/{band}/{index}',record=contextual,checks=checks,mapped_responses=mapped))
        assert empty,'Every reviewed band must exercise its empty-subset case.'
        for index in sorted({0,1,empty[0]}):
            q=copy.deepcopy(records[index]['question']);q[':db/id']=len(visual)+1
            q[':question/difficulty']={':db/ident':q[':question/difficulty']}
            # Local numeric identities model the API's resolved references.
            # All rendered text, keys, choices and truth values remain exact.
            for j,f in enumerate(q[':question/answer-fields']):
                f[':db/id']=10000+10*len(visual)+j;f[':answer-field/type']={':db/ident':f[':answer-field/type']}
                correct=f[':answer-field/correct'][1]
                for z,a in enumerate(f[':answer-field/choices']):
                    a[':db/id']=20000+20*len(visual)+2*j+z;a[':answer/type']={':db/ident':a[':answer/type']}
                f[':answer-field/correct']=next(a for a in f[':answer-field/choices'] if a[':answer/id']==correct)
            visual.append(q)
(H/'engine-input.json').write_text(json.dumps(engine,indent=2)+'\n')
(H/'speculative-questions.json').write_text(json.dumps(visual,indent=2)+'\n')
subprocess.run(['/tmp/checkbox-generator-fix-grade',str(H/'engine-input.json'),str(H/'engine-report.json')],check=True)
prior=(ROOT/'reference/edb-math/repairs/2026-11-10-homogeneous-checkboxes/check_player.py').read_text()
prior=prior.replace('17592186397107,17592186311909',','.join(str(i+1) for i in range(min(len(visual),6))))
prior=prior.replace('checkbox_toggles=144,saved_correct_restorations=24','checkbox_toggles=6*len(checks),saved_correct_restorations=len(checks)')
(H/'check_player.py').write_text(prior)
print(f'Checked {len(engine)} exact generated questions; prepared {len(visual)} representative UI fixtures.')
