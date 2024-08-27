# Use the official Python image from Docker Hub
FROM python:3.9-slim

# Install sqlite3
RUN apt-get update && apt-get install -y sqlite3 

# Set the working directory in the container
WORKDIR /esp
# Copy the current directory contents into the container at /app
COPY . /esp

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the website will run on
EXPOSE 8000

# Command to run your entrypoint script
CMD bash -c "./bin/espdb create && ./bin/esprun"
