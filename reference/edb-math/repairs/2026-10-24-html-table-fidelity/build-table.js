// Embedded verbatim in both browser extractors; checked by regression tests.
function sourceHTMLTable(table, renderLeaf, reportError) {
  const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
  const safeText=value=>{const math=[];let prefix='CATABLETEXT';while(String(value).includes(prefix))prefix+='X';let text=String(value).replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$/g,m=>{math.push(m);return prefix+(math.length-1)+'END'});return esc(text).replace(new RegExp(prefix+'(\\d+)END','g'),(_,i)=>math[Number(i)])};
  const props=node=>Object.fromEntries((node.getAttribute('style')||'').split(';').filter(x=>x.includes(':')).map(x=>{const i=x.indexOf(':');return[x.slice(0,i).trim().toLowerCase(),x.slice(i+1).trim()]}));
  const align=value=>['left','right','center','justify'].includes(value)?value:null;
  const color=raw=>{let v=String(raw||'').trim();if(/^[\da-f]{6}$/i.test(v))v='#'+v;if(/^#[\da-f\s]+$/i.test(v))v=v.replace(/\s/g,'');return /^(?:#[\da-f]{3}(?:[\da-f]{3})?|[a-z]+|rgba?\([\d.,%\s]+\))$/i.test(v)&&!['transparent','inherit','initial','unset','currentcolor'].includes(v.toLowerCase())?v:null};
  const structural=new Set(['table','thead','tbody','tfoot','tr','td','th','caption','colgroup','col']);
  const lastRows=new Set();for(const t of [table,...table.querySelectorAll('table')]){const rows=[...t.querySelectorAll('tr')].filter(r=>r.closest('table')===t);if(rows.length)lastRows.add(rows.at(-1))}
  function attributes(node){
    const tag=node.localName,s=props(node),a=[];const put=(k,v)=>a.push(' '+k+'="'+esc(v)+'"');
    if(/^(?:grid|inline-grid|flex|inline-flex)$/.test(s.display)||['absolute','fixed'].includes(s.position))reportError('Unsupported table layout style');
    if(tag==='table'){
      put('class','source-table');put('data-rules',['all','rows','cols'].includes(node.getAttribute('rules'))?node.getAttribute('rules'):'none');
      const location=align(node.getAttribute('align'))||((s.margin==='auto'||s['margin-left']==='auto'&&s['margin-right']==='auto')?'center':null);if(location)put('data-table-align',location);
      if(!['','0'].includes(node.getAttribute('border')||'0')||s.border&&!/^(?:none|0(?:px)?)(?:\s|$)/.test(s.border))put('data-frame','true');
    }else if(tag==='tr'&&!lastRows.has(node))put('data-next-row','true');
    for(const k of ['rowspan','colspan','span'])if(node.hasAttribute(k)){const v=node.getAttribute(k);if(!/^\d{1,3}$/.test(v)||Number(v)===0&&k!=='rowspan')reportError('Unsupported table span: '+k+'='+v);else put(k,v)}
    if(tag==='th'&&['row','col','rowgroup','colgroup'].includes(node.getAttribute('scope')))put('scope',node.getAttribute('scope'));
    const ancestors=[node];if(['td','th'].includes(tag))for(let p=node.parentElement;p;p=p.parentElement){ancestors.push(p);if(p.localName==='table')break}
    for(const p of ancestors){const value=(p.localName==='table'?null:align(p.getAttribute('align')))||align(props(p)['text-align']);if(value){put('data-cell-align',value);break}}
    const fill=color(node.getAttribute('bgcolor')||s['background-color']||s.background);if(fill)put('data-fill',fill);
    if(['td','th'].includes(tag))for(const side of ['top','right','bottom','left']){const value=s['border-'+side]??s.border;if(value!==undefined)put('data-border-'+side,/^(?:none|0(?:px)?)(?:\s|$)/.test(value)?'none':'solid')}
    return a.join('');
  }
  function walk(node){
    if(node.nodeType===3)return safeText(renderLeaf(node));if(node.nodeType!==1)return '';
    const tag=node.localName;if(node.matches('script,style,mjx-assistive-mml,.studentAnswer,.studentAnswerHeader,.stepHeader,.helpButton,[id^="continueButton-"],[id^="submitButton-"]'))return '';
    if(node.matches('math,mjx-container,svg,input,select,img,.freeResponseTextbox,.selectList,.mjpage,.MathJax')){
      const value=renderLeaf(node),image=/^!\[([^\]]*)\]\(([^)]+)\)$/.exec(value.trim());return image?'<img src="'+esc(image[2])+'" alt="'+esc(image[1])+'">':safeText(value);
    }
    const content=()=>[...node.childNodes].map(walk).join('');
    if(structural.has(tag)){const result='<'+tag+attributes(node)+'>'+content()+(tag==='col'?'':'</'+tag+'>');return tag==='table'?'<div class="source-table-scroll">'+result+'</div>':result}
    if(tag==='br')return '<br>';
    const normalized=({b:'strong',i:'em'})[tag]||tag;
    if(['strong','em','sup','sub','p','ul','ol','li'].includes(normalized)){
      let attrs='';for(const k of ['type','start','reversed','value'])if(node.hasAttribute(k))attrs+=' '+k+'="'+esc(node.getAttribute(k))+'"';
      return '<'+normalized+attrs+'>'+content()+'</'+normalized+'>';
    }
    if(tag==='a'&&node.hasAttribute('href'))return '<a href="'+esc(node.getAttribute('href'))+'">'+content()+'</a>';
    return content();
  }
  return '\n\n'+walk(table)+'\n\n';
}

import {marked} from '/ui/vendor/marked/marked.esm.js';
import {protectMath} from '/ui/math-protection.js';
function cellHTML(value){
 if(value&&typeof value==='object')return value.parts?value.parts.map(cellHTML).join(''):sourceTable(value.table,value.rows);
 const saved=[];let prefix='CAREPAIRMATH';while(String(value).includes(prefix))prefix+='X';
 return marked.parseInline(protectMath(String(value),m=>{saved.push(m);return prefix+(saved.length-1)+'END'})).replace(new RegExp(prefix+'(\\d+)END','g'),(_,i)=>saved[Number(i)]);
}
export function sourceTable(source,rows){
 const table=new DOMParser().parseFromString(source.source_html,'text/html').querySelector('table');
 const own=[...table.querySelectorAll('tr')].filter(r=>r.closest('table')===table).map(r=>[...r.children].filter(c=>['td','th'].includes(c.localName)));
 if(rows.length!==own.length||rows.some((r,i)=>r.length!==own[i].length))throw Error('Source/current cell mismatch');
 const values=[];let prefix='CAREPAIRCELL';while(source.source_html.includes(prefix)||JSON.stringify(rows).includes(prefix))prefix+='X';
 own.forEach((r,i)=>r.forEach((c,j)=>{values.push(cellHTML(rows[i][j]));c.textContent=prefix+(values.length-1)+'END'}));
 if(table.querySelector('caption'))throw Error('Caption requires individual review');
 return sourceHTMLTable(table,n=>{if(n.nodeType!==3)throw Error('Unreviewed source leaf');return n.textContent},m=>{throw Error(m)}).trim().replace(new RegExp(prefix+'(\\d+)END','g'),(_,i)=>values[Number(i)]);
}
