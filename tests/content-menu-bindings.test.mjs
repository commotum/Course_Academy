import assert from 'node:assert/strict';
import test from 'node:test';
import { readFile } from 'node:fs/promises';
import vm from 'node:vm';

const source = await readFile(new URL('../ui/topic.js', import.meta.url), 'utf8');
const renderer = source.slice(source.indexOf('function sidebar('), source.indexOf('function revealHash('));
function fixture() {
  const registrations = [];
  const el = (tag, className, text) => ({ tag, className, text, children: [], attrs: {},
    append(...nodes) { this.children.push(...nodes); },
    setAttribute(key, value) { this.attrs[key] = value; },
  });
  const context = vm.createContext({ el, link: text => el('a', '', text),
    targetControls: {createToggle: () => null}, graphURL: () => '/', courseURL: () => '/progress',
    markdown: () => el('div', 'prose'),
    attachStepMenu: (node, id, ma, options) => registrations.push({node, id, ma, kind: options.kind}),
    attachTopicMenu: (node, topic) => registrations.push({node, id:topic.id, ma:topic.mathAcademyId, kind:'topic'}),
  });
  vm.runInContext(renderer, context);
  context.section = {anchor:'skill',kind:'example',title:'Skill',contentId:22,mathAcademyId:'e-9',knowledgePoint:{id:33},fields:[],markdown:'Example'};
  return { registrations, run: code => vm.runInContext(code, context) };
}

test('topic contents links copy the knowledge point without borrowing the example source ID', () => {
  const f = fixture();
  f.run('sidebar({topic:{id:11,title:"Topic",mathAcademyId:123}},[section],null)');
  assert.deepEqual(f.registrations.map(({id,ma,kind}) => ({id,ma,kind})), [
    {id:11,ma:123,kind:'topic'}, {id:33,ma:undefined,kind:'knowledge point'},
  ]);
});

test('worked example body and knowledge point heading retain distinct identities and types', () => {
  const f = fixture();
  f.run('instructionalSection(section)');
  assert.deepEqual(f.registrations.map(({id,ma,kind}) => ({id,ma,kind})), [
    {id:22,ma:'e-9',kind:'question'}, {id:33,ma:undefined,kind:'knowledge point'},
  ]);
});
