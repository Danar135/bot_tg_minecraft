from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

app = FastAPI()

@app.get("/craft")
def get_craft(name: str = Query(..., description="Название предмета")):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        driver.get("https://minecraft-inside.ru/crafting/")
        search_box = driver.find_element(By.ID, "search")
        search_box.clear()
        search_box.send_keys(name)
        time.sleep(2)

        first_result = driver.find_element(By.CLASS_NAME, "item-block")
        first_result.click()
        time.sleep(2)

        title = driver.find_element(By.CSS_SELECTOR, "div.content h1").text
        image = driver.find_element(By.CSS_SELECTOR, "div.recipe img").get_attribute("src")
        materials = driver.find_elements(By.CSS_SELECTOR, "div.recipe-items li")

        mats = []
        for item in materials:
            mats.append(item.text)

        return JSONResponse({
            "title": title,
            "image": image,
            "materials": mats
        })

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    finally:
        driver.quit()
