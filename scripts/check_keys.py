"""Compare site answers with the official key PDFs (ANS + MOD).
Usage: python scripts/check_keys.py <exam> <3-6>   e.g. 113-1 4"""
import fitz, sys, re, json, glob
sys.stdout.reconfigure(encoding="utf-8")
exam, s = sys.argv[1], sys.argv[2]
code = {"3": "11", "4": "22", "5": "33", "6": "44"}[s]
cn = {"3": "三", "4": "四", "5": "五", "6": "六"}[s]
q = {x["id"]: x for x in json.load(open("src/data/questions.json", encoding="utf-8"))}
tr = str.maketrans("ＡＢＣＤ＃", "ABCD#")

def parse(path):
    page = fitz.open(path)[0]
    words = [(w[0], w[1], w[2], w[3], w[4].translate(tr)) for w in page.get_text("words")]
    nums = [w for w in words if re.fullmatch(r"\d\d", w[4]) and 1 <= int(w[4]) <= 80]
    lets = [w for w in words if re.fullmatch(r"[A-D#]+", w[4])]
    ans = {}
    for n in nums:
        cx = (n[0] + n[2]) / 2
        cands = [l for l in lets if abs((l[0] + l[2]) / 2 - cx) < 12 and 0 < l[1] - n[1] < 40]
        if cands:
            ans[int(n[4])] = min(cands, key=lambda l: l[1] - n[1])[4]
    note = re.findall(r"第\d+題[^\n]*", page.get_text())
    return ans, note

key, notes = {}, []
for kind in ("ANS", "MOD"):
    fs = glob.glob(f"C:/Users/yuwei/Desktop/歷屆試題/{exam}/*_{kind}{code}_*.pdf")
    if fs:
        a, n = parse(fs[0]); key.update(a); notes += n
print("parsed", len(key), "notes:", " ".join(notes))
for i in range(1, 81):
    site = q[f"{exam}-醫學({cn})-{i}"]["answer"]
    k = key.get(i, "?")
    if k != site.replace(",", "") and not (k == "#" and site == "ALL"):
        print(f"  Q{i}: site={site} key={k}")
