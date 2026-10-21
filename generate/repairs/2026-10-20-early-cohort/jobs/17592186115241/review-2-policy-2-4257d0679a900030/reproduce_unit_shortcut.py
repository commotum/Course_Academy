"""Strict acceptance regression: printed unit coefficients must not identify the key."""
import sys,pathlib,importlib.util,json,re
sys.dont_write_bytecode=True
E=pathlib.Path(__file__).resolve().parent;P=E.parent/'workspace';sys.path.insert(0,str(P))
s=importlib.util.spec_from_file_location('generator',P/'17592186115241.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
def probe(r):
 cs=r['question'][':question/answer-fields'][0][':answer-field/choices'];key=r['question'][':question/answer-fields'][0][':answer-field/correct'][-1];candidates=[]
 for i,c in enumerate(cs):
  value=c[':answer/value'];value=value.replace('\\\\','\\') if r'\\begin' in value else value
  match=re.search(r'\\begin\{bmatrix\}(.*?)\\end\{bmatrix\}',value,re.S)
  if not match:continue
  rows=[x.strip() for x in match[1].split(r'\\')]
  if len(rows)!=2 or rows[1]!='y':continue
  # Match visible y with no explicit numerical multiplier (ignore the system).
  if re.search(r'(?<![0-9A-Za-z}])y(?![A-Za-z])',rows[0]):candidates.append(i)
 chosen=cs[candidates[0]][':answer/id'] if len(candidates)==1 else None
 return {'strategy':'Among two-coordinate choices, select the only first entry with unmultiplied y or -y. Ignore equations, constants and signs.','candidate_positions':[i+1 for i in candidates],'applicable':len(candidates)==1,'selected_answer_id':chosen,'shortcut_correct':chosen==key,'baseline':0.2}
if __name__=='__main__':
 r=g.generate_easy(seed=71383,profile='q-32244');out={'command':str(sys.executable)+' -B reproduce_unit_shortcut.py','record':r,'probe':probe(r)}
 (E/'minimal-unit-shortcut.json').write_text(json.dumps(out,indent=2)+'\n')
 print(json.dumps(out['probe']))
 assert not out['probe']['shortcut_correct'],'INCIDENTAL SHORTCUT: the sole unmultiplied parameter choice is correct'
