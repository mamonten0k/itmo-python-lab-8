# Dictionary Semantic Graph Service
Проект представляет собой сервис словаря с семантическим графом, реализованный с использованием gRPC, Protocol Buffers, FastAPI и Cytoscape.js для визуализации. Проект включает два основных компонента:

### Серверная часть:=
Реализует gRPC-сервис для управления терминами и их связями, а также REST API для доступа из браузера.
### Клиентская часть
Веб-приложение, которое визуализирует семантический граф терминов с использованием Cytoscape.js.

### Технологии
Python 3.11
gRPC и Protocol Buffers
FastAPI
SQLAlchemy
Cytoscape.js
Docker и Docker Compose

### Требования
Docker версии 19.03 или выше
Docker Compose версии 1.25 или выше

### Установка
Склонируйте репозиторий:

```git clone <адрес_вашего_репозитория>
cd <имя_репозитория>
```

### Структура проекта
project_root/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── server.py
│   ├── models.py
│   ├── schemas.py
│   ├── database.py
│   ├── seed.py
│   ├── protobufs/
│   │   ├── __init__.py
│   │   └── dictionary.proto
│   └── static/
│       ├── index.html
│       └── main.js
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md

## Запуск приложения
Последовательно команды:
```
docker-compose build
```
Команда создаст Docker-образы для сервиса.

```
docker-compose up
```
Контейнер запустит серверное приложение на основе FastAPI на порту 8081 и gRPC-сервер на порту 50051.

По адресу: http://localhost:8081/  
Можно посмотреть веб-приложение, визуализирующее семантический граф.  

### API Эндпоинты
Сервис предоставляет REST API для взаимодействия с данными. Основные эндпоинты:

GET /terms/: Получение списка всех терминов.  
curl http://localhost:8081/terms/  

GET /relationships/: Получение списка всех связей между терминами.  
curl http://localhost:8081/relationships/  

Автодокументация Swagger UI: доступна по адресу http://localhost:8081/docs  
