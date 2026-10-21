"""Batch-render every repaired field using the unchanged learner UI."""
import hashlib,json,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('review_renderer',ROOT/'generate/pipeline/render_preview.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
def run():
    changes=json.loads((HERE/'changes.json').read_text());records=[];groups=[]
    for start in range(0,len(changes),20):
        group=changes[start:start+20];groups.append([{'entity':c['entity'],'attribute':c['attribute']} for c in group])
        prose='\n\n'.join('### Review '+str(start+i)+' — '+str(c['entity'])+' '+c['attribute']+'\n\n'+c['after'] for i,c in enumerate(group))
        records.append({':question/problem':prose,':question/worked-solution':'',':question/answer-fields':[]})
    original=HERE/'render-all';cached={}
    for previous in (original,HERE/'render-recheck',HERE/'render-final'):
        if not (previous/'rendering.json').exists():continue
        old_records=json.loads((previous/'input.json').read_text());old_report=json.loads((previous/'rendering.json').read_text())
        old_hashes=json.loads((previous/'ui-hashes.json').read_text())
        assert all(hashlib.sha256((ROOT/'ui'/n).read_bytes()).hexdigest()==s for n,s in old_hashes.items())
        for old,c in zip(old_records,old_report['cases']):
            if c['passed']:
                for i,record in enumerate(records):
                    if old==record:cached[i]=c
    pending=[i for i in range(len(records)) if i not in cached]
    out=original if not cached else next(HERE/name for name in ('render-recheck','render-final','render-rebased','render-latest') if not (HERE/name).exists());out.mkdir(exist_ok=True);(out/'groups.json').write_text(json.dumps([groups[i] for i in pending],indent=2))
    script=renderer.BROWSER_SCRIPT
    script=script.replace("mathContainers:document.querySelectorAll('mjx-container').length,",r"""mathContainers:document.querySelectorAll('mjx-container').length,
        undefinedCommands:[...document.querySelectorAll('mjx-container [data-mml-node="mtext"]')]
          .filter(node=>/^\\[A-Za-z]+$/.test(node.textContent.trim()))
          .map(node=>({command:node.textContent,math:node.closest('mjx-container')?.getAttribute('data-mathml')})),""")
    script=script.replace("await page.screenshot({path:stem+'.png',fullPage:true,animations:'disabled'});",'')
    script=script.replace("fs.writeFileSync(stem+'.html',await page.content());","if(state.mathErrors.length || state.undefinedCommands.length) fs.writeFileSync(stem+'.html',await page.content());")
    script=script.replace('state.passed=!errors.length','state.passed=!state.undefinedCommands.length && !errors.length')
    script=script.replace('reports.push(state);',"reports.push(state); fs.writeFileSync(config.output+'/progress.json',JSON.stringify(reports,null,2)); console.log('Rendered group '+index+': '+state.mathContainers+' math expressions; passed='+state.passed);")
    renderer.BROWSER_SCRIPT=script
    config=json.loads((ROOT/'reference/mathacademy/repairs/2026-10-18-power-lesson/ui/browser-config.json').read_text())
    renderer.render([records[i] for i in pending],out,['/media/jake/SSD/EDB/math',ROOT,'/'],config['browser'],config['playwright'],config['node'])
    report=json.loads((out/'rendering.json').read_text())
    combined=dict(cached);combined.update(dict(zip(pending,report['cases'])));assert len(combined)==len(records)
    summary={'passed':all(c['passed'] for c in combined.values()),'fields':len(changes),'math_expressions':sum(c['mathContainers'] for c in combined.values()),'unchanged_groups_reused':len(cached),'groups_rechecked':len(pending),'changes_sha256':hashlib.sha256((HERE/'changes.json').read_bytes()).hexdigest(),'ui_sha256':json.loads((out/'ui-hashes.json').read_text()),'checked_undefined_commands':True,'database_writes':0}
    (HERE/'render-verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':run()
