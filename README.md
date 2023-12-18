#Strikeemall

Strikeemall - это сайт по продаже страйкбольного вооружения с системой регистрации, корзиной, каталогом товаров(Взаимодействие с бд)

## Оглавление
- [Установка](#Установка)
- [Документация](#Документация)
- [Поддержка](#Поддержка)

<!--Установка-->
## Установка.

1. Клонирование репозитория git clone https://gitlab.com/SadEnjoyer/strikeemallback-nd.git
2. Перейти в директорию проекта
3. Установить зависимости pip3 install -r requirements.txt
4. Иницилиазировать alembic командой: alembic init alembic
5. Создать первую ревезию БД: alembic revision --autogenerate -m "migration name"
5. Перейти к последней ревизии БД: alembic upgrade head
7. Запустить сервис командой: uvicorn main:app —reload


<!--Документация-->
##Документация.
Пользовательская документация: https://docs.google.com/document/d/1Mzhn89WKlKXKrR19FHHAVMTzkriWdwmeddIEcM3HZbw/edit?usp=sharing

<!--Поддержка-->
##Поддержка.
Если у вас возникли сложности или вопросы по использованию пакета, создайте обсуждение в данном (https://github.com/SadEnjoyer/strikeEmAllBackend/issues/new) репозитории.

