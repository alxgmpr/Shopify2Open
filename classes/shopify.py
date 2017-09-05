# coding = utf-8

# Shopify ATC v0.2.0 Open Source
# By Alex Gompper @edzart
# http://github.com/alxgmpr

from logger import Logger
from product import Product
from variant import Variant

import threading
import re
from time import time, sleep
from json import load
import urllib3

import requests

logger = Logger()
log = logger.log

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Shopify(threading.Thread):
    def __init__(self, thread_id, task_file, proxy_manager):
        threading.Thread.__init__(self)
        self.start_time = time()
        logger.set_tid(thread_id)
        self.S = requests.Session()
        with open('config.json') as cfg:
            self.c = load(cfg)
        with open(task_file) as tsk:
            self.t = load(tsk)
        if self.t['exec_config']['use_proxies']:
            proxy = proxy_manager.get_next_proxy()
            log('[{}] adding proxy to task'.format(proxy), color='blue')
            p = {
                'http': 'http://{}'.format(proxy),
                'https': 'https://{}'.format(proxy)
            }
            self.S.proxies = p
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
        sleep(self.t['exec_config']['sleep_time'])

    # config check validates config settings
    def check_config(self):
        if self.c['log_config']['slack_enable'] and self.c['log_config']['slack_hook'] in {None, ''}:
            log('[error][config.json] Slack logging enabled but no webhook provided')
            return False
        return True

    # gets all products on the site. returns a list of product objects
    # tries 'sitemap_products_1.xml'
    def get_products(self):
        log('[sitemap_products_1.xml] Getting products', color='blue')
        endpoint = '{}/sitemap_products_1.xml'.format(self.t['site_config']['base_url'])
        r = requests.get(
            endpoint,
            headers=self.headers,
            verify=False
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            log('[error][{}][sitemap_products_1.xml] Failed to get all products'.format(r.status_code), color='red')
            return None
        expression = '<loc>(.*)</loc>\s.*</lastmod>\s.*\s.*\s.*\s.*\s.*\s.*<image:title>(.*)</image:title>'
        products = re.findall(expression, r.text)
        product_objects = []
        for prod in products:
            product_objects.append(Product(prod[1], prod[0]))
        return product_objects

    # compares a list of product objects against configured keywords.
    # if a match is found, return that single product object
    def compare_products(self, product_list):
        if not all(isinstance(p, Product) for p in product_list):
            raise Exception('Expected list of product objects')
        log('Comparing {} products against keywords'.format(len(product_list)), color='blue')
        return product_list[0]

    # gets all product variants from a product. returns a list of variant objects
    # tries 'productname.json'
    def get_product_variants(self, product):
        if not(isinstance(product, Product)):
            raise Exception('Expected product object')
        log('[{}.json] Getting product variants'.format(product.url), color='blue')
        endpoint = '{}.json'.format(product.url)
        r = self.S.get(
            endpoint,
            headers=self.headers,
            verify=False
        )
        try:
            r.raise_for_status()
        except requests.exceptions.HTTPError:
            log('[error][{}][{}.json] Failed to get variants'.format(r.status_code, product.url), color='red')
            return None
        

    # compares a list of variant objects against configured size
    # if a match is found, return that single variant object
    def compare_variants(self, variant_list):
        if not all(isinstance(v, Variant) for v in variant_list):
            raise Exception('Expected list of variant objects')
        log('Comparing variants against sizes', color='blue')

    # scrapes a given page source for captcha presence. if there is one, cry
    def captcha(self, page_source):
        if 'g-recaptcha' in page_source:
            log('[error] Encountered captcha. Handling not provided.', color='red')
            exit(-1)
        return

    # # adds a product to cart. returns a checkout url
    def add_to_cart(self, variant):
        if not isinstance(variant, Variant):
            raise Exception('Expected variant object')
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
        products = self.get_products()
        selected_product = self.compare_products(products)
        variants = self.get_product_variants(selected_product)
        #selected_variant = self.compare_variants(variants)
        #checkout_url = self.add_to_cart(selected_variant)

