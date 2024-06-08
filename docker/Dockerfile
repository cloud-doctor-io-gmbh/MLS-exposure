FROM python:3.10-slim

WORKDIR /usr/src/app

COPY docker/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080

CMD ["python", "app.py", "--host=0.0.0.0", "--port=8080"]
