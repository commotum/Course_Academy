import json,pathlib,re
E=pathlib.Path(__file__).resolve().parent;J=pathlib.Path('/home/jake/Developer/Course_Academy/generate/repairs/2026-10-20-early-cohort/jobs/17592186229182')
source={q[':question/math-academy-id']:q for q in json.load(open(J/'source/source.json'))['material']['kp'][':knowledge-point/questions']}
replay={r['generation']['template']:r['question'] for r in json.load(open(E/'source-replays.json'))}
checks=json.load(open(E/'source-replay-results.json'))
def normal(x):return re.sub(r'\s+','',x.replace('\\left','').replace('\\right',''))
for item in checks:
 ma=item['template']
 if ma not in replay:continue
 q=source[ma];r=replay[ma];f=q[':question/answer-fields'][0];rf=r[':question/answer-fields'][0]
 item['numeric_bank_match']=sorted(re.match(r'[\d.]+',a[':answer/value'])[0] for a in f[':answer-field/choices'])==sorted(re.match(r'[\d.]+',a[':answer/value'])[0] for a in rf[':answer-field/choices'])
 item['solution_math_presentation_match']=normal(q.get(':question/worked-solution',''))==normal(r.get(':question/worked-solution',''))
 item['normalization_note']='Delimiter sizing ignored; bank numeric values compared separately from unit escaping. Missing attributes are substantive failures.'
(E/'source-replay-results.json').write_text(json.dumps(checks,indent=2))
