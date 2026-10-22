import sys,json,pathlib
sys.dont_write_bytecode=True
job=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(job/'workspace'))
import generator as g
original=json.load(open(job/'source/source.json'))['material']['kp'][':knowledge-point/questions']
byid={q[':question/id']:q for q in original}
def bank(q):return {(f[':answer-field/key'],tuple(a[':answer/value'] for a in f[':answer-field/choices'])) for f in q[':question/answer-fields']}
for i in range(10):
 r=g.replay_source(i);sid=r['generation']['source_id']
 assert bank(r['question'])==bank(byid[sid]),f'Source {sid} full answer bank differs at replay index {i}'
assert len(original)==10,'Supplied source has an additional unreplayed question'
