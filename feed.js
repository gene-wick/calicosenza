// Live refresh of the @calicosenza xfeed block from /feed.json (baked by tools/build_feed.py).
(function(){var box=document.getElementById('xfallback');if(!box||!window.fetch)return;
function esc(t){return t.replace(/[&<>"]/g,function(c){return{'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];});}
fetch('/feed.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():null;}).then(function(j){
if(!j||!j.posts||!j.posts.length)return;
box.innerHTML=j.posts.map(function(p){return '<article class="xcard"><p class="xmeta">@'+esc(j.handle)+' · '+esc(p.time)+'</p><p>'+esc(p.text).replace(/\n/g,'<br>')+'</p><a href="https://x.com/'+esc(j.handle)+'/status/'+encodeURIComponent(p.id)+'" target="_blank" rel="noopener">View on X →</a></article>';}).join('');
}).catch(function(){});})();
