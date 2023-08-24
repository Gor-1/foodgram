<h1>Продуктовый помощник</h1> 
дипломный проект курса Backend-разработки Яндекс.Практикум. Проект представляет собой онлайн-сервис и API для него.

<h2>Развертывание проекта</h2>

1: Создайте файл /infra/.env. Шаблон для заполнения файла нахоится в /infra/.env.example.
2: Выполните команду docker-compose up.
3: Выполните миграции docker-compose exec backend python manage.py migrate
4: Соберите статику docker-compose exec backend python manage.py collectstatic
5: Заполните базу ингредиентами docker-compose exec backend python manage.py import_ingredients

<h2>Автор</h2>
<a href="https://t.me/Gcodm">Гор Галстян</a>

domen: https://g-foodgram.sytes.net/
login superuser: g@mail.ru
password superuser: g