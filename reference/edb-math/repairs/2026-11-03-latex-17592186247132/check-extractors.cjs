const fs=require('fs'),assert=require('assert');
const config=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const {chromium}=require(config.playwright);
(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:config.browser,args:['--disable-dev-shm-usage']});
 const page=await browser.newPage();await page.route('**/*',route=>route.abort());const checks=[];
 try{
  for(const path of config.extractors){
   const source=fs.readFileSync(path,'utf8');
   for(const name of ['arcsec','arccsc','arccot','arsinh','arcosh','arcoth','arsech','det','min','cis','curl','ln','sin']){
    for(const powered of [false,true]){
     const operator='<mi>'+name+'</mi>';
     const body=(powered?'<msup>'+operator+'<mn>2</mn></msup>':operator)+'<mi>x</mi>';
     await page.setContent('<div id="fixture"><div class="questionWidget-text"><math>'+body+'</math></div></div>');
     const result=await page.evaluate(source=>eval('('+source+'\n)')(document.querySelector('#fixture')),source);
     assert.deepStrictEqual(result.errors,[]);assert(result.problem.includes('\\operatorname{'+name+'}'));
     checks.push({extractor:path,name,powered,output:result.problem});
    }
   }
  }
 }finally{await browser.close()}
 fs.writeFileSync(config.output,JSON.stringify({passed:true,checks},null,2)+'\n');
 console.log(JSON.stringify({passed:true,checks:checks.length}));
})().catch(error=>{console.error(error);process.exitCode=1});
