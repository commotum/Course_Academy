import hashlib,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[3]/'scripts'))
from migrate_learner_history import dumps,kw
r=json.loads((H/'entity.json').read_text())['rows'][0][0]
before=r[':question/worked-solution']
old=r'|\begin{aligned}1 & 3 \\ 2 & -3\end{aligned}|'
new=r'\begin{vmatrix}1 & 3 \\ 2 & -3\end{vmatrix}'
assert before.count(old)==1 and before.count('det(M) &')==1
after=before.replace(old,new).replace('det(M) &',r'\det(M) &')
f={'entity':r[':db/id'],'attribute':'question/worked-solution','before':before,'after':after,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(after.encode()).hexdigest()}
(H/'fields.json').write_text(json.dumps([f],indent=2)+'\n')
(H/'transaction.edn').write_text(dumps([[kw('db/cas'),f['entity'],kw(f['attribute']),before,after]])+'\n')
print(after)
