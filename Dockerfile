FROM python:3.8
RUN mkdir /code
WORKDIR /code
COPY ./folder/ /code/
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python new.py
