from review import *
rs=json.loads((E/'boundary-records.json').read_text());extra=json.loads((E/'extra-grader-input.json').read_text());cases=json.loads((E/'boundary-grader-input.json').read_text())+extra
dump('second-grader-input.json',cases)
p=run('second-grader-command.json',[R/'generate/runs/current/check-engine',E/'second-grader-input.json',E/'second-grader-report.json']);print('grader',p.returncode,p.stdout[-400:],p.stderr[-800:])
for level in ['moderate','hard']:
 sub=[r for r in rs if r['question'][':question/difficulty'].endswith('/'+level)];dump('boundary-'+level+'.json',sub)
 p=run('delivery-boundary-'+level+'-command.json',[P,R/'generate/pipeline/check_delivery.py','--input',E/('boundary-'+level+'.json'),'--source',J/'source/source.json','--inventory',J/'source/inventory.json','--difficulty',level,'--output',E/('delivery-boundary-'+level),'--asset-root',E/'assets','--asset-root',PK/KP,'--math-root','/media/jake/SSD/EDB/math']);print('boundary delivery',level,p.returncode,p.stderr[-500:])
# UI cases specific to new raster runtime: batch all, scaled empirical banks and nonlinear field.
p=run('render-batch-command.json',[P,R/'generate/pipeline/render_preview.py','--input',E/'delivery-batch/accepted.json','--output',E/'render-batch','--asset-root',E/'delivery-batch/assets','--math-root','/media/jake/SSD/EDB/math']);print('batch render',p.returncode,p.stdout[-300:],p.stderr[-500:])
fresh=json.loads((E/'fresh-records.json').read_text());extra=json.loads((E/'irrelevant-display-records.json').read_text())
dump('render-rest-records.json',[rs[0],rs[2],rs[4],fresh[3],fresh[6],extra[1]])
p=run('render-rest-command.json',[P,R/'generate/pipeline/render_preview.py','--input',E/'render-rest-records.json','--output',E/'render-rest','--asset-root',E/'assets','--asset-root',PK/KP,'--math-root','/media/jake/SSD/EDB/math']);print('rest render',p.returncode,p.stdout[-300:],p.stderr[-500:])
