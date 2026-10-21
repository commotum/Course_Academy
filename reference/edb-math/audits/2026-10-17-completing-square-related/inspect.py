"""Read-only source inventory for the ten related completing-the-square lessons."""
from pathlib import Path
import collections,json,re,sys
sys.dont_write_bytecode=True
ROOT=next(p for p in Path(__file__).resolve().parents if (p/'Cargo.toml').exists());sys.path.insert(0,str(ROOT))
from capture.scripts.database.edn import loads
HERE=Path(__file__).resolve().parent
MATH=re.compile(r'\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$')
TEXT_ATTRS={':question/problem',':question/worked-solution',':tutorial/content',':multistep/context',':answer/value',':answer/feedback'}

def flatten(v):
 out={}
 def visit(v):
  if isinstance(v,dict):
   if ':db/id' in v:out.setdefault(v[':db/id'],{}).update(v)
   for x in v.values():visit(x)
  elif isinstance(v,list):
   for x in v:visit(x)
 visit(v);return out

def main():
 rows=loads((HERE/'lessons.edn').read_text());assert len(rows)==10
 entities=flatten(rows);examples={v[':knowledge-point/canonical-example'][':db/id'] for v in entities.values() if ':knowledge-point/canonical-example' in v}
 summaries=[];membership=collections.defaultdict(list);routes=[]
 for topic,activity in rows:
  local=flatten([topic,activity]);qid={e for e,v in local.items() if ':question/id'in v};ex=qid&examples
  summary={'topic':topic[':db/id'],'activity':activity[':db/id'],'title':topic[':topic/title'],'entities':sorted(local),'tutorials':sum(':tutorial/id'in v for v in local.values()),'examples':len(ex),'practice':len(qid-ex),'steps':sum(':step/id'in v for v in local.values()),'knowledge_points':sum(':knowledge-point/id'in v for v in local.values())}
  summaries.append(summary)
  for e in local:membership[e].append(topic[':db/id'])
  for owner in local.values():
   for ns in ['activity','multistep']:
    if ':'+ns+'/steps' not in owner:continue
    steps=owner[':'+ns+'/steps'];expected={s[':db/id'] for s in steps};chain=[];cur=owner.get(':'+ns+'/first-step',{}).get(':db/id');error=None
    while cur:
     if cur not in expected or cur in chain:error='Step chain leaves owner or cycles';break
     chain.append(cur);st=local[cur]
     if not isinstance(st.get(':step/content'),dict) or len(st[':step/content'])<2:error='Content projection incomplete';break
     cur=st.get(':step/next',{}).get(':db/id')
    if not error and set(chain)!=expected:error='Step chain does not cover every member'
    routes.append({'topic':topic[':db/id'],'owner':owner[':db/id'],'chain':chain,'error':error})
 findings=[]
 def add(code,e,a,s,detail=None):findings.append({'code':code,'entity':e,'attribute':a,'lessons':membership[e],'detail':detail,'excerpt':s[:600]})
 for e,v in entities.items():
  for a,s in v.items():
   if a not in TEXT_ATTRS or not isinstance(s,str):continue
   if '⏟' in s or '⏞' in s:add('literal_brace',e,a,s)
   if re.search(r'\\begin\{aligned\}.*?&\s*=\s*\\\\',s,re.S):add('trailing_equals',e,a,s)
   if re.search(r'\\(?:eqalign|matrix|pmatrix|cases)\s*\{',s):add('legacy_command',e,a,s)
   if a==':question/problem' and any(re.search(r'[A-Za-z]\.$|\$\.$',s[:m.start()]) for m in MATH.finditer(s)):add('missing_separation',e,a,s)
   if a==':question/problem' and re.search(r'\?\$',s):add('inline_question_mark',e,a,s)
   if '{)}'in s:add('parenthesis_group',e,a,s)
   if re.search(r'(?m)^\s*\|(?:\s*:?-{3,}:?\s*\|)+',s):add('markdown_table_review',e,a,s)
   if a==':answer/value' and v.get(':answer/type',{}).get(':db/ident')==':answer.type/math':expressions=[s]
   else:
    remainder=MATH.sub('',s)
    if re.search(r'(?<!\\)\$|\\[\[\]()]',remainder):add('unmatched_delimiter',e,a,s,remainder[:600])
    expressions=[m[0] for m in MATH.finditer(s)]
   for expr in expressions:
    depth=0
    for c in re.sub(r'\\[{}]','',expr):
     depth+=(c=='{')-(c=='}')
     if depth<0:break
    if depth:add('unbalanced_brace',e,a,s,expr)
    envs=[];env_error=False
    for direction,name in re.findall(r'\\(begin|end)\{([^{}]+)\}',expr):
     if direction=='begin':envs.append(name)
     elif not envs or envs.pop()!=name:env_error=True
    if envs or env_error:add('unbalanced_environment',e,a,s,expr)
  if ':question/id'in v:
   if not v.get(':question/worked-solution','').strip():add('missing_solution',e,':question/worked-solution','')
   fs=v.get(':question/answer-fields',[]);keys=[f.get(':answer-field/key') for f in fs]
   for marker in re.findall(r'\{\{(?:answer-field:)?([^}]+)\}\}',v.get(':question/problem','')):
    if marker not in keys:add('orphan_placeholder',e,':question/problem',v[':question/problem'],marker)
   missing=[f[':db/id'] for f in fs if ':answer-field/correct'not in f]
   if missing:add('missing_key',e,':question/answer-fields','',missing)
  if ':tutorial/id'in v and not v.get(':tutorial/content','').strip():add('empty_tutorial',e,':tutorial/content','')
 totals={kind:sum(':'+kind+'/id'in v for v in entities.values()) for kind in ['activity','step','knowledge-point','question','tutorial','multistep','answer-field','answer']}
 totals.update({'examples':len(examples),'practice':totals['question']-len(examples),'worked_solutions':sum(':question/worked-solution'in v for v in entities.values()),'answer_feedback':sum(':answer/feedback'in v for v in entities.values())})
 for name,data in [('entities.json',entities),('lessons.json',rows),('inventory.json',{'totals':totals,'lessons':summaries,'routes':routes}),('source-findings.json',findings)]:
  (HERE/name).write_text(json.dumps(data,indent=2,ensure_ascii=False,default=str)+'\n')
 text=[]
 for topic,activity in rows:
  local=flatten([topic,activity]);text += ['\nLESSON '+topic[':topic/title']+'\n']
  for e,v in local.items():
   if ':tutorial/id'in v:text += [f'\nTUTORIAL {e} {v.get(":tutorial/title")}\n{v.get(":tutorial/content", "")}\n']
   if e in examples:text += [f'\nEXAMPLE {e}\n{v.get(":question/problem", "")}\n\n{v.get(":question/worked-solution", "")}\n']
  for e,v in local.items():
   if ':question/id'in v and e not in examples:text += [f'\nQUESTION {e}\n{v.get(":question/problem", "")}\n\n{v.get(":question/worked-solution", "")}\n']
 (HERE/'source-review.txt').write_text('\n'.join(text))
 print(json.dumps({'totals':totals,'lessons':[{k:v for k,v in s.items() if k!='entities'}for s in summaries],'flags':dict(collections.Counter(f['code']for f in findings)),'route_errors':[r for r in routes if r['error']]},indent=2))
if __name__=='__main__':main()
