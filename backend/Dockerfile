FROM python:3.10.9-slim
RUN apt update && apt install -y gcc cmake libpq-dev python-dev
WORKDIR /app/backend
COPY requirements.txt /requirements.txt
RUN pip3 install --upgrade pip --no-cache-dir
RUN pip3 install -r /requirements.txt --no-cache-dir
COPY . /app
CMD ["gunicorn", "back.wsgi:application", "--bind", "0.0.0.0:8000" ]