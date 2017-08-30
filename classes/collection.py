# coding = utf-8

# Shopify ATC v0.2.0
# By Alex Gompper @edzart
# http://github.com/alxgmpr


class Collection:
    def __init__(self, title, url, product_count=None, last_update=None, products=None):
        self.title = title
        self.url = url
        self.product_count = product_count
        self.last_update = last_update
        self.products = products
