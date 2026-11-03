#!/usr/bin/env python3
"""Bake the latest @calicosenza X posts into /feed.json and the static fallback
cards on every page that carries the xfeed block (between XFEED markers).
Usage: tools/build_feed.py RAW_X_TOOL_OUTPUT [SITE_DIR]
RAW = output of the `x` tool get_users_posts for id 2115614759718641664
(max_results 10, exclude retweets,replies, post.fields created_at,text)."""
import json, re, sys, html, os
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
HANDLE = "calicosenza"
raw = open(sys.argv[1]).read()
site = sys.argv[2] if len(sys.argv) > 2 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m = re.search(r'\{"data":.*\}\}', raw, re.S) or re.search(r'\{"data":.*\}', raw, re.S)
data = [p for p in json.loads(m.group(0))["data"] if not p["text"].startswith("RT @")][:4]
if not data:
    sys.exit("no posts parsed; refusing to blank the feed")
pt = ZoneInfo("America/Los_Angeles")
posts = []
for p in data:
    dt = datetime.fromisoformat(p["created_at"].replace("Z", "+00:00")).astimezone(pt)
    posts.append({"id": p["id"], "text": p["text"], "created_at": p["created_at"],
                  "time": dt.strftime("%a %b %-d · %-I:%M %p PT"),
                  "url": f"https://x.com/{HANDLE}/status/{p['id']}"})
json.dump({"handle": HANDLE, "updated": datetime.now(timezone.utc).isoformat(), "posts": posts},
          open(os.path.join(site, "feed.json"), "w"), ensure_ascii=False, indent=1)
def card(p):
    return (f'<article class="xcard"><p class="xmeta">@{HANDLE} · {p["time"]}</p><p>{html.escape(p["text"]).replace(chr(10), "<br>")}</p>'
            f'<a href="{p["url"]}" target="_blank" rel="noopener">View on X →</a></article>')
cards = "".join(card(p) for p in posts)
pages = ["index.html", "it/index.html", "writing/index.html", "writing/wolves-come-home-at-dawn/index.html"]
for rel in pages:
    f = os.path.join(site, rel); s = open(f).read()
    if "<!-- XFEED:START -->" not in s:  # first run: wrap the existing fallback div
        s = re.sub(r'(<div class="xfallback" id="xfallback">)(.*?)(</div>)', lambda mm: mm.group(1) + "<!-- XFEED:START -->" + mm.group(2) + "<!-- XFEED:END -->" + mm.group(3), s, count=1, flags=re.S)
    s = re.sub(r'<!-- XFEED:START -->.*?<!-- XFEED:END -->', lambda mm: "<!-- XFEED:START -->" + cards + "<!-- XFEED:END -->", s, flags=re.S)
    if '/feed.js' not in s:
        s = s.replace('<main id="main">', '<script defer src="/feed.js"></script>\n<main id="main">', 1)
    open(f, "w").write(s)
print(f"{len(posts)} posts baked into {len(pages)} pages; newest {posts[0]['created_at']}")
