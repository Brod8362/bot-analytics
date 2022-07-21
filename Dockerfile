FROM python:3.10

COPY app.py /app/app.py
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r /app/requirements.txt
EXPOSE 9646

ENTRYPOINT ["python3", "-m", "flask", "run", "-h", "0.0.0.0", "-p", "9646"]