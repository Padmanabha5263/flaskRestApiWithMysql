FROM python:3.10-slim

COPY . /app

WORKDIR /app

RUN pip install -r req.txt

EXPOSE 5000

CMD ["python", "crud.py"]