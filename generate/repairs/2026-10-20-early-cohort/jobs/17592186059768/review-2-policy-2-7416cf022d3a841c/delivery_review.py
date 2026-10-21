import sys
sys.dont_write_bytecode=True
import review as a
E=a.E
base=[a.PY,'-B',a.REPO/'generate/pipeline/check_delivery.py','--source',a.JOB/'source/source.json','--inventory',a.JOB/'source/inventory.json','--math-root','/media/jake/SSD/EDB/math']
results=[]
for label,level,input in [('batch','easy','runner-batch.json'),('easy','easy','independent-easy.json'),('moderate','moderate','independent-moderate.json'),('unit-easy','easy','unit-easy.json'),('unit-moderate','moderate','unit-moderate.json')]:
 p=a.run(base+['--input',E/input,'--difficulty',level,'--output',E/('delivery-'+label)],'delivery-'+label+'-command.json');assert p.returncode==0,p.stderr
 report=a.read(E/('delivery-'+label)/'delivery.json');results.append({'label':label,'report':report})
a.save('delivery-stage-results.json',results)
# Duplicate against captured inventory, duplicate within batch, and wrong-difficulty.
a.save('duplicate-input.json',[a.read(E/'runner-batch.json')[0]]*2+[a.read(E/'generated-records.json')[0]])
p=a.run(base+['--input',E/'duplicate-input.json','--difficulty','easy','--output',E/'delivery-duplicate'],'delivery-duplicate-command.json');assert p.returncode==0,p.stderr
p=a.run(base+['--input',E/'independent-moderate.json','--difficulty','easy','--output',E/'delivery-wrong-difficulty'],'delivery-wrong-difficulty-command.json');assert p.returncode!=0
# Unchanged batch question objects; record generation version may be updated.
old=a.read(a.JOB/'review-1-policy-2-a0f21dc2de58c6f5/runner-batch.json');new=a.read(E/'runner-batch.json')
a.save('batch-comparison.json',{'same_exact_question_objects':[r['question'] for r in new]==[r['question'] for r in old],'records':len(new),'all_survive':len(a.read(E/'delivery-batch/accepted.json'))==len(new),'limit':'Five-record pool evaluated separately from larger current sample.'})
for row in results:
 print(row['label'],row['report'].get('counts',row['report'].get('stage_counts')))
