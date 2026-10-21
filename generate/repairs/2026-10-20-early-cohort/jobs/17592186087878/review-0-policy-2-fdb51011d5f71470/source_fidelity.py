from audit import *
qs=json.load(open('source-extract.json'))['questions'];rs=json.load(open('source-replays.json'));out=[]
def prose(t):return re.sub(r'\s+',' ',re.sub(r'\$\$.*?\$\$|\$[^$]*\$','<MATH>',t,flags=re.S)).strip()
for q,r in zip(qs,rs):
 P,Q=equation(q);rp,rq=equation(r['question'])
 out.append({'source_id':q[':question/id'],'same_ODE':s.simplify(P-rp)==0 and s.simplify(Q-rq)==0,'prompt_prose_preserved':prose(q[':question/problem'])==prose(r['question'][':question/problem']),'solution_prose_preserved':prose(q[':question/worked-solution'])==prose(r['question'][':question/worked-solution']) if ':question/worked-solution' in q else 'source missing: authored explanation allowed'})
canon=json.load(open('boundary-records.json'))[0];P,Q=equation(canon['question'])
out.append({'source_id':'89446fd7-75c2-5da5-bd97-469100f3ca7b','canonical_equation_matches':s.simplify(P-3/x)==0 and s.simplify(Q-s.cos(x)/x**2)==0,'canonical_solution_matches':s.simplify((x*s.sin(x)+s.cos(x)+C)/x**3-parse(next(c[':answer/value'] for f in canon['question'][':question/answer-fields'] if f[':answer-field/key']=='field-2' for c in f[':answer-field/choices'] if c[':answer/id']==f[':answer-field/correct'][1])))==0,'response_note':'Canonical example is worked prose, not an authored answer-field contract; generated two-select practice preserves bank task contract.'})
save('source-fidelity.json',out);print(json.dumps(out))
