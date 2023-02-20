FROM python:3.10

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY req.txt /code/

RUN pip install --upgrade pip
RUN pip install django-ninja==0.20.0 --force
RUN pip install django-ninja-auth==0.1.5 --force
RUN pip install  django-ninja-extra --force
RUN pip install -r req.txt


ADD . /code/

CMD ["python", "manage.py", "migrate"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]