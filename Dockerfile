FROM python:3.8-slim
RUN mkdir /code
WORKDIR /code
# copy requirements separately to avoid reinstallation
ADD requirements.txt /code/
# Upgrade pip version and Install requirements
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# Copy the files
ADD . /code/





