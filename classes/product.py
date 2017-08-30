# coding = utf-8

# Shopify ATC v0.2.0
# By Alex Gompper @edzart
# http://github.com/alxgmpr

class Product:
    def __init__(self, name, url, variants=None, price=None):
        self.name = name
        self.url = url
        self.variants = variants
        self.price = price
