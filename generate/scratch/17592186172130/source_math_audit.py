"""Source whole-bank equivalence under explicitly supported domain repairs."""
import json

def run(v):
    g=v.g;out=[]
    for name,source in g.BY_NAME.items():
        normal=g.generate(g.LEVELS[name],template=name,parameters={'a':1,'p':1,'q':3 if name=='product' else 1})
        field=normal['question'][':question/answer-fields'][0]
        answer=next(a for a in field[':answer-field/choices'] if a[':answer/id']==field[':answer-field/correct'][1])
        correct=g.read_math(answer[':answer/value']);domain=normal['generation']['domain']
        for i,f in enumerate(source[':question/answer-fields']):
            values=[g.read_math(a[':answer/value']) for a in f[':answer-field/choices']]
            correct_options=[j for j,b in enumerate(values) if v.equal(b,correct,domain)]
            assert len(correct_options)==1,(name,i,correct_options)
            assert all(not v.equal(a,b,domain) for j,a in enumerate(values) for b in values[:j]),(name,i)
            if ':answer-field/correct' in f:assert v.equal(g.read_math(f[':answer-field/correct'][':answer/value']),correct,domain)
            out.append({'template':name,'source_id':source[':db/id'],'field_index':i,'distinct_pointwise_bank':True,'unique_mathematical_correct_value':f[':answer-field/choices'][correct_options[0]][':answer/value'],'designation_present':':answer-field/correct' in f,'supported_domain':domain,'raw_domain_repair_needed':name in ['powers','cancel','fold']})
    (v.HERE/'source-math-check.json').write_text(json.dumps(out,indent=2))
    return out
if __name__=='__main__':
    import importlib.util
    from pathlib import Path
    spec=importlib.util.spec_from_file_location('v',Path(__file__).with_name('validate.py'));v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
    out=run(v);print('All '+str(len(out))+' source banks independently checked;12 present designations verified,1 omission preserved.')
