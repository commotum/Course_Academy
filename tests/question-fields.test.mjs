import assert from 'node:assert/strict';
import test from 'node:test';
import vm from 'node:vm';
import { readFile } from 'node:fs/promises';

const shared = (await readFile(new URL('../ui/question-fields.js', import.meta.url), 'utf8')).replaceAll('export ', '');
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
    return { inlinePrompt, mountInlineFields, richSelect, questionFeedback,
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
