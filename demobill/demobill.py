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
    balance = FloatField(default=0)

    class Meta:
        database = db 

app = bottle.Bottle()

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


@app.post('/do')
def do():
    """
    Основной метод проведения операций:
    curl -X POST -d '{"plus":0, "minus":3, "session": "session1"}' http://localhost:9000/do

    Ответ:
    * { "status":"OK", "balance":1956.50 }
    * { "status":"not_enough_money", "balance":2 }
    * { "status":"session_not_found" }
    """
    response.content_type = 'application/json; charset=utf-8'
    j = json.loads(request.body.read())
    return json.dumps(do_billing(j))


@app.get('/list')
def list():
    """
    Список пользователей системы:
    curl http://localhost:9000/list
    """
    response.content_type = 'text/plain; charset=utf-8'
    res = ""
    for user in User.select():
        res += "%s = %s \n" % (user.user, user.balance)
    return res


@app.get('/new')
def new():
    """
    Создание нового пользователя:
    curl http://localhost:9000/new?name=session2&balance=1000
    """
    response.content_type = 'text/plain; charset=utf-8'
    res = ""
    name = request.GET.get("name", "")
    balance = float(request.GET.get("balance", "0"))

    try:
        User.get(User.user == name)
    except:
        User.create(user=name, balance=balance)
        return "OK"
    return "Already Exist"


@app.get('/')
def root():
    response.content_type = 'text/plain; charset=utf-8'
    res = """ /do (POST) curl -X POST -d '{"plus":0, "minus":3, "session": "session1"}' http://localhost:9000/do
 /list (GET) список пользователей и балансов curl http://localhost:9000/list
 /new?name=test&balance=1000  (GET) добавить пользователя curl http://localhost:9000/new?name=session2&balance=1000
    """
    return res


def usage():
    res = """ Demonstration Billing server v1.0
 ---------------------------------
 -h   --help    показывает текущую справку
 -p   --port=   указать порт (default: 8000)
      --debug   включить режим отладки"""
    print res
    sys.exit(0)


def main():
    level = logging.INFO 
    port = 9000
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

    app.run(host='0.0.0.0', port=port, reloader=True, debug=True)

if __name__== "__main__":
    main()