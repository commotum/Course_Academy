const fs=require('fs');
const config=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
const fixtures=JSON.parse(fs.readFileSync(process.argv[3],'utf8')).fixtures;
const source=fs.readFileSync(process.argv[4],'utf8');
const {chromium}=require(config.playwright);
(async()=>{const browser=await chromium.launch({headless:true,executablePath:config.browser,args:['--disable-dev-shm-usage']});const page=await browser.newPage();await page.route('**/*',r=>r.abort());const results=[];
for(const f of fixtures){const html=f.kind==='mathml'?f.html:'<div class="mjpage mjpage__block">'+f.html+'</div>';await page.setContent('<div id="fixture"><div class="questionWidget-text">'+html+'</div></div>');results.push(await page.locator('#fixture').evaluate((el,src)=>eval('('+src+'\n)')(el),source));}
await browser.close();fs.writeFileSync(process.argv[5],JSON.stringify(results,null,2));})().catch(e=>{console.error(e);process.exit(1)});
