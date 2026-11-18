"""回歸檢查：python3 tests/check.py [index.html]
需要 Playwright（pip install playwright && playwright install chromium）。
檢查項目：各寬度／深淺色下有沒有橫向捲動、JS 錯誤、新視窗連結的朗讀名稱、
按鈕的可存取名稱、12/13 與 12/16 分組切換、打包自訂項目與預設項目的兩段式刪除、預設項目還原。"""
import asyncio, sys, os
from playwright.async_api import async_playwright

PATH = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "index.html"))
F = "file://" + PATH
VIEWS = ["home", "trip", "spots", "prep", "pack"]
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
        await b.close()
    seen = list(dict.fromkeys(problems))
    print("\n".join(seen) if seen else "全部通過")
    sys.exit(1 if seen else 0)


asyncio.run(main())
