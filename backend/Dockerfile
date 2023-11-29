FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY . .

COPY ./entrypoint.sh /app/entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]