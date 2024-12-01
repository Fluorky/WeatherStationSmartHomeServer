# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8080 available to the world outside this container
EXPOSE 8080

# Make port 51826 available to the world outside this container
EXPOSE 51826

# Define environment variable
ENV FLASK_APP=main.py

# Copy .env to app
COPY .env /app/.env

# Run app.py when the container launches
CMD ["python", "main.py"]
