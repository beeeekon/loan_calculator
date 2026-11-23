FROM python:3.12-slim

# Создаем рабочую папку внутри контейнера
WORKDIR /code

# Копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Открываем порт
EXPOSE 8000

# Запускаем Uvicorn с флагом --reload для авто-перезагрузки
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]