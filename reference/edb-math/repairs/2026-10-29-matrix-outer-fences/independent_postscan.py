"""Independent broad fence-context discovery over the fresh full database."""
import collections,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[3];W=R/'.local/edb/outer-fences-2026-10-29';sys.path.insert(0,str(R/'scripts'));from question_capture.math_format import ENV,environment
spacing=r'(?:\s|\\[,;! ]|\\(?:quad|qquad)\b|\\hspace\{[^{}]*\})*'
plain=r'(?:[\[|(|∣‖∥⟨]|\\[|{]|\\(?:lbrack|lbrace|lvert|lVert|Vert|vert|langle)(?![A-Za-z]))'
pattern=re.compile(r'(?P<f>(?:\\(?:left|bigl?|Bigl?|biggl?|Biggl?)\s*)?'+plain+')'+spacing+'$')
names={'array','aligned','alignedat','gathered','matrix','bmatrix','pmatrix','vmatrix','Bmatrix','Vmatrix','cases','split','align','align*','gather','gather*','multline','multline*'};counts=collections.Counter();reviewed=[];unexpected=[]
for line in(W/'after.jsonl').open():
 d=json.loads(line);v=d['v']
 if not isinstance(v,str)or r'\begin'not in v:continue
 for m in ENV.finditer(v):
  if m[1]!='begin'or m[2]not in names:continue
  s=environment(v,m.start());assert s;left=v[max(0,m.start()-180):m.start()];right=v[s[2]:s[2]+180];found=pattern.search(left)
  if not found:counts['unfenced_or_outer_content']+=1;continue
  f=found['f'];kind='scalable'if'\\left'in f else'sized'if re.search(r'\\(?:big|Big)',f)else'plain_or_exotic';counts[kind]+=1
  if kind!='plain_or_exotic':continue
  record={'entity':d['e'],'attribute':d['a'],'left':left,'right':right,'environment':m[2]}
  if f=='['and left.rstrip().endswith(r'\[')and right.lstrip().startswith(r'\]'):record['classification']='Display-math delimiters, not visible brackets'
  elif f in ['|',r'\vert',r'\lvert']and r'\left\{'in left and right.lstrip().startswith(r'\right\}'):record['classification']='Conditional separator inside an already scalable set, not a table fence'
  elif d['e']==17592186360463 and d['a']=='question/problem'and f=='|'and r'F={A\in 'in left and right.startswith('A=A'):record['classification']='Conditional set-builder separator between membership and a matrix relation, not a determinant or enclosing table fence; retained.'
  else:unexpected.append(record);continue
  reviewed.append(record)
result={'passed':not unexpected,'counts':dict(counts),'reviewed_residual_contexts':reviewed,'unexpected_plain_fences':unexpected,'database_writes':0};(H/'independent-final-verification.json').write_text(json.dumps(result,indent=2)+'\n');print('Independentcontextscan:',dict(counts),'benignresiduals',len(reviewed),'unexpected',len(unexpected));print(unexpected[:3]);assert result['passed']
