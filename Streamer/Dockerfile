FROM piotrsicinski/pam-base:latest

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN chmod +x RTMP_Server/rtsp-simple-server

CMD [ "sh", "-c", "cd /app/RTMP_Server && ./rtsp-simple-server & cd /app && python ./app.py" ]
