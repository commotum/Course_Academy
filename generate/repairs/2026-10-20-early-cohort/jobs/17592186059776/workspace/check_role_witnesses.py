"""Close sampled rank/position coverage gaps with fixed-prompt witnesses.
These bank-only changes are explicitly not counted as new semantic instances.
"""
import json, importlib.util
import check_repair as c
spec=importlib.util.spec_from_file_location('witness',c.ROOT/'17592186059776/validate.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
records=[];summary={};cases=[]
for sid,q in c.g.CASES.items():
    ranks=set();positions=set();attempts=0; retained=[]
    for seed in range(100):
        r=c.g.generate(q[':question/difficulty'][':db/ident'].split('/')[-1],seed,sid,[2,3]);f=c.features(r);attempts+=1
        if f['rank'] not in ranks or f['position'] not in positions:
            v.independent(r);records.append(r);retained.append({'seed':seed,'rank':f['rank'],'position':f['position']})
            cases.append({'label':'role:'+r['question'][':question/id'],'record':r,'checks':v.checks(r)})
        ranks.add(f['rank']);positions.add(f['position'])
        if ranks==positions==set(range(1,6)):break
    assert ranks==positions==set(range(1,6)),(sid,ranks,positions)
    summary[sid]={'ranks':sorted(ranks),'positions':sorted(positions),'attempts':attempts,'witnesses':retained,'parameters':[2,3]}
out=c.ROOT/'evidence/roles';out.mkdir(exist_ok=True)
(out/'records.json').write_text(json.dumps(records,indent=2));(out/'native-input.json').write_text(json.dumps(cases,indent=2));(out/'coverage.json').write_text(json.dumps(summary,indent=2))
print(json.dumps({'families':len(summary),'every_rank_and_position_witnessed':True,'retained_bank_witnesses':len(records),'new_semantic_instances_claimed':0}))
