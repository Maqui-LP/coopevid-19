FROM python:3.7.5

ENV FLASK_ENV=development
ENV FLASK_APP "run.py"
ENV FLASK_ENV=development
ENV DB_USER=root
ENV DB_PASS=root
ENV DB_NAME=proyecto

RUN mkdir /app
WORKDIR /app

ADD . .

RUN pip install -r requirements.txt

EXPOSE 5000:5000

CMD flask run
