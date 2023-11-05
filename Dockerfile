FROM ubuntu:22.04

RUN apt-get update && apt-get install -y python3 python3-pip sqlite3 libgl1-mesa-glx libglib2.0-0

WORKDIR /app

COPY . . 

RUN pip3 install -r requirements.txt

RUN bash build/create_db.sh

CMD ["python3", "src/main.py"]