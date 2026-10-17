import assert from 'node:assert/strict';
import test from 'node:test';
import vm from 'node:vm';
import { readFile } from 'node:fs/promises';
import { marked } from '../ui/vendor/marked/marked.esm.js';

const shared = (await readFile(new URL('../ui/question-fields.js', import.meta.url), 'utf8')).replace(/^[\s\S]*?(?=\/\/ Shared presentation)/, '').replaceAll('export ', '');
const assignmentSource = await readFile(new URL('../ui/assignments.js', import.meta.url), 'utf8');
const assignments = assignmentSource.slice(assignmentSource.indexOf('const $'), assignmentSource.indexOf('createCoursePicker({'));

function fixture() {
  class Element extends EventTarget {
    constructor(tag) { super(); this.tagName = tag; this.childNodes = []; this.dataset = {}; this.style = {}; this.className = ''; this.attrs = {}; }
    get children() { return this.childNodes.filter(node => node.tagName !== '#text'); }
    get childElementCount() { return this.children.length; }
    get classList() { return { contains: name => this.className.split(' ').includes(name), toggle: (name, enabled) => {
      const names = new Set(this.className.split(' ').filter(Boolean)); if (enabled) names.add(name); else names.delete(name); this.className = [...names].join(' ');
    } }; }
    get textContent() { return (this.text || '') + this.childNodes.map(node => node.textContent).join(''); }
    set textContent(value) { this.replaceChildren(); this.text = String(value); }
    append(...nodes) { for (const node of nodes) { node.remove(); node.parent = this; this.childNodes.push(node); } }
    replaceChildren(...nodes) { for (const node of this.childNodes) node.parent = null; this.childNodes = []; this.text = ''; this.append(...nodes); }
    remove() { if (this.parent) this.parent.childNodes = this.parent.childNodes.filter(node => node !== this); this.parent = null; }
    contains(node) { for (; node; node = node.parent) if (node === this) return true; return false; }
    get isConnected() { return document.body.contains(this); }
    setAttribute(key, value) { this.attrs[key] = String(value); }
    getAttribute(key) { return this.attrs[key] ?? null; }
    matches(selector) {
      if (selector.startsWith('.')) return this.classList.contains(selector.slice(1));
      if (selector.startsWith('[data-')) return selector.slice(6, -1).replace(/-([a-z])/g, (_, c) => c.toUpperCase()) in this.dataset;
      if (selector === 'input:checked') return this.tagName === 'input' && this.checked;
      return this.tagName === selector;
    }
    querySelectorAll(selector) { return this.children.flatMap(child => [...(selector.split(',').some(s => child.matches(s.trim())) ? [child] : []), ...child.querySelectorAll(selector)]); }
    querySelector(selector) { return this.querySelectorAll(selector)[0] || null; }
    dispatchEvent(event) { const result = super.dispatchEvent(event); if (event.bubbles && this.parent) this.parent.dispatchEvent(event); return result; }
    click() { if (!this.disabled) this.dispatchEvent(new Event('click', { bubbles: true })); }
    focus() { document.activeElement = this; }
  }
  const document = new EventTarget(); document.body = new Element('body'); document.hidden = false;
  document.createElement = tag => new Element(tag);
  document.createTextNode = text => { const node = new Element('#text'); node.textContent = text; return node; };
  document.getElementById = () => null;
  const context = vm.createContext({ document, Event, crypto, URL, marked, attachStepMenu: (node, id) => { node.dataset.stepDbId = id; }, location: { href: 'http://127.0.0.1:8765/assignments' }, isDeveloperMode: () => false });
  const h = vm.runInContext(`(() => {
    ${shared}
    ${assignments}
    markdown = (value, fields = []) => {
      const prompt = el('div', 'prose', value || '');
      for (const marker of marked.parse(inlinePrompt(value, fields)).matchAll(/<span[^>]+data-field-key="([^"]+)"/g)) {
        const slot = el('span', 'field-location'); slot.dataset.fieldKey = marker[1]; prompt.append(slot);
      }
      return prompt;
    };
    typeset = async () => {};
    return { inlinePrompt, mountInlineFields, richSelect, questionFeedback, feedbackHeading, checkboxControl, freeInput, responsesComplete, choiceIndicator, fieldFeedback,
      render: question => { assignmentData = { basis: 1, preview: false }; const view = questionView(question); refreshControls(); return questionViews.get(questionKey(question)); },
      update: question => applyAssignment({ basis: 2, preview: false, assignment: { steps: [{ content: question }] } }, generation),
      responses: view => collectResponses(view),
    };
  })()`, context);
  return { h, document, node: tag => new Element(tag) };
}

const field = { id: 'field', entityId: 11, key: 'blank-1', type: 'blank' };

test('markers follow prose and equation positions while unrelated math and code stay unchanged', () => {
  const { h } = fixture();
  assert.equal(h.inlinePrompt('$x^2+1$', [field]), '$x^2+1$');
  assert.match(h.inlinePrompt('The value is {{answer-field:blank-1}}.', [field]), /value is <span[^>]+data-field-key="blank-1"[^>]*><\/span>\./);
  assert.match(h.inlinePrompt('$y={{blank-1}}+1$', [field]), /\\\(y=\\\)<span.*<\/span>\\\(\+1\\\)/);
  assert.match(h.inlinePrompt('$$y={{blank-1}}$$', [field]), /class="question-equation"/);
  assert.match(h.inlinePrompt('$\\frac{ {{blank-1}} }{2}$', [field]), /^\$\\frac\{ \\underline\{\\phantom\{xxxx\}\} \}\{2\}\$<span/);
  const aligned = String.raw`$$\begin{aligned}A &= {{blank-1}} \\ B &= 2\end{aligned}$$`;
  assert.match(h.inlinePrompt(aligned, [field]), /^\$\$\\begin\{aligned\}[\s\S]*\\end\{aligned\}\$\$<span/);
  assert.match(h.inlinePrompt('$x^{{blank-1}}$', [field]), /^\$x\^\\underline\{\\phantom\{xxxx\}\}\$<span/);
  assert.match(h.inlinePrompt('${{blank-1}}_2$', [field]), /^\$\\underline\{\\phantom\{xxxx\}\}_2\$<span/);
  assert.equal(h.inlinePrompt('`$y={{blank-1}}$`\n```text\n{{blank-1}}\n```', [field]), '`$y={{blank-1}}$`\n```text\n{{blank-1}}\n```');
  assert.equal(h.inlinePrompt('{{missing}} {{choice}}', [{ key: 'choice', type: 'radio' }]), '{{missing}} {{choice}}');
  assert.ok(!h.inlinePrompt('{{bad"key}}', [{ ...field, key: 'bad"key' }]).includes('data-field-key="bad"key"'));
});

test('indented standalone answer markers render controls rather than escaped HTML', () => {
  const f = fixture();
  const question = { id: 'indented', kind: 'question', stepId: 'step', gradable: true, status: 'paused',
    problem: '$\\frac{\\text{d}h}{\\text{d}x}\\,=$\n\n' + ' '.repeat(28) + '\n' + ' '.repeat(40) + '{{blank-1}}\n\n\t{{answer-field:term}}',
    fields: [field, { id: 'term', entityId: 12, key: 'term', type: 'select', choices: [{ id: 'a', entityId: 31, type: 'text', value: 'derivative' }] }],
  };
  const html = marked.parse(f.h.inlinePrompt(question.problem, question.fields));
  assert.ok(!html.includes('<pre>') && !html.includes('&lt;span'), html);
  const view = f.h.render(question);
  assert.equal(view.prompt.querySelectorAll('.answer-inline').length, 2);
  assert.equal(view.prompt.querySelectorAll('input').length, 1);
  assert.equal(view.prompt.querySelectorAll('select').length, 1);
  assert.equal(view.fieldList.childElementCount, 0);
  assert.equal(view.fieldList.hidden, true);
  view.prompt.querySelector('input').value = '-4cos(x)';
  view.prompt.querySelector('select').value = '31';
  assert.deepEqual(JSON.parse(JSON.stringify(f.h.responses(view))), [{ fieldId: 11, value: '-4cos(x)' }, { fieldId: 12, choiceId: 31 }]);
});

test('answer indentation repair leaves prose, code examples, and non-inline markers unchanged', () => {
  const { h } = fixture(), indent = ' '.repeat(40);
  const unchanged = '    Ordinary indented code.\n\n- A list item\n  with its continuation.\n\n'
    + '`{{blank-1}}`\n\n```text\n' + indent + '{{blank-1}}\n```\n\n'
    + indent + '{{unknown}}\n\n' + indent + '{{choice}}\n\n' + indent + '{{explanation}}\n\n' + indent + '{{check}}';
  assert.equal(h.inlinePrompt(unchanged, [field, { key: 'choice', type: 'radio' }, { key: 'explanation', type: 'free' }, { key: 'check', type: 'checkbox' }]), unchanged);
  assert.match(marked.parse(h.inlinePrompt(unchanged, [field])), /<pre><code>Ordinary indented code\./);
});

test('rich selects keep choice IDs, show authored content, support keyboard navigation, and respect read-only state', () => {
  const f = fixture(), select = f.node('select'); select.value = ''; select.setAttribute('aria-label', 'Term');
  const choices = [{ id: 31, value: '$2x$' }, { id: 32, value: 'constant' }];
  const rich = f.h.richSelect(select, choices, choice => { const node = f.node('span'); node.textContent = choice.value; return node; });
  f.document.body.append(rich);
  const trigger = rich.querySelector('.answer-select-trigger'), menu = rich.querySelector('.answer-select-menu');
  const options = rich.querySelectorAll('.answer-select-option');
  let changed = 0; select.addEventListener('change', () => { changed++; });
  trigger.click(); assert.equal(menu.hidden, false); assert.equal(f.document.activeElement, options[0]);
  const down = new Event('keydown', { bubbles: true, cancelable: true }); Object.defineProperty(down, 'key', { value: 'ArrowDown' });
  options[0].dispatchEvent(down); assert.equal(f.document.activeElement, options[1]);
  options[0].click(); assert.equal(select.value, '31'); assert.equal(changed, 1);
  assert.equal(rich.querySelector('.answer-select-value').textContent, '$2x$');
  assert.equal(menu.hidden, true); assert.equal(f.document.activeElement, trigger);
  assert.equal(options[0].getAttribute('aria-selected'), 'true');
  trigger.click(); const escape = new Event('keydown', { bubbles: true, cancelable: true }); Object.defineProperty(escape, 'key', { value: 'Escape' });
  options[0].dispatchEvent(escape); assert.equal(menu.hidden, true);
  trigger.click(); f.document.dispatchEvent(new Event('pointerdown')); assert.equal(menu.hidden, true);
  select.disabled = true; trigger.click(); assert.equal(menu.hidden, true);
  options[1].click(); assert.equal(select.value, '31'); assert.equal(changed, 1);
});

test('read-only inline blanks repeat the saved value without adding an editable control', () => {
  const f = fixture(), prompt = f.node('div'), list = f.node('div');
  const slots = [f.node('span'), f.node('span')];
  for (const slot of slots) { slot.dataset.fieldKey = 'blank-1'; prompt.append(slot); }
  const saved = { ...field, response: { value: '3' } };
  f.h.mountInlineFields(prompt, list, [saved], () => {
    const control = f.node('fieldset'), value = f.node('span');
    value.className = 'answer-saved-value'; value.textContent = '3'; control.append(value); return control;
  });
  assert.equal(slots[0].querySelector('.answer-saved-value').textContent, '3');
  assert.equal(slots[1].textContent, '3');
  assert.equal(prompt.querySelector('input'), null);
  assert.equal(list.hidden, true);
});

test('assignment inline responses submit by entity ID and survive graded replacement; missing markers stay below', () => {
  const f = fixture();
  const question = { id: 'q', kind: 'question', stepId: 'step', gradable: true, status: 'paused',
    problem: '$y=$ {{blank-1}}, select {{term}}.', fields: [field,
      { id: 'term', entityId: 12, key: 'term', type: 'select', choices: [{ id: 'answer', entityId: 31, type: 'text', value: 'derivative' }] },
      { id: 'extra', entityId: 13, key: 'extra', type: 'blank' },
    ] };
  const view = f.h.render(question); f.document.body.append(view.node);
  assert.equal(view.node.querySelectorAll('.answer-inline').length, 2);
  assert.equal(view.fieldList.querySelectorAll('fieldset').length, 1);
  view.form.querySelector('input').value = '2x'; view.form.querySelector('select').value = '31'; view.fieldList.querySelector('input').value = 'kept';
  assert.deepEqual(JSON.parse(JSON.stringify(f.h.responses(view))), [{ fieldId: 11, value: '2x' }, { fieldId: 12, choiceId: 31 }, { fieldId: 13, value: 'kept' }]);
  const fields = question.fields.map((item, index) => ({ ...item, response: index === 1 ? { entityId: 31 } : { value: index === 0 ? '2x' : 'kept' } }));
  f.h.update({ ...question, status: 'correct', fields });
  assert.equal(view.form.querySelector('input').value, '2x'); assert.equal(view.form.querySelector('select').value, '31');
  assert.equal(view.form.querySelector('.answer-select-trigger').disabled, true);
  assert.equal(view.node.querySelectorAll('.answer-inline').length, 2);
  assert.equal(view.result.querySelector('.feedback').dataset.feedback, 'correct');
  f.h.update({ ...question, status: 'incorrect', fields });
  assert.equal(view.result.querySelector('.feedback').dataset.feedback, 'incorrect');
  f.h.questionFeedback(view.result, 'skipped'); assert.equal(view.result.dataset.feedback, '');
});

test('feedback accents retain readable contrast on dark and light question surfaces', async () => {
  const styles = await readFile(new URL('../ui/navigation.css', import.meta.url), 'utf8');
  const luminance = hex => {
    const rgb = hex.match(/[a-f0-9]{2}/gi).map(part => parseInt(part, 16) / 255)
      .map(value => value <= .04045 ? value / 12.92 : ((value + .055) / 1.055) ** 2.4);
    return rgb[0] * .2126 + rgb[1] * .7152 + rgb[2] * .0722;
  };
  const roots = [...styles.matchAll(/:root(\[data-theme="light"\])?\s*\{([^}]+)\}/g)];
  const declarations = { dark: '', light: '' };
  roots.forEach(root => { declarations[root[1] ? 'light' : 'dark'] += root[2]; });
  for (const [theme, rules] of Object.entries(declarations)) {
    for (const name of ['correct', 'incorrect']) {
      const color = rules.match(new RegExp('--answer-' + name + ':\\s*(#[a-f0-9]+)'))?.[1];
      assert.ok(color);
      const ink = luminance(color), background = luminance(theme === 'light' ? '#eeeeee' : '#111111');
      assert.ok((Math.max(ink, background) + .05) / (Math.min(ink, background) + .05) >= 4.5);
    }
  }
});


test('math blanks use editable equations, retain LaTeX responses, and lock after grading', () => {
  const f = fixture();
  const math = { ...field, answerType: 'math', response: { value: String.raw`\frac{11}{4x}` } };
  const question = { id: 'math-q', kind: 'question', gradable: true, status: 'started',
    problem: '$y=$ {{blank-1}}.', fields: [math, { id: 'text', entityId: 12, key: 'word', type: 'blank', answerType: 'text' }] };
  const view = f.h.render(question); f.document.body.append(view.node);
  const editor = view.form.querySelector('math-field');
  assert.ok(editor); assert.equal(editor.getAttribute('aria-label'), 'Answer 1');
  assert.equal(editor.mathVirtualKeyboardPolicy, 'auto');
  assert.equal(editor.getAttribute('placeholder'), '');
  assert.equal(editor.disabled, false);
  assert.equal(view.form.querySelectorAll('input').length, 1);
  editor.value = String.raw`-\frac{7}{3x}`;
  editor.dispatchEvent(new Event('input', { bubbles: true }));
  assert.equal(view.check.disabled, true); // second, text field is still empty
  view.form.querySelector('input').value = 'text';
  view.form.querySelector('input').dispatchEvent(new Event('input', { bubbles: true }));
  assert.equal(view.check.disabled, false);
  editor.value = String.raw`\frac{11}{\placeholder{}}`;
  editor.dispatchEvent(new Event('input', { bubbles: true }));
  assert.equal(view.check.disabled, true);
  editor.value = String.raw`-\frac{7}{3x}`;
  editor.dispatchEvent(new Event('input', { bubbles: true }));
  assert.equal(view.check.disabled, false);
  assert.deepEqual(JSON.parse(JSON.stringify(f.h.responses(view))), [
    { fieldId: 11, value: String.raw`-\frac{7}{3x}` }, { fieldId: 12, value: 'text' },
  ]);
  f.h.update({ ...question, status: 'correct', fields: [{ ...math, response: { value: editor.value } }, question.fields[1]] });
  assert.equal(view.form.querySelector('math-field').disabled, true);
  assert.equal(view.form.querySelector('math-field').value, String.raw`-\frac{7}{3x}`);
});


const checkboxFields = ['I', 'II', 'III', 'None'].map((key, index) => ({
  id: 'field-' + key, entityId: 10 + index, key, type: 'checkbox',
  choices: [{ entityId: 100 + 2 * index, type: 'text', value: 'false' },
    { entityId: 101 + 2 * index, type: 'text', value: 'true' }],
}));

test('each checkbox submits its own true or false answer, including untouched unchecked fields', () => {
  const f = fixture();
  const question = { id: 'check-question', entityId: 500, kind: 'question', gradable: true,
    status: 'started', itemId: 600, problem: 'Which equations?', fields: checkboxFields };
  const view = f.h.render(question);
  assert.deepEqual(JSON.parse(JSON.stringify(f.h.responses(view))), [
    { fieldId: 10, choiceId: 100 }, { fieldId: 11, choiceId: 102 },
    { fieldId: 12, choiceId: 104 }, { fieldId: 13, choiceId: 106 },
  ]);
  assert.equal(f.h.responsesComplete(question.fields, f.h.responses(view)), true);
  const inputs = view.form.querySelectorAll('input').filter(input => input.type === 'checkbox');
  assert.equal(inputs.length, 4);
  inputs[1].checked = true; inputs[1].dispatchEvent(new Event('input'));
  inputs[2].checked = true; inputs[2].dispatchEvent(new Event('change'));
  assert.deepEqual(JSON.parse(JSON.stringify(f.h.responses(view))), [
    { fieldId: 10, choiceId: 100 }, { fieldId: 11, choiceId: 103 },
    { fieldId: 12, choiceId: 105 }, { fieldId: 13, choiceId: 106 },
  ]);
  // None has no generated exclusivity behavior: it exists only as authored.
  inputs[3].checked = true; inputs[3].dispatchEvent(new Event('input'));
  assert.equal(f.h.responses(view)[3].choiceId, 107);
});

test('checkbox responses restore as read-only, and malformed banks are rejected', () => {
  const f = fixture();
  const render = label => { const node = f.node('span'); node.textContent = label; return node; };
  const control = f.h.checkboxControl({ ...checkboxFields[1], response: { choiceId: 103 } }, render, true);
  const input = control.querySelectorAll('input').find(input => input.type === 'checkbox');
  assert.equal(input.checked, true); assert.equal(input.disabled, true);
  assert.equal(control.querySelector('.answer-choice-value').value, '103');
  assert.throws(() => f.h.checkboxControl({ ...checkboxFields[1], choices: [] }, render), /true and false/);
});

test('free fields collect verbatim Markdown and LaTeX without displaying the bank or grading feedback', () => {
  const f = fixture(), value = '  **Reason:**\n\n$y=2x$  ';
  const question = { id: 'written', entityId: 510, kind: 'question', collectable: true, gradable: false,
    status: 'started', itemId: 610, problem: 'Explain your reasoning.', fields: [{ id: 'free', entityId: 20,
      key: 'explanation', type: 'free', choices: [{ entityId: 90, value: 'private bank value' }] }] };
  const view = f.h.render(question), input = view.form.querySelector('textarea');
  input.value = value; input.dispatchEvent(new Event('input'));
  assert.deepEqual(JSON.parse(JSON.stringify(f.h.responses(view))), [{ fieldId: 20, value }]);
  assert.equal(f.h.responsesComplete(question.fields, f.h.responses(view)), true);
  assert.equal(view.form.querySelectorAll('.choice').length, 0);
  assert.equal(view.check.textContent, 'Save response');
  assert.match(view.form.querySelector('.answer-preview').textContent, /Reason/);
  assert.equal(f.h.feedbackHeading('completed').textContent, 'Response saved');
});

test('questions have one overall badge with plain status text', () => {
  const { h } = fixture();
  for (const [status, label] of [['correct', 'Correct'], ['incorrect', 'Incorrect']]) {
    const heading = h.feedbackHeading(status, true);
    assert.equal(heading.querySelectorAll('.feedback-badge').length, 1);
    assert.equal(heading.querySelector('.feedback-badge').textContent, label);
    assert.equal(heading.querySelector('.feedback-badge').dataset.grade, status);
    assert.equal(heading.querySelector('.feedback-preview').textContent, 'Preview only');
  }
  const skipped = h.feedbackHeading('skipped');
  assert.equal(skipped.querySelector('.feedback-icon'), null);
  assert.equal(skipped.textContent, 'Skipped');
});

test('filled feedback badges keep at least 4.5:1 contrast with their white text', async () => {
  const css = await readFile(new URL('../ui/learning.css', import.meta.url), 'utf8');
  for (const match of css.matchAll(/--feedback-fill: (#[a-f0-9]{6})/g)) {
    const rgb = match[1].slice(1).match(/../g).map(part => parseInt(part, 16) / 255)
      .map(v => v <= .04045 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4);
    const luminance = .2126 * rgb[0] + .7152 * rgb[1] + .0722 * rgb[2];
    assert.ok(1.05 / (luminance + .05) >= 4.5);
  }
});


test('choice feedback separates wrong selections, missed correct choices, and neutral choices', () => {
  const f = fixture();
  const fields = [
    {entityId:11,key:'selection',type:'radio',choices:[{entityId:101,value:'wrong'},{entityId:102,value:'right'},{entityId:103,value:'other'}],response:{choiceId:101},correctAnswer:{entityId:102}},
    ...checkboxFields.slice(0,3).map((field,index) => ({...field, entityId:12+index,
      response:{choiceId:field.choices[index===1 ? 0 : 1].entityId},
      correctAnswer:field.choices[index===2 ? 0 : 1]})),
  ];
  const view = f.h.render({id:'graded',entityId:90,kind:'question',status:'incorrect',fields});
  const indicators = view.form.querySelectorAll('.answer-indicator');
  assert.deepEqual(indicators.map(n => n.dataset.result), ['incorrect','missed','neutral','correct','missed','incorrect']);
  assert.deepEqual(indicators.map(n => n.querySelector('.answer-symbol').textContent), ['×','−','','✓','−','×']);
  assert.equal(indicators[1].querySelector('.sr-only').textContent, 'Correct choice missed.');
  assert.equal(view.result.querySelectorAll('.feedback-badge').length,1);
  assert.deepEqual(JSON.parse(JSON.stringify(f.h.responses(view))).map(r => r.choiceId), [101,101,102,105]);
  for (const status of ['started','paused','submitted','skipped']) {
    for (const field of fields) f.h.fieldFeedback(view.form, field, status);
    assert.ok(indicators.every(n => !n.dataset.result));
  }
});

test('blank colors use engine grades for equivalent math and selects color their chosen value', () => {
  const f = fixture();
  const fields = [
    {entityId:11,key:'value',type:'blank',answerType:'math',response:{value:'0.5'},correctAnswer:{type:'math',value:'1/2'},grade:'correct'},
    {entityId:12,key:'term',type:'select',choices:[{entityId:31,value:'wrong'},{entityId:32,value:'right'}],response:{choiceId:31},correctAnswer:{entityId:32},grade:'incorrect'},
    {entityId:13,key:'other',type:'blank',response:{value:'different'},correctAnswer:{value:'answer'},grade:'incorrect'},
  ];
  const view = f.h.render({id:'mixed',entityId:90,kind:'question',status:'incorrect',fields});
  assert.equal(view.form.querySelector('.answer-math').dataset.grade, 'correct');
  assert.equal(view.form.querySelector('.answer-select-trigger').dataset.grade, 'incorrect');
  assert.equal(view.form.querySelector('.answer-input').dataset.grade, 'incorrect');
  const unknown = f.node('div'), input=f.node('input'); input.className='answer-input'; unknown.append(input);
  f.h.fieldFeedback(unknown,{...fields[2],grade:undefined},'incorrect');
  assert.equal(input.dataset.grade,'');
  f.h.fieldFeedback(unknown,{...fields[2],type:'free'},'incorrect');
  assert.equal(input.dataset.grade,'');
});
