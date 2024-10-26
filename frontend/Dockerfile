# Используем официальный образ Node.js в качестве базового
FROM node:18-alpine

# Создаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем package.json и package-lock.json для установки зависимостей
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install --legacy-peer-deps --no-cache

# Копируем оставшиеся файлы проекта
COPY . .

# Собираем React-приложение
RUN npm run build

# Используем nginx для сервинга статических файлов
FROM nginx:alpine

# Копируем сборку React в папку, откуда Nginx будет раздавать статику
COPY --from=0 /app/build /usr/share/nginx/html

# Указываем порт, который будет использовать контейнер
EXPOSE 80

# Запускаем Nginx
CMD ["nginx", "-g", "daemon off;"]
