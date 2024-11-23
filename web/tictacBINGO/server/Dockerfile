FROM python:3.13.0a6-alpine3.18

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["flask", "--app=server.py", "run", "--host=0.0.0.0", "--port=5000"]