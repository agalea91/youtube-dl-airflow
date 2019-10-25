# youtube-dl-airflow

Schedule and execute playlist downloads.

*Warning: Youtube has started banning IP addresses from using youtube-dl for bulk downloading. Use cautiously. Note, however, this ban would not affect your ability to use youtube.com through your browser.*

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

By default, the airflow scheduler trigger the script to run daily.

Define your playlists in `dags/youtube_playlists.json`. For example:

```
[
    {
        "name": "NutritionFacts.org",
        "url": "https://www.youtube.com/playlist?list=PL5TLzNi5fYd8AjdKq-w8Te5gE_23NfUr_"
    },
    {
        "name": "NHL Goals",
        "url": "https://www.youtube.com/playlist?list=PLo12SYwt93SRpev0BAtupgW7HMKfYfkWH"
    }
]
```


For each playlist included in `youtube_playlists.json`, the most recently added videos will be downloaded, ignoring anything downloaded already.

Set configurations by changing `docker-compose.yaml`.

 - Change environment variables, such as the number of max downloads per playlist:
```
environment:
   # User defined
   - MAX_DOWNLOADS=10
```

 - Change the mounted volumes, such as the place where videos are saved on your host machine:
 ```
volumes:
   - /path/on/your/host:/videos
 ```


## Tips

### Resetting the database

We use a volume to persist the airflow database on the host. It can be reset by running `rm -r airflow-db/postgresql`

Similarly, the log history can be removed by running `rm -r airflow-logs`


