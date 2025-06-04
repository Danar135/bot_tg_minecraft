from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from playwright.sync_api import sync_playwright

app = FastAPI()

@app.get("/craft")
def get_craft(name: str = Query(..., description="Название предмета")):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            page.goto("https://minecraft-inside.ru/crafting/")
            page.fill("#search", name)
            page.wait_for_timeout(2000)

            page.click(".item-block")
            page.wait_for_timeout(2000)

            title = page.text_content("div.content h1")
            image = page.get_attribute("div.recipe img", "src")
            mats = [el.inner_text() for el in page.query_selector_all(".recipe-items li")]

            return JSONResponse({
                "title": title,
                "image": image,
                "materials": mats
            })

        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)

        finally:
            browser.close()
