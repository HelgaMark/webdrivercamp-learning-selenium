from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#1.Open Browser and print URL
driver = webdriver.Chrome()
driver.get("https://www.ebay.com")
print(driver.current_url)
driver.quit()

#2.Add wait
driver = webdriver.Chrome()
driver.get("https://www.ebay.com")
time.sleep(5)
print(driver.current_url)
driver.quit()

#3.Search items
driver = webdriver.Chrome()
driver.get("https://www.ebay.com")
time.sleep(5)
print(driver.current_url)
search_items = driver.find_element(By.XPATH, '//*[@id="gh-ac"]')
search_items.send_keys("women watch")
time.sleep(5)
search_items.send_keys(Keys.RETURN)
time.sleep(5)
driver.quit()

#4.Verify the search results
driver = webdriver.Chrome()
driver.get("https://www.ebay.com")
time.sleep(5)
print(driver.current_url)
search_items = driver.find_element(By.XPATH, '//*[@id="gh-ac"]')
search_items.send_keys("women watch")
time.sleep(5)
search_items.send_keys(Keys.RETURN)

try:
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//h1[@class="srp-controls__count-heading"]'))
    )

    header_result = driver.find_element(By.XPATH, '//h1[@class="srp-controls__count-heading"]')
    assert "results for women watch" in header_result.text.lower(), f"{'results for women watch'}"
    print("Verified")

finally:
    driver.quit()



