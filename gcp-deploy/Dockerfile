# Start with a base image containing Python runtime
FROM python:3.10.9-slim-buster

# Set the working directory in the Docker image
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install the needed packages 
RUN pip install simpleaichat==0.2.0
RUN pip install chainlit==0.6.2
RUN pip install octoai-sdk

# Make ports 80 and 443 available to the world outside this container
EXPOSE 8080 443

# Run chainlit command when the container launches
CMD ["chainlit", "run", "app_octo.py"]
