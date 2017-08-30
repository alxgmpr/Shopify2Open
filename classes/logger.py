# coding = utf-8

# Shopify ATC v0.2.0
# By Alex Gompper @edzart
# http://github.com/alxgmpr

from time import strftime

from termcolor import colored


class Logger:
    def __init__(self, tid=None):
        self.tid = tid

    def set_tid(self, tid):
        self.tid = tid

    def log(self, text, color=None):
        if color is not None:
            text = colored(text, color)
        if self.tid is not None:
            text = '[{}] :: {}'.format(self.tid, text)
        print('[{}] {}'.format(strftime('%H:%M:%S'), text))

    def slack(self, text):
        # TODO: beautify this output
        print('slack not implemented yet')
