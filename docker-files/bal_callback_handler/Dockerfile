# Use an official Python runtime as the base image
FROM python:3.8-buster

# Set the working directory in the container
WORKDIR /app

# Clone the GitHub repository
RUN git clone https://github.com/akshay-ap/bal-callback-handler.git .

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable for Flask
ENV FLASK_APP=server.py

ENV FLASK_RUN_PORT=5010

# Expose port 5000 for the Flask server
EXPOSE 5010

# Run the command to start the Flask server
CMD ["flask", "run", "--host=0.0.0.0"]