FROM puckel/docker-airflow:1.10.4

USER root
RUN pip install --upgrade youtube_dl
USER airflow

# RUN curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl
# RUN chmod a+rx /usr/local/bin/youtube-dl

# COPY requirements.txt .
# RUN pip install -r requirements.txt

