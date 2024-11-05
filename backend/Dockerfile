FROM python:3.12-slim

COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы проекта после установки зависимостей
COPY . .

# Устанавливаем команду запуска
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]