import asyncio, json
from playwright.async_api import async_playwright
BASE="http://127.0.0.1:8899"
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--no-sandbox"])
        ctx = await b.new_context(viewport={"width":390,"height":844})
        pg = await ctx.new_page()
        await pg.goto(f"{BASE}/index.html", wait_until="networkidle")
        await pg.wait_for_timeout(1500)
        r = await pg.evaluate("""() => {
            const de = document.documentElement;
            const over=[];
            document.querySelectorAll('body *').forEach(el=>{
              const b=el.getBoundingClientRect();
              if(b.width>0 && b.right > de.clientWidth+1){
                over.push({t:el.tagName+'.'+(el.className||'').toString().split(' ').filter(Boolean).slice(0,2).join('.'), right:Math.round(b.right), w:Math.round(b.width)});
              }
            });
            return {scrollW:de.scrollWidth, clientW:de.clientWidth, over};
        }""")
        print("AVEC banniere:", json.dumps(r, indent=1, ensure_ascii=False))
        await b.close()
asyncio.run(main())
