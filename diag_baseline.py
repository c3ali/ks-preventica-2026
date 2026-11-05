import asyncio, json
from playwright.async_api import async_playwright
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch(args=["--no-sandbox"])
        for label, url in [("PROD (avant modif)","https://knsconsulting.ma/"),
                           ("LOCAL (avec banniere)","http://127.0.0.1:8899/index.html")]:
            ctx = await b.new_context(viewport={"width":390,"height":844})
            pg = await ctx.new_page()
            try:
                await pg.goto(url, wait_until="networkidle")
                await pg.wait_for_timeout(1500)
                r = await pg.evaluate("""() => {
                    const de=document.documentElement;
                    const over=[];
                    document.querySelectorAll('body *').forEach(el=>{
                      const q=el.getBoundingClientRect();
                      if(q.width>0 && q.right > de.clientWidth+1 && !el.closest('.refs-carousel')){
                        over.push(el.tagName+'.'+(el.className||'').toString().split(' ').filter(Boolean).slice(0,2).join('.')+' r='+Math.round(q.right));
                      }
                    });
                    return {scrollW:de.scrollWidth, clientW:de.clientWidth, over:over.slice(0,6)};
                }""")
                print(f"{label:24} scrollW={r['scrollW']} clientW={r['clientW']} deborde={r['scrollW']-r['clientW']}px  {r['over']}")
            except Exception as e:
                print(f"{label:24} ERREUR {e}")
            await ctx.close()
        await b.close()
asyncio.run(main())
