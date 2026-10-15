import { marked } from '/ui/vendor/marked/marked.esm.js';
import { romanLists } from '/ui/prose-lists.js';
import { loadMathInputs,inlinePrompt,mountInlineFields,richSelect,checkboxControl,freeInput,blankInput,choiceIndicator,fieldFeedback } from '/ui/question-fields.js';
const short=v=>String(v||'').split('/').at(-1);const typeset=n=>MathJax.typesetPromise([n]);
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function fieldLabel(key) {
  if (!key || key === 'selection') return 'Answer';
  const numbered = /^field-(\d+)$/.exec(key);
  return numbered ? `Answer ${numbered[1]}` : `Answer: ${key}`;
}

function escapeHTML(text) { return String(text).replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]); }
function assetURL(value) {
  if (!value) return '';
  if (String(value).startsWith('/api/asset?')) return value;
  return '/api/asset?path=' + encodeURIComponent(String(value).replace(/^file:\/\//, ''));
}
function markdown(value, className = 'prose', fields = []) {
  const container = el('div', className);
  // Protect TeX from Markdown's underscore, backslash, and table processing.
  const math = [];
  const prefix = 'CAMATH' + crypto.randomUUID().replaceAll('-', '') + 'TOKEN';
  const fieldKeys = new Set(fields.map(field => field.key));
  const placeholder = /\{\{(?:answer-field:)?([^}]+)\}\}/g;
  let source = inlinePrompt(value, fields).replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g, match => {
    math.push(match.replace(placeholder, (whole, key) => fieldKeys.has(key)
      ? `\\underbrace{\\qquad}_{\\text{answer ${fields.findIndex(field => field.key === key) + 1}}}` : whole));
    return prefix + (math.length - 1) + 'END';
  });
  source = source.replace(placeholder, (whole, key) => fieldKeys.has(key) ? `<span class="field-location">${escapeHTML(fieldLabel(key))}</span>` : whole);
  let html = marked.parse(romanLists(source), { async: false, gfm: true, breaks: false });
  html = html.replace(new RegExp(prefix + '(\\d+)END', 'g'), (_, i) => escapeHTML(math[Number(i)]));
  const fragment = DOMPurify.sanitize(html, {
    RETURN_DOM_FRAGMENT: true,
    USE_PROFILES: { html: true },
    FORBID_TAGS: ['style', 'form', 'input', 'button', 'textarea', 'select', 'iframe', 'object', 'embed'],
    FORBID_ATTR: ['style', 'srcset'],
  });
  for (const image of fragment.querySelectorAll('img')) {
    image.src = assetURL(image.getAttribute('src'));
    image.referrerPolicy = 'no-referrer';
    image.loading = 'lazy';
    image.addEventListener('error', () => {
      const note = el('span', 'math-error', `Image unavailable${image.alt ? ': ' + image.alt : '.'}`);
      image.replaceWith(note);
    }, { once: true });
  }
  for (const link of fragment.querySelectorAll('a')) {
    const href = link.getAttribute('href') || '';
    if (!/^https?:\/\//i.test(href) && !href.startsWith('#')) link.removeAttribute('href');
    else { link.target = '_blank'; link.rel = 'noopener noreferrer'; }
  }
  container.append(fragment);
  return container;
}
function answerValue(answer) {
  if (!answer) return el('span');
  const type = short(answer.type);
  if (type === 'image') {
    const holder = el('div', 'prose');
    const img = el('img'); img.src = assetURL(answer.value); img.alt = 'Answer option';
    holder.append(img); return holder;
  }
  const value = String(answer.value ?? '');
  return markdown(type === 'math' && !/^\s*(\$|\\\[|\\\()/.test(value) ? '$' + value + '$' : value);
}

function choiceOrder(choices, seed) {
  const hash = value => { let n = 2166136261; for (const c of value) n = Math.imul(n ^ c.charCodeAt(0), 16777619); return n >>> 0; };
  return [...choices].sort((a, b) => hash(`${seed}:${a.id}`) - hash(`${seed}:${b.id}`));
}
function fieldControl(field, readOnly, itemId, promptText = '', status = '') {
  const set = el('fieldset', 'answer-field');
  set.dataset.fieldId = String(field.id);
  set.dataset.type = short(field.type);
  const label = field.key === 'selection' ? 'Choose an answer' : fieldLabel(field.key);
  set.append(el('legend', field.key === 'selection' || short(field.type) === 'checkbox' ? 'sr-only' : '', label));
  const type = short(field.type), response = field.response;
  const choices = choiceOrder(field.choices || [], `${itemId}:${field.id}`);
  const responseId = response?.choiceId ?? response?.id;
  const checklist = checkboxControl(field, label => answerValue({ type: 'text', value: label }), readOnly);
  if (checklist) {
    set.append(checklist);
  } else if (type === 'free') {
    set.append(freeInput(field, label, field.id, value => markdown(value), typeset, readOnly));
  } else if (type === 'blank') {
    set.append(blankInput(field, label, field.id, readOnly));
  } else if (type === 'radio') {
    const list = el('div', 'choices');
    for (const choice of choices) {
      const option = el('label', 'choice');
      const input = el('input'); input.type = 'radio'; input.name = String(field.id); input.value = String(choice.id);
      input.checked = String(responseId) === String(choice.id); input.disabled = readOnly;
      option.append(choiceIndicator(input), answerValue(choice)); list.append(option);
    }
    set.append(list);
  } else if (type === 'select') {
    const select = el('select', 'answer-select'); select.name = String(field.id); select.disabled = readOnly;
    select.setAttribute('aria-label', label);
    const placeholder = el('option', '', 'Select an answer…'); placeholder.value = ''; select.append(placeholder);
    choices.forEach(choice => {
      const option = el('option', '', choice.value);
      option.value = String(choice.id); option.selected = String(responseId) === String(choice.id); select.append(option);
    });
    select.value = responseId == null ? '' : String(responseId);
    set.append(richSelect(select, choices, answerValue, answer => answer.id, typeset));
  }
  for (const input of set.querySelectorAll('input,select,math-field,textarea,.answer-select-trigger')) {
    input.dataset.answerInput = 'true'; input.dataset.readOnly = String(readOnly);
  }
  fieldFeedback(set, field, status);
  return set;
}

window.renderRecord=async record=>{
 await MathJax.startup.promise;await loadMathInputs();MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],answerType:':answer.type/math',key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map(a=>({id:a[':answer/id'],type:a[':answer/type'],value:a[':answer/value']}))}));
 const main=el('main','lesson-main'),card=el('section','lesson-content'),prompt=markdown(q[':question/problem'],'prose prompt',fields),list=el('div','answer-fields');card.append(prompt,list);main.append(card);document.body.append(main);
 mountInlineFields(prompt,list,fields,f=>fieldControl(f,false,q[':question/id'],q[':question/problem']));
 if(q[':question/worked-solution'])card.append(markdown(q[':question/worked-solution'],'prose worked-solution solution'));
 else card.append(el('p','missing','Raw source has no worked solution or correct designation.'));
 await MathJax.typesetPromise([document.body]);
 if(fields[0].type.endsWith('/blank')){await customElements.whenDefined('math-field');const input=document.querySelector('math-field');input.value='7';input.dispatchEvent(new Event('input',{bubbles:true}));}
 else {for(const input of document.querySelectorAll('input[type=radio]'))input.click();}
 const matricesPrompt=document.querySelectorAll('.prompt [data-mml-node="mtable"]').length;
 const matricesSolution=document.querySelectorAll('.solution [data-mml-node="mtable"]').length;
 const tables=[...document.querySelectorAll('.solution [data-mml-node="mtable"]')];
 const alignedRows=tables[0]?[...tables[0].children].filter(n=>n.dataset.mmlNode==='mtr').length:0;
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container,math-field').forEach(n=>n.remove());
 const controls=[...document.querySelectorAll('input[type=radio],math-field')];
 return {mathJaxVersion:MathJax.version,browserUserAgent:navigator.userAgent,errors:document.querySelectorAll('[data-mml-node="merror"]').length,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),controlCount:controls.length,controlTypes:controls.map(n=>n.tagName),controlVisibility:controls.every(n=>{const r=n.getBoundingClientRect();const c=getComputedStyle(n);return r.width>0&&r.height>0&&c.display!=='none'&&c.visibility!=='hidden'}),blankValue:document.querySelector('math-field')?.value,matricesPrompt,matricesSolution,alignedRows,overflow:[...document.querySelectorAll('mjx-container[display="true"]')].some(n=>n.scrollWidth>n.clientWidth+2),solutionPresent:Boolean(q[':question/worked-solution']),documentHeight:document.documentElement.scrollHeight};
};
