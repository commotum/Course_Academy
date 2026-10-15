import {marked} from './reference/ui/vendor/marked/marked.esm.js';
import {romanLists} from './reference/ui/prose-lists.js';
import {loadMathInputs,inlinePrompt,mountInlineFields,richSelect,checkboxControl,freeInput,blankInput,choiceIndicator,fieldFeedback,responsesComplete} from './reference/ui/question-fields.js';
let typesetting=Promise.resolve(),mathLoader=null;
function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}
function short(value) { return String(value || '').split('/').at(-1); }
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
function loadMath() {
  if (window.MathJax?.startup?.promise) return MathJax.startup.promise;
  if (!mathLoader) {
    mathLoader = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.src = '/ui/vendor/mathjax/tex-svg.js';
      script.async = true;
      script.onload = () => {
        if (window.MathJax?.startup?.promise) MathJax.startup.promise.then(resolve, reject);
        else reject(new Error('Math rendering could not start. Refresh the page to try again.'));
      };
      script.onerror = () => { script.remove(); reject(new Error('Math rendering could not load. Please try again.')); };
      document.head.append(script);
    }).catch(error => { mathLoader = null; throw error; });
  }
  return mathLoader;
}
function typeset(element) {
  typesetting = typesetting.catch(() => {}).then(async () => {
    if (!element.isConnected || !/\$|\\\(|\\\[|\\begin\{/.test(element.textContent)) return;
    await loadMath();
    if (element.isConnected) await MathJax.typesetPromise([element]);
  }).catch(error => {
    if (element.isConnected) element.append(el('p', 'math-error', error.message));
  });
  return typesetting;
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
function collectResponses(form, fields) {
  return fields.map(field => {
    const set = [...form.querySelectorAll('[data-field-id]')].find(node => node.dataset.fieldId === String(field.id));
    if (['blank', 'free'].includes(short(field.type))) return { fieldId: field.id, value: set.querySelector('input,math-field,textarea').value };
    const input = set.querySelector('.answer-choice-value') || set.querySelector('input:checked, select');
    return { fieldId: field.id, choiceId: input?.value ? Number(input.value) : '' };
  });
}

async function openPreview(query) {
  if (!isDeveloperMode() || modeChanging) return;
  homeController?.abort(); homeController = null; homeRequest = null;
  homeRendered = false; clock.running = false;
  drafts.clear(); clearError(); setBusy(true);
  const revision = settingsRevision;
  try {
    const data = await api('/api/preview?' + new URLSearchParams(query));
    if (revision !== settingsRevision || modeChanging || !isDeveloperMode()) return;
    if (short(data.type) === 'assignment' && data.activityUuid) {
      location.replace('/assignments?assignment=' + encodeURIComponent(data.activityUuid));
      return;
    }
    task = data;
    previewStepIndex = 0;
    lessonView = null;
    history.replaceState(null, '', '/learn?activityId=' + encodeURIComponent(data.activityId));
    await renderPreview();
  } catch (error) { if (revision === settingsRevision) showError(error, () => openPreview(query)); }
  finally { if (revision === settingsRevision) setBusy(false); }
}

try {
 const r=JSON.parse(document.querySelector('#data').textContent),q=r.question;
 const fields=q[':question/answer-fields'].map((f,i)=>({id:20+i,key:f[':answer-field/key'],type:f[':answer-field/type'],choices:f[':answer-field/choices'].map((a,j)=>({id:100+2*i+j,type:a[':answer/type'],value:a[':answer/value']}))}));
 const article=document.querySelector('article'),form=document.createElement('form');article.append(form);
 form.append(el('h1','',r.generation.level+' | '+r.generation.template+' | '+r.generation.profile));
 const prompt=markdown(q[':question/problem'],'prose',fields),list=el('div','field-list');form.append(prompt,list);
 mountInlineFields(prompt,list,fields,f=>fieldControl(f,false,q[':question/id'],q[':question/problem']));
 const inputs=[...form.querySelectorAll('input[type="checkbox"]')];if(inputs.length!==3)throw Error('Expected actual three checkbox controls');
 const subsets=[];
 for(let mask=0;mask<8;mask++){
  inputs.forEach((input,i)=>{if(input.checked!==Boolean(mask&(1<<i)))input.click();});
  const responses=collectResponses(form,fields);
  if(!responsesComplete(fields,responses))throw Error('Unchecked false responses incomplete');
  responses.forEach((response,i)=>{const wanted=mask&(1<<i)?'true':'false';if(response.choiceId!==fields[i].choices.find(a=>a.value===wanted).id)throw Error('UI finite-subset encoding mismatch');});
  subsets.push({mask,responses});
 }
 const key=q[':question/answer-fields'].map(f=>f[':answer-field/choices'].find(a=>a[':answer/id']===f[':answer-field/correct'][1])[':answer/value']==='true');
 inputs.forEach((input,i)=>{if(input.checked!==key[i])input.click();});
 form.append(el('h2','','Answer key (review only)'),markdown(key.map((v,i)=>['I','II','III'][i]+': '+v).join('; ')));
 form.append(el('h2','','Complete fixed worked solution'),markdown(q[':question/worked-solution']));
 await MathJax.startup.promise;await MathJax.typesetPromise([article]);
 const errors=[...article.querySelectorAll('[data-mml-node="merror"],mjx-merror,.MathJax_Error')].map(n=>n.textContent);
 const controls=[...article.querySelectorAll('.answer-indicator')].map(n=>{let s=getComputedStyle(n),b=n.getBoundingClientRect();return {width:b.width,height:b.height,border:s.borderWidth,borderColor:s.borderColor};});
 const result={passed:true,errors,checkbox_controls:inputs.length,radio_controls:article.querySelectorAll('input[type="radio"]').length,subsets,controls,math_expressions:article.querySelectorAll('mjx-container svg').length,whole_record_visible:article.getBoundingClientRect().bottom<innerHeight,horizontal_overflow:document.documentElement.scrollWidth>innerWidth,raw_delimiters:article.textContent.includes('$$'),document_height:document.documentElement.scrollHeight,viewport:[innerWidth,innerHeight],renderer:'actual learning.js fieldControl/collectResponses/markdown + actual question-fields/marked/DOMPurify/MathJax; navigation theme tokens'};
 result.passed=!errors.length&&result.whole_record_visible&&!result.horizontal_overflow&&!result.raw_delimiters&&controls.every(c=>c.width>=20&&c.height>=20&&parseFloat(c.border)>=1&&c.borderColor!=='rgba(0, 0, 0, 0)');
 document.querySelector('#summary').textContent=JSON.stringify(result);document.title=result.passed?'PASS':'FAIL';
}catch(e){document.querySelector('#summary').textContent=JSON.stringify({passed:false,error:String(e),stack:e.stack});}
