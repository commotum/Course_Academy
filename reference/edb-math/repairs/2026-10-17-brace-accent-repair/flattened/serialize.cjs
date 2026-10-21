const fs=require('fs'),os=require('os'),path=require('path'),{spawn}=require('child_process'),assert=require('assert/strict');
const source=fs.readFileSync(__dirname+'/dom-for-source-recovery.js','utf8');
const rows=JSON.parse(fs.readFileSync(__dirname+'/source-candidates.json','utf8'));
const profile=fs.mkdtempSync(path.join(os.tmpdir(),'brace-source-'));
const child=spawn('/usr/bin/google-chrome',['--headless=new','--no-sandbox','--disable-gpu','--no-first-run','--remote-debugging-pipe','--user-data-dir='+profile,'about:blank'],{stdio:['ignore','ignore','ignore','pipe','pipe']});
let id=0,buf='',session;const pending=new Map();
child.stdio[4].on('data',chunk=>{buf+=chunk;let i;while((i=buf.indexOf('\0'))>=0){const msg=JSON.parse(buf.slice(0,i));buf=buf.slice(i+1);if(msg.id){const p=pending.get(msg.id);pending.delete(msg.id);msg.error?p.reject(new Error(JSON.stringify(msg.error))):p.resolve(msg.result);}}});
const send=(method,params={},sid=session)=>new Promise((resolve,reject)=>{const n=++id;pending.set(n,{resolve,reject});child.stdio[3].write(JSON.stringify({id:n,method,params,...(sid?{sessionId:sid}:{})})+'\0');});
const evaluate=async expression=>{const r=await send('Runtime.evaluate',{expression,awaitPromise:true,returnByValue:true});if(r.exceptionDetails)throw new Error(JSON.stringify(r.exceptionDetails));return r.result.value;};
(async()=>{try{
const target=await send('Target.createTarget',{url:'about:blank'},null);session=(await send('Target.attachToTarget',{targetId:target.targetId,flatten:true},null)).sessionId;
const cache=new Map();
async function convert(mathml){
 if(cache.has(mathml))return cache.get(mathml);
 const wrapped=mathml.startsWith('<math')?mathml:'<math>'+mathml+'</math>';
 await evaluate('document.body.innerHTML='+JSON.stringify('<div id="steps"><div class="step" id="fixture"><div class="questionWidget-text">'+wrapped+'</div></div></div>'));
 const r=await evaluate('('+source+')(document.querySelector("#fixture"))');assert.deepEqual(r.errors,[]);
 const tex=r.problem.trim().replace(/^\$+|\$+$/g,'').trim();assert(!/[⏟⏞]/.test(tex),tex);cache.set(mathml,tex);return tex;
}
for(const row of rows){for(const a of row.accents){a.good=await convert(a.mathml);if(row.entity===17592186078326)a.whole_good=await convert(a.math_source);}}
fs.writeFileSync(__dirname+'/serialized-candidates.json',JSON.stringify(rows,null,2)+'\n');console.log(JSON.stringify({rows:rows.length,unique_source_fragments:cache.size}));
}catch(e){console.error(e);process.exitCode=1;}finally{child.kill();}})();
