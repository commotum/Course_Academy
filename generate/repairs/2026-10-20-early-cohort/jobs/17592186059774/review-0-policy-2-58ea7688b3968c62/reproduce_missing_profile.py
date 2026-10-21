"""Acceptance regression: every complete captured source bank must replay.
Run with the job Python from evidence_root. Current generator exits nonzero.
"""
import sys,json
from pathlib import Path
sys.dont_write_bytecode=True
job=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(job/'workspace'))
import generator
source=json.load(open(job/'source/source.json'))
q=next(q for q in source['material']['kp'][':knowledge-point/questions'] if q[':question/id']=='372c1499-bf5a-558e-ad8a-af28e6ae7898')
assert q[':question/worked-solution'] and q[':question/answer-fields'][0][':answer-field/correct']
record=generator.replay('q-72858')  # must support this complete bank; currently ValueError
assert len(record['question'][':question/answer-fields'][0][':answer-field/choices'])==5
