"""Rebuild private human review artifacts from parameterized normal/public replay."""
import importlib.util,json,hashlib,sys
from pathlib import Path
import sympy as sp
HERE=Path(__file__).resolve().parent
s=importlib.util.spec_from_file_location('g',HERE.with_suffix('.py'));g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
cases=[];components=[];records=[];review=['# Circle equation from labeled center and radius\n\nOriginal labels and omissions below come from math basis 1356. Generated variants are clearly labeled; moderate/hard are authored extensions. Raw incomplete sources are evidence only.\n']
for sid,q in g.QUESTIONS.items():
    cases.append({'source_id':sid,'template':'missing_input_blank' if sid=='q-167932' else 'graph_radio','parameters':g.ORIGINAL[sid],'bank_profile':'raw:'+sid,'source_difficulty':'easy' if ':question/difficulty' in q else None,'authored_replay_workload':'easy' if ':question/difficulty' not in q else None})
    bank='blank' if sid=='q-167932' else sid
    source_choices=q[':question/answer-fields'][0][':answer-field/choices'];rows=[]
    for a,recipe in zip(source_choices,g.BANKS[bank]):rows.append({'source_answer_id':a[':answer/id'],'source_value':a[':answer/value'],'proposed_center':[recipe[0],recipe[1]],'proposed_squared_radius':recipe[2],'correct_observed':a[':answer/id']==q[':question/answer-fields'][0].get(':answer-field/correct',{}).get(':answer/id'),'recipe_interpretation':'Coordinate sign reversal/swap/origin omission and radius-not-squared/square-root radius, as indicated; author intention inferred only.'})
    components.append({'source_id':sid,'question_id':q[':question/id'],'bank':bank,'parameters':g.ORIGINAL[sid],'field_key':q[':question/answer-fields'][0][':answer-field/key'],'field_type':q[':question/answer-fields'][0][':answer-field/type'][':db/ident'],'choices':rows,'presence':{k:k in q for k in (':question/difficulty',':question/worked-solution',':question/answer-fields')},'correct_ref_present':':answer-field/correct' in q[':question/answer-fields'][0]})
    raw=g.generate('easy',parameters=g.ORIGINAL[sid],profile='raw:'+sid)
    review.append(f'## Original {sid} — '+('easy' if ':question/difficulty' in q else 'unrated; raw correct/solution absent')+'\n\n'+g.markdown(raw)+'\n')
    # Fix relative source image references for the human review only.
    review[-1]=review[-1].replace('![](images/','![](/media/jake/SSD/EDB/math/images/')
    for seed in (101,102):
        r=g.generate('easy',seed=seed,profile='completed:'+sid);records.append(r)
        review.append(f'### Generated easy variant, {sid} original bank, seed {seed}\n\n'+g.markdown(r)+'\n')
for level in ('easy','moderate','hard'):
    for seed in (42,57):
        r=g.generate(level,seed=seed,field_type='blank' if seed==57 else 'radio');records.append(r)
        review.append(f'## Generated {level} — '+('authored missing-level extension' if level!='easy' else 'authored common operation bank')+f', seed {seed}\n\n'+g.markdown(r)+'\n')
(HERE/'source-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(HERE/'source-components.json').write_text(json.dumps(components,indent=2)+'\n');(HERE/'review.json').write_text(json.dumps(records,indent=2)+'\n');(HERE/'review.md').write_text('\n'.join(review))
radii={sp.Rational(n,d) for d in (2,3,4) for n in range(3,20) if sp.Rational(n,d).q==d and 1<sp.Rational(n,d)<5};fractions={sp.Rational(n,d) for d in (2,3,4) for n in range(3,25) if sp.Rational(n,d).q==d and 1<=sp.Rational(n,d)<=6}
cap={'easy':16*16*8,'moderate':12*12*len(radii),'hard':2*len(fractions)**2*len(radii),'radius_forms':len(radii),'hard_positive_center_forms':len(fractions),'counting':'Distinct center and positive squared radius; layout, profile and orientation excluded. All authored complete banks valid because nonzero centers and radius >1; fraction denominators remain reduced.'};(HERE/'capabilities.json').write_text(json.dumps(cap,indent=2)+'\n')
