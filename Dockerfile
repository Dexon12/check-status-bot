# Use an official Python runtime based on Alpine as a parent image
FROM python:3.11

# Set the working directory in the container to /app
WORKDIR /app


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the current directory contents into the container at /app
COPY . .

# Install pipenv and dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Run app.py when the container launches
CMD ["hupper", "-m", "app"]
