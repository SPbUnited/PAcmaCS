FROM python:3.12-slim

WORKDIR /app

# COPY requirements.txt /app/requirements.txt
# RUN pip install -r requirements.txt

COPY . /app

EXPOSE 3000
CMD ["python3", "-m", "http.server", "3000", "--directory", "/app"]
