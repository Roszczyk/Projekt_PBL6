FROM piotrsicinski/pam-base:latest

WORKDIR /app

COPY . .

RUN chmod +x RTMP_Server/rtsp-simple-server

CMD [ "sh", "-c", "RTMP_Server/rtsp-simple-server & python ./app.py" ]
