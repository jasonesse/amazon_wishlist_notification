from wishlist_notification.models.scraper import get_current_wishlist_details as get_products
from wishlist_notification.models.data import get_product_changes as get_changes
from wishlist_notification.messaging.notifier import notify

def get_current_wishlist_details(url):
    return get_products(url)

def get_wishlist_changes(curent_products):
    return get_changes(curent_products)

def notify(results):
    return notify(results)