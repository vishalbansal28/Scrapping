import requests
from bs4 import BeautifulSoup

# URL of the Grab Food Delivery website
url = "https://food.grab.com/sg/en/restaurants"

# Set a Chrome user agent in the request headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
}

# Send a GET request to the website with custom headers
response = requests.get(url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Extract the HTML content from the response
    html_content = response.text

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting restaurant details
    restaurant_details = {}

    # Restaurant Name
    restaurant_name_selector = '#page-content > div:nth-of-type(5) > div > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(1) > a > div > div:nth-of-type(2) > p'
    restaurant_name_elem = soup.select_one(restaurant_name_selector)
    restaurant_name = restaurant_name_elem.get_text(strip=True) if restaurant_name_elem else None
    restaurant_details['Restaurant Name'] = restaurant_name

    # Restaurant Cuisine
    restaurant_cuisine_selector = '#page-content > div:nth-of-type(5) > div > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(1) > a > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(1)'
    restaurant_cuisine_elem = soup.select_one(restaurant_cuisine_selector)
    restaurant_cuisine = restaurant_cuisine_elem.get_text(strip=True) if restaurant_cuisine_elem else None
    restaurant_details['Restaurant Cuisine'] = restaurant_cuisine

    # Restaurant Rating
    restaurant_rating_selector = '#page-content > div:nth-of-type(5) > div > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(1) > a > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1)'
    restaurant_rating_elem = soup.select_one(restaurant_rating_selector)
    restaurant_rating = restaurant_rating_elem.get_text(strip=True) if restaurant_rating_elem else None
    restaurant_details['Restaurant Rating'] = restaurant_rating

    # Estimate time of Delivery and Restaurant Distance from Delivery Location
    delivery_info_selector = '#page-content > div:nth-of-type(5) > div > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(1) > a > div > div:nth-of-type(2) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(2)'
    delivery_info_elem = soup.select_one(delivery_info_selector)
    delivery_info_text = delivery_info_elem.get_text(strip=True) if delivery_info_elem else None
    if delivery_info_text:
        delivery_info_parts = delivery_info_text.split('•')
        estimate_time_of_delivery = delivery_info_parts[0].strip()
        restaurant_distance = delivery_info_parts[1].strip()
    else:
        estimate_time_of_delivery = None
        restaurant_distance = None
    restaurant_details['Estimate time of Delivery'] = estimate_time_of_delivery
    restaurant_details['Restaurant Distance from Delivery Location'] = restaurant_distance

    # Promotional Offers
    promotional_offers_selector = '#page-content > div:nth-of-type(5) > div > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(1) > a > div > div:nth-of-type(2) > div:nth-of-type(2) > span'
    promotional_offers_elem = soup.select_one(promotional_offers_selector)
    promotional_offers = promotional_offers_elem.get_text(strip=True) if promotional_offers_elem else None
    restaurant_details['Promotional Offers'] = promotional_offers

    # Is promo available (True/False)
    is_promo_available = promotional_offers is not None
    restaurant_details['Is promo available (True/False)'] = is_promo_available

    # Restaurant ID
    restaurant_id_selector = '#page-content > div:nth-of-type(5) > div > div > div > div > div:nth-of-type(1) > div > div > div:nth-of-type(1) > a'
    restaurant_id_elem = soup.select_one(restaurant_id_selector)
    restaurant_id = "4-" + restaurant_id_elem['href'].split('/')[-1].replace("?", "") if restaurant_id_elem else None
    restaurant_details['Restaurant ID'] = restaurant_id

    # Printing the extracted details
    for key, value in restaurant_details.items():
        print(f"{key}: {value}")
else:
    print("Failed to fetch HTML content:", response.status_code)
