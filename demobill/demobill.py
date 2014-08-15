#!/usr/bin/env python
#coding:utf-8

import getopt
import logging
import bottle
from bottle import get, post, request, response
import json
from peewee import *
import sys

db = SqliteDatabase('demobilling.db')

class User(Model):
    user = CharField()
    balance = IntegerField(default=0)

    class Meta:
        database = db 

app = bottle.Bottle()


# { "status": "OK", "balance": 195650 }
# { "status": "not_enough_money", "balance": 2 }
# { "status": "session_not_found" }

def do_billing(j):
    user = None
    try:
        user = User.get(User.user == j["session"])
    except:
        return { "status": "session_not_found" }

    if (j["minus"] > user.balance):
        return { "status": "not_enough_money", "balance": user.balance }

    user.balance -= j["minus"]
    user.balance += j["plus"]
    user.save()
    
    return { "status": "OK", "balance": user.balance }


@app.post('/go')
def go():
    response.content_type = 'application/json; charset=utf-8'
    j = json.loads(request.body.read())
    return json.dumps(do_billing(j))


@app.get('/list')
def list():
    response.content_type = 'text/plain; charset=utf-8'
    res = ""
    for user in User.select():
        res += "%s = %d \n" % (user.user, user.balance)
    return res


@app.get('/new/')
def new():
    response.content_type = 'text/plain; charset=utf-8'
    res = ""
    name = request.GET.get("name", "")
    balance = int(request.GET.get("balance", "0"))

    try:
        User.get(User.user == name)
    except:
        return "Already Exist"

    User.create(user=name, balance=balance)
    return "OK"

@app.get('/')
def root():
    response.content_type = 'text/plain; charset=utf-8'
    res = """ /go (POST) curl -X POST -d '{"plus":0, "minus":3, "session": "zed"}' http://localhost:8000/go
 /list (GET) список пользователей и балансов
 /new?name=test&balance=1000  (GET) добавить пользователя
    """
    return res

def usage():
    """ Demonstration Billing server v1.0
 ---------------------------------
 -h   --help    показывает текущую справку
 -p=  --port=   указать порт (default: 8000)
      --debug   включить режим отладки
"""
    sys.exit(0)

def main():

    level = logging.INFO 
    port = 8000
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hp:', ['help','port=', 'debug'])
    except getopt.GetoptError, err: 
        usage(err)

    for opt, arg in opts:
        if opt in ('-h', '--help'): 
            usage()
        elif opt in ('-p', '--port'): 
            port = int(arg)
        elif opt in ('--debug',): 
            level = logging.DEBUG
        else:
            print "Ошибка аргумента %s", opt
            sys.exit(1)

    FORMAT = '[%(asctime)-15s] %(message)s'
    logging.basicConfig(format=FORMAT, level=level)

    try:
        db.create_tables([User])
    except:
        pass

    app.run(host='0.0.0.0', port=port, reloader=True, debug=True) #, server='gunicorn', workers=5)

if __name__== "__main__":
    main()