# 閘門：禁用詞、數字追溯、編碼、連結存在
import re, sys, pathlib, html as H
sys.stdout.reconfigure(encoding="utf-8")
root = pathlib.Path(r"E:/北醫附醫/建名/個人網頁")
site = (root / "index.html").read_text(encoding="utf-8")
resume = pathlib.Path(r"E:/北醫附醫/建名/林建名_履歷_1151101.html").read_text(encoding="utf-8")
pub = (root / "_build/resume_public.html").read_text(encoding="utf-8")

def text(h):
    h = re.sub(r"<style.*?</style>", " ", h, flags=re.S)
    h = re.sub(r"data:image/[a-z]+;base64,[A-Za-z0-9+/=]+", " ", h)
    h = re.sub(r"<[^>]+>", " ", h)
    return H.unescape(h)

st, rt, pt = text(site), text(resume), text(pub)
fail = 0

# 1. 禁用詞（機密／敏感對象／個資）
banned = ["校長", "董事", "協助營", "協助總", "協助長", "泌尿", "心臟內科", "GA_MEDMAT", "api_medmat", "10.165", "tmu-cmd",
          "112151", "109041", "\\\\", "D:/", "E:/", "N:/", "0958725805", "69/10/31", "已婚", "hotmail",
          "NSSM", "PBIRS", "kpi2"]
for src_name, t in (("index.html", st), ("resume_public.html", pt)):
    for b in banned:
        n = t.count(b)
        if n:
            fail += 1
            print(f"[禁用詞] {src_name}: {b} x{n}")

# 2. 數字追溯：網頁每個數字（含單位前綴）都要在履歷原文中找得到
nums = sorted(set(re.findall(r"\d+(?:\.\d+)?", st)))
norm_r = rt.replace(",", "")
missing = [n for n in nums if n not in norm_r]
print("網頁數字共", len(nums), "個；履歷找不到：", missing)
if missing:
    fail += 1

# 3. 編碼
for name, t in (("index.html", site), ("resume_public.html", pub)):
    if "\ufffd" in t:
        fail += 1
        print("[U+FFFD]", name)

# 4. 本機相對連結存在
for href in re.findall(r'(?:href|src)="([^"]+)"', site):
    if href.startswith(("http", "mailto:", "data:", "#")):
        continue
    if not (root / href).exists():
        fail += 1
        print("[缺檔]", href)

print("RESULT", "FAIL" if fail else "PASS", fail)
sys.exit(1 if fail else 0)
