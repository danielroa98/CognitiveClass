# FROM python:3.6.1-alpine -> this version doesn't contain all of the required headers
FROM python:3
RUN pip3 install flask
CMD ["python","app.py"]
COPY app.py /app.py