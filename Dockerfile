# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install necessary system dependencies
RUN apt-get update && apt-get install -y gcc libpq-dev build-essential

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Ensure psycopg2-binary is installed
RUN pip install psycopg2-binary
RUN pip install boto3

# Collect static files
RUN python manage.py collectstatic --noinput

# Make port 80 available to the world outside this container
EXPOSE 80

# Set the DJANGO_SETTINGS_MODULE environment variable
ENV DJANGO_SETTINGS_MODULE=online_shop.settings

# Run the application
#CMD ["sh", "-c", "python manage.py runserver 0.0.0.0:80"]
# Run the application with Gunicorn
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:80","online_shop.wsgi:application"]

