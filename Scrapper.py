from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import requests


class GrabFoodScraper:
    def __init__(self, proxy_url):
        self.base_url = 'https://www.grab.com/sg/food/'
        self.proxy_url = proxy_url

    def scrape_restaurant_names(self, location):
        # Configure proxy for Selenium
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--proxy-server=%s' % self.proxy_url)
        driver = webdriver.Chrome(options=chrome_options)

        try:
            # Open the Grab Food Delivery website
            driver.get(self.base_url)

            # Click on the "Order Now" button using JavaScript
            order_now_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '.round-button___2cysa'))
            )
            driver.execute_script("arguments[0].click();", order_now_button)

             # Wait for the location input box to be visible
            location_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input#location-input'))
            )
            # Enter the location into the input box
            location_input.clear()
            location_input.send_keys(location)
            location_input.send_keys(Keys.RETURN)

            # Wait for the restaurant list to load
            time.sleep(5)  # Adjust the wait time as needed

            # Extract the restaurant names
            restaurant_elements = driver.find_elements_by_css_selector('.restaurant-name')
            restaurant_names = [restaurant.text.strip() for restaurant in restaurant_elements]

            return restaurant_names
        finally:
            # Close the browser after scraping
            driver.quit()


# Set up the proxy configuration
proxy_url = "http://7a9781083f4095a193f7bb3bfc38b91ed89472bc:js_render=true@proxy.zenrows.com:8001"

# Example usage:
scraper = GrabFoodScraper(proxy_url)
location = "PT Singapore - Choa Chu Kang North 6, Singapore, 689577"
restaurant_names = scraper.scrape_restaurant_names(location)
print("Restaurant names for", location, ":")
for name in restaurant_names:
    print(name)

# Request using proxy
url = 'https://www.grab.com/sg/food/'
response = requests.get(url, proxies={'https': proxy_url})
print(response.text)