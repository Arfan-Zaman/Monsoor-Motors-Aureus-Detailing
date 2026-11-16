"""fetch.py name=jobid ... : waits for Higgsfield jobs and downloads each result into this folder (stills/, clips/, audio/)."""
import json, os, re, subprocess, sys, time, urllib.request
HERE = os.path.dirname(os.path.abspath(__file__))
pending = dict(a.split("=") for a in sys.argv[1:]); t0 = time.time()
while pending and time.time() - t0 < 540:
    for name, jid in list(pending.items()):
        raw = subprocess.run(["higgsfield", "generate", "get", jid, "--json"], capture_output=True, text=True).stdout
        st = re.search(r'"status":\s*"(\w+)"', raw); st = st.group(1) if st else "?"
        if st in ("completed", "failed", "nsfw", "canceled"):
            del pending[name]
            urls = re.findall(r'https://[^"\s]+?%s[^"\s]*?\.(?:png|jpg|jpeg|webp|mp4|wav|mp3)' % jid, raw)
            if st != "completed" or not urls: print(name, st, "no file"); continue
            u = max(urls, key=len) if False else [x for x in urls if "min" not in x.rsplit("/",1)[-1]][0]
            ext = u.rsplit(".", 1)[1]; sub = "stills" if ext in ("png", "jpg", "jpeg", "webp") else "clips" if ext == "mp4" else "audio"
            out = os.path.join(HERE, sub, f"{name}.{ext}"); urllib.request.urlretrieve(u, out); print(name, st, os.path.getsize(out))
    if pending: time.sleep(8)
for n in pending: print(n, "still running")
