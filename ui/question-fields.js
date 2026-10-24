let mathInputsLoader = null;
export function loadMathInputs() {
  if (!mathInputsLoader) mathInputsLoader = import('./vendor/mathlive/mathlive.min.mjs').then(({ MathfieldElement }) => {
    MathfieldElement.fontsDirectory = new URL('./vendor/mathlive/fonts', import.meta.url).href;
    MathfieldElement.soundsDirectory = null;
  }).catch(error => { mathInputsLoader = null; throw error; });
  return mathInputsLoader;
}

// Shared presentation only: response IDs and grading remain with the activity API.
const answerKind = field => String(field.answerType || field.correctAnswer?.type || field.response?.type || '').split('/').at(-1);
export function responsesComplete(fields, responses) {
  return fields.every((field, index) => {
    const response = responses[index];
    if (!['blank', 'free'].includes(fieldType(field))) return Boolean(response?.choiceId);
    return typeof response?.value === 'string' && Boolean(response.value.trim())
      && (fieldType(field) === 'free' || answerKind(field) !== 'math' || !/\\placeholder\b/.test(response.value));
  });
}
// Each authored checkbox option is an independent Boolean field. The bank's
// false entity is submitted explicitly, including before the first interaction.
export function checkboxControl(field, renderLabel, readOnly = false, name = field.id) {
  if (fieldType(field) !== 'checkbox') return null;
  const bank = field.choices || [];
  const identity = answer => answer.entityId ?? answer.id;
  const yes = bank.find(answer => answer.value === 'true' && String(answer.type).split('/').at(-1) === 'text');
  const no = bank.find(answer => answer.value === 'false' && String(answer.type).split('/').at(-1) === 'text');
  if (bank.length !== 2 || !yes || !no) throw new Error('Checkbox field needs text true and false answers');
  const row = document.createElement('label'); row.className = 'choice';
  const input = document.createElement('input'); input.type = 'checkbox'; input.name = String(name);
  const response = field.response, responseId = response?.choiceId ?? response?.entityId ?? response?.id;
  input.checked = String(responseId) === String(identity(yes)); input.disabled = readOnly;
  const encoded = document.createElement('input'); encoded.type = 'hidden'; encoded.className = 'answer-choice-value';
  encoded.name = String(name); encoded.disabled = readOnly;
  const update = () => { encoded.value = String(identity(input.checked ? yes : no)); };
  input.addEventListener('input', update); input.addEventListener('change', update); update();
  row.append(choiceIndicator(input), renderLabel(field.key), encoded); return row;
}

// Keep the native input for selection, keyboard focus and submission; its
// visible indicator can distinguish a wrong selection from a missed answer.
export function choiceIndicator(input) {
  const indicator = document.createElement('span'); indicator.className = 'answer-indicator';
  indicator.dataset.control = input.type;
  const symbol = document.createElement('span'); symbol.className = 'answer-symbol'; symbol.setAttribute('aria-hidden', 'true');
  const description = document.createElement('span'); description.className = 'sr-only';
  const update = () => { if (!indicator.dataset.result) symbol.textContent = input.type === 'checkbox' && input.checked ? '✓' : ''; };
  input.addEventListener('input', update); input.addEventListener('change', update);
  indicator.append(input, symbol, description); update(); return indicator;
}

const answerId = answer => answer?.choiceId ?? answer?.entityId ?? answer?.id;
export function fieldFeedback(host, field, status) {
  const state = String(status || '').split('/').at(-1);
  const graded = ['correct', 'incorrect'].includes(state) && field.response && field.correctAnswer && fieldType(field) !== 'free';
  const expected = answerId(field.correctAnswer), selected = answerId(field.response);
  const grade = graded ? field.grade || (fieldType(field) === 'blank'
    ? state === 'correct' ? 'correct' : ''
    : String(selected) === String(expected) ? 'correct' : 'incorrect') : '';
  for (const indicator of host.querySelectorAll('.answer-indicator')) {
    const input = indicator.querySelector('input');
    const correct = input.type === 'checkbox' ? field.correctAnswer?.value === 'true' : String(input.value) === String(expected);
    const result = graded ? correct ? input.checked ? 'correct' : 'missed' : input.checked ? 'incorrect' : 'neutral' : '';
    indicator.dataset.result = result;
    indicator.querySelector('.answer-symbol').textContent = result === 'correct' ? '✓' : result === 'missed' ? '−' : result === 'incorrect' ? '×' : !graded && input.type === 'checkbox' && input.checked ? '✓' : '';
    const description = ({ correct: 'Correct choice selected.', missed: 'Correct choice missed.', incorrect: 'Incorrect choice selected.', neutral: 'Incorrect choice left unselected.' })[result] || '';
    indicator.querySelector('.sr-only').textContent = description;
    indicator.title = description;
  }
  for (const control of host.querySelectorAll('.answer-input,.answer-math,.answer-select-trigger,.answer-saved-value')) {
    control.dataset.grade = grade;
  }
}

export function freeInput(field, label, name, renderMarkdown, typeset = () => {}, readOnly = false) {
  const editor = document.createElement('div'); editor.className = 'answer-free-editor';
  const input = document.createElement('textarea'); input.className = 'answer-free';
  input.name = String(name); input.setAttribute('aria-label', label); input.rows = 7;
  input.value = field.response?.value ?? ''; input.disabled = readOnly;
  const preview = document.createElement('details'); preview.className = 'answer-preview';
  const heading = document.createElement('summary'); heading.textContent = 'Preview response';
  const body = document.createElement('div');
  const update = () => { body.replaceChildren(renderMarkdown(input.value)); if (preview.open) void typeset(body); };
  input.addEventListener('input', update); preview.addEventListener('toggle', () => { if (preview.open) update(); });
  preview.append(heading, body); editor.append(input, preview); update(); return editor;
}

export function blankInput(field, label, name, readOnly = false) {
  const kind = answerKind(field);
  const input = document.createElement(kind === 'math' ? 'math-field' : 'input');
  input.className = kind === 'math' ? 'answer-math' : 'answer-input';
  // Standalone answers start wider; inline values get a compact minimum when
  // mounted. These are presentation defaults, never inferred from the key.
  input.dataset.inputSize = 'statement';
  input.setAttribute('name', String(name)); input.setAttribute('aria-label', label);
  if (kind === 'math') {
    input.mathVirtualKeyboardPolicy = 'auto';
    input.setAttribute('placeholder', '');
  } else {
    input.type = 'text'; input.autocomplete = 'off'; input.spellcheck = false;
    input.placeholder = '';
  }
  input.value = field.response?.value ?? '';
  if (kind !== 'math') {
    // field-sizing handles rendered text where supported. The native size is
    // a fallback, with no artificial maximum on the entered answer length.
    const fit = () => { input.size = Math.max(1, Array.from(input.value).length + 1); };
    input.addEventListener('input', fit); fit();
  }
  input.disabled = readOnly;
  // MathLive owns keyboard events inside its shadow root. Capture Enter so
  // both visual math and text blanks use the form's normal submit checks.
  input.addEventListener('keydown', event => {
    if (event.key !== 'Enter' || event.isComposing || event.shiftKey
      || event.ctrlKey || event.altKey || event.metaKey) return;
    event.preventDefault(); event.stopPropagation();
    if (event.repeat || input.disabled || input.readOnly) return;
    const form = input.closest('form');
    const submit = form?.querySelector('button[type="submit"]');
    // The form rechecks completeness and saving state on submit, including
    // when MathLive's deferred input event hasn't updated the button yet.
    if (submit) form.requestSubmit(submit);
  }, { capture: true });
  return input;
}
const fieldMarker = /\{\{(?:answer-field:)?([^}]+)\}\}/g;
const mathBlock = /\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g;
const fieldType = field => String(field.type || '').split('/').at(-1);
const htmlText = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

export function inlinePrompt(value, fields) {
  const keys = new Set(fields.filter(field => ['blank', 'select'].includes(fieldType(field))).map(field => field.key));
  const slot = key => `<span class="field-location" data-field-key="${htmlText(key)}"></span>`;
  // Separate simple equation fragments around an authored field so the control
  // stays outside MathJax's SVG. Ordinary TeX without fields is untouched.
  const code = [], codePrefix = 'CAQUIZCODE' + crypto.randomUUID().replaceAll('-', '');
  let source = String(value || '').replace(/```[\s\S]*?```|`[^`\n]*`/g, match => {
    code.push(match); return codePrefix + (code.length - 1) + 'END';
  });
  // Captured standalone answer markers can retain HTML source indentation.
  // Keep those controls out of Markdown code blocks without dedenting prose
  // or changing the code examples protected above.
  source = source.replace(/^([ \t]+)(\{\{(?:answer-field:)?([^}]+)\}\})[ \t]*$/gm,
    (whole, indent, marker, key) => keys.has(key) && (indent.length >= 4 || indent.includes('\t')) ? marker : whole);
  source = source.replace(mathBlock, match => {
    const display = match.startsWith('$$') || match.startsWith('\\[');
    const edge = match.startsWith('$') && !display ? 1 : 2;
    const body = match.slice(edge, -edge);
    if (![...body.matchAll(fieldMarker)].some(marker => keys.has(marker[1]))) return match;
    const fragments = body.split(fieldMarker);
    const balanced = fragment => {
      const environments = [];
      for (const token of fragment.matchAll(/\\(begin|end)\{([^{}]+)\}/g)) {
        if (token[1] === 'begin') environments.push(token[2]);
        else if (environments.pop() !== token[2]) return false;
      }
      if (environments.length || /^\s*[_^]|[_^]\s*$/.test(fragment)) return false;
      let depth = 0;
      for (const char of fragment.replace(/\\[{}]/g, '')) {
        if (char === '{') depth++; else if (char === '}') depth--;
        if (depth < 0) return false;
      }
      return depth === 0 && (fragment.match(/\\left\b/g)?.length || 0) === (fragment.match(/\\right\b/g)?.length || 0);
    };
    // Groups, scripts and equation environments must remain complete TeX runs.
    // Keep their formula intact and place its answer controls beside it.
    if (fragments.some((part, index) => index % 2 === 0 && !balanced(part))) {
      return match.replace(fieldMarker, (whole, key) => keys.has(key) ? '\\underline{\\phantom{xxxx}}' : whole)
        + [...body.matchAll(fieldMarker)].filter(marker => keys.has(marker[1])).map(marker => slot(marker[1])).join('');
    }
    const parts = fragments.map((part, index) => index % 2
      ? keys.has(part) ? slot(part) : htmlText(`{{${part}}}`)
      : part.trim() ? `\\(${part.trim()}\\)` : '').join('');
    return display ? `\n\n<div class="question-equation">${parts}</div>\n\n` : parts;
  });
  // Code examples must not acquire interactive controls.
  source = source.replace(fieldMarker, (whole, key) => keys.has(key) ? slot(key) : whole);
  return source.replace(new RegExp(codePrefix + '(\\d+)END', 'g'), (_, index) => code[Number(index)]);
}

export function mountInlineFields(prompt, fieldList, fields, makeControl, idOf = field => field.id) {
  fieldList.replaceChildren();
  for (const field of fields) {
    const slots = ['blank', 'select'].includes(fieldType(field))
      ? [...prompt.querySelectorAll('[data-field-key]')].filter(slot => slot.dataset.fieldKey === field.key) : [];
    const control = makeControl(field);
    if (!slots.length) { fieldList.append(control); continue; }
    const inline = document.createElement('span'); inline.className = 'answer-inline';
    inline.dataset.fieldId = String(idOf(field)); inline.dataset.type = fieldType(field);
    for (const child of [...control.children]) {
      if (child.tagName.toLowerCase() !== 'legend' && !child.classList.contains('input-help')) inline.append(child);
    }
    slots[0].replaceChildren(inline);
    const blank = inline.querySelector('.answer-input,.answer-math');
    if (fieldType(field) === 'blank' && blank) {
      blank.dataset.inputSize = 'value';
    }
    // Repeated references show the same answer without creating a second field.
    const sync = () => {
      const input = inline.querySelector('input,select,math-field');
      const value = input?.value ?? (fieldType(field) === 'blank' ? field.response?.value : field.response?.choiceId ?? field.response?.id);
      const selected = field.choices?.find(choice => String(idOf(choice)) === String(value));
      for (const slot of slots.slice(1)) slot.textContent = selected?.value || value || '…';
    };
    inline.addEventListener('input', sync); inline.addEventListener('change', sync); sync();
  }
  fieldList.hidden = !fieldList.childElementCount;
}

export function richSelect(select, choices, renderAnswer, idOf = answer => answer.id, typeset = () => {}) {
  const wrapper = document.createElement('span'); wrapper.className = 'answer-dropdown';
  const trigger = document.createElement('button'); trigger.type = 'button'; trigger.className = 'answer-select-trigger';
  trigger.disabled = select.disabled;
  trigger.setAttribute('aria-label', select.getAttribute('aria-label') || 'Select an answer');
  trigger.setAttribute('aria-haspopup', 'listbox'); trigger.setAttribute('aria-expanded', 'false');
  const value = document.createElement('span'); value.className = 'answer-select-value';
  const arrow = document.createElement('span'); arrow.className = 'answer-select-arrow'; arrow.setAttribute('aria-hidden', 'true'); arrow.textContent = '⌄';
  const menu = document.createElement('span'); menu.className = 'answer-select-menu'; menu.hidden = true;
  menu.id = 'answer-options-' + crypto.randomUUID(); menu.setAttribute('role', 'listbox');
  menu.setAttribute('aria-label', trigger.getAttribute('aria-label')); trigger.setAttribute('aria-controls', menu.id);
  select.className = 'answer-select-native sr-only'; select.tabIndex = -1; select.setAttribute('aria-hidden', 'true');
  select.value = choices.some(choice => String(idOf(choice)) === String(select.value)) ? select.value : '';
  const buttons = [];
  const update = () => {
    const chosen = choices.find(choice => String(idOf(choice)) === select.value);
    value.replaceChildren(chosen ? renderAnswer(chosen) : document.createTextNode('Select…'));
    trigger.setAttribute('aria-label', `${select.getAttribute('aria-label') || 'Answer'}: ${chosen?.value || 'Select an answer'}`);
    buttons.forEach((button, index) => button.setAttribute('aria-selected', String(String(idOf(choices[index])) === select.value)));
  };
  const close = (restore = false) => {
    menu.hidden = true; trigger.setAttribute('aria-expanded', 'false');
    document.removeEventListener('pointerdown', outside);
    if (restore) trigger.focus({ preventScroll: true });
  };
  const outside = event => { if (!wrapper.contains(event.target)) close(); };
  const open = (last = false) => {
    if (select.disabled || trigger.disabled || !buttons.length) return;
    menu.hidden = false; trigger.setAttribute('aria-expanded', 'true');
    void typeset(menu);
    document.addEventListener('pointerdown', outside);
    const selected = choices.findIndex(choice => String(idOf(choice)) === select.value);
    buttons[selected >= 0 ? selected : last ? buttons.length - 1 : 0].focus({ preventScroll: true });
  };
  choices.forEach(choice => {
    const option = document.createElement('button'); option.type = 'button'; option.className = 'answer-select-option';
    option.tabIndex = -1; option.setAttribute('role', 'option'); option.append(renderAnswer(choice));
    option.addEventListener('click', () => {
      if (select.disabled || trigger.disabled) { close(); return; }
      select.value = String(idOf(choice)); update(); close(true);
      select.dispatchEvent(new Event('change', { bubbles: true })); void typeset(value);
    });
    buttons.push(option); menu.append(option);
  });
  trigger.addEventListener('click', () => menu.hidden ? open() : close(true));
  trigger.addEventListener('keydown', event => {
    if (['ArrowDown', 'ArrowUp'].includes(event.key)) { event.preventDefault(); open(event.key === 'ArrowUp'); }
  });
  menu.addEventListener('keydown', event => {
    const index = buttons.indexOf(document.activeElement);
    const next = event.key === 'Home' ? 0 : event.key === 'End' ? buttons.length - 1
      : event.key === 'ArrowDown' ? (index + 1) % buttons.length
      : event.key === 'ArrowUp' ? (index + buttons.length - 1) % buttons.length : null;
    if (next !== null) { event.preventDefault(); buttons[next].focus({ preventScroll: true }); }
    else if (event.key === 'Escape') { event.preventDefault(); close(true); }
    else if (event.key === 'Tab') close();
  });
  wrapper.addEventListener('focusout', event => { if (!wrapper.contains(event.relatedTarget)) close(); });
  select.addEventListener('change', update);
  trigger.append(value, arrow); wrapper.append(select, trigger, menu); update();
  return wrapper;
}

export function questionFeedback(host, status) {
  const value = String(status || '').split('/').at(-1);
  host.dataset.feedback = ['correct', 'incorrect'].includes(value) ? value : '';
}

// One filled result badge per question; individual controls carry field results.
export function feedbackHeading(status, preview = false) {
  const value = String(status || '').split('/').at(-1);
  const heading = document.createElement('div'); heading.className = 'feedback-heading';
  const badge = document.createElement('span'); badge.className = 'feedback-badge';
  badge.setAttribute('role', 'status');
  badge.dataset.grade = ['correct', 'incorrect'].includes(value) ? value : '';
  const label = document.createElement('span'); label.textContent = value === 'correct' ? 'Correct' : value === 'incorrect' ? 'Incorrect' : value === 'completed' ? 'Response saved' : 'Skipped';
  badge.append(label); heading.append(badge);
  if (preview) {
    const note = document.createElement('span'); note.className = 'feedback-preview'; note.textContent = 'Preview only'; heading.append(note);
  }
  return heading;
}
