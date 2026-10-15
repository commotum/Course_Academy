import { marked } from '/ui/vendor/marked/marked.esm.js';
import { romanLists } from '/ui/prose-lists.js';
import { inlinePrompt,loadMathInputs,blankInput,choiceIndicator } from '/ui/question-fields.js';
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

window.renderRecord=async record=>{
 await MathJax.startup.promise;await loadMathInputs();MathJax.typesetClear([document.body]);document.body.replaceChildren();
 const q=record.question;const fields=q[':question/answer-fields'].map(f=>({key:f[':answer-field/key'],type:f[':answer-field/type'],id:f[':answer-field/id'],answerType:'answer.type/math'}));
 const prompt=markdown(q[':question/problem'],'prose prompt',fields);document.body.append(prompt);
 let blanks=0,radios=0;
 for(let i=0;i<fields.length;i++){
  const f=fields[i],raw=q[':question/answer-fields'][i];
  if(f.type.endsWith('/blank')){
   const slot=prompt.querySelector('[data-field-key="'+f.key+'"]');if(!slot)throw Error('Missing slot '+f.key);
   const control=blankInput(f,fieldLabel(f.key),f.id);slot.replaceChildren(control);control.value=raw[':answer-field/choices'][0][':answer/value'];
   if(!control.shadowRoot||!control.value)throw Error('MathLive failed '+f.key);blanks++;
  }else{
   for(const a of raw[':answer-field/choices']){
    const row=document.createElement('label');row.className='choice';const input=document.createElement('input');input.type='radio';input.name=f.id;input.value=a[':answer/id'];
    row.append(choiceIndicator(input),markdown('$'+a[':answer/value']+'$','prose'));document.body.append(row);if(a[':answer/id']===raw[':answer-field/correct'][1]){input.click();if(!input.checked)throw Error('Radio interaction failed');}radios++;
   }
  }
 }
 document.body.append(markdown(q[':question/worked-solution'],'prose solution'));
 await MathJax.typesetPromise([document.body]);
 const tables=[],undefinedCommands=[];
 for(const item of MathJax.startup.document.math)item.root.walkTree(node=>{
  if(node.kind==='mtable')tables.push({rows:node.childNodes.length,columns:node.childNodes[0].childNodes.length});
  if(node.kind==='merror'||/Undefined command|\\[a-zA-Z]+/.test(node.getText?.()||''))undefinedCommands.push(node.getText?.()||node.kind);
 });
 const clone=document.body.cloneNode(true);clone.querySelectorAll('mjx-container,math-field').forEach(n=>n.remove());
 return {errors:document.querySelectorAll('[data-mml-node="merror"]').length,redNodes:document.querySelectorAll('[fill="red"],[stroke="red"],[data-mjx-error]').length,undefinedCommands,exposed:/\$|\\begin|\\end|\{\{field-/.test(clone.textContent),tables,blanks,radios,checkedRadios:document.querySelectorAll('input[type=radio]:checked').length,mathLiveValues:[...document.querySelectorAll('math-field')].map(e=>({value:e.value,shadow:Boolean(e.shadowRoot)})),overflow:[...document.querySelectorAll('mjx-container')].some(n=>n.getBoundingClientRect().width>1050)};
};
