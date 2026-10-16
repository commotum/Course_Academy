import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const source = await readFile(new URL('../ui/activity.js', import.meta.url), 'utf8');
const code = source.slice(source.indexOf('const $'), source.indexOf('createCoursePicker({'));
const fieldUI = (await readFile(new URL('../ui/question-fields.js', import.meta.url), 'utf8')).replace(/^[\s\S]*?(?=\/\/ Shared presentation)/, '').replaceAll('export ', '');
function fixture() {
  const calls = []; let fail = false; let malformed = false;
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName = tag; this.children = []; this.attrs = {}; this.dataset = {}; this.className = ''; this.text = ''; }
    append(...nodes) { this.children.push(...nodes); }
    replaceChildren(...nodes) { this.children = nodes; }
    get textContent() { return this.text + this.children.map(n => n.textContent || '').join(' '); }
    set textContent(value) { this.text = String(value); this.children = []; }
    setAttribute(key, value) { this.attrs[key] = value; }
    removeAttribute(key) { delete this.attrs[key]; }
    querySelector() { return null; }
    get isConnected() { return true; }
  }
  const document = {createElement: tag => new Element(tag), getElementById() {return null;}};
  const context = vm.createContext({ document, window: {}, Intl, Date, Number, Map, String, Promise,
    readRequest: async path => { calls.push(path); return {ok: !fail, json: async () => fail ? {error:'Try later'} : malformed ? {} : {items:[], activity:{taskId:10}}}; },
    checkboxControl: () => null,
    attachStepMenu: (node, id, ma, options = {}) => { node.dataset.stepDbId = id; node.dataset.mathAcademyId = ma; node.dataset.contentKind = options.kind; },
  });
  vm.runInContext(fieldUI + '\n' + code, context);
  return {context, calls, setFail(value) {fail=value;}, setMalformed(value) {malformed=value;}, run: code => vm.runInContext(code, context)};
}
const flush = () => new Promise(resolve => setImmediate(resolve));

test('activity rows defer loading, reuse an expanded history, and make no mutations', async () => {
  const f=fixture();
  const row=f.run('activityRow({taskId:10,title:"Calculus",type:"lesson",xp:8,xpBase:10,elapsedSeconds:61,questionCount:2,correctCount:1})');
  assert.equal(f.calls.length,0);
  row.open=true; row.dispatchEvent(new Event('toggle')); await flush();
  assert.deepEqual(f.calls,['/api/activity?taskId=10']);
  assert.match(row.textContent,/8\/10 XP/); assert.match(row.textContent,/1\/2 correct/);
  assert.match(row.textContent,/Elapsed: 1:01/);
  row.open=false; row.dispatchEvent(new Event('toggle')); row.open=true; row.dispatchEvent(new Event('toggle')); await flush();
  assert.equal(f.calls.length,1);
});
test('concurrent expansions coalesce and rejected requests can be retried', async () => {
  const f=fixture();
  await Promise.all([f.run('detailRequest(10)'),f.run('detailRequest(10)')]); assert.equal(f.calls.length,1);
  f.setFail(true); await assert.rejects(f.run('detailRequest(11)'),/Try later/);
  f.setFail(false); await f.run('detailRequest(11)'); assert.equal(f.calls.length,3);
});
test('malformed responses do not poison the detail cache', async () => {
  const f=fixture(); f.setMalformed(true); await assert.rejects(f.run('detailRequest(10)'),/unavailable/);
  f.setMalformed(false); await f.run('detailRequest(10)'); assert.equal(f.calls.length,2);
});
test('missing recorded data is distinguished from zero time and incorrect answers', () => {
  const f=fixture(); assert.equal(f.run('duration(null)'),'Time unavailable'); assert.equal(f.run('duration(0)'),'0:00'); assert.equal(f.run('duration(3661)'),'1:01:01');
  assert.equal(f.run('timestamp(null).textContent'),'Date unavailable');
  assert.equal(f.run('resultLabel({status:"paused",kind:"question"})'),'Not submitted');
  assert.equal(f.run('resultLabel({status:"incorrect",kind:"question"})'),'Incorrect');
});

test('history cards and group headings identify their displayed entities rather than presentations', () => {
  const f = fixture();
  f.run("markdown = value => el('div', 'prose', value || '')");
  const card = f.run('renderItem({itemId:101,stepId:202,contentId:303,mathAcademyId:"q-123",kind:"question",fields:[],status:"correct"},1)');
  assert.equal(card.dataset.stepDbId, 303);
  assert.equal(card.dataset.mathAcademyId, 'q-123');
  assert.equal(card.dataset.contentKind, 'question');
  const host = f.run("el('div')"); f.context.host = host;
  f.run('renderDetails(host,{items:[{itemId:101,stepId:202,contentId:303,kind:"example",title:"Skill",group:"Skill",knowledgePoint:{id:404},fields:[]}]})');
  assert.equal(host.children[0].dataset.stepDbId, 404);
  assert.equal(host.children[0].dataset.contentKind, 'knowledge point');
  assert.equal(host.children[1].dataset.stepDbId, 303);
  const row = f.run('activityRow({taskId:101,activityId:505,title:"Lesson"})');
  assert.equal(row.dataset.stepDbId, 505);
});
