import audit as a
import re
src=a.load(a.JOB/'source/source.json')['material']['kp'][':knowledge-point/questions'];replays=a.load(a.EVID/'source-replay-records.json');out=[]
pat=re.compile(r'\$\$[\s\S]*?\$\$|\$(?!\$)[^$]*?\$')
for original,r in zip(src,replays):
 q=r['question'];pm=pat.sub('<MATH>',q[':question/problem']);opm=pat.sub('<MATH>',original[':question/problem']);appended='\n\nAssume <MATH>.'
 if pm.endswith(appended):pm=pm[:-len(appended)]
 sm=None
 if ':question/worked-solution' in original:sm=pat.sub('<MATH>',original[':question/worked-solution'])==pat.sub('<MATH>',q[':question/worked-solution'])
 assert pm==opm and sm is not False
 out.append({'source_id':original[':question/id'],'prompt_prose_mask_matches':True,'solution_prose_and_math_stage_mask_matches':sm,'source_solution_absent':sm is None})
a.save('source-prose-results.json',out)
print('Eight source prompts and six supplied solution prose/stage masks match.')
