FROM python:3.10.6

RUN mkdir /app

COPY requirements.txt /app

RUN python -m pip install --upgrade pip && pip3 install -r app/requirements.txt --no-cache-dir

COPY . /app

WORKDIR /app/foodgram
# При старте контейнера запустить сервер разработки.
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "foodgram.wsgi"]
