"""Build renderer coverage for all built KP source profiles and supported levels."""
import importlib.util,json,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
sys.path.insert(0,str(ROOT/'scripts/question_capture'))
from math_format import validate_generated_record
records=[];coverage={}
for kp in [17592186115241,17592186115242,17592186115299,17592186129114,17592186129176,17592186059768]:
    path=ROOT/f'generate/scratch/{kp}.py';spec=importlib.util.spec_from_file_location('kp'+str(kp),path);g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
    own=[]
    if kp in [17592186115241,17592186115242]:
        for c in json.loads(path.with_suffix('').joinpath('source-cases.json').read_text()):
            if kp==17592186115241:
                own.append(g.generate('easy',7,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']))
            else:own.append(g.generate(c['level'],33,template=c['template'],parameters=c['parameters'],profile=c['bank_profile']))
    elif kp==17592186115299:
        for name in g.TEMPLATES:own.append(g.generate('moderate',731,template=name))
    elif kp==17592186129114:
        for name in g.PROFILES:own.append(g.generate('easy',73,profile=name))
    elif kp==17592186129176:
        for name in g.CASES:own.append(g.generate('easy',73,profile=name))
    else:
        for name,src in g.PROFILES.items():own.append(g.generate(src[':question/difficulty'][':db/ident'].split('/')[-1],73,name))
    levels=['easy'] if kp in [17592186129114,17592186129176] else list(g.SUPPORTED) if kp==17592186059768 else ['easy','moderate','hard']
    for level in levels:
        for seed in [0,1,5]:own.append(g.generate(level,seed))
    for r in own:validate_generated_record(r)
    records+=own;coverage[str(kp)]={'records':len(own),'levels':levels}
(HERE/'generator-smoke.json').write_text(json.dumps({'records':records,'coverage':coverage,'errors':[]},indent=2)+'\n')
print(json.dumps({'records':len(records),'coverage':coverage}))
