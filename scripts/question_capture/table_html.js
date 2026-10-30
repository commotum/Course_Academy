// Embedded verbatim in both browser extractors; checked by regression tests.
function sourceHTMLTable(table, renderLeaf, reportError) {
  function canonicalMatrixLayout(){
    const rows=t=>[...t.querySelectorAll('tr')].filter(r=>r.closest('table')===t),cells=r=>[...r.children].filter(c=>['td','th'].includes(c.localName));
    const controls='input,select,textarea,.freeResponseTextbox,.matheditor-wrapper-answer,[contenteditable="true"]';
    const empty=c=>!c.textContent.trim()&&!c.querySelector(controls);
    const edge=(c,side)=>{const value=c.style.getPropertyValue('border-'+side)||c.style.border;return !!value&&!/^(?:hidden|none|0(?:px)?)(?:\s|$)/.test(value)};
    function grid(t,label=false){const rr=rows(t),out=[],labels=[];const spanning=rr.length&&cells(rr[0])[0]?.getAttribute('rowspan')===String(rr.length);
      for(const [i,row]of rr.entries()){const cc=cells(row);if(label&&(!spanning||i===0))labels.push(cc.shift());
        if(cc.length<3||!empty(cc[0])||!empty(cc.at(-1))||!edge(cc[0],'left')||!edge(cc.at(-1),'right'))return null;
        const entries=cc.slice(1,-1);if(!entries.every(empty))out.push(entries);
      }return out.length&&new Set(out.map(r=>r.length)).size===1&&!out.some(r=>r.some(empty))?{rows:out,labels}:null;
    }
    const escape=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
    const entry=c=>renderLeaf(c).trim().replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$/g,m=>m.startsWith('$$')||m.startsWith('\\[')||m.startsWith('\\(')?m.slice(2,-2):m.slice(1,-1)).trim();
    const field=value=>/^\{\{(?:answer-field:)?[^{}]+\}\}$/.test(value)?escape(value):'$'+escape(value)+'$';
    const body=(rr,label)=>'<table aria-label="'+label+'"><tbody>\n'+rr.map(r=>'<tr>'+r.map(c=>'<td>'+field(entry(c))+'</td>').join('')+'</tr>').join('\n')+'\n</tbody></table>';
    const matrix=rr=>'<div class="matrix-answer-brackets">\n'+body(rr,'Answer matrix')+'\n</div>';
    const equation=parts=>'\n\n<div class="matrix-answer">\n'+parts.join('\n')+'\n</div>\n\n';
    const label=value=>'<span class="matrix-answer-label">$'+escape(value)+'$</span>';
    const nested=[...table.querySelectorAll('table')].filter(t=>t.parentElement.closest('table')===table),outer=rows(table);
    if(nested.length===3&&outer.length===1){const parsed=nested.map(t=>grid(t));if(parsed.some(p=>!p))return null;
      const outside=cells(outer[0]).filter(c=>!c.querySelector('table')&&!empty(c));
      if(outside.length!==1||outside[0].textContent.trim()!=='=')return null;
      return equation([matrix(parsed[0].rows),matrix(parsed[1].rows),label('='),matrix(parsed[2].rows)]);
    }
    if(nested.length)return null;
    if(outer.length>=2){const first=cells(outer[0]);if(first[0]?.getAttribute('rowspan')===String(outer.length)&&first[0].textContent.trim()==='{'){
      const rr=outer.map((r,i)=>i===0?cells(r).slice(1):cells(r));
      if(rr.every(r=>r.length===3&&r[1].textContent.trim()==='='))return equation(['<div class="matrix-system" role="group" aria-label="System of equations">\n'+body(rr,'Equation rows')+'\n</div>']);
    }}
    const parsed=grid(table,true);if(parsed){const labels=parsed.labels.filter(c=>!empty(c));
      if(labels.length===1&&labels[0].textContent.includes('='))return equation([label(entry(labels[0])),matrix(parsed.rows)]);
    }
    return null;
  }
  const matrixLayout=canonicalMatrixLayout();if(matrixLayout!==null){
    const widgets=table.querySelectorAll('.freeResponseTextbox,.matheditor-wrapper-answer,.selectList').length;
    if([...matrixLayout.matchAll(/\{\{(?:answer-field:)?[^{}]+\}\}/g)].length<widgets)reportError('Matrix layout lost source controls; preserve widget identities before rendering');
    return matrixLayout;
  }
  const esc=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
  const safeText=value=>{const math=[];let prefix='CATABLETEXT';while(String(value).includes(prefix))prefix+='X';let text=String(value).replace(/\\\[[\s\S]*?\\\]|\\\([\s\S]*?\\\)|\$\$[\s\S]*?\$\$|(?<!\\)\$(?!\$)(?:\\[\s\S]|[^$\\])*?(?<!\\)\$/g,m=>{math.push(m);return prefix+(math.length-1)+'END'});return esc(text).replace(/(?<!\\)\$/g,'\\$').replace(new RegExp(prefix+'(\\d+)END','g'),(_,i)=>math[Number(i)])};
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
      if(!['','0'].includes(node.getAttribute('border')||'0')||s.border&&!/^(?:none|hidden|0(?:px)?)(?:\s|$)/.test(s.border))put('data-frame','true');
    }else if(tag==='tr'&&!lastRows.has(node))put('data-next-row','true');
    for(const k of ['rowspan','colspan','span'])if(node.hasAttribute(k)){const v=node.getAttribute(k);if(!/^\d{1,3}$/.test(v)||Number(v)===0&&k!=='rowspan')reportError('Unsupported table span: '+k+'='+v);else put(k,v)}
    if(tag==='th'&&['row','col','rowgroup','colgroup'].includes(node.getAttribute('scope')))put('scope',node.getAttribute('scope'));
    const ancestors=[node];if(['td','th'].includes(tag))for(let p=node.parentElement;p;p=p.parentElement){ancestors.push(p);if(p.localName==='table')break}
    for(const p of ancestors){const value=(p.localName==='table'?null:align(p.getAttribute('align')))||align(props(p)['text-align']);if(value){put('data-cell-align',value);break}}
    const fill=color(node.getAttribute('bgcolor')||s['background-color']||s.background);if(fill)put('data-fill',fill);
    if(/^(?:bold|[6-9]00)$/.test(s['font-weight']||''))put('data-cell-weight','bold');
    if(['top','middle','bottom'].includes(s['vertical-align']||node.getAttribute('valign')))put('data-cell-valign',s['vertical-align']||node.getAttribute('valign'));
    if(['td','th'].includes(tag))for(const side of ['top','right','bottom','left']){const value=s['border-'+side]??s.border;if(value!==undefined)put('data-border-'+side,/\bhidden\b/.test(value)?'hidden':/^(?:none|0(?:px)?)(?:\s|$)/.test(value)?'none':'solid')}
    return a.join('');
  }
  function walk(node){
    if(node.nodeType===3)return safeText(renderLeaf(node));if(node.nodeType!==1)return '';
    const tag=node.localName;if(node.matches('script,style,mjx-assistive-mml,.studentAnswer,.studentAnswerHeader,.stepHeader,.helpButton,[id^="continueButton-"],[id^="submitButton-"]'))return '';
    if(node.matches('math,mjx-container,svg,input,textarea,select,img,[contenteditable="true"],.matheditor-wrapper-answer,.freeResponseTextbox,.selectList,.mjpage,.MathJax')){
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
