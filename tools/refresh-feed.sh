#!/usr/bin/env bash
# Cosenza X feed refresh (self-contained; mirrors the HMS baked-feed approach).
# 1) Agent: x tool get_users_posts {"id":"2115614759718641664","max_results":10,"exclude":"retweets,replies","post.fields":"created_at,text"} with write_to_file.
# 2) bash tools/refresh-feed.sh /path/to/that_output.txt   -> rebakes feed.json + 4 pages, commits, pushes.
# 3) Deploy: Vercel MCP deploy_to_vercel / create deployment, teamId halamadridstreet,
#    project prj_CG9kdmGpmKmg7Hfi3q0pKhbgfdQC, target production, forceNew, pinned to the new SHA.
set -euo pipefail
RAW="${1:?usage: tools/refresh-feed.sh RAW_X_OUTPUT}"
cd "$(dirname "$0")/.."
python3 tools/build_feed.py "$RAW" .
git add feed.json index.html it/index.html writing/index.html writing/wolves-come-home-at-dawn/index.html
git diff --cached --quiet && { echo "feed unchanged"; exit 0; }
git commit -qm "X feed refresh $(date +%F\ %H:%M)" && git push -q origin HEAD && git rev-parse HEAD
