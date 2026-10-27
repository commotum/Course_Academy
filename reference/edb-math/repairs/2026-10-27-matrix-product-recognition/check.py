"""Reconstruct products from displayed matrices, including supplied entries."""
import importlib.util,json,re,sys
from pathlib import Path
H=Path(__file__).resolve().parent;ROOT=H.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(H/'package'))
from generate.matrix_product_prompt_policy import validate_delivery_batch,KP
from scripts.generator_publish import prepare_records,inventory_fingerprints
spec=importlib.util.spec_from_file_location('matrix_verified',H/'package/generator.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
slash=re.escape(chr(92))
def matrices(text):
    return [[[int(v.strip()) for v in row.split('&')] for row in re.split(slash+r'{2,}',body)] for body in re.findall(slash+r'+begin[{]bmatrix[}](.*?)'+slash+r'+end[{]bmatrix[}]',text,re.S)]
def check(r):
    validate_delivery_batch([r],KP);q=r['question'];a,b=matrices(q[':question/problem'])
    c=[[sum(x*y for x,y in zip(row,column)) for column in zip(*b)] for row in a]
    fields={f[':answer-field/key']:f for f in q[':question/answer-fields']};count=0;prefilled=0
    for i,row in enumerate(re.findall(r'<tr>(.*?)</tr>',q[':question/problem'])):
        for j,cell in enumerate(re.findall(r'<td>(.*?)</td>',row)):
            if cell.startswith('{{'):
                f=fields[cell[2:-2]];v=next(a[':answer/value'] for a in f[':answer-field/choices'] if a[':answer/id']==f[':answer-field/correct'][1]);count+=1
            else:v=cell.strip('$');prefilled+=1
            assert int(v)==c[i][j],(i,j,v,c)
    assert count==len(fields) and count+prefilled==9
    assert matrices(q[':question/worked-solution'])[-1]==c
    return {'requested_entries':count,'supplied_entries':prefilled,'product':c}
pool=json.loads((H/'candidate-pool.json').read_text());grading=[];reports=[];fresh=0
for i,r in enumerate(pool):
    reports.append(check(r));checks=[]
    for j,f in enumerate(r['question'][':question/answer-fields']):
        key=f[':answer-field/choices'][0][':answer/value']
        checks += [{'field_index':j,'submitted':v,'expected':outcome} for v,outcome in ((key,'accepted'),(key+'.000','accepted'),(str(int(key)+1),'rejected'))]
    grading.append({'label':str(i),'record':r,'checks':checks})
for level in ('easy','moderate','hard'):
    for seed in (7,37,20261027):
        for r in g.generate(level,20,seed):check(r);fresh+=1
before=json.loads((H/'before.json').read_text());fps=inventory_fingerprints(before[':knowledge-point/questions']+[before[':knowledge-point/canonical-example']])
new,dup=prepare_records(pool,KP,before[':knowledge-point/id'],fps,ROOT,H/'package');assert len(new)==5 and dup==0
for name,value in [('grader-input',grading),('generator-verification',{'passed':True,'candidate_records':5,'fresh_records':fresh,'new_questions':len(new),'duplicates':dup,'delivered':reports})]:
    (H/(name+'.json')).write_text(json.dumps(value,indent=2)+'\n')
print('Printed operands, all supplied/requested entries and worked products verified:',5+fresh,'records')
