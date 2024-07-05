FROM python:latest

#Creating dir and cd
WORKDIR /app

COPY requirments.txt .

RUN pip install -r requirments.txt

COPY hello.py .

#Use Port 5000
EXPOSE 5000

#This will be executed during runtime of the container
CMD ["python", "hello.py"]