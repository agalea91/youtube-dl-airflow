# youtube-dl-airflow

Schedule and execute playlist downloads.

## Installation

 - [Docker compose](https://docs.docker.com/compose/install/)

## Running with Docker
```
# Download source
git clone https://github.com/agalea91/youtube-dl-airflow.git
cd youtube-dl-airflow

# Launch docker container
docker-compose -f docker-compose.yaml up -d --build

# Check that your container is live
docker container ls
docker ps

# Check container's logs
docker logs <ID>
```

Open the airflow webserver console here on port 8080:

http://localhost:8080

Turn the "download_youtube_playlists" DAG on.

The service can be shut down with docker-compose:
```
docker-compose -f docker-compose.yaml down
```

As the jobs run, you should see files appear in the `videos` folder. These will be partitioned by playlist.


## Configuration

By default, the airflow scheduler trigger the script to run daily. For each playlist included in `dags/youtube_playlists.json`, up to 10 of the most recetly added videos will be downloaded, ignoring anything downloaded already.

Some of these configuration options can be changed by edditing the DAG file `dags/download_youtube_playlists.py`, or by setting environment variables in `docker-compose.yaml`. In particular, you can change any of the following defaults:

```
# Max number of videos downloaded per day per playlist
MAX_DOWNLOADS=10
```

## Tips

### Re-setting the database

We use a volume to persist the airflow database on the host. It can be reset by running `rm -r airflow-db/postgresql`

Similarly, the log history can be removed by running `rm -r airflow-logs`


