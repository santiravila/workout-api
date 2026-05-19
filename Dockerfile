# python 3 interpreter as my base image
FROM python:3.12.3

# filesystem to run commands to to copy files to
WORKDIR /app

# copy requirements before the source code to take advantage of cached builds 
COPY requirements.txt /app/

# Install dependencies
RUN pip install -r requirements.txt

# copy the rest of the project
COPY . .

# when a container is run, execute the following command to start the application
# Exec instead of shell form so uvicorn is PID 1 of the container
CMD ["uvicorn", "main:create_app", "--factory", "--host", "0.0.0.0"] 
