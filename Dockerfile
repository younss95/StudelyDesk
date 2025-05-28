FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip && pip install -r requirements.txt

ENV PYTHONPATH=/app/src

EXPOSE 3000

CMD ["python", "./src/studelydesk/views/web.py"]