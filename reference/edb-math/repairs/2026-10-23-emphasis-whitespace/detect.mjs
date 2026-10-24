import {marked} from '../../../../ui/vendor/marked/marked.esm.js';
import {protectMath} from '../../../../ui/math-protection.js';
export function masked(source){return protectMath(source,m=>'M'.repeat(m.length)).replace(/```[\s\S]*?```|~~~[\s\S]*?~~~|`[^`\n]+`/g,m=>'C'.repeat(m.length));}
export function plain(source){return marked.parse(source).replace(/<[^>]*>/g,'').replaceAll('&amp;','&').replaceAll('&lt;','<').replaceAll('&gt;','>').replaceAll('&#39;',"'").replaceAll('&quot;','"');}
export function candidates(source){
 const s=masked(source),visible=plain(s),out=[];
 for(const re of [/(?<![\\*])\*\*(?!\*)((?:(?!\*\*)[\s\S])*?)\*\*(?!\*)/g,/(?<![\\_])__(?!_)([^_]*?)__(?!_)/g,/(?<![\\*])\*(?!\*)((?:\*\*(?!\*)[\s\S]*?\*\*(?!\*)|[^*])*?)\*(?!\*)/g,/(?<![\\_])_(?!_)([^_]*?)_(?!_)/g]){
  for(const m of s.matchAll(re)){
   if(!m[1].trim()||/\n\s*\n/.test(m[1])||!/^\s|\s$/.test(m[1]))continue;
   const marker=m[0].match(/^[*_]+/)[0];
   const literal=visible.includes(m[0])||visible.includes(marker+plain(m[1]).replace(/\n$/,'')+marker);
   out.push({start:m.index,end:m.index+m[0].length,text:source.slice(m.index,m.index+m[0].length),marker,literal,status:marker.includes('_')?'retain-answer-placeholder':literal?'repair':'retain-rendered-formatting'});
  }
 }
 return out;
}
export function replacement(text,marker){const body=text.slice(marker.length,-marker.length),core=body.trim();return body.slice(0,body.length-body.trimStart().length)+marker+core+marker+body.slice(body.trimEnd().length);}
