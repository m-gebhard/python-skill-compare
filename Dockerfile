# init with python image
FROM python:3.8-slim-buster

EXPOSE 5000

# install project dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# make the '/app' folder the current working directory
WORKDIR /app
COPY . .

# run schedule
CMD ["python3", "main.py"]