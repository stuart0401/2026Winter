"""回歸檢查：python3 tests/check.py [index.html]
需要 Playwright（pip install playwright && playwright install chromium）。
檢查項目：各寬度／深淺色下有沒有橫向捲動、JS 錯誤、新視窗連結的朗讀名稱、
按鈕的可存取名稱、12/13 與 12/16 分組切換、打包自訂項目與預設項目的兩段式刪除、預設項目還原；
記帳的加總、新增、刪除還原、匯出 Excel（用 openpyxl 打開驗證）與列印版面。"""
import asyncio, sys, os, tempfile
from playwright.async_api import async_playwright

PATH = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "index.html"))
F = "file://" + PATH
VIEWS = ["home", "trip", "spots", "prep", "pack", "ledger"]
DAYS = ["d1", "d2", "d3", "d4", "d5", "d6", "d7"]
JS_AUDIT = """() => {
  const bad = [];
  for (const a of document.querySelectorAll('a[target=_blank]'))
    if (!(a.getAttribute('aria-label') || '').endsWith('（另開新視窗）')) bad.push('link:' + (a.innerText || a.href).slice(0, 30));
  for (const b of document.querySelectorAll('button'))
    if (b.offsetParent && !((b.getAttribute('aria-label') || b.innerText || '').trim())) bad.push('button-no-name');
  return bad;
}"""


async def main():
    problems = []
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for w in (320, 390, 640, 1440):
            for theme in ("light", "dark"):
                pg = await b.new_page(viewport={"width": w, "height": 900}, color_scheme=theme, reduced_motion="reduce")
                pg.on("pageerror", lambda e, w=w: problems.append(f"{w} JS error: {e}"))
                for v in VIEWS:
                    await pg.goto(F + "#" + v)
                    await pg.wait_for_timeout(150)
                    for d in (DAYS if v == "trip" else [None]):
                        if d:
                            await pg.click(f'[data-day="{d}"]')
                            await pg.wait_for_timeout(80)
                        groups = ["A", "B"] if (d and w < 860 and await pg.locator(".seg").count()) else [None]
                        for g in groups:
                            if g:
                                await pg.click(f'.seg button[data-g="{g}"]')
                                await pg.wait_for_timeout(60)
                            if await pg.evaluate("document.documentElement.scrollWidth > innerWidth"):
                                problems.append(f"{w} {theme} {v} {d or ''} {g or ''} 橫向溢出")
                            for x in await pg.evaluate(JS_AUDIT):
                                problems.append(f"{w} {theme} {v} {d or ''} {x}")
                await pg.close()
        # 打包自訂項目：新增 → 第一次按刪除只進入確認 → 第二次才真的刪
        pg = await b.new_page(viewport={"width": 390, "height": 900})
        await pg.goto(F + "#pack")
        await pg.wait_for_timeout(200)
        await pg.click('[data-packcat="0"]')
        await pg.fill("#add-0", "測試項目")
        await pg.press("#add-0", "Enter")
        await pg.wait_for_timeout(150)
        await pg.click("[data-delcustom]")
        await pg.wait_for_timeout(100)
        if await pg.locator("[data-delcustom]").count() != 1:
            problems.append("刪除第一次就刪掉了（應先確認）")
        await pg.click("[data-delcustom]")
        await pg.wait_for_timeout(150)
        if await pg.locator("[data-delcustom]").count() != 0:
            problems.append("刪除確認後項目仍在")
        # 打包預設項目：勾選 → 兩段式刪除 → 重新整理後仍是刪掉的 → 還原後回來且不帶勾選
        n0 = await pg.locator("#view-pack [data-delpack]").count()
        await pg.click('label[for="pack-0-0"]')
        await pg.click('[data-delpack="0-0"]')
        await pg.wait_for_timeout(100)
        if await pg.locator('[data-delpack="0-0"]').count() != 1:
            problems.append("預設項目第一次按刪除就刪掉了（應先確認）")
        await pg.click('[data-delpack="0-0"]')
        await pg.wait_for_timeout(150)
        await pg.reload()
        await pg.wait_for_timeout(200)
        if await pg.locator('[data-delpack="0-0"]').count() != 0 or await pg.locator("#view-pack [data-delpack]").count() != n0 - 1:
            problems.append("預設項目刪除後重新整理又出現")
        if await pg.evaluate("JSON.parse(localStorage.getItem('twc26:pack')||'{}')['0-0']"):
            problems.append("刪除的預設項目勾選沒清掉")
        await pg.click('[data-restorepack="0"]')
        await pg.wait_for_timeout(150)
        if await pg.locator('[data-delpack="0-0"]').count() != 1 or await pg.locator("[data-restorepack]").count() != 0:
            problems.append("還原預設項目失敗")
        if await pg.is_checked("#pack-0-0"):
            problems.append("還原後的項目不該保留勾選")
        # 記帳：填金額 → 合計；幣別；新增；刪除與還原；重新整理後保留；匯出 Excel；列印版面
        pg = await b.new_page(viewport={"width": 390, "height": 900}, accept_downloads=True)
        pg.on("pageerror", lambda e: problems.append(f"記帳 JS error: {e}"))
        await pg.goto(F + "#ledger")
        await pg.wait_for_timeout(200)
        if not await pg.locator("#led-jpy").inner_text() == "¥4,000":
            problems.append("記帳預設金額（JTTP 4,000 日圓）沒算進日圓合計")
        await pg.fill('.led-in[data-lid="fly:JX314"]', "12,500")
        await pg.fill('.led-in[data-lid="fly:JX315"]', "１２５００")
        await pg.fill('.led-in[data-lid="stay:TOSEI酒店 可可尼築地銀座:13"]', "abc")
        await pg.wait_for_timeout(100)
        if await pg.locator("#led-twd").inner_text() != "NT$25,000":
            problems.append("記帳台幣合計錯誤：" + await pg.locator("#led-twd").inner_text())
        if await pg.get_attribute('.led-in[data-lid="stay:TOSEI酒店 可可尼築地銀座:13"]', "aria-invalid") != "true":
            problems.append("記帳金額輸入錯字沒有提示")
        await pg.fill('.led-in[data-lid="stay:TOSEI酒店 可可尼築地銀座:13"]', "")
        await pg.fill("#led-rate", "0.2")
        await pg.wait_for_timeout(100)
        if "NT$25,800" not in await pg.locator("#led-all").inner_text():
            problems.append("記帳換算合計錯誤：" + await pg.locator("#led-all").inner_text())
        await pg.click('[data-ledcat="1"]')
        await pg.select_option('.led-cur[data-lid="d1:散步、晚餐"]', "TWD")
        await pg.fill('.led-in[data-lid="d1:散步、晚餐"]', "1000")
        await pg.fill("#ledadd-1", "藥妝店")
        await pg.press("#ledadd-1", "Enter")
        await pg.wait_for_timeout(150)
        cid = await pg.evaluate("document.activeElement && document.activeElement.dataset.lid")
        if not (cid or "").startswith("c"):
            problems.append("記帳新增項目後游標沒有移到金額欄")
        else:
            await pg.keyboard.type("3000")
        await pg.click('[data-delled][data-lid="d1:銀座 伊東屋 本店"]')
        await pg.wait_for_timeout(80)
        if await pg.locator('[data-delled][data-lid="d1:銀座 伊東屋 本店"]').count() != 1:
            problems.append("記帳刪除第一次就刪掉了（應先確認）")
        await pg.click('[data-delled][data-lid="d1:銀座 伊東屋 本店"]')
        await pg.wait_for_timeout(120)
        await pg.reload()
        await pg.wait_for_timeout(200)
        if await pg.locator('.led-in[data-lid="d1:銀座 伊東屋 本店"]').count() != 0 or await pg.locator('[data-ledrestore="1"]').count() != 1:
            problems.append("記帳刪除預設項目後重新整理又出現，或沒有還原按鈕")
        if await pg.locator("#led-twd").inner_text() != "NT$26,000" or await pg.locator("#led-jpy").inner_text() != "¥7,000":
            problems.append("記帳重新整理後合計不對：" + await pg.locator("#led-twd").inner_text() + " " + await pg.locator("#led-jpy").inner_text())
        await pg.click('[data-ledrestore="1"]')
        await pg.wait_for_timeout(100)
        if await pg.locator('.led-in[data-lid="d1:銀座 伊東屋 本店"]').count() != 1:
            problems.append("記帳還原預設項目失敗")
        async with pg.expect_download() as dl:
            await pg.click('[data-ledexp="xlsx"]')
        d = await dl.value
        path = os.path.join(tempfile.mkdtemp(), d.suggested_filename)
        await d.save_as(path)
        if not d.suggested_filename.endswith(".xlsx"):
            problems.append("記帳 Excel 檔名不對：" + d.suggested_filename)
        try:
            import openpyxl
            ws = openpyxl.load_workbook(path).active
            vals = {(r[2], r[4]) for r in ws.iter_rows(values_only=True) if r and len(r) > 4}
            if ("JX314 機票", 12500) not in vals or ("藥妝店", 3000) not in vals:
                problems.append("記帳 Excel 內容缺項目或金額")
            if not any(str(r[4]).startswith("=SUMIF") for r in ws.iter_rows(values_only=True) if r and len(r) > 4 and r[4]):
                problems.append("記帳 Excel 缺合計公式")
        except ImportError:
            pass
        except Exception as ex:
            problems.append(f"記帳 Excel 檔打不開：{ex}")
        await pg.evaluate("window.print = () => {}")
        await pg.click('[data-ledexp="pdf"]')
        await pg.emulate_media(media="print")
        if not await pg.evaluate("getComputedStyle(document.getElementById('ledprint')).display !== 'none' && getComputedStyle(document.querySelector('.wrap')).display === 'none'"):
            problems.append("記帳列印版面沒有只顯示記帳表")
        if await pg.locator("#ledprint tbody tr").count() < 50:
            problems.append("記帳列印表格列數太少")
        await pg.emulate_media(media="screen")
        # 記帳跟著行程：行程拿掉或改名、但填過金額的項目 → 出現在「行程已變更的項目」，也算進合計
        await pg.evaluate("""() => { const k='twc26:ledger', st=JSON.parse(localStorage.getItem(k)||'{}');
          st['d5:已經不存在的行程'] = {a:500, c:'JPY', n:'測試：改名前的項目'}; localStorage.setItem(k, JSON.stringify(st)); }""")
        await pg.reload()
        await pg.wait_for_timeout(200)
        if await pg.locator('.led-in[data-lid="d5:已經不存在的行程"]').count() != 1:
            problems.append("記帳：行程改名後，填過金額的舊項目沒有出現在「行程已變更的項目」")
        if await pg.locator("#led-jpy").inner_text() != "¥7,500":
            problems.append("記帳：行程已變更的項目沒有算進合計：" + await pg.locator("#led-jpy").inner_text())
        await pg.close()
        # 記帳跟著行程：在 src 的行程裡多加一個吃飯項目、一班航班和換一家住宿，建置出的記帳頁要自動出現
        src = open(os.path.join(os.path.dirname(__file__), "..", "src", "build_site.py"), encoding="utf-8").read()
        i = src.index('{id:"d5"'); j = src.index("items:[", i) + len("items:[")
        src = src[:j] + '{t:"08:00", title:"測試新增的早餐", note:"", m:"bowl"},' + src[j:]
        src = src.replace('{t:"14:25", title:"JX315 成田第 2 航廈起飛"', '{t:"14:25", title:"JX999 成田第 2 航廈起飛"', 1)
        tmpd = tempfile.mkdtemp()
        tsrc = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src", "_tmp_variant.py")
        open(tsrc, "w", encoding="utf-8").write(src)
        try:
            import subprocess
            vhtml = os.path.join(tmpd, "v.html")
            subprocess.run([sys.executable, tsrc, vhtml], check=True, capture_output=True)
        finally:
            os.remove(tsrc)
        pg = await b.new_page(viewport={"width": 390, "height": 900})
        await pg.goto("file://" + vhtml + "#ledger")
        await pg.wait_for_timeout(200)
        if await pg.locator('.led-in[data-lid="d5:測試新增的早餐"]').count() != 1:
            problems.append("記帳沒有跟著行程新增項目")
        if await pg.locator('.led-in[data-lid="fly:JX999"]').count() != 1 or await pg.locator('.led-in[data-lid="fly:JX315"]').count() != 0:
            problems.append("記帳機票沒有跟著航班變更")
        await pg.close()
        await b.close()
    seen = list(dict.fromkeys(problems))
    print("\n".join(seen) if seen else "全部通過")
    sys.exit(1 if seen else 0)


asyncio.run(main())
