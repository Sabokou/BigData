# fetches Python image based on Slim
FROM python:3.8-slim

# setup working directory
WORKDIR /Webapp

# install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

# copy folder into working directory
COPY Webapp/ /Webapp

EXPOSE 80
EXPOSE 5000

CMD ["python", "/Webapp/code/run.py"]
