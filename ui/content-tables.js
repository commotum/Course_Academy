// Source-backed table colors and responsive keyboard access after sanitization.
const color = raw => {let value=String(raw||'').trim();if(/^[\da-f]{6}$/i.test(value))value='#'+value;if(/^#[\da-f\s]+$/i.test(value))value=value.replace(/\s/g,'');return /^(?:#[\da-f]{3}(?:[\da-f]{3})?|[a-z]+|rgba?\([\d.,%\s]+\))$/i.test(value) && CSS.supports('color',value) && !/^(?:inherit|initial|currentcolor|transparent|unset)$/i.test(value)?value:null};
const luminance = c => c.map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((v,x,i)=>v+x*[.2126,.7152,.0722][i],0);
const contrast = (a,b) => {const x=luminance(a),y=luminance(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
const hex = c => '#'+c.map(x=>Math.round(x).toString(16).padStart(2,'0')).join('');
function fillFor(rgb,light,alpha=1) {
 const ink=light?[20,20,20]:[242,242,242],base=light?255:0;
 rgb=rgb.map(x=>alpha*x+(1-alpha)*base);
 for(let k=0;k<=20;k++){let t=k/20,c=rgb.map(x=>x*(1-t)+base*t);if(contrast(c,ink)>=5)return hex(c)}
 return light?'#eee':'#333';
}
const watched = new WeakSet();
export function decorateSourceTables(root) {
 for(const cell of root.querySelectorAll('.source-table [data-fill]')){
  const value=color(cell.dataset.fill);if(!value)continue;
  // A validated source color is resolved to RGB, never copied as arbitrary CSS.
  const canvas=document.createElement('canvas'),context=canvas.getContext('2d');
  if(!context)continue;context.fillStyle=value;const resolved=context.fillStyle;
  const components=resolved.startsWith('#')?[1,3,5].map(i=>parseInt(resolved.slice(i,i+2),16)):resolved.match(/[\d.]+/g)?.map(Number),rgb=components?.slice(0,3);
  if(!rgb||rgb.length!==3)continue;
  cell.style.setProperty('--table-fill-light',fillFor(rgb,true,components[3]??1));cell.style.setProperty('--table-fill-dark',fillFor(rgb,false,components[3]??1));
 }
 for(const wrapper of root.querySelectorAll('.source-table-scroll')){
  const update=()=>{
   if(wrapper.scrollWidth>wrapper.clientWidth+1){wrapper.tabIndex=0;wrapper.setAttribute('role','region');wrapper.setAttribute('aria-label','Scrollable data table')}
   else{wrapper.removeAttribute('tabindex');wrapper.removeAttribute('role');wrapper.removeAttribute('aria-label')}
  };
  update();
  if(!watched.has(wrapper)&&typeof ResizeObserver!=='undefined'){
   watched.add(wrapper);
   const observer=new ResizeObserver(()=>{if(!wrapper.isConnected){observer.disconnect();return}update()});
   observer.observe(wrapper);const table=wrapper.querySelector('table');if(table)observer.observe(table);
  }
 }
}
