FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8000
CMD ["python3", "-u", "main.py"]
# CMD ["eventlet", "-w", "1", "main:app"]
# CMD ["gunicorn", "-k", "eventlet","-b", "0.0.0.0:8000", "main:app"]
