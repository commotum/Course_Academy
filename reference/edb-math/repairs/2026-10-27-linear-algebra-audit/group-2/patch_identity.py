"""Hash normalized served solutions as well as prompts/parameters before UUIDs."""
from pathlib import Path

def patch(kp,p):
 s=p.read_text()
 if kp==17592186119856:
  old='signature=json.dumps([level,rows,rhs,sorted(tex(b) for b in bank)],sort_keys=True)';new='signature=json.dumps([level,problem,solution,rows,rhs,sorted(tex(b) for b in bank)],sort_keys=True)';assert old in s;s=s.replace(old,new).replace("'generation':{'version':1,","'generation':{'version':'1.0.1-content-identity',")
 elif kp==17592186124629:
  old="content = [q[':question/problem'], [(key, kind, sorted(values), correct) for key, kind, values, correct in specs]]";new="content = [q[':question/problem'], q[':question/worked-solution'], [(key, kind, sorted(values), correct) for key, kind, values, correct in specs]]";assert old in s;s=s.replace(old,new).replace("VERSION = '2.0.1'","VERSION = '2.0.2-content-identity'")
 elif kp==17592186124630:
  old='identity = digest([problem, sorted(values)])';new='identity = digest([problem, solution, sorted(values)])';assert old in s;s=s.replace(old,new).replace("VERSION = '2.0.0'","VERSION = '2.0.1-content-identity'")
  s=s.replace("fid = uid('field:' + source_id)","served = digest([q[':question/problem'], q[':question/worked-solution'], q[':question/answer-fields']])\n    fid = uid('field:' + source_id + ':' + served)")
  s=s.replace("uid('question:' + source_id)","uid('question:' + source_id + ':' + served)")
 elif kp==17592186115227:
  old="qid=uid(KP['id'],digest({'prompt':prompt,'bank':bank}))";new="qid=uid(KP['id'],digest({'prompt':prompt,'solution':solution,'bank':bank}))";assert old in s;s=s.replace(old,new).replace("'associative-matrices-2.0.0'","'associative-matrices-2.0.1-content-identity'")
 else:return
 p.write_text(s)
