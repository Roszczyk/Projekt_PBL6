FROM 10.141.10.69:5000/pam-base:latest

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN chmod +x RTMP_Server/rtsp-simple-server

CMD [ "sh", "-c", "cd RTMP_Server && ./rtsp-simple-server & cd .. && python ./app.py" ]
