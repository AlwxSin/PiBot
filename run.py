# coding=utf-8
__author__ = 'Alwx'

from settings import INTERVAL
from bot import check_updates
import time

if __name__ == "__main__":
    while True:
        try:
            print 'running'
            check_updates()
            time.sleep(INTERVAL)
        except KeyboardInterrupt:
            print 'Прервано пользователем..'
            break
