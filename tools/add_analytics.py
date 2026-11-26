#!/usr/bin/env python3
"""Вставляє тег Google Analytics у автономний HTML дашборда Фарм-монітор.
Використання: python3 tools/add_analytics.py <вхідний.html> <index.html>
Тег додається один раз (повторний запуск нічого не дублює)."""
import sys,re
GTM='GTM-5FPCDBH8'
SNIP='''<!-- fm-analytics --><script async src="https://www.googletagmanager.com/gtm.js?id=%s"></script>
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag('js',new Date());
(function(){var seenTab='',seenBrand='';function ev(n,p){try{gtag('event',n,p||{});}catch(e){}}
function tabName(b){return (b.textContent||'').trim();}
document.addEventListener('click',function(e){if(!e.target.closest)return;var cs=e.target.closest('.fx-case');if(cs&&!e.target.closest('a')){var ttl=cs.querySelector('.fx-case-title')||cs;ev('case_open',{value:ttl.textContent.trim().slice(0,60)});}
 var t=e.target.closest('button');if(!t)return;
 if(t.dataset&&t.dataset.tab){var n=tabName(t);if(n&&n!==seenTab){seenTab=n;ev('tab_view',{tab_name:n});}}
 if(t.dataset&&t.dataset.act==='xlsx')ev('export',{format:'excel'});
 if(t.dataset&&t.dataset.act==='pdf')ev('export',{format:'pdf'});
 var seg=t.closest('.fx-seg');if(seg&&!(t.dataset&&t.dataset.tab)){var sec=t.closest('.fx-sec,.fx-hero,.fx-filters,.fx-page');var hd=sec&&sec.querySelector('h1,h2');
  ev('toggle',{control:seg.id||seg.dataset.p||'seg',value:tabName(t).slice(0,40),section:hd?hd.textContent.trim().slice(0,60):'фільтри'});}
 var chip=t.closest('.fx-chip');if(chip)ev('comp_change',{action:'remove',value:chip.textContent.replace('✕','').trim().slice(0,40)});
 if(t.dataset&&t.dataset.more!==undefined)ev('expand',{value:tabName(t).slice(0,60)});
},true);
document.addEventListener('change',function(e){var t=e.target;if(!t||t.tagName!=='SELECT')return;var opt=t.options[t.selectedIndex];
 ev('filter',{control:t.id||t.dataset.p||t.getAttribute('aria-label')||'select',value:(opt?opt.textContent:t.value).trim().slice(0,80)});},true);
function brandCheck(){var c=document.querySelector('.fx-crumbs');if(!c)return;var last=c.querySelector('span.fx-crumb.on');var b=last?last.textContent.trim():'';
 if(b&&b!==seenBrand){seenBrand=b;ev('brand_view',{brand_name:b});}}
var mo=new MutationObserver(function(){clearTimeout(mo._t);mo._t=setTimeout(brandCheck,400);});
function start(){var c=document.querySelector('.fx-crumbs');if(c)mo.observe(c,{childList:true,subtree:true,characterData:true});else setTimeout(start,1000);}
if(document.readyState==='loading')document.addEventListener('DOMContentLoaded',start);else start();})();</script>
'''%GTM
src,dst=sys.argv[1],sys.argv[2]
s=open(src,encoding='utf-8').read()
if 'fm-analytics' in s: out=s
else:
    m=re.search(r'<head[^>]*>',s)
    if not m: sys.exit('не знайдено <head>')
    out=s[:m.end()]+SNIP+s[m.end():]
open(dst,'w',encoding='utf-8').write(out)
print('ok',len(out)//1024,'KB')
