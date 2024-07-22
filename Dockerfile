FROM python:3.7
WORKDIR /app
COPY ./app ./app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# COPY ./init_db.py ./init_db.py
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
