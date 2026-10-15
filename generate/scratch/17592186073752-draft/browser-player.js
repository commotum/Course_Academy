import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {romanLists} from './reference/ui/prose-lists.js';
const el=(tag,cls,text)=>{let n=document.createElement(tag);if(cls)n.className=cls;if(text)n.textContent=text;return n};
const short=value=>String(value||'').split('/').at(-1);
import {checkboxControl,freeInput,choiceIndicator,fieldFeedback,blankInput,richSelect,inlinePrompt,mountInlineFields} from './reference/ui/question-fields.js';
import {MathfieldElement} from './reference/ui/vendor/mathlive/mathlive.min.mjs';
MathfieldElement.fontsDirectory=new URL('./reference/ui/vendor/mathlive/fonts',import.meta.url).href;MathfieldElement.soundsDirectory=null;
const typeset=()=>{};
const fieldLabel=key=>key, assetURL=value=>value.startsWith('generate/')?'file:///home/jake/Developer/Course_Academy/'+value:value.startsWith('/')?'file://'+value:'file:///media/jake/SSD/EDB/math/'+value;
const escapeHTML=text=>String(text).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
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

try {
await MathJax.startup.promise;const rows=JSON.parse(document.querySelector('#data').textContent);let reports=[];
for(let {label,record} of rows){let q=record.question,a=document.createElement('article');a.dataset.label=label;let h=document.createElement('h2');h.textContent=label;a.append(h);
const fields=q[':question/answer-fields'].map(f=>({id:f[':answer-field/id'],key:f[':answer-field/key'],type:f[':answer-field/type'],answerType:':answer.type/math',choices:f[':answer-field/choices'].map(c=>({id:c[':answer/id'],type:c[':answer/type'],value:c[':answer/value']}))}));
const inputs=[q[':question/problem'],q[':question/worked-solution']||'No solution captured.'];
let expected=inputs.reduce((n,text)=>n+(text.match(/\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\.|[^$\\])*?(?<!\\)\$/g)||[]).length,0);
let problem=markdown(inputs[0],'prose',fields);a.append(problem);let fieldList=document.createElement('div');a.append(fieldList);mountInlineFields(problem,fieldList,fields,f=>fieldControl(f,false,q[':question/id']));
for(let f of fields){if(f.type.endsWith('/radio'))expected+=f.choices.length;else {let key=document.createElement('div');key.append(document.createTextNode('Review key '+f.key+': '),answerValue(f.choices[0]));a.append(key);expected++;}}a.append(markdown(inputs[1]));
document.querySelector('main').append(a);for(let im of a.querySelectorAll('img'))im.loading='eager';let before=[...MathJax.startup.document.math].length;await MathJax.typesetPromise([a]);let items=[...MathJax.startup.document.math].slice(before);
let errors=[...a.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error,mjx-container [fill="red"],mjx-container [stroke="red"],mjx-container [data-mjx-error]')].map(n=>n.textContent),svgs=[...a.querySelectorAll('mjx-container svg')];
reports.push({label,expected_math:expected,rendered_math:svgs.length,items:items.map(i=>({tex:i.math,tree:i.root.toString()})),errors,literal_dollars:a.innerText.includes('$'),spacing_only_svg:items.filter(i=>/^(?:\\[,;! ]|\s)*$/.test(i.math)).length,empty_svg:svgs.filter((n,i)=>!n.querySelector('path,use,text,rect,line,polygon')&&!/^(?:\\[,;! ]|\s)*$/.test(items[i]?.math||'')).length,horizontal_overflow:a.scrollWidth>a.clientWidth,images:[...a.querySelectorAll('img')].map(im=>({src:im.src,width:im.naturalWidth,height:im.naturalHeight,display_width:im.getBoundingClientRect().width,display_height:im.getBoundingClientRect().height,role:im.closest('.choice')?'choice':'prose',content_width:im.getBoundingClientRect().width-parseFloat(getComputedStyle(im).borderLeftWidth)-parseFloat(getComputedStyle(im).borderRightWidth),content_height:im.getBoundingClientRect().height-parseFloat(getComputedStyle(im).borderTopWidth)-parseFloat(getComputedStyle(im).borderBottomWidth)}))});
}
await new Promise(resolve=>setTimeout(resolve,5000));for(let report of reports){let article=[...document.querySelectorAll('article')].find(a=>a.dataset.label===report.label);report.images=[...article.querySelectorAll('img')].map(im=>({src:im.src,width:im.naturalWidth,height:im.naturalHeight,display_width:im.getBoundingClientRect().width,display_height:im.getBoundingClientRect().height,role:im.closest('.choice')?'choice':'prose',content_width:im.getBoundingClientRect().width-parseFloat(getComputedStyle(im).borderLeftWidth)-parseFloat(getComputedStyle(im).borderRightWidth),content_height:im.getBoundingClientRect().height-parseFloat(getComputedStyle(im).borderTopWidth)-parseFloat(getComputedStyle(im).borderBottomWidth)}));report.horizontal_overflow=article.scrollWidth>article.clientWidth;}let passed=reports.every(r=>r.expected_math===r.rendered_math&&!r.errors.length&&!r.literal_dollars&&!r.empty_svg&&!r.horizontal_overflow&&r.images.every(im=>im.width>0));document.querySelector('#summary').textContent=JSON.stringify({passed,records:reports});document.title=passed?'PASS':'FAIL';
}catch(e){document.querySelector('#summary').textContent=JSON.stringify({passed:false,error:String(e),stack:e.stack});document.title='FAIL';}
