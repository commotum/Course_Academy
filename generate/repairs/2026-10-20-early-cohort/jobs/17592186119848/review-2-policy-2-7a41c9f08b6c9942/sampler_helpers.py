"""Targeted independent sampler regression. Run with repo .venv/bin/python -B."""
import sys,json,importlib.util,hashlib,subprocess,random,collections
from pathlib import Path
from unittest.mock import patch
sys.dont_write_bytecode=True
E=Path(__file__).resolve().parent;J=E.parent;W=J/'workspace';R=Path('/home/jake/Developer/Course_Academy')
sys.path.insert(0,str(W));s=importlib.util.spec_from_file_location('g',W/'17592186119848.py');g=importlib.util.module_from_spec(s);s.loader.exec_module(g)
from audit_delivery import info,matrices,rank
load=lambda p:json.loads(Path(p).read_text())
def save(n,x):(E/n).write_text(json.dumps(x,indent=2)+'\n')
def group(r):
 x=info(r)
 return (x['profile'],x['target'],tuple(sorted(tuple(v) for v in x['shapes'].values())),tuple(x['excluded']),len(r['question'][':question/answer-fields']),r['generation']['choice_profile'])
def audit(rs):
 groups=collections.defaultdict(list)
 for r in rs:groups[group(r)].append(info(r))
 results=[]
 for k,rows in groups.items():
  forced=[lab for lab in rows[0]['eligible'] if len({lab in row['matches'] for row in rows})==1]
  results.append({'group':str(k),'count':len(rows),'truths':[x['matches'] for x in rows],'forced_labels':forced,'singleton':len(rows)==1,'failed':len(rows)>1 and bool(forced)})
 return {'groups':results,'failures':[r for r in results if r['failed']]}
