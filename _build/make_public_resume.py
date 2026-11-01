# 由現行履歷 HTML 產生公開版複本（不動原檔）：
# 去掉生日、婚姻、電話，Email 改為個人 gmail。
import re, sys, pathlib
sys.stdout.reconfigure(encoding="utf-8")
src = pathlib.Path(r"E:/北醫附醫/建名/林建名_履歷_1151101.html")
dst = pathlib.Path(r"E:/北醫附醫/建名/個人網頁/_build/resume_public.html")
s = src.read_text(encoding="utf-8")
old = '<div class="contact"><span>69/10/31</span><span>已婚</span><span>0958725805</span><span>babym_lin@hotmail.com</span></div>'
assert s.count(old) == 1, "contact line not found exactly once"
new = '<div class="contact"><span>babymlin.tw@gmail.com</span><span>github.com/babymlin</span></div>'
s = s.replace(old, new)
for bad in ("69/10/31", "已婚", "0958725805", "hotmail"):
    assert bad not in s, bad
dst.write_text(s, encoding="utf-8")
print("written", dst, len(s))
