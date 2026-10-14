#!/usr/bin/env python3
"""Current-version readback and immutable-original/refreshed-inventory comparison.

Writes only beside this file. Original MA fidelity remains based on basis1356.
"""
import copy, hashlib, importlib.util, json, re, subprocess, sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
v=load(HERE/'validate.py','current_validator');g=v.g
def save(name,data):(HERE/name).write_text(json.dumps(data,indent=2)+'\n')
def normalized_field(f):
 typ=f[':answer-field/type'];typ=typ[':db/ident'] if isinstance(typ,dict) else typ
 out={'key':f[':answer-field/key'],'type':typ,'values':sorted(a[':answer/value'] for a in f[':answer-field/choices']),'correct_present':':answer-field/correct' in f}
 if out['correct_present']:
  ref=f[':answer-field/correct'];out['correct']=ref[':answer/value'] if isinstance(ref,dict) else next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==ref[1])
 return out

def main():
 prior=json.loads((ROOT/'generate/runs/current/qa/17592186100990-sampled.json').read_text())
 impact={'prior_approved_sha256':'bd044f64ebe2528a90b796f3eb9b5c36092d3ceeb6dd563dc8e44f4924729b37','current_sha256':hashlib.sha256(HERE.with_suffix('.py').read_bytes()).hexdigest(),'approved_samples_replayed':0,'exact_after_documented_notation_repair':0,'all_content_ids_changed':True}
 for r in prior:
  q=r['question'];m=r['generation'];n=v.check(g.generate(q[':question/difficulty'].split('/')[-1],m['seed'],m['template'],parameters=m['parameters'],profile=m['profile']))['question']
  for key in (':question/problem',':question/worked-solution'):
   assert n[key]==q[key].replace(r'[\begin{aligned}',r'\begin{bmatrix}').replace(r'\end{aligned}]',r'\end{bmatrix}')
  assert [normalized_field(f) for f in n[':question/answer-fields']]==[normalized_field(f) for f in q[':question/answer-fields']]
  assert n[':question/id']!=q[':question/id']
  impact['approved_samples_replayed']+=1;impact['exact_after_documented_notation_repair']+=1
 # Same matrix/letter/profile with different queried cells: entry lookup cannot
 # establish this task. Every number is zero, so only actual box position works.
 changed_targets=[]
 for level,(m,n),pair in [('easy',(3,3),((1,1),(3,3))),('moderate',(5,6),((4,2),(2,5))),('hard',(6,7),((5,2),(2,6)))]:
  records=[]
  for i,j in pair:
   p={'matrix':[[0]*n for _ in range(m)],'i':i,'j':j,'letter':'Q'}
   records.append(v.check(g.generate(level,template='display_radio',parameters=p,profile='q-13489')))
  assert records[0]['generation']['mathematical_fingerprint']!=records[1]['generation']['mathematical_fingerprint']
  changed_targets.append({'level':level,'records':records})
 save('changed-targets.json',changed_targets)
 # Deterministic external CLI, including omission-safe raw Markdown.
 cmd=[sys.executable,str(HERE.with_suffix('.py')),'--difficulty','all','--seed','12','--count','2','--format','json']
 first=subprocess.check_output(cmd);assert first==subprocess.check_output(cmd)
 cli=json.loads(first);assert len(cli)==6
 for r in cli:v.check(r)
 save('previews.json',cli)
 rawcmd=[sys.executable,str(HERE.with_suffix('.py')),'--difficulty','easy','--profile','raw:q-13503','--format','markdown']
 raw=subprocess.check_output(rawcmd,text=True);assert 'Unrated original evidence' in raw and 'Worked solution:' not in raw and 'Correct:' not in raw
 (HERE/'raw-cli-preview.md').write_text(raw)
 fresh=json.loads((ROOT/'generate/runs/current/refresh-2026-10-14/sources/17592186100990.json').read_text());save('refreshed-source.json',fresh)
 old={q[':question/math-academy-id']:q for q in g.CAPTURE['record'][':knowledge-point/questions']}
 ma={q[':question/math-academy-id']:q for q in fresh['record'][':knowledge-point/questions'] if ':question/math-academy-id' in q}
 authored=[q for q in fresh['record'][':knowledge-point/questions'] if ':question/math-academy-id' not in q]
 assert set(ma)==set(old) and len(authored)==1
 refreshed=[]
 for sid,oq in old.items():
  fq=ma[sid];completed=g.generate('easy',profile='completed:'+sid)['question']
  matrix,letter,box=v.read_display(fq[':question/problem']);cm,cl,cb=v.read_display(completed[':question/problem'])
  assert (matrix,letter,box)==(cm,cl,cb)
  for key in (':question/difficulty',':question/worked-solution'):
   assert (key in oq)==(key in fq)
   if key in oq:assert oq[key]==fq[key]
  assert [normalized_field(f) for f in oq[':question/answer-fields']]==[normalized_field(f) for f in fq[':question/answer-fields']]
  assert ':question/math-academy-id' in fq
  refreshed.append({'source_id':sid,'matrix_and_highlight_match_completed':True,'field_bank_and_correct_presence_unchanged':True,'solution_and_difficulty_presence_unchanged':True,'raw_prompt_changed':oq[':question/problem']!=fq[':question/problem'],'compact_placeholder_layout':sid=='q-139426'})
 a=authored[0];text=a[':question/problem']
 assert text.count('\n')>0 and text.count(r'\n')==0 and '\\'*2+'begin' not in text
 assert [normalized_field(f)['correct'] for f in a[':question/answer-fields']]==['1','1']
 # Read its bbox marker directly; it is authored context, never a ninth MA template.
 am,al,ab=v.read_display(text.replace(r'\bbox[lightgray, 2pt]',r'\boxed'))
 assert (am,al,ab)==([[0,-2,2],[2,0,-2],[-2,2,0]],'P',[(1,1)])
 assert re.search(r'intersection of the \$1\$st row and \$1\$st column',a[':question/worked-solution'])
 authored_replica=v.check(g.generate('easy',template='two_indices',parameters={'matrix':[[0,-2,2],[2,0,-2],[-2,2,0]],'i':1,'j':1,'letter':'P'}))
 save('authored-context-preview.json',authored_replica)
 schema=(ROOT/'schema/content/4-question.edn').read_text();assert 'Omit for independently created content.' in schema
 subprocess.run([sys.executable,str(HERE/'independent-readback.py')],check=True)
 report={'status':'passed','script_sha256':impact['current_sha256'],'current_changes_impact':impact,'changed_target_constant_matrix_checks':6,'deterministic_cli_records':6,'source_wrapper_exact_basis1356':True,'refresh_provenance':{k:fresh[k] for k in ('database','basis','lineage')},'refreshed_inventory_counts':{'original_ma_questions':8,'independently_authored_context_questions':1,'total':9},'refreshed_ma_comparison':refreshed,'independently_authored_context':{'db_id':a[':db/id'],'ma_id_absent':True,'schema_basis':'schema/content/4-question.edn: optional MA identifier omitted for independently created content','intended_indices':[1,1],'real_newlines':text.count('\n'),'literal_backslash_n':text.count(r'\n'),'doubled_tex_command_slashes':False,'scope':'same two-index family; context only, excluded from original source-fidelity counts','displayed_matrix_highlight_and_solution_match':[1,1]},'independent_readback':json.loads((HERE/'independent-readback.json').read_text()),'unresolved_findings':['Symbolic-index blank native parser limitation retained in ineligible evidence/drafts.']}
 save('current-version-revalidation.json',report)
 print(json.dumps({'status':report['status'],'script_sha256':report['script_sha256'],'refreshed_inventory_counts':report['refreshed_inventory_counts']}))
if __name__=='__main__':main()
