
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
  await page.locator('.lesson-content').waitFor();await page.evaluate(async()=>{await MathJax.startup.promise;await document.fonts.ready;});
  for(let start=workerIndex*50;start<cases.length;start+=150){
   const batch=cases.slice(start,start+50);
   const report=await page.evaluate(async batch=>{
    const out=[];
    function state(node){return {errors:[...node.querySelectorAll('[data-mml-node="merror"],mjx-merror')].map(n=>n.getAttribute('data-mjx-error')||n.textContent),undefined:[...node.querySelectorAll('[data-mml-node="mtext"]')].map(n=>n.textContent.trim()).filter(s=>/^\\[A-Za-z]+$/.test(s)),hasSVG:!!node.querySelector('svg')};}
    for(const c of batch){
     let before,after;
     try{before=state(await MathJax.tex2svgPromise(c.before,{display:c.display}));}catch(e){before={errors:[String(e)],undefined:[],hasSVG:false};}
     try{after=state(await MathJax.tex2svgPromise(c.after,{display:c.display}));}catch(e){after={errors:[String(e)],undefined:[],hasSVG:false};}
     const newErrors=after.errors.filter(e=>!before.errors.includes(e));const newUndefined=after.undefined.filter(e=>!before.undefined.includes(e));
     out.push({index:c.index,before,after,newErrors,newUndefined,passed:!newErrors.length&&!newUndefined.length&&(after.hasSVG||!before.hasSVG)});
    }
    return out;
   },batch);
   for(const item of report){results[item.index]=item;if(item.before.errors.length||item.before.undefined.length||!item.passed)exceptions.push(item);}
   completed+=report.length;fs.writeFileSync(config.output+'/progress.json',JSON.stringify({completed,total:cases.length,exceptions},null,2));
   if(completed%500<50)console.log('Checked '+completed+' / '+cases.length+' formula pairs');
  }
  await context.close();
 }
 try{await Promise.all([0,1,2].map(worker));}finally{await browser.close();}
 const report={passed:results.every(r=>r?.passed),pairs:results.length,new_errors:results.filter(r=>!r.passed),preexisting_error_pairs:results.filter(r=>r.before.errors.length||r.before.undefined.length).length,cases:results};
 fs.writeFileSync(config.output+'/rendering.json',JSON.stringify(report,null,2));console.log(JSON.stringify({passed:report.passed,pairs:report.pairs,new_errors:report.new_errors.length,preexisting_error_pairs:report.preexisting_error_pairs}));if(!report.passed)process.exitCode=1;
})().catch(e=>{console.error(e);process.exitCode=1});
