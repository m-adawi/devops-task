FROM python:3.9.7-alpine3.14

ENV APP_HOME /app
WORKDIR $APP_HOME

COPY APP/ .

RUN pip install -r requirements.txt

ENTRYPOINT [ "python" ]
CMD [ "app.py" ]
