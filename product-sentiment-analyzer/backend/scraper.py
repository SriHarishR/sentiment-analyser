from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import random
import time

def convert_to_reviews_url(product_url):
    parts = product_url.split("/dp/")
    if len(parts) < 2:
        raise ValueError("Invalid Amazon product URL")
    asin = parts[1].split("/")[0]
    return f"https://www.amazon.in/product-reviews/{asin}/?reviewerType=all_reviews"

def scrape_amazon_reviews(product_url, limit=5):
    reviews_url = convert_to_reviews_url(product_url)

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--headless")  # optional
    options.add_argument(
        "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/113.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(options=options)
    driver.get(reviews_url)

    print("👉 Please log in to Amazon in the opened browser window (if not already).")
    input("➡️ Press ENTER once you are logged in...")

    # Scroll multiple times
    for _ in range(10):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    selectors = [
        "span[data-hook='review-body'] span",
        "div[data-hook='review-collapsed'] span",
        "div.review-text-content span"
    ]

    reviews = []
    for sel in selectors:
        elements = driver.find_elements(By.CSS_SELECTOR, sel)
        if elements:
            reviews = [e.text.strip() for e in elements if e.text.strip()]
            break

    driver.quit()

    if not reviews:
        print("❌ No reviews found — check the URL.")
        return []

    if len(reviews) > limit:
        reviews = random.sample(reviews, limit)

    print(f"✅ Found {len(reviews)} reviews!")
    for i, r in enumerate(reviews, 1):
        print(f"{i}. {r}\n")

    return reviews


if __name__ == "__main__":
    product_url = "https://www.amazon.in/Apple-iPhone-13-128GB-Midnight/dp/B09G9HD6PD/ref=asc_df_B09G9HD6PD?mcid=48759fea28bb33c19dbfcaac12fc8ff5&tag=googleshopdes-21&linkCode=df0&hvadid=709962856229&hvpos=&hvnetw=g&hvrand=11202920729903852626&hvpone=&hvptwo=&hvqmt=&hvdev=c&hvdvcmdl=&hvlocint=&hvlocphy=9148884&hvtargid=pla-1486222845754&gad_source=1&th=1"
    scrape_amazon_reviews(product_url, limit=5)
