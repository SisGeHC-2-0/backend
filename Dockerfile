FROM python:3.12-alpine

COPY ./requirements.txt .

RUN pip install -r requirements.txt

RUN apk add git

COPY . .

EXPOSE 8000

CMD python manage.py migrate && python manage.py runscript populate_db && python manage.py runserver 
