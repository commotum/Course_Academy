from audit import *
import copy
base=json.loads(Path('selection-input.json').read_text());d=copy.deepcopy(base);mapping=json.loads(Path('selection-map.json').read_text());records=json.loads(Path('delivery-shortcut/accepted.json').read_text());n=990000000
for j,r in enumerate(records):
 qid=980000000+j;f=field(r);fid=970000000+j;ids=[];uuidmap={}
 for a in f[':answer-field/choices']:
  n+=1;ids.append(n);uuidmap[a[':answer/id']]=n;d['entities'][str(n)]={'answer/type':'answer.type/math','answer/value':a[':answer/value']}
 d['entities'][str(fid)]={'answer-field/type':'answer-field.type/radio','answer-field/key':'selection','answer-field/choices':ids,'answer-field/correct':uuidmap[f[':answer-field/correct'][1]]}
 d['entities'][str(qid)]={'question/id':r['question'][':question/id'],'question/problem':r['question'][':question/problem'],'question/answer-fields':[fid],'question/difficulty':'question.difficulty/easy'};d['question_ids'].append(qid);mapping[str(qid)]={'kind':'shortcut_easy','uuid':r['question'][':question/id'],'template':'slope_sum_radio','a':r['generation']['parameters']['a']}
save('selection-shortcut-input.json',d);save('selection-shortcut-map.json',mapping)
source=Path('selection.rs').read_text().replace('selection-input.json','selection-shortcut-input.json').replace('selection-results.json','selection-shortcut-results.json');Path('selection-shortcut.rs').write_text(source)
cmd=json.loads(Path('selection-command.json').read_text());cmd[cmd.index('selection.rs')]='selection-shortcut.rs';cmd[cmd.index('selection')]='selection-shortcut';p=subprocess.run(cmd,capture_output=True,text=True);Path('selection-shortcut-compile.log').write_text(p.stdout+p.stderr);save('selection-shortcut-command.json',cmd)
if p.returncode:raise RuntimeError(p.stderr)
p=subprocess.run(['./selection-shortcut'],capture_output=True,text=True);Path('selection-shortcut.stderr').write_text(p.stderr);assert p.returncode==0
rs=json.loads(Path('selection-shortcut-results.json').read_text());draw=next(x for x in rs['draws'] if x['scenario']=='configured all bands, fresh');hits={qid:ct for qid,ct in draw['selection_counts'].items() if qid in mapping and mapping[qid]['kind']=='shortcut_easy'}
save('sum-shortcut-delivered-selection.json',{'scenario':'configured all bands, fresh','weights':[1,1,1],'unique_shortcut_cases_selected':len(hits),'shortcut_selection_count':sum(hits.values()),'selected_counts':hits,'eligible_shortcut_cases':len(records),'limits':'Supported easy band separate from requested moderate batch. With moderate-only weights this easy family is excluded. IDs for unpublished questions synthetic; equal-band configured policy scenario, actual weights absent.'})
print('selected shortcut cases',len(hits),'draws',sum(hits.values()))
