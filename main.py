# coding = utf-8

# Shopify ATC v0.2.0
# By Alex Gompper @edzart
# http://github.com/alxgmpr

from classes.logger import Logger
from classes.shopify import Shopify

from os import listdir


def main():
    log = Logger().log
    log('*************************\n\nSHOPIFY ATC V0.2.0 OPEN SOURCE\nBY ALEX GOMPPER @edzart\n\n**********************'
        '***', color='blue', timestamp=False)
    log('starting tasks', color='green')
    threads = []
    i = 0
    for task in listdir('tasks'):
        threads.append(Shopify(i, 'tasks/{}'.format(task)))
        threads[i].start()
        i += 1


if __name__ == '__main__':
    main()
