import json, sys
words = json.load(open(sys.argv[1]))["words"]
MAXW, MAXC = 3, 22
WEAK = {"a", "an", "the", "of", "and", "or", "to", "in", "at", "for", "with", "but"}
def ends_sentence(t): return t.rstrip('"\'').endswith((".", "!", "?"))
cues, cur = [], []
for w in words:
    cur.append(w)
    text = " ".join(x["text"] for x in cur)
    if len(cur) == MAXW or len(text) > MAXC or ends_sentence(w["text"]):
        if len(text) > MAXC and len(cur) > 1:
            nxt = [cur.pop()]
        else:
            nxt = []
        if not ends_sentence(cur[-1]["text"]) and len(cur) > 1 and cur[-1]["text"].lower().strip(",") in WEAK:
            nxt.insert(0, cur.pop())
        cues.append(cur); cur = nxt
if cur: cues.append(cur)
def ts(s):
    ms = int(round(s * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); se, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{se:02d},{ms:03d}"
with open(sys.argv[2], "w") as f:
    for i, c in enumerate(cues, 1):
        f.write(f"{i}\n{ts(c[0]['start'])} --> {ts(c[-1]['end'])}\n{' '.join(x['text'] for x in c)}\n\n")
print(len(cues), "cues")
