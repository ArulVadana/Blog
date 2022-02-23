FROM python:latest
WORKDIR /app
COPY . .
RUN pip install -r requiremenys.txt
EXPOSE 80
CMD["python","main.py"]
