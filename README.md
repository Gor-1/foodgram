# praktikum_new_diplom
How to start program.

1: cd infra : docker compose up
2: docker exec -it backend /bin/bash
3: makemigrations and migrate (users and recipes)
4: python manage.py collectstatic (static files copies to '/app/foodgram/static')
5: python manage.py import_ingredients (import ingredients)
cp -R /app/foodgram/media/ /var/html/