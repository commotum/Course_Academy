// Prototype contract: source structure + current cell content, no source CSS.
import {marked} from '/ui/vendor/marked/marked.esm.js';
import {protectMath} from '/ui/math-protection.js';
const escape = v => String(v).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'})[c]);
const props = node => Object.fromEntries(String(node?.style||'').split(';').filter(x=>x.includes(':')).map(x=>{const i=x.indexOf(':');return [x.slice(0,i).trim().toLowerCase(),x.slice(i+1).trim()]}));
const color = raw => {let value=String(raw||'').trim();if(/^[\da-f]{6}$/i.test(value))value='#'+value;if(/^#[\da-f\s]+$/i.test(value))value=value.replace(/\s/g,'');return /^(?:#[\da-f]{3}(?:[\da-f]{3})?|[a-z]+|rgba?\([\d.,%\s]+\))$/i.test(value) && CSS.supports('color',value) && !/^(?:inherit|initial|currentcolor|transparent|unset)$/i.test(value)?value:null};
const align = value => ['left','center','right','justify'].includes(value) ? value : null;
function cellHTML(text) {
 const saved=[],prefix='CATABLEMATH'+crypto.randomUUID().replaceAll('-','');
 const protectedText=protectMath(String(text),m=>{saved.push(m);return prefix+(saved.length-1)+'END'});
 return marked.parseInline(protectedText).replace(new RegExp(prefix+'(\\d+)END','g'),(_,i)=>saved[Number(i)]);
}
export function sourceTable(source, currentRows=source.rows) {
 if(currentRows.length!==source.cells.length || currentRows.some((row,i)=>row.length!==source.cells[i].length))throw Error('Source/current table cells require review');
 const table=source.table_attrs||{},style=props(table),location=align(table.align)||((style.margin==='auto'||style['margin-left']==='auto'&&style['margin-right']==='auto')?'center':null);
 const rules=['all','rows','cols'].includes(table.rules)?table.rules:'none';
 const frame=String(table.border||'0')!=='0'||style.border&&!/^(?:none|0(?:px)?)(?:\s|$)/.test(style.border);
 let result='<div class="source-table-scroll"><table class="source-table" data-rules="'+rules+'"'+(location?' data-table-align="'+location+'"':'')+(frame?' data-frame="true"':'')+'>';
 if(source.caption)result+='<caption>'+cellHTML(source.caption)+'</caption>';
 let section=null;
 source.cells.forEach((row,i)=>{const next=['thead','tfoot','tbody'].includes(source.row_sections?.[i])?source.row_sections[i]:'tbody';if(next!==section){if(section)result+='</'+section+'>';result+='<'+next+'>';section=next}result+='<tr'+(i<source.cells.length-1?' data-next-row="true"':'')+'>';row.forEach((cell,j)=>{
  const a=cell.attrs||{},s=props(a),tag=cell.tag==='th'?'th':'td';let attrs='';
  for(const name of ['rowspan','colspan'])if(a[name]&&/^[1-9]\d{0,2}$/.test(a[name]))attrs+=' '+name+'="'+a[name]+'"';
  if(tag==='th'&&['row','col','rowgroup','colgroup'].includes(a.scope))attrs+=' scope="'+a.scope+'"';
  const alignment=align(a.align)||align(s['text-align'])||align(style['text-align']);if(alignment)attrs+=' data-cell-align="'+alignment+'"';
  const fill=color(a.bgcolor||s['background-color']||s.background);if(fill)attrs+=' data-fill="'+escape(fill)+'"';
  const value=currentRows[i][j],content=value&&typeof value==='object'&&value.table?sourceTable(value.table,value.rows):cellHTML(value);
  result+='<'+tag+attrs+'>'+content+'</'+tag+'>';
 });result+='</tr>'});return result+(section?'</'+section+'>':'')+'</table></div>';
}
const luminance = c => c.map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((v,x,i)=>v+x*[.2126,.7152,.0722][i],0);
const contrast = (a,b) => {const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
const hex = c => '#'+c.map(x=>Math.round(x).toString(16).padStart(2,'0')).join('');
function fillFor(rgb,light,alpha=1) {
 const ink=light?[20,20,20]:[242,242,242],base=light?255:0;
 rgb=rgb.map(x=>alpha*x+(1-alpha)*base);
 for(let k=0;k<=20;k++){let t=k/20,c=rgb.map(x=>x*(1-t)+base*t);if(contrast(c,ink)>=5)return hex(c)}
 return light?'#eee':'#333';
}
export function decorateSourceTables(root) {
 for(const cell of root.querySelectorAll('.source-table [data-fill]')){
  const value=color(cell.dataset.fill);if(!value)continue;
  // A validated source color is resolved to RGB, never copied as arbitrary CSS.
  const probe=document.createElement('span');probe.style.color=value;cell.append(probe);const components=getComputedStyle(probe).color.match(/[\d.]+/g)?.map(Number),rgb=components?.slice(0,3);probe.remove();
  if(!rgb||rgb.length!==3)continue;
  cell.style.setProperty('--table-fill-light',fillFor(rgb,true,components[3]??1));cell.style.setProperty('--table-fill-dark',fillFor(rgb,false,components[3]??1));
 }
 for(const wrapper of root.querySelectorAll('.source-table-scroll')){
  if(wrapper.scrollWidth>wrapper.clientWidth+1){wrapper.tabIndex=0;wrapper.setAttribute('role','region');wrapper.setAttribute('aria-label','Scrollable data table')}
  else{wrapper.removeAttribute('tabindex');wrapper.removeAttribute('role');wrapper.removeAttribute('aria-label')}
 }
}
