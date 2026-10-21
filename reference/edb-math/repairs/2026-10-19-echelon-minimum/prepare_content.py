"""Prepare repaired authored banks while preserving question/field identities."""
from pathlib import Path
import json, sys, random, itertools, uuid, copy
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=next(p for p in HERE.parents if (p/'Cargo.toml').exists())
sys.path[:0]=[str(ROOT),str(HERE)]
from validate import parse,entries,brute_minima,ref,g,check
from scripts.generator_publish import normalized_question
from capture.scripts.database.edn import kw,dumps

snapshot=ROOT/(HERE/'snapshot-path.txt').read_text()
kp=json.loads((snapshot/'kp.json').read_text())[0][0]
forms=[];records=[];audit=[]
for q in kp[':knowledge-point/questions']:
    m=parse(q[':question/problem']);mins=brute_minima(m)
    assert len(mins)==1
    f=q[':question/answer-fields'][0];oldkey=entries(f[':answer-field/correct'][':answer/value'])
    row={'question':q[':db/id'],'source':q.get(':question/math-academy-id'),'old_key':oldkey,'minimum':mins[0],'faulty_key':oldkey!=mins[0]}
    if not q.get(':question/math-academy-id'):
        cells=[(i,j) for i,row in enumerate(m) for j,v in enumerate(row) if v]
        wrong=[list(map(list,b)) for b in itertools.combinations(cells,len(mins[0])) if not ref(m,b)]
        bank=random.Random(q[':db/id']).sample(wrong,4)+mins
        random.Random(q[':db/id']+1).shuffle(bank)
        r=g.generate('moderate',q[':db/id'],parameters={'matrix':m,'bank':bank})
        fixed=r['question'];fixed[':question/id']=q[':question/id'];nf=fixed[':question/answer-fields'][0]
        nf[':answer-field/id']=f[':answer-field/id'];nf[':answer-field/key']=f[':answer-field/key']
        oldcorrect=nf[':answer-field/correct'][1]
        for a in nf[':answer-field/choices']:
            old=a[':answer/id'];a[':answer/id']=str(uuid.uuid5(uuid.UUID(f[':answer-field/id']),'minimum-v3/'+a[':answer/value']))
            if old==oldcorrect:nf[':answer-field/correct']=[':answer/id',a[':answer/id']]
            forms.append({kw('db/id'):a[':answer/id'],kw('answer/id'):uuid.UUID(a[':answer/id']),kw('answer/type'):kw('answer.type/text'),kw('answer/value'):a[':answer/value'],kw('db/ensure'):kw('answer/validate')})
        for a in f[':answer-field/choices']:forms.append([kw('db/retract'),f[':db/id'],kw('answer-field/choices'),a[':db/id']])
        for a in nf[':answer-field/choices']:forms.append([kw('db/add'),f[':db/id'],kw('answer-field/choices'),a[':answer/id']])
        forms.append([kw('db/cas'),f[':db/id'],kw('answer-field/correct'),f[':answer-field/correct'][':db/id'],nf[':answer-field/correct'][1]])
        for attr in ('question/problem','question/worked-solution'):
            forms.append([kw('db/cas'),q[':db/id'],kw(attr),q[':'+attr],fixed[':'+attr]])
        forms += [[kw('db/ensure'),f[':db/id'],kw('answer-field/validate')],[kw('db/ensure'),q[':db/id'],kw('question/validate')]]
        check(fixed);records.append(r)
        row['new_correct_uuid']=nf[':answer-field/correct'][1]
    elif q.get(':question/math-academy-id')=='q-73151':
        # Repair the known malformed conjunction without changing its meaning.
        for a in f[':answer-field/choices']:
            if a[':answer/value'].count('only')>1:
                value=g.entry_text(entries(a[':answer/value']))+' only'
                forms.append([kw('db/cas'),a[':db/id'],kw('answer/value'),a[':answer/value'],value])
                row['malformed_label_repaired']=a[':db/id']
    audit.append(row)
(HERE/'content-forms.edn').write_text(dumps(forms)+'\n')
(HERE/'repaired-records.json').write_text(json.dumps(records,indent=2)+'\n')
(HERE/'bank-audit.json').write_text(json.dumps({'basis':int(snapshot.name.split('-')[-1]),'questions':audit,'authored_banks_repaired':len(records),'faulty_keys':sum(r['faulty_key'] for r in audit)},indent=2)+'\n')
print(json.dumps({'audited':len(audit),'authored_banks_repaired':len(records),'faulty_keys':sum(r['faulty_key'] for r in audit),'forms':len(forms)}))
