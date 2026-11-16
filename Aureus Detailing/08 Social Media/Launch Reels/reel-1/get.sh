#!/bin/zsh
# usage: get.sh <job_id> <out_file>  : waits for a Higgsfield job and downloads its result
for i in $(seq 1 60); do r=$(higgsfield generate get $1 --json 2>/dev/null); s=$(echo "$r" | python3 -I -c "import sys,json;d=json.load(sys.stdin);d=d[0] if isinstance(d,list) else d;print(d.get('status',''))" 2>/dev/null); case "$s" in completed|failed|nsfw|canceled) break;; esac; sleep 8; done
echo "$2 $s"; u=$(echo "$r" | grep -oE 'https://[^"]+hf_[^"]+\.(png|jpg|jpeg|webp|mp4)' | head -1); [ -n "$u" ] && curl -s -o "$2" "$u"
