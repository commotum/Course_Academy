// Exercise real MathLive keyboard shortcuts through the shared answer control.
// All assets are local; no study API or learner database is used.
const assert = require('node:assert/strict');
const fs = require('node:fs'), http = require('node:http'), path = require('node:path'), os = require('node:os');
const root = path.resolve(__dirname, '..');
const { chromium } = require(process.env.COURSE_ACADEMY_PLAYWRIGHT_MODULE || path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright'));
const cache = path.join(os.homedir(), '.cache/ms-playwright');
const executablePath = fs.readdirSync(cache).filter(n => n.startsWith('chromium_headless_shell-')).sort().reverse().map(n => path.join(cache,n,'chrome-headless-shell-linux64/chrome-headless-shell')).find(fs.existsSync);
const html = `<!doctype html><link rel="stylesheet" href="/ui/learning.css"><form id="form"><span id="host"></span><button type="submit">Check answer</button></form><script type="module">
import {loadMathInputs,blankInput} from '/ui/question-fields.js';await loadMathInputs();
window.editor=blankInput({answerType:'math'},'Answer','answer');host.append(editor);
window.submissions=[];form.addEventListener('submit',e=>{e.preventDefault();submissions.push(editor.value)});window.ready=true;
</script>`;
const server = http.createServer((req,res)=>{
 const url=new URL(req.url,'http://localhost');if(url.pathname==='/fixture'){res.setHeader('Content-Type','text/html');res.end(html);return;}
 const file=path.resolve(root,'.'+url.pathname);if(!file.startsWith(root+'/ui/')||!fs.existsSync(file)){res.statusCode=404;res.end();return;}
 const ext=path.extname(file);res.setHeader('Content-Type',({'.js':'text/javascript','.mjs':'text/javascript','.css':'text/css','.woff2':'font/woff2'})[ext]||'application/octet-stream');res.end(fs.readFileSync(file));
});
(async()=>{let browser;try{
 await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));browser=await chromium.launch({headless:true,executablePath,args:['--disable-dev-shm-usage']});
 const page=await browser.newPage();page.setDefaultTimeout(10000);const errors=[];page.on('pageerror',error=>errors.push(String(error)));
 const origin='http://127.0.0.1:'+server.address().port;await page.route('**/*',route=>new URL(route.request().url()).origin===origin?route.continue():route.abort());
 await page.goto(origin+'/fixture');await page.waitForFunction(()=>window.ready);await page.locator('math-field').focus();await page.waitForFunction(()=>editor.shadowRoot.activeElement);
 const checks=[];
 for(const [typed,expected] of [['inf','\\infty'],['-inf','-\\infty'],['+inf','+\\infty'],['infty','\\infty'],['infinity','\\infty']]){
  await page.evaluate(()=>editor.value='');await page.keyboard.type(typed);assert.equal(await page.evaluate(()=>editor.value),expected,typed);checks.push({typed,value:expected});
 }
 await page.evaluate(()=>editor.value='');await page.keyboard.type('in');await page.waitForTimeout(600);await page.keyboard.type('f');assert.equal(await page.evaluate(()=>editor.value),'\\infty');
 await page.keyboard.press('Enter');assert.deepEqual(await page.evaluate(()=>submissions),['\\infty']);checks.push({typed:'in, pause, f, Enter',value:'\\infty'});
 for(const [typed,expected] of [['x in RR',/\\in\\mathbb\{R\}/],['sin(x)',/\\sin/],['11/4x',/\\frac\{11\}\{4x\}/]]){
  await page.evaluate(()=>editor.value='');await page.keyboard.type(typed);const value=await page.evaluate(()=>editor.value);assert.match(value,expected,typed);checks.push({typed,value});
 }
 assert.deepEqual(errors,[]);console.log(JSON.stringify({checks,pageErrors:errors},null,2));
 }finally{await browser?.close();server.closeAllConnections();server.close();}})().catch(error=>{console.error(error);process.exitCode=1;});
