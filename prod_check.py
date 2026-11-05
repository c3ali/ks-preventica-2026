import asyncio, json
from playwright.async_api import async_playwright

OUT = r"C:\Users\DELL\Documents\ks-preventica-2026\assets"
SITE = "https://knsconsulting.ma"
INVITE = "https://www.knsconsulting.ma/invitation-preventica-2026.html"
REG = "https://preventica.ma/participer?origin=EIX226707"


async def main():
    rep = {}
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--no-sandbox"])
        ctx = await b.new_context(viewport={"width": 1440, "height": 900})
        pg = await ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.on("console", lambda m: errs.append(f"{m.type}: {m.text}") if m.type == "error" else None)

        # ---- ACCUEIL PROD ----
        await pg.goto(SITE, wait_until="networkidle")
        await pg.wait_for_timeout(1200)
        card = pg.locator(".event-card")
        await card.scroll_into_view_if_needed()
        await pg.wait_for_timeout(1500)

        rep["banner"] = await pg.evaluate("""() => {
            const c = document.querySelector('.event-card');
            const i = document.querySelector('.event-card__media img');
            const cs = getComputedStyle(c);
            const r = c.getBoundingClientRect();
            const de = document.documentElement;
            return {
              present: !!c,
              opacity: cs.opacity,
              visible: r.width > 0 && r.height > 0 && cs.opacity !== '0',
              href: c.getAttribute('href'),
              target: c.getAttribute('target'),
              rel: c.getAttribute('rel'),
              imgLoaded: i.complete && i.naturalWidth === 1080,
              imgNatural: i.naturalWidth + 'x' + i.naturalHeight,
              btn: document.querySelector('.event-card .btn').textContent.trim(),
              rightAfterHero: !!document.querySelector('.hero + .event-banner'),
              hOverflow: de.scrollWidth - de.clientWidth
            };
        }""")
        await card.screenshot(path=f"{OUT}/prod-banner.png")

        # ---- TEST DE CLIC REEL : ouvre l'onglet d'inscription ----
        async with ctx.expect_page() as newpage_info:
            await card.click(position={"x": 40, "y": 40})
        popup = await newpage_info.value
        await popup.wait_for_load_state("domcontentloaded")
        rep["click"] = {"url": popup.url, "expected": REG, "match": popup.url.startswith("https://preventica.ma/participer")}
        await popup.close()

        # ---- PAGE INVITATION PROD ----
        await pg.goto(INVITE, wait_until="networkidle")
        await pg.wait_for_timeout(1200)
        rep["invitation"] = await pg.evaluate("""() => {
            const i = document.querySelector('.invite-visual img');
            return {
              ogImage: document.querySelector('meta[property="og:image"]').content,
              ogTitle: document.querySelector('meta[property="og:title"]').content,
              ogUrl: document.querySelector('meta[property="og:url"]').content,
              visualHref: document.querySelector('.invite-visual').getAttribute('href'),
              ctaHref: document.querySelector('.invite-actions .btn-primary').getAttribute('href'),
              waOk: document.getElementById('waShare').href.startsWith('https://wa.me/?text='),
              imgOk: i.complete && i.naturalWidth === 1080,
              logoOk: document.querySelector('.invite-logo').complete
            };
        }""")
        await pg.screenshot(path=f"{OUT}/prod-invitation.png", full_page=True)

        # ---- MOBILE PROD ----
        m = await ctx.new_page()
        await m.set_viewport_size({"width": 390, "height": 844})
        await m.goto(SITE, wait_until="networkidle")
        await m.wait_for_timeout(1200)
        await m.locator(".event-card").scroll_into_view_if_needed()
        await m.wait_for_timeout(1200)
        rep["mobile"] = await m.evaluate("""() => {
            const c = document.querySelector('.event-card');
            const i = document.querySelector('.event-card__media img');
            const r = c.getBoundingClientRect();
            const de = document.documentElement;
            return { visible: getComputedStyle(c).opacity === '1', cardW: Math.round(r.width),
                     imgLoaded: i.complete && i.naturalWidth === 1080,
                     hOverflow: de.scrollWidth - de.clientWidth };
        }""")
        await m.locator(".event-card").screenshot(path=f"{OUT}/prod-banner-mobile.png")

        rep["consoleErrors"] = errs
        await b.close()

    print(json.dumps(rep, indent=2, ensure_ascii=False))

asyncio.run(main())
