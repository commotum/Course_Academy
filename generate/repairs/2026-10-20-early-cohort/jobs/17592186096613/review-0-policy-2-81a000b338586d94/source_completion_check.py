import pathlib,json,importlib.util,sys,re
sys.dont_write_bytecode=True
P=pathlib.Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('candidate',P.parent/'workspace/17592186096613.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
s=json.loads((P.parent/'source/source.json').read_text());q=next(q for q in s['material']['kp'][':knowledge-point/questions'] if q[':question/math-academy-id']=='q-70889')
r=g.generate_easy(seed=917,profile='euler',parameters=dict(n=6,d=1,k=1))
def norm(t):return re.sub(r'\s+','',t.replace('\\operatorname{ln}','\\ln').replace('\u2061','').replace('ln','\\ln').replace('\\\\ln','\\ln'))
bank=lambda q:sorted(a[':answer/value'] for a in q[':question/answer-fields'][0][':answer-field/choices'])
assert norm(q[':question/problem'])==norm(r['question'][':question/problem'])
assert bank(q)==bank(r['question'])
expected='\\frac{6e}{x}';f=r['question'][':question/answer-fields'][0]
assert next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1])==expected
(P/'source-euler-replay.json').write_text(json.dumps({'source_id':q[':question/id'],'raw_profile_absent':True,'normal_profile_replays_math_and_complete_bank':True,'prompt_equal_after_ln_normalization':True,'solution':'Same derivative identity and constant multiple stages; explicit dot versus implicit multiplication in source is immaterial.','record':r},indent=2))
print('q-70889 normal Euler replay passed; raw-name omission is not a separate finding.')
