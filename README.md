# SERVIZ - vizualisation server

## Установка и запуск через docker-compose

```bash
make build
make up
```

## Запуск в ручном режиме

```bash
git clone https://github.com/arsenier/serviz.git
cd serviz
pip install -r backend/requirements.txt
```

```bash
cd frontend
python3 -m http.server 3000 --directory /app
```

```bash
cd backend
python3 main.py
```
