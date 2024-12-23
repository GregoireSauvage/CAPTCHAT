# Start the Flask app in a container

# base python image
FROM python:3.10-slim

# Working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY requirements.txt ./
COPY app ./app
COPY src ./src
COPY main.py ./
COPY ML ./ML
COPY models ./models

# run the pip install command
RUN pip install -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

ENV FLASK_APP=app.app:app

# command to run on container start
CMD ["python", "main.py"]