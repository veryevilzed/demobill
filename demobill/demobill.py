#!/bin/env/python

import getopt
import logging


def usage():
    """ Demonstration Billing server v1.0
 ---------------------------------
 -h   --help    показывает текущую справку
 -p=  --port=   указать порт (default: 8000)
 -u=  --url=    указать префикс для урла (default: /go)
 -d=  --db=     указать путь к базе данных (default: :memory:)
 -n   --new     создать данные по умолчанию 
      --debug   включить режим отладки
"""
    sys.exit(0)

def main():

    level = logging.INFO 

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:u:d:n', ['help','port=','url=','db=','new', 'debug'])
    except getopt.GetoptError, err: 
        usage(err)

    for opt, arg in opts:
        if opt in ('-h', '--help'): 
            usage()
        elif opt in ('-p', '--port'): 
            pass
        elif opt in ('-u', '--url'): 
            pass
        elif opt in ('-d', '--db'): 
            pass
        elif opt in ('-n', '--new'): 
            pass
        elif opt in ('--debug',): 
            level = logging.DEBUG
        else:
            print "Ошибка аргумента %s", opt
            sys.exit(1)

    FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
    logging.basicConfig(format=FORMAT, level=level)
