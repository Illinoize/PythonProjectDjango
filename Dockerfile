FROM python:3.10

WORKDIR /test_app
EXPOSE 8000

COPY ./requirements.txt /test_app/requirements.txt
RUN pip install -r /test_app/requirements.txt
RUN python manage.py migrate
COPY . /test_app

CMD ['python', 'manage.py', 'migrate']
