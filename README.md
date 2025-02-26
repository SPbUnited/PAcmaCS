# SERVIZ - vizualisation server

## Установка и запуск через docker-compose

```bash
make build
make up
```

После запуска можно подключится к serviz по адресу http://localhost:8000

## Более подробное описание реализованных инструкций:

- `make build` - собирает образы для serviz и larcmacs
- `make up` - запускает все сервисы кроме grsim (а именно: serviz, larcmacs)
- `make up-grsim` - запускает headless grsim
- `make up-all` - запускает все сервисы (serviz, larcmacs, grsim)
- `make down` - останавливает все сервисы
