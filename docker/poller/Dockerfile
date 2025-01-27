FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY modbus-async.py .

CMD ["python", "./modbus-async.py"]