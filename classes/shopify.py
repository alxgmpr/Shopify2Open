# coding = utf-8

# Shopify ATC v0.2.0
# By Alex Gompper @edzart
# http://github.com/alxgmpr

from logger import Logger
from collection import Collection
from product import Product
from variant import Variant

import threading
from time import time, sleep
from json import load
import urllib3

import requests

logger = Logger()
log = logger.log

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Shopify(threading.Thread):
    def __init__(self, thread_id, task_file):
        threading.Thread.__init__(self)
        self.start_time = time()
        logger.set_tid(thread_id)
        self.S = requests.Session()
        with open('config.json') as cfg:
            self.c = load(cfg)
        with open(task_file) as tsk:
            self.t = load(tsk)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/58.0.3029.81 Safari/537.36',
            'Content-Type': '',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': self.t['site_config']['base_url'].split('//')[1],
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1'
        }
        self.form_headers = self.headers
        self.form_headers['content-type'] = 'application/x-www-form-urlencoded'
        self.json_headers = self.headers
        self.json_headers['content-type'] = 'application/json'

    # poll function waits a configured amount of time before continuing
    def poll(self):
        log('Waiting {} sec(s) before continuing'.format(self.t['exec_config']['sleep_time']), color='blue')

    # config check validates config settings
    def check_config(self):
        # TODO: complete check_config
        return True

    # gets all products on the site. returns a list of product objects
    # tries 'sitemap_products_1.xml'
    def get_products(self):

    # compares a list of product objects against configured keywords.
    # if a match is found, return that single product object
    def compare_products(self, product_list):
        if not all(isinstance(p, Product) for p in product_list):
            raise Exception('Expected list of product objects')

    # gets all product variants from a product. returns a list of variant objects
    # tries 'productname.json'
    def get_product_variants(self, product):
        if not(isinstance(product, Product)):
            raise Exception('Expected product object')

    # compares a list of variant objects against configured size
    # if a match is found, return that single variant object
    def compare_variants(self, variant_list):
        if not all(isinstance(v, Variant) for v in variant_list):
            raise Exception('Expected list of variant objects')

    # scrapes a given page source for captcha presence. if there is one, get a solution
    # returns a captcha object if present or false if not present
    # def captcha(self, page_source):
    #
    # # adds a product to cart. returns a checkout url
    # def add_to_cart(self):
    #
    # # opens checkout and calls subsequent fx to check for sold out, captcha
    # def go_to_checkout(self, checkout_url):
    #
    # # submits customer information
    # def submit_customer_info(self, checkout_url):
    #
    # # submits shipping information
    # def submit_shipping_info(self, checkout_url):
    #
    # def submit_payment_info(self, checkout_url):

    def run(self):
        if not self.check_config():
            raise Exception('Configuration check failed')