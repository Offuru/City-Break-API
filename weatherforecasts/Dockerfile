FROM python

ENV DB_HOST=127.0.0.1
ENV DB_USER=myuser
ENV DB_PASSWORD=mypassword
ENV HOST=0.0.0.0
ENV PORT=5000

ADD . /weatherforecasts
WORKDIR /weatherforecasts

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python", "__init__.py"]