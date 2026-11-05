import asyncio, sys, json
from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:8899"
OUT = r"C:\Users\DELL\Documents\ks-preventica-2026\assets"


async def main():
    report = {}
    async with async_playwright() as p:
        browser = await p.chromium.launch(args=["--no-sandbox"])
        ctx = await browser.new_context(viewport={"width": 1440, "height": 900},
                                        device_scale_factor=1)
        page = await ctx.new_page()
        errors = []
        page.on("console", lambda m: errors.append(f"{m.type}: {m.text}") if m.type == "error" else None)
        page.on("pageerror", lambda e: errors.append(f"pageerror: {e}"))

        # ---------- ACCUEIL : banniere ----------
        await page.goto(f"{BASE}/index.html", wait_until="networkidle")
        await page.wait_for_timeout(1200)
        card = page.locator(".event-card")
        await card.scroll_into_view_if_needed()
        await page.wait_for_timeout(1200)

        info = await page.evaluate("""() => {
            const c = document.querySelector('.event-card');
            const i = document.querySelector('.event-card__media img');
            const cs = getComputedStyle(c);
            const r = c.getBoundingClientRect();
            const de = document.documentElement;
            return {
              opacity: cs.opacity, transform: cs.transform,
              cardW: Math.round(r.width), cardH: Math.round(r.height),
              href: c.getAttribute('href'), target: c.getAttribute('target'),
              imgComplete: i.complete, imgNatural: i.naturalWidth + 'x' + i.naturalHeight,
              imgBox: (() => { const q = i.getBoundingClientRect(); return Math.round(q.width)+'x'+Math.round(q.height); })(),
              imgRatioNatural: i.naturalWidth ? (i.naturalWidth/i.naturalHeight).toFixed(3) : null,
              imgRatioBox: (() => { const q = i.getBoundingClientRect(); return (q.width/q.height).toFixed(3); })(),
              scrollW: de.scrollWidth, clientW: de.clientWidth,
              btn: document.querySelector('.event-card .btn').textContent.trim(),
              bannerAfterHero: (() => {
                const hero = document.querySelector('.hero');
                const ban = document.querySelector('.event-banner');
                return hero.compareDocumentPosition(ban) & Node.DOCUMENT_POSITION_FOLLOWING ? true : false;
              })()
            };
        }""")
        report["banner"] = info
        await card.screenshot(path=f"{OUT}/check-banner.png")

        # ---------- ACCUEIL : page complete (haut) ----------
        await page.goto(f"{BASE}/index.html", wait_until="networkidle")
        await page.wait_for_timeout(800)
        await page.screenshot(path=f"{OUT}/check-home.png")

        # ---------- INVITATION ----------
        await page.goto(f"{BASE}/invitation-preventica-2026.html", wait_until="networkidle")
        await page.wait_for_timeout(1200)
        inv = await page.evaluate("""() => {
            const i = document.querySelector('.invite-visual img');
            const de = document.documentElement;
            return {
              title: document.title,
              ogImage: document.querySelector('meta[property="og:image"]').content,
              ogUrl: document.querySelector('meta[property="og:url"]').content,
              visualHref: document.querySelector('.invite-visual').getAttribute('href'),
              ctaHref: document.querySelector('.invite-actions .btn-primary').getAttribute('href'),
              waHref: (document.getElementById('waShare')||{}).href ? document.getElementById('waShare').href.slice(0,60) : null,
              imgComplete: i.complete, imgNatural: i.naturalWidth + 'x' + i.naturalHeight,
              logoOk: document.querySelector('.invite-logo').complete,
              scrollW: de.scrollWidth, clientW: de.clientWidth,
              docH: de.scrollHeight
            };
        }""")
        report["invitation"] = inv
        await page.screenshot(path=f"{OUT}/check-invitation.png", full_page=True)

        # ---------- MOBILE ----------
        m = await ctx.new_page()
        await m.set_viewport_size({"width": 390, "height": 844})
        await m.goto(f"{BASE}/index.html#evenement", wait_until="networkidle")
        await m.wait_for_timeout(1500)
        mob = await m.evaluate("""() => {
            const de = document.documentElement;
            const c = document.querySelector('.event-card');
            const r = c.getBoundingClientRect();
            return { hOverflow: de.scrollWidth > de.clientWidth ? (de.scrollWidth-de.clientWidth)+'px' : 'none',
                     cardW: Math.round(r.width), cardH: Math.round(r.height),
                     cols: getComputedStyle(c).gridTemplateColumns };
        }""")
        report["mobile"] = mob
        await m.locator(".event-card").screenshot(path=f"{OUT}/check-banner-mobile.png")

        report["consoleErrors"] = errors
        await browser.close()

    print(json.dumps(report, indent=2, ensure_ascii=False))

asyncio.run(main())
