# fetches Python image based on Slim
FROM python:3.8-slim

# setup working directory
WORKDIR /workdir

# copy folder into working directory
COPY src/ /workdir
# we can use the Book class to get additional information about the books that are generated
#COPY ../../webapp/code/app/book.py /workdir/

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt


CMD ["python", "/workdir/run.py"]
