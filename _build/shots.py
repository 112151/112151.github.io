# 兩種寬度截圖＋橫向捲動檢查
import sys, pathlib
sys.stdout.reconfigure(encoding="utf-8")
from playwright.sync_api import sync_playwright
root = pathlib.Path(r"E:/北醫附醫/建名/個人網頁")
url = (root / "index.html").as_uri()
out = pathlib.Path(sys.argv[1])
out.mkdir(parents=True, exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for w in (375, 1440):
        pg = b.new_page(viewport={"width": w, "height": 900})
        pg.goto(url)
        pg.wait_for_timeout(500)
        sw = pg.evaluate("document.documentElement.scrollWidth")
        cw = pg.evaluate("document.documentElement.clientWidth")
        print(w, "scrollWidth", sw, "clientWidth", cw, "橫向溢出" if sw > cw else "OK")
        pg.screenshot(path=str(out / f"w{w}.png"), full_page=True)
        pg.close()
    b.close()
