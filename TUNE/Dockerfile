FROM python:3.11

ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY req.txt /code/

RUN pip install --upgrade pip && pip install -r req.txt

ADD . /code/

CMD ["python", "manage.py", "migrate"]
