from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import time

class GrabFoodScraper:
    def __init__(self):
        self.base_url = 'https://food.grab.com/sg/en/?utm_campaign=gw_exp_home0_202110&utm_source=grab.com&utm_medium=referral&utm_content=GrabFood_SG&pid=website&af_sub5=referral&c=gw_exp_home0_202110&deep_link_value=grab%3A%2F%2Fopen%3FscreenType%3DGRABFOOD'
        self.location = "PT Singapore - Choa Chu Kang North 6, Singapore, 689577"

    def scrape_restaurant_names(self):
        # Launch the Chrome browser using Selenium WebDriver
        driver = webdriver.Chrome()

        try:
            # Open the Grab Food Delivery website
            driver.get(self.base_url)

            # Wait for the location input box to be visible
            location_input = WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.XPATH, '//*[@id="location-input"]'))
            )

            # Click on the location input box
            location_input.click()

            # Type the location address into the input box
            location_input.send_keys(self.location)

            # Find and click the search button
            search_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="page-content"]/div[3]/div/button'))
            )
            search_button.click()

            # Wait for the restaurant list to load
            time.sleep(30)  # Adjust the wait time as needed

            restaurant_info = []
            restaurant_elements = driver.find_elements(By.XPATH, '//div[@class="listing-item"]')
            for restaurant in restaurant_elements:
                name = restaurant.find_element(By.XPATH, './/div[contains(@class, "restaurant-name")]').text.strip()
                cuisine = restaurant.find_element(By.XPATH, './/div[contains(@class, "cuisine")]').text.strip()
                rating = restaurant.find_element(By.XPATH, './/div[contains(@class, "rating")]/span').text.strip()
                delivery_time = restaurant.find_element(By.XPATH, './/div[contains(@class, "eta-time")]').text.strip()
                distance = restaurant.find_element(By.XPATH, './/div[contains(@class, "distance")]').text.strip()
                promo_offers = restaurant.find_element(By.XPATH, './/div[contains(@class, "promo")]/span').text.strip()
                notice = restaurant.find_element(By.XPATH, './/div[contains(@class, "notice")]').text.strip()
                image_link = restaurant.find_element(By.XPATH, './/div[contains(@class, "image")]/img').get_attribute("src")
                promo_available = "True" if promo_offers else "False"
                restaurant_id = restaurant.get_attribute("id").split("-")[1]
                latitude = restaurant.get_attribute("data-lat")
                longitude = restaurant.get_attribute("data-lng")
                delivery_fee = restaurant.find_element(By.XPATH, './/div[contains(@class, "delivery-fee")]').text.strip()
                
                # Append restaurant information to the list
                restaurant_info.append({
                    "Restaurant Name": name,
                    "Restaurant Cuisine": cuisine,
                    "Restaurant Rating": rating,
                    "Estimate time of Delivery": delivery_time,
                    "Restaurant Distance from Delivery Location": distance,
                    "Promotional Offers Listed for the Restaurant": promo_offers,
                    "Restaurant Notice If Visible": notice,
                    "Image Link of the Restaurant": image_link,
                    "Is promo available": promo_available,
                    "Restaurant ID": restaurant_id,
                    "Restaurant Latitude": latitude,
                    "Restaurant Longitude": longitude,
                    "Estimate Delivery Fee": delivery_fee
                })

            return restaurant_info
        finally:
            # Close the browser after scraping
            driver.quit()

# Example usage:
scraper = GrabFoodScraper()
restaurant_names = scraper.scrape_restaurant_names()
print("Restaurant names:")
for name in restaurant_names:
    print(name)
