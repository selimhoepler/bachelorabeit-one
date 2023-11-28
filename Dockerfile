# Use an official Python runtime as a parent image
FROM python:3.10

# Setting work directory
WORKDIR /app

# copy only requirements.txt first for cache purposes
COPY ./requirements.txt /app/requirements.txt

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app

# Make port 80 available to the world outside this container
EXPOSE 80

# set env variables for temp path files
ENV PICKLE_PATH=/app/app/temp
ENV JSON_PATH=/app/static/json


# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]