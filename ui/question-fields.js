import { MathfieldElement } from './vendor/mathlive/mathlive.min.mjs';

MathfieldElement.fontsDirectory = new URL('./vendor/mathlive/fonts', import.meta.url).href;
MathfieldElement.soundsDirectory = null;

// Shared presentation only: response IDs and grading remain with the activity API.
const answerKind = field => String(field.answerType || field.correctAnswer?.type || field.response?.type || '').split('/').at(-1);
export function responsesComplete(fields, responses) {
  return fields.every((field, index) => {
    const response = responses[index];
    if (fieldType(field) !== 'blank') return Boolean(response?.choiceId);
    return typeof response?.value === 'string' && Boolean(response.value.trim())
      && (answerKind(field) !== 'math' || !/\\placeholder\b/.test(response.value));
  });
}
// Some authored radio banks enumerate every combination of Roman statements.
// Present those as independent checkboxes while preserving the original choice
// IDs for grading, saved responses, and historical feedback.
export function statementCheckboxControl(field, prompt, renderLabel, readOnly = false, name = field.id) {
  if (field.presentation !== 'checkbox' || fieldType(field) !== 'radio') return null;
  const roman = ['I', 'II', 'III', 'IV', 'V', 'VI'];
  const labels = [...String(prompt || '').matchAll(/^ {0,3}([IVX]+)\.[ \t]+.+$/gm)].map(match => match[1]);
  if (labels.length < 2 || labels.length > roman.length || labels.some((label, i) => label !== roman[i])) return null;
  const identity = choice => choice.entityId ?? choice.id;
  const combinations = new Map(), choiceLabels = new Map();
  for (const choice of field.choices || []) {
    const value = String(choice.value || '').trim();
    let selected = [];
    if (!/^None(?: of (?:those listed|the above))?$/i.test(value)) {
      const remaining = value.replace(/\bonly\b|\band\b|[,\s]/gi, '');
      selected = value.match(/\b[IVX]+\b/g) || [];
      if (!selected.length || selected.some(label => !labels.includes(label)) || remaining !== selected.join('')) return null;
    }
    const key = labels.filter(label => selected.includes(label)).join('|');
    if (new Set(selected).size !== selected.length || combinations.has(key)) return null;
    combinations.set(key, identity(choice)); choiceLabels.set(String(identity(choice)), selected);
  }
  if (combinations.size !== 2 ** labels.length) return null;
  const response = field.response, responseId = response?.choiceId ?? response?.entityId ?? response?.id;
  const selected = choiceLabels.get(String(responseId)) || [];
  const control = document.createElement('div'); control.className = 'choices statement-checkboxes';
  const encoded = document.createElement('input'); encoded.type = 'hidden'; encoded.className = 'answer-choice-value';
  encoded.name = String(name); encoded.disabled = readOnly;
  const inputs = labels.map(label => {
    const row = document.createElement('label'); row.className = 'choice';
    const input = document.createElement('input'); input.type = 'checkbox'; input.name = `${name}-${label}`;
    input.value = label; input.checked = selected.includes(label); input.disabled = readOnly;
    row.append(input, renderLabel(label)); control.append(row); return input;
  });
  const update = () => { encoded.value = String(combinations.get(inputs.filter(input => input.checked).map(input => input.value).join('|'))); };
  for (const input of inputs) { input.addEventListener('input', update); input.addEventListener('change', update); }
  update(); control.append(encoded);
  return control;
}

export function blankInput(field, label, name, readOnly = false) {
  const kind = answerKind(field);
  const input = document.createElement(kind === 'math' ? 'math-field' : 'input');
  input.className = kind === 'math' ? 'answer-math' : 'answer-input';
  input.setAttribute('name', String(name)); input.setAttribute('aria-label', label);
  if (kind === 'math') {
    input.mathVirtualKeyboardPolicy = 'auto';
    input.setAttribute('placeholder', '');
  } else {
    input.type = 'text'; input.autocomplete = 'off'; input.spellcheck = false;
    input.placeholder = '';
  }
  input.value = field.response?.value ?? '';
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
  source = source.replace(mathBlock, match => {
    const display = match.startsWith('$$') || match.startsWith('\\[');
    const edge = match.startsWith('$') && !display ? 1 : 2;
    const body = match.slice(edge, -edge);
    if (![...body.matchAll(fieldMarker)].some(marker => keys.has(marker[1]))) return match;
    const fragments = body.split(fieldMarker);
    const balanced = fragment => {
      let depth = 0;
      for (const char of fragment.replace(/\\[{}]/g, '')) {
        if (char === '{') depth++; else if (char === '}') depth--;
        if (depth < 0) return false;
      }
      return depth === 0 && (fragment.match(/\\left\b/g)?.length || 0) === (fragment.match(/\\right\b/g)?.length || 0);
    };
    // A field inside a fraction/root argument cannot split into independent TeX
    // runs. Preserve that formula and keep its answer controls beside it.
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
    const blank = inline.querySelector('input');
    if (fieldType(field) === 'blank' && blank) {
      blank.placeholder = '';
      const fit = () => { blank.style.width = `${Math.min(30, Math.max(8, String(blank.value || '').length + 2))}ch`; };
      blank.addEventListener('input', fit); fit();
    }
    // Repeated references show the same answer without creating a second field.
    const sync = () => {
      const input = inline.querySelector('input,select,math-field');
      const selected = field.choices?.find(choice => String(idOf(choice)) === input?.value);
      for (const slot of slots.slice(1)) slot.textContent = selected?.value || input?.value || '…';
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

// A filled result marker keeps grading clear in both themes and review history.
export function feedbackHeading(status, preview = false) {
  const value = String(status || '').split('/').at(-1);
  const heading = document.createElement('div'); heading.className = 'feedback-heading';
  const badge = document.createElement('span'); badge.className = 'feedback-badge';
  if (['correct', 'incorrect'].includes(value)) {
    const icon = document.createElement('span'); icon.className = 'feedback-icon';
    icon.setAttribute('aria-hidden', 'true'); icon.textContent = value === 'correct' ? '✓ ' : '✕ ';
    badge.append(icon);
  }
  const label = document.createElement('span'); label.textContent = value === 'correct' ? 'Correct!' : value === 'incorrect' ? 'Incorrect!' : 'Skipped';
  badge.append(label); heading.append(badge);
  if (preview) {
    const note = document.createElement('span'); note.className = 'feedback-preview'; note.textContent = 'Preview only'; heading.append(note);
  }
  return heading;
}
