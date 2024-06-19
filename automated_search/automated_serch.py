from selenium import webdriver
from selenium.common import exceptions, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()

# 1. Open eBay watch page
driver.get("https://www.ebay.com/sch/i.html?_from=R40&_trksid=p4432023.m570.l1313&_nkw=watch&_sacat=0")

# 2. Select option Brand / Rolex in Filter pane
rolex_brand = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'x-refine__select__svg')]//span[contains(text(), 'Rolex')]"))
    )
rolex_brand.click()
time.sleep(5)

# 3. Verify the first two result items contain “rolex” in their title
WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id = 'srp-river-results']//span[@role = 'heading']"))
        )
item_titles = driver.find_elements(By.XPATH, "//div[@id = 'srp-river-results']//span[@role = 'heading']")[:2]
prices_items = driver.find_elements(By.XPATH, "//div[@id = 'srp-river-results']//span[@class = 's-item__price']")[:2]

items = []
for item, price in zip(item_titles, prices_items):
            title_text = item.text
            price_text = price.text
            print(f"Title: {title_text}, Price: {price_text}")
            assert "rolex" in title_text.lower(), f"Item doesn't contain 'rolex': {title_text}"
            items.append({'title': title_text, 'price': price_text})

 # 4. Store title and price of the first two results in a variable
stored_items = items

# 5. Open item in a new tab and verify the title and the price by comparing them with the stored data
mismatches = []
for index, item in enumerate(stored_items[:2]):
            item_titles[index].click()
            driver.switch_to.window(driver.window_handles[1])
            time.sleep(5)

            try:
                new_tab_title = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//h1[@class = 'x-item-title__mainTitle']"))
                ).text
                new_tab_price = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@class = 'x-price-primary']/span"))
                ).text

                if item["title"].lower() != new_tab_title.lower():
                    mismatches.append(f"Title mismatch: '{item['title']}' != '{new_tab_title}'")
                if item['price'] != new_tab_price.strip("US "):
                    mismatches.append(f"Price mismatch: '{item['price']}' != '{new_tab_price}'")
            except TimeoutException:
                mismatches.append(f"Timed out waiting for elements in the new tab")

            driver.close()
            driver.switch_to.window(driver.window_handles[0])

# Print all mismatches
if mismatches:
    print("Mismatches found during comparing:")
    for mismatch in mismatches:
                print(mismatch)
else:
    print("No mismatches found during comparing")

 # 6. Uncheck “Rolex“ option
rolex_checkbox = WebDriverWait(driver, 10).until(
         EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Rolex']"))
        )
rolex_checkbox.click()
time.sleep(10)

# 7. Check the "Casio" option
casio_checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//ul[@class='x-refine__left__nav']//span[contains(text(),'Casio')]"))
        )
casio_checkbox.click()
time.sleep(10)

# 8. Verify the last two result items contain “Casio“ in their title
WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='srp-river-results']//span[@role='heading']"))
            )
item_titles = driver.find_elements(By.XPATH, "//div[@id='srp-river-results']//span[@role='heading']")[-2:]
prices_items = driver.find_elements(By.XPATH, "//div[@class='s-item__details clearfix']//span[@class='s-item__price']")[-2:]

casio_items = []
for item, price in zip(item_titles, prices_items):
                title_text = item.text
                price_text = price.text
                print(f"Title: {title_text}, Price: {price_text}")

                if "casio" not in title_text.lower():
                   print(f"Item doesn't contain 'Casio': {title_text}")
                casio_items.append({'title': title_text, 'price': price_text})

# 9. Save and print all the mismatches if any
if mismatches:
    print("Mismatches found during comparing:")
    for mismatch in mismatches:
        print(mismatch)
else:
    print("No mismatches found during comparing")
