from wishlist_notification.controller import get_current_wishlist_details, get_wishlist_changes
from config import AMAZON_WISHLISTS
from wishlist_notification.messaging.notifier import notify
from wishlist_notification.models.data import save

def main():
    for wishlist_url in AMAZON_WISHLISTS:
        current_wishlist = get_current_wishlist_details(url=wishlist_url)
        changes = get_wishlist_changes(current_wishlist)
        save(changes, current_wishlist)
        notify(changes, current_wishlist, send=True)



if __name__ == "__main__":
    main()