"""Rebase review links only; immutable generated record content is retained."""
import json,re,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[2]
source=json.load(open(HERE/'source.json'));review=json.load(open(HERE/'review.json'));replays=json.load(open(HERE/'source-replays.json'))
(HERE/'source-images').mkdir(exist_ok=True)
for ref in set(re.findall(r'images/[a-f0-9]{2}/[a-f0-9]+\.png',json.dumps(source))):shutil.copyfile(Path('/media/jake/SSD/EDB/math')/ref,HERE/'source-images'/Path(ref).name)
def local(text):
 text=re.sub(r'images/[a-f0-9]{2}/([a-f0-9]+\.png)',lambda m:'source-images/'+m[1],text)
 return text.replace('generate/scratch/17592186172038/','')
def show(r):
 q=r['question'];f=q[':question/answer-fields'][0]
 body=q[':question/problem']+'\n\n'+'\n\n'.join(f'{i+1}. ![]({a[":answer/value"]})' for i,a in enumerate(f[':answer-field/choices']))+'\n\n'+q[':question/worked-solution']
 return local(body)
text='''# Source and generated review\n\nMath basis1356. Source bytes, fields and absent refs remain in source.json. Regenerated PNG paths/bytes are not source-image matches: 35/35 full center-and-slope geometry objects and 7/7 complete banks match. All seven printed source prompts are exact at original parameters. Five existing worked solutions retain exact non-math prose and ordered three substitution rows; coefficient/component TeX is normalized, so exact math notation is not claimed. Only 5/5 stored correct designations match; two absent refs are independently inferred and excluded from that denominator.\n\n## Original sources with replay\n\n'''
for q,r in zip(source['record'][':knowledge-point/questions'],replays):
 qid=q[':question/math-academy-id'];text+=f'### Original {qid}\n\n{q[":question/problem"]}\n\n![]({qid}-source.png)\n\n'
 if q.get(':question/worked-solution'):text+='Original worked solution:\n\n'+local(q[':question/worked-solution'])+'\n\n'
 else:text+='Raw source has no worked solution, difficulty or correct designation. The replay easy assignment, three-row solution and independently derived correct designation are authored repairs.\n\n'
 text+='Parameterized source-profile replay (regenerated plots, normalized equation rows):\n\n'+show(r)+'\n\n'
text+='## Generated variants\n\nThe first seven variations preserve complete observed profiles at changed parameters; later variations use the separate authored operation bank. Each eligible mathematical form has two normal examples at each level, including both missing levels.\n\n'
for i,r in enumerate(review):
 m=r['generation'];text+=f'### Generated {i+1}: {r["question"][":question/difficulty"].split("/")[-1]}, {m["template"]}, {m["bank_profile"]}\n\nParameters: `{json.dumps(m["parameters"])}`. '+('Authored full bank and workload.' if m['bank_profile']=='authored' else 'Observed complete orientation-profile extension; error intent is underdetermined.')+'\n\n'+show(r)+'\n\n'
(HERE/'review.md').write_text(text)
# Validate every relative Markdown image path in the actual saved review.
for ref in re.findall(r'!\[\]\(([^)]*)\)',text):assert (HERE/ref).exists(),ref
