FROM python:3.12-slim

#создаем рабочую папку внутри контейнера
WORKDIR /code

#копируем файл с зависимостями и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#копируем остальной код
COPY . .

#открываем порт
EXPOSE 8000

#запускаем Uvicorn с флагом --reload для авто-перезагрузки
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]