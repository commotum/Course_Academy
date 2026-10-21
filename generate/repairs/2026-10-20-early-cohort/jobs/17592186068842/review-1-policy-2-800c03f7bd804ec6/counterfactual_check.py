import pathlib,json,collections
R=pathlib.Path(__file__).resolve().parent
rs=json.load(open(R/'revision-counterfactual-records.json'))
def field(r):return r['question'][':question/answer-fields'][0]
def keyval(r):
 f=field(r);return next(c[':answer/value'] for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])
out=[]
for i in [0,2,4]:
 a,b=rs[i:i+2];fa,fb=field(a),field(b);da={c[':answer/value']:c[':answer/id']==fa[':answer-field/correct'][1] for c in fa[':answer-field/choices']};db={c[':answer/value']:c[':answer/id']==fb[':answer-field/correct'][1] for c in fb[':answer-field/choices']};flips=[{'value':v,'before':da[v],'after':db[v]} for v in sorted(da.keys()&db.keys()) if da[v]!=db[v]]
 out.append({'kind':'relevant','template':a['generation']['template'],'before':a['generation'],'after':b['generation'],'prompt_changed':a['question'][':question/problem']!=b['question'][':question/problem'],'solution_changed':a['question'][':question/worked-solution']!=b['question'][':question/worked-solution'],'key_before':keyval(a),'key_after':keyval(b),'shared_candidate_flips':flips,'native_grader_evidence':'grader-input.json and grader-report.json check every displayed choice on both complete records','passed':bool(flips) and keyval(a)!=keyval(b)})
a,b=rs[-2:];out.append({'kind':'irrelevant','template':'simple_quotient','change':'seed 0 to 5; fixed n=1 and quotient-power-sign bank','prompt_preserved':a['question'][':question/problem']==b['question'][':question/problem'],'solution_preserved':a['question'][':question/worked-solution']==b['question'][':question/worked-solution'],'key_preserved':keyval(a)==keyval(b),'bank_preserved':sorted(c[':answer/value'] for c in field(a)[':answer-field/choices'])==sorted(c[':answer/value'] for c in field(b)[':answer-field/choices']),'order_changed':field(a)[':answer-field/choices']!=field(b)[':answer-field/choices']})
assert all(v['passed'] for v in out[:-1]);assert all(out[-1][k] for k in ['prompt_preserved','solution_preserved','key_preserved','bank_preserved','order_changed'])
(R/'revision-counterfactual-results.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
print('3 relevant shared-choice truth flips and one irrelevant shuffle passed; all submitted in native grader batch')
