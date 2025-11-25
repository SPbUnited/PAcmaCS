FROM nikolaik/python-nodejs

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["honcho", "start"]
