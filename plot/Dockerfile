FROM python:3.12

COPY requirements.txt /requirements.txt

RUN python3 -m pip install -r /requirements.txt

RUN mkdir /service_data

COPY src/plot.py /plot.py

CMD python3 /plot.py >> /log.txt
