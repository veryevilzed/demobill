Установка
=========

```
python setup.py install
```

Проект устанавливается в систему и создаёт скрипт demobill для запуска cервера.


Наполнение БД
=============

```
echo "insert into user values (1,'session1',10000), (2,'session2',10000), (3,'session3',0);" | sqlite3 demobilling.db
```

Созданы пользователи session1, session2, session3.


Запуск
======

```
demobill -p 9000 --debug
```

Биллинг застартован по адресу http://127.0.0.1:9000/do
