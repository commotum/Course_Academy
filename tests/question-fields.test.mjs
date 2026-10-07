import assert from 'node:assert/strict';
import test from 'node:test';
import vm from 'node:vm';
import { readFile } from 'node:fs/promises';

const shared = (await readFile(new URL('../ui/question-fields.js', import.meta.url), 'utf8')).replace(/^import .*;\n/m, '').replace(/^MathfieldElement\..*;\n/gm, '').replaceAll('export ', '');
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
  const context = vm.createContext({ document, Event, crypto, URL, location: { href: 'http://127.0.0.1:8765/assignments' }, isDeveloperMode: () => false });
  const h = vm.runInContext(`(() => {
    ${shared}
    ${assignments}
    markdown = (value, fields = []) => {
      const prompt = el('div', 'prose', value || '');
      for (const marker of inlinePrompt(value, fields).matchAll(/data-field-key="([^"]+)"/g)) {
        const slot = el('span', 'field-location'); slot.dataset.fieldKey = marker[1]; prompt.append(slot);
      }
      return prompt;
    };
    typeset = async () => {};
    return { inlinePrompt, mountInlineFields, richSelect, questionFeedback, feedbackHeading, statementCheckboxControl,
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
  assert.equal(h.inlinePrompt('`$y={{blank-1}}$`\n```text\n{{blank-1}}\n```', [field]), '`$y={{blank-1}}$`\n```text\n{{blank-1}}\n```');
  assert.equal(h.inlinePrompt('{{missing}} {{choice}}', [{ key: 'choice', type: 'radio' }]), '{{missing}} {{choice}}');
  assert.ok(!h.inlinePrompt('{{bad"key}}', [{ ...field, key: 'bad"key' }]).includes('data-field-key="bad"key"'));
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


const statementPrompt = 'Which equations?\n\nI. - $y\'\'=x$\nII. - $y\'=x$\nIII. - $y\'=y$';
const combinationValues = ['None of those listed', 'I only', 'II only', 'I and II only', 'III only', 'I and III only', 'II and III only', 'I, II, and III'];
const statementField = { id: 10, key: 'selection', type: 'radio', presentation: 'checkbox',
  choices: combinationValues.map((value, index) => ({ id: 100 + index, type: 'text', value })) };

test('independent Roman checkboxes submit exactly the original authored choice for every combination', () => {
  const f = fixture();
  const render = label => { const node = f.node('span'); node.textContent = label; return node; };
  const control = f.h.statementCheckboxControl(statementField, statementPrompt, render);
  assert.ok(control);
  const inputs = control.querySelectorAll('input').filter(input => input.type === 'checkbox');
  assert.deepEqual(Array.from(inputs, input => input.value), ['I', 'II', 'III']);
  const encoded = control.querySelector('.answer-choice-value');
  for (let mask = 0; mask < 8; mask++) {
    inputs.forEach((input, i) => { input.checked = Boolean(mask & (1 << i)); input.dispatchEvent(new Event('input')); });
    assert.equal(encoded.value, String(100 + mask));
  }
});

test('saved combination answers reopen as the matching read-only checkbox selection', () => {
  const f = fixture();
  const control = f.h.statementCheckboxControl({ ...statementField, response: { choiceId: 106 } }, statementPrompt,
    label => { const node = f.node('span'); node.textContent = label; return node; }, true);
  const inputs = control.querySelectorAll('input').filter(input => input.type === 'checkbox');
  assert.deepEqual(Array.from(inputs, input => input.checked), [false, true, true]);
  assert.equal(inputs.every(input => input.disabled), true);
  assert.equal(control.querySelector('.answer-choice-value').value, '106');
});

test('ordinary radio fields and incomplete or ambiguous combination maps retain their existing presentation', () => {
  const f = fixture();
  for (const field of [{ ...statementField, presentation: '' }, { ...statementField, choices: statementField.choices.slice(0, 7) },
    { ...statementField, choices: statementField.choices.map((choice, index) => index === 7 ? { ...choice, value: 'Something else' } : choice) }]) {
    assert.equal(f.h.statementCheckboxControl(field, statementPrompt, () => f.node('span')), null);
  }
});

test('assignments collect the encoded combination rather than the individual checkbox label', () => {
  const f = fixture();
  const question = { id: 'check-question', entityId: 500, kind: 'question', status: 'started', itemId: 600, problem: statementPrompt,
    fields: [{ ...statementField, entityId: 10, choices: statementField.choices.map(choice => ({ ...choice, entityId: choice.id })) }] };
  const view = f.h.render(question);
  const inputs = view.form.querySelectorAll('input').filter(input => input.type === 'checkbox');
  inputs[1].checked = true; inputs[1].dispatchEvent(new Event('input', { bubbles: true }));
  inputs[2].checked = true; inputs[2].dispatchEvent(new Event('input', { bubbles: true }));
  assert.deepEqual(JSON.parse(JSON.stringify(f.h.responses(view))), [{ fieldId: 10, choiceId: 106 }]);
});


test('grading feedback has a visible badge, a large separate symbol, and plain status text', () => {
  const { h } = fixture();
  for (const [status, label, icon] of [['correct', 'Correct!', '✓ '], ['incorrect', 'Incorrect!', '✕ ']]) {
    const heading = h.feedbackHeading(status, true);
    assert.equal(heading.querySelector('.feedback-icon').textContent, icon);
    assert.equal(heading.querySelector('.feedback-icon').getAttribute('aria-hidden'), 'true');
    assert.equal(heading.querySelector('.feedback-badge').textContent, icon + label);
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
