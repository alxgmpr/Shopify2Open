# coding = utf-8

# Shopify ATC v0.2.0
# By Alex Gompper @edzart
# http://github.com/alxgmpr


class Variant:
    def __init__(self, vid, title, stock=None):
        self.vid = vid
        self.title = title
        self.stock = stock
