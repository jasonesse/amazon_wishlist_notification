from wishlist_notification.models.product import AMZNProduct

class ProductList():
    def __init__(self, title: str = "Product List"):
        self.title = title
        self.products = {}
    
    def add_product(self, product):
        # if isinstance(product, dict):
        #     self.products.append(product)
        # else:
        #     self.products.append(product.__dict__)
        self.products.update({product.iid : {'title': product.title, 'url': product.url, 'img_url': product.img_url, 'price': product.price, 'new_price': product.new_price, 'pct_change': product.pct_change}})

    # def get_product_dict(self):
    #     #create a dictinary of products
    #     product_dict = {}
    #     for product in self.products:
    #         product_dict.update({product.iid : [product.title, product.price, product.url]})
    #     return product_dict

class AMZNWishlist(ProductList):

    def __init__(self, url=""):
        super().__init__(self)
        self.url = url
        self.iid = url[url.rfind('/')+1:]