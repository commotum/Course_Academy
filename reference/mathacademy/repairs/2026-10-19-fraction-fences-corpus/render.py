"""Compare every changed formula using the learner UI's exact MathJax setup."""
import hashlib,importlib.util,json,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent;ROOT=HERE.parents[3]
spec=importlib.util.spec_from_file_location('fence_ui_renderer',ROOT/'generate/pipeline/render_preview.py');renderer=importlib.util.module_from_spec(spec);spec.loader.exec_module(renderer)
SCRIPT=r'''
const fs=require('fs');const config=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const cases=JSON.parse(fs.readFileSync(config.output+'/math-cases.json','utf8'));
const {chromium}=require(config.playwright);
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:config.browser,args:['--disable-dev-shm-usage']});
 const results=new Array(cases.length);let completed=0;const exceptions=[];
 async function worker(workerIndex){
  const context=await browser.newContext({viewport:{width:1280,height:1000}});const page=await context.newPage();
  await page.route('**/*',r=>new URL(r.request().url()).origin===config.origin?r.continue():r.abort());
  await page.goto(config.origin+'/learn?activityId=0',{waitUntil:'networkidle'});
  await page.locator('.lesson-content').waitFor();await page.locator('mjx-container').first().waitFor();await page.evaluate(async()=>{await MathJax.startup.promise;await document.fonts.ready;if(typeof MathJax.typesetPromise!=='function')throw Error('MathJax runtime did not load');});
  for(let start=workerIndex*50;start<cases.length;start+=150){
   const batch=cases.slice(start,start+50);
   const report=await page.evaluate(async batch=>{
    const out=[];const root=document.createElement('div');document.querySelector('.lesson-content').append(root);const pairs=[];
    function state(node){return {errors:[...node.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),undefined:[...node.querySelectorAll('[data-mml-node="mtext"]')].map(n=>n.textContent.trim()).filter(s=>/^\\[A-Za-z]+$/.test(s)),hasSVG:!!node.querySelector('svg')};}
    for(const c of batch){
     const hosts=[];for(const text of [c.before,c.after]){const host=document.createElement('div');const delimiter=c.display?'$$':'$';host.textContent=delimiter+text+delimiter;root.append(host);hosts.push(host);}pairs.push(hosts);
    }
    await MathJax.typesetPromise([root]);
    for(let i=0;i<batch.length;i++){
     const c=batch[i];const before=state(pairs[i][0]),after=state(pairs[i][1]);
     const newErrors=after.errors.filter(e=>!before.errors.includes(e));const newUndefined=after.undefined.filter(e=>!before.undefined.includes(e));
     out.push({index:c.index,before,after,newErrors,newUndefined,passed:!newErrors.length&&!newUndefined.length&&(after.hasSVG||!before.hasSVG)});
    }
    MathJax.typesetClear([root]);root.remove();return out;
   },batch);
   for(const item of report){results[item.index]=item;if(item.before.errors.length||item.before.undefined.length||!item.passed)exceptions.push(item);}
   completed+=report.length;fs.writeFileSync(config.output+'/progress.json',JSON.stringify({completed,total:cases.length,exceptions},null,2));
   if(completed%500<50)console.log('Checked '+completed+' / '+cases.length+' formula pairs');
  }
  await context.close();
 }
 try{await Promise.all([0,1,2].map(worker));}finally{await browser.close();}
 const rendered=results.filter(r=>r?.after.hasSVG).length;if(rendered<cases.length*0.99)throw new Error('Too few formulas rendered: '+rendered+' / '+cases.length);
 const report={passed:results.every(r=>r?.passed),pairs:results.length,rendered,new_errors:results.filter(r=>!r.passed),preexisting_error_pairs:results.filter(r=>r.before.errors.length||r.before.undefined.length).length,cases:results};
 fs.writeFileSync(config.output+'/rendering.json',JSON.stringify(report,null,2));console.log(JSON.stringify({passed:report.passed,pairs:report.pairs,new_errors:report.new_errors.length,preexisting_error_pairs:report.preexisting_error_pairs}));if(!report.passed)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
'''
def run():
    out=HERE/'render-all';out.mkdir(exist_ok=True);shutil.copyfile(HERE/'math-cases.json',out/'math-cases.json');renderer.BROWSER_SCRIPT=SCRIPT
    record={':question/problem':'Fraction-parenthesis rendering check: $x$.',':question/worked-solution':'',':question/answer-fields':[]}
    config=json.loads((ROOT/'reference/mathacademy/repairs/2026-10-18-power-lesson/ui/browser-config.json').read_text())
    original_run=renderer.subprocess.run
    def bounded_run(*args,**kwargs):
        if args and any(str(a).endswith('render-browser.cjs') for a in args[0]):kwargs['timeout']=1200
        return original_run(*args,**kwargs)
    renderer.subprocess.run=bounded_run
    try:renderer.render([record],out,[ROOT,'/'],config['browser'],config['playwright'],config['node'])
    finally:renderer.subprocess.run=original_run
    report=json.loads((out/'rendering.json').read_text());summary={'passed':report['passed'],'unique_formula_pairs':report['pairs'],'new_rendering_errors':len(report['new_errors']),'preexisting_error_pairs':report['preexisting_error_pairs'],'changes_sha256':hashlib.sha256((HERE/'changes.json').read_bytes()).hexdigest(),'math_cases_sha256':hashlib.sha256((HERE/'math-cases.json').read_bytes()).hexdigest(),'ui_sha256':json.loads((out/'ui-hashes.json').read_text())};(HERE/'render-verification.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':run()
