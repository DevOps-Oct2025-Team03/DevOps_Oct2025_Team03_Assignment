# #how to package the app into a docker image, ensure every app runs on same machine.

# FROM python:3.9-slim
 
# # Install system dependencies required for database drivers
# RUN apt-get update && apt-get install -y libpq-dev gcc
 
# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
 
# ENV FLASK_APP=run.py
# CMD ["flask", "run", "--host=0.0.0.0"]



# FROM python:3.9-slim

# RUN apt-get update && apt-get install -y libpq-dev gcc

# WORKDIR /app

# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# ENV PYTHONPATH=/app

# ENV FLASK_APP=run.py

# CMD ["flask", "run", "--host=0.0.0.0"]



# FROM python:3.9-slim

# RUN apt-get update && apt-get install -y libpq-dev gcc

# WORKDIR /app
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt

# COPY . .

# CMD ["python", "run.py"]


FROM python:3.9-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD ["python", "run.py"]
