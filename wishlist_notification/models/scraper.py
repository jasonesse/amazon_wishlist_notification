from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
from wishlist_notification.models.wishlist import AMZNWishlist
from wishlist_notification.models.product import AMZNProduct
from config import SCROLL_PAUSE_TIME, HEADLESS

# logging_format = "%(asctime)s (%(levelname)s): %(message)s"
# logging.basicConfig(level=logging.INFO, format=logging_format)

def get_driver() -> webdriver:
    chrome_options = Options()
    if HEADLESS:
        chrome_options.add_argument("--headless")
    chrome_options.add_argument("--log-level=3");
    return webdriver.Chrome(options=chrome_options)
    
def scroll_to_bottom(driver):
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:

        time.sleep(SCROLL_PAUSE_TIME)

        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_current_wishlist_details(url: str):

    driver = get_driver()
    driver.get(f'{url}?viewType=list')
    scroll_to_bottom(driver)

    amzn_wishlist = AMZNWishlist(url=url)

    amzn_wishlist.title = driver.find_element_by_xpath("//span[@id='profile-list-name']").text
    wishlist = driver.find_element_by_xpath("//ul[@id='g-items']")
    products = wishlist.find_elements_by_xpath("//div[@class='a-row']/div[1]")

    for product in products:
        amzn_product = AMZNProduct()
        try:
            details = product.text.split('\n')
            amzn_product.title = details[0]
            amzn_product.url = product.find_element_by_xpath(".//a[contains(@id,itemName)]").get_attribute('href')
            itemImage = amzn_product.url[amzn_product.url.find('?coliid')+8:amzn_product.url.find('&')]
            amzn_product.img_url = driver.find_element_by_xpath(f"//div[@id='itemImage_{itemImage}']/a[@class='a-link-normal' and 1]/img[1]").get_attribute('src')
            amzn_product.iid = amzn_product.url[str.rfind(amzn_product.url[:str.find(amzn_product.url,'?coliid')-1],'/')+1:str.find(amzn_product.url,'?coliid')-1]
            #grab the first price found, that comes before the used price.
            price_found = False
            for detail in details:
                if '$' in detail and 'Used' not in detail and not price_found:
                    price_found = True
                    amzn_product.price = '.'.join(re.findall(r'[1-9]\d*', detail)[:2])
                    amzn_wishlist.add_product(amzn_product)
        except:
            
            continue

    driver.close()
    return amzn_wishlist