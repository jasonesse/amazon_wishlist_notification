import json
from wishlist_notification.models.product import AMZNProduct
from wishlist_notification.models.wishlist import AMZNWishlist, ProductList
from decimal import *
import os
from config import PRICE_CHANGE_DEFAULT_PCT

def get_previous_product_dict(current_wishlist: AMZNWishlist, filename: str):

    previous_productlist = ProductList(title='Current Products')

    try:
        with open(filename) as json_file:
            product_data = json.load(json_file)
    
        previous_productlist.products = product_data
    except:
        pass
    
    return previous_productlist


def get_product_changes(current_wishlist: AMZNWishlist):

    filename = f"{os.path.dirname(os.path.dirname(os.path.dirname(__file__)))}/wishlist_notification/data/{current_wishlist.iid}.json"
    previous_productlist = get_previous_product_dict(current_wishlist, filename)

    new_products = ProductList(title='New Products')
    new_products.products = { k : current_wishlist.products[k] for k in set(current_wishlist.products) - set(previous_productlist.products) }
     
    new_prices = ProductList(title='New Prices')

    for key in current_wishlist.products.keys() & previous_productlist.products.keys():
        final = Decimal(current_wishlist.products[key]['price'])
        initial = Decimal(previous_productlist.products[key]['price'])

        #todo old price, new price.
        diff = 100 * ((final-initial)/abs(initial))
        if abs(diff) > PRICE_CHANGE_DEFAULT_PCT:
            diff_product = AMZNProduct()
            diff_product.price = initial
            diff_product.new_price = final
            diff_product.pct_change = str(diff.quantize(Decimal(10)**-2))
            diff_product.iid = key
            diff_product.title = current_wishlist.products[key]['title']
            diff_product.url = current_wishlist.products[key]['url']
            diff_product.img_url = current_wishlist.products[key]['img_url']
            new_prices.add_product(diff_product)
    
    pricematched_products = get_price_matches(current_wishlist)

    return [new_products, new_prices, pricematched_products]



def get_price_matches(current_wishlist: AMZNWishlist):

    filename = f"{os.path.dirname(os.path.dirname(os.path.dirname(__file__)))}/wishlist_notification/data/pricematch.json"
    pricematch_product_list = get_previous_product_dict(current_wishlist, filename)

    pricematched_products = ProductList(title='Price Matches')

    for key in current_wishlist.products.keys() & pricematch_product_list.products.keys():
        original_price = Decimal(current_wishlist.products[key]['price'])
        target_price = Decimal(pricematch_product_list.products[key]['price'])
        if original_price < target_price:
            diff = 100 * ((original_price-target_price)/abs(target_price))
            diff_product = AMZNProduct()
            diff_product.price = original_price
            diff_product.new_price = target_price
            diff_product.pct_change = str(diff.quantize(Decimal(10)**-2))
            diff_product.iid = key
            diff_product.title = current_wishlist.products[key]['title']
            diff_product.url = current_wishlist.products[key]['url']
            diff_product.img_url = current_wishlist.products[key]['img_url']
            pricematched_products.add_product(diff_product)
        
    return pricematched_products


def save(changes, current_wishlist):
    filename = f"{os.path.dirname(os.path.dirname(os.path.dirname(__file__)))}//wishlist_notification/data/{current_wishlist.iid}.json"
    with open(filename, 'w+') as outfile:
        outfile.writelines(json.dumps(current_wishlist.products, indent=4, sort_keys = True))