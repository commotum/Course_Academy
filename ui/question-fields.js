// Shared presentation only: response IDs and grading remain with the activity API.
const fieldMarker = /\{\{(?:answer-field:)?([^}]+)\}\}/g;
const mathBlock = /\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g;
const fieldType = field => String(field.type || '').split('/').at(-1);
const htmlText = value => String(value).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]);

export function inlinePrompt(value, fields) {
  const keys = new Set(fields.filter(field => ['blank', 'select'].includes(fieldType(field))).map(field => field.key));
  const slot = key => `<span class="field-location" data-field-key="${htmlText(key)}"></span>`;
  // Separate simple equation fragments around an authored field so the control
  // stays outside MathJax's SVG. Ordinary TeX without fields is untouched.
  let source = String(value || '').replace(mathBlock, match => {
    const display = match.startsWith('$$') || match.startsWith('\\[');
    const edge = match.startsWith('$') && !display ? 1 : 2;
    const body = match.slice(edge, -edge);
    if (![...body.matchAll(fieldMarker)].some(marker => keys.has(marker[1]))) return match;
    const parts = body.split(fieldMarker).map((part, index) => index % 2
      ? keys.has(part) ? slot(part) : htmlText(`{{${part}}}`)
      : part.trim() ? `\\(${part.trim()}\\)` : '').join('');
    return display ? `\n\n<div class="question-equation">${parts}</div>\n\n` : parts;
  });
  // Code examples must not acquire interactive controls.
  source = source.replace(/```[\s\S]*?```|`[^`\n]*`|\{\{(?:answer-field:)?([^}]+)\}\}/g,
    (whole, key) => key && keys.has(key) ? slot(key) : whole);
  return source;
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
    // Repeated references show the same answer without creating a second field.
    const sync = () => {
      const input = inline.querySelector('input,select');
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
