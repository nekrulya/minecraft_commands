# minecraft commands
[Minecraft commands](http://37.139.62.167/) - мини web-приложение для добавления alias'ов (комманд) на майнкрафт сервера по sftp.

## Требования
* Mac / Linux
* docker

## Установка
```
git clone https://github.com/nekrulya/minecraft_commands.git
cd minecraft_commands
```

### Доп. файлы
Необходимо перейти в папки и создать .env файлы по шаблону
```
cd backend/
nano .env
```

Содержимое файла:
```
DATABASE_URL=sqlite:///test.db
SECRET_KEY=****
SERVER_DNS=****
SERVER_PORT=****
SERVER_USERNAME=***
SERVER_PASSWORD=****
LEGAL_USERNAMES=user1,user2,user3
```

```
cd ..
```

```
cd frontend/
nano .env
```

Содержимое файла:
```
REACT_APP_API_URL=http://your_server_ip_or_dns:8000
```

```
docker compose up --build
```
