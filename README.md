# AlgontTestTask

Веб сервис, который выполняет следующие функции:

1. Постоянно сохраняет в базу данных историю величины загрузки процессора с интервалом в 5 секунд.

2. Предоставляет страницу, которая изображает срез данных с историей загрузки процессора за последний час в виде двух графиков.

Первый график отображает историю изменения моментальной загрузки процессора.

Второй - отображает график усредненной загрузки процессора (среднее значение за 1 минуту)

В случае, если сервис на какое-то время был выключен, на графиках видны пустые промежутки времени, для которых нет данных.

В качестве базы данных используется SQlite.
