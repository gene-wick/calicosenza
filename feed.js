// Live refresh of the @calicosenza xfeed block from /feed.json (baked by tools/build_feed.py).
(function(){var box=document.getElementById('xfallback');if(!box||!window.fetch)return;
function esc(t){return t.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
fetch('/feed.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():null;}).then(function(j){
if(!j||!j.posts||!j.posts.length)return;
var it=document.documentElement.lang==='it',G={Mon:'lun',Tue:'mar',Wed:'mer',Thu:'gio',Fri:'ven',Sat:'sab',Sun:'dom'},M={Jan:'gen',Feb:'feb',Mar:'mar',Apr:'apr',May:'mag',Jun:'giu',Jul:'lug',Aug:'ago',Sep:'set',Oct:'ott',Nov:'nov',Dec:'dic'};
function tm(t){if(!it)return t;var a=t.split(' ');if(a.length<3)return t;return (G[a[0]]||a[0])+' '+a[2]+' '+(M[a[1]]||a[1])+' '+a.slice(3).join(' ');}
box.innerHTML=j.posts.map(function(p){return '<article class="xcard"><p class="xmeta">@'+esc(j.handle)+' · '+esc(tm(p.time))+'</p><p>'+esc(p.text).replace(/\n/g,'<br>')+'</p><a href="https://x.com/'+esc(j.handle)+'/status/'+encodeURIComponent(p.id)+'" target="_blank" rel="noopener">'+(it?'Vedi su X':'View on X')+' →</a></article>';}).join('');
}).catch(function(){});})();
