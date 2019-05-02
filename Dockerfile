FROM python:3.7.2

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/

RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install uWSGI

RUN chown -R www-data:www-data /usr/src/app

COPY . /usr/src/app


EXPOSE 8080

CMD ["uwsgi" , "--ini", "uwsgi.ini"]



