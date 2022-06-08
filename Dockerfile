FROM python:3.10

RUN mkdir /home/app

COPY ./app /home/app

RUN pip install -r /home/app/requirements.txt

WORKDIR /home/app


ENV DEFECT_DOJO_BASE_URL=http://example.com/api/v2
ENV DEFECT_DOJO_USERNAME=username 
ENV DEFECT_DOJO_PASSWORD=password
ENV JENKINS_BASE_URL=http://example.com/api/v2
ENV JENKINS_USERNAME=username
ENV JENKINS_PASSWORD=password
ENV USER_NOTF_API_BASE_URL=http://0.0.0.0:0000
ENV SSO_API_BASE_URL=https://0.0.0.0:0000
ENV USER_API_BASE_URL=http://0.0.0.0:0000
ENV ALPHA_SCALE_DB_USER=username
ENV ALPHA_SCALE_DB_PASSWORD=password
ENV ALPHA_SCALE_DB_HOST=0.0.0.0
ENV ALPHA_SCALE_DB_PORT=3306
ENV ALPHA_SCALE_DB_DATABASE=database-name

ENTRYPOINT [ "python" ]

CMD [ "/home/app/app.py" ]