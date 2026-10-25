// Offline browser regression for rich field keys in preview and learner feedback.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const http = require('node:http');
const os = require('node:os');
const path = require('node:path');
const root = path.resolve(process.argv[2] || path.join(__dirname, '..'));
const reportPath = process.argv[3];
const playwright = process.env.COURSE_ACADEMY_PLAYWRIGHT_MODULE || path.join(os.homedir(), '.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright');
const { chromium } = require(playwright);
const cache = path.join(os.homedir(), '.cache/ms-playwright');
const browserPath = fs.readdirSync(cache).filter(name => name.startsWith('chromium_headless_shell-')).sort().reverse()
  .map(name => path.join(cache, name, 'chrome-headless-shell-linux64/chrome-headless-shell')).find(name => fs.existsSync(name));
const learning = fs.readFileSync(path.join(root, 'ui/learning.js'), 'utf8');
const controllers = learning.slice(learning.indexOf('const $'), learning.indexOf("$('retryButton').addEventListener"));
const html = `<!doctype html><html><head><meta charset="utf-8"><script src="/ui/vendor/dompurify/purify.min.js"></script></head>
<body><main id="main"></main><script type="module">
import {marked} from '/ui/vendor/marked/marked.esm.js';
import {decorateSourceTables} from '/ui/content-tables.js';
import {protectMath} from '/ui/math-protection.js';
import {romanLists} from '/ui/prose-lists.js';
import {inlinePrompt,mountInlineFields,blankInput,checkboxControl,choiceIndicator,fieldFeedback,richSelect,freeInput,questionFeedback,feedbackHeading,responsesComplete} from '/ui/question-fields.js';
const isDeveloperMode=()=>false,attachStepMenu=()=>{};
${controllers}
window.renderCase=(mode,key)=>{
 const field={id:'f',key,type:'checkbox',choices:[{id:'yes',type:'text',value:'true'},{id:'no',type:'text',value:'false'}],correctAnswer:{id:'no',type:'text',value:'false'},response:{choiceId:'yes',value:'true'}};
 const step={itemId:10,contentId:101,kind:'question',status:'incorrect',problem:'Select all true statements.',fields:[field],solution:'Explanation.'};
 const data={type:'review',status:'started',steps:[step]};
 const node=mode==='preview'?previewContent(data,step,0,true):taskContent(data,step,1,1,true);
 document.getElementById('main').replaceChildren(node);
};
window.ready=true;
</script></body></html>`;
const server = http.createServer((req,res) => {
  const url = new URL(req.url, 'http://localhost');
  if(url.pathname === '/fixture') {res.setHeader('content-type','text/html');res.end(html);return;}
  const file = path.resolve(root, '.' + decodeURIComponent(url.pathname));
  if(!file.startsWith(root + path.sep) || !fs.existsSync(file) || !fs.statSync(file).isFile()) {res.statusCode=404;res.end();return;}
  res.setHeader('content-type',file.endsWith('.js')?'text/javascript':file.endsWith('.css')?'text/css':'text/plain');
  res.end(fs.readFileSync(file));
});
(async()=>{
 let browser; const cases=[],errors=[];
 try {
  await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve));
  const origin='http://127.0.0.1:'+server.address().port;
  browser=await chromium.launch({headless:true,executablePath:browserPath,args:['--disable-dev-shm-usage']});
  const page=await browser.newPage();page.on('pageerror',e=>errors.push(String(e)));
  await page.route('**/*',route=>new URL(route.request().url()).origin===origin?route.continue():route.abort());
  await page.goto(origin+'/fixture');await page.waitForFunction('window.ready===true');
  for(const mode of ['preview','learner']) {
   const key=String.raw`$A$ is **not** *singular* & $\det(A)\ne0$ <span onclick="window.injected=true">safe</span><script>window.injected=true</script>`;
   await page.evaluate(({mode,key})=>renderCase(mode,key),{mode,key});
   const result=await page.locator('.response-summary').evaluate(node=>({text:node.textContent,strong:node.querySelector('strong')?.textContent,em:node.querySelector('em')?.textContent,unsafe:!!node.querySelector('script,[onclick]'),tag:node.tagName,injected:!!window.injected}));
   cases.push({mode,...result});
   assert.equal(result.strong,'not',mode+' summary must render Markdown emphasis');
   assert.equal(result.em,'singular');assert.ok(!result.text.includes('**')&&!result.text.includes('*singular*'));
   assert.ok(result.text.includes(String.raw`$A$`)&&result.text.includes(String.raw`\det(A)\ne0`),'math must survive Markdown for MathJax');
   assert.ok(result.text.includes('&'));assert.equal(result.unsafe,false);assert.equal(result.injected,false);
  }
  assert.deepEqual(errors,[]);
  const report={passed:true,cases,javascriptErrors:errors,database_writes:0};
  if(reportPath)fs.writeFileSync(reportPath,JSON.stringify(report,null,2)+'\n');
  console.log(JSON.stringify(report));
 } catch(error) {
  if(reportPath)fs.writeFileSync(reportPath,JSON.stringify({passed:false,cases,javascriptErrors:errors,error:String(error)},null,2)+'\n');
  throw error;
 } finally {if(browser)await browser.close();await new Promise(resolve=>server.close(resolve));}
})().catch(error=>{console.error(error);process.exitCode=1;});
