Установка
=========

```
python setup.py install
```


Наполнение БД
=============

```
echo "insert into user values (1,'session1',10000), (2,'session2',10000), (3,'session3',10000);" | sqlite3 demobilling.db
```

Запуск
======

```
demobill -p 9000 --debug
```