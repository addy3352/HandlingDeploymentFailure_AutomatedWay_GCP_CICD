# Use the official lightweight Python image.
#### Installing GIT
FROM bitnami/git:latest
FROM python:3.8-slim
RUN apt-get update
RUN apt-get install -y pip 
FROM gcr.io/google.com/cloudsdktool/cloud-sdk:latest
ENV APP_HOME /app
#ENV GOOGLE_APPLICATION_CREDENTIALS 
WORKDIR $APP_HOME
#RUN ["ls"]
#ENV GOOGLE_APPLICATION_CREDENTIALS $key_file
# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
COPY . ./
RUN export GOOGLE_IMPERSONATE_SERVICE_ACCOUNT=<impersonate service account>
RUN pip install --no-cache-dir -r requirements.txt
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app
