# minecraft commands
[Minecraft commands](http://37.139.62.167/) - мини web-приложение для добавления alias'ов (команд) на майнкрафт сервера по sftp.

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

Содержимое файла /backend/.env:
```
DATABASE_URL=sqlite:///test.db
SECRET_KEY=****
SERVER_DNS=****
SERVER_PORT=****
SERVER_USERNAME=***
SERVER_PASSWORD=****
LEGAL_USERNAMES=user1,user2,user3
```
SERVER_DNS, SERVER_PORT - DNS и port minecraft сервера
SERVER_USERNAME, SERVER_PASSWORD - username и пароль minecraft сервера
LEGAL_USERNAMES - имена пользователей, которые могут отправлять команды на сервер (send commands)
```
cd ..
```

```
cd frontend/
nano .env
```

Содержимое файла /frontend/.env:
```
REACT_APP_API_URL=http://your_server_ip_or_dns:8000
```
REACT_APP_API_URL - ip адрес или DNS вашего сервера
```
docker compose up --build
```

### grats!

## Использование
* sign up - регистрация
* sign in - войти в аккаунт
* add command - добавить команду (имя и описание)
* log out - выйти из аккаунта
* copy commands - скопировать команды в формате .yml, требуемый сервером
* send commands - отправка команда на сервер (необходимо настроить подключение по sftp)
