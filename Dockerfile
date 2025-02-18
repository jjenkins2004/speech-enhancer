FROM python:3.11

RUN apt-get update && \
    apt-get install -y build-essential gcc python3-dev && \
    apt-get clean

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN make clean -C /app/rnnoise_IO

RUN make -C /app/rnnoise_IO

CMD ["python", "rnnoise_wrapper.py"]