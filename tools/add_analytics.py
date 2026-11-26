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
document.addEventListener('click',function(e){var t=e.target.closest&&e.target.closest('button');if(!t)return;
 if(t.dataset&&t.dataset.tab){var n=tabName(t);if(n&&n!==seenTab){seenTab=n;ev('tab_view',{tab_name:n});}}
 if(t.dataset&&t.dataset.act==='xlsx')ev('export',{format:'excel'});
 if(t.dataset&&t.dataset.act==='pdf')ev('export',{format:'pdf'});},true);
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
