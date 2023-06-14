from datetime import datetime, timedelta
import urllib.request
import json
import time

from airflow import DAG
from airflow.providers.google.cloud.operators.pubsub import PubSubCreateTopicOperator, PubSubPublishMessageOperator
from airflow.decorators import task
from airflow.models import Variable

now = datetime.now()
start_date_with_minutes = now - timedelta(minutes=3)
with DAG(
    'lastfm',
    description='Meu Lastfm',
    schedule_interval = '* * * * *',
    start_date=start_date_with_minutes,
    tags=['lastfm']
) as dag:
    
    project_id = Variable.get("project_id")
    topic_name = 'lastfm_topic'

    create_topic = PubSubCreateTopicOperator(
    task_id='create_topic',
    project_id=project_id,
    topic=topic_name,
    gcp_conn_id='gcp_conn',
    fail_if_exists=False)

    @task
    def get_data_and_send_to_pubsub():
        for _ in range(21):
            lastfm_username = Variable.get("lastfm_username")
            lastfm_public_key = Variable.get("lastfm_public_key")

            url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + lastfm_username + "&api_key=" + lastfm_public_key + "&format=json"
            data = urllib.request.urlopen(url).read().decode()
            obj = json.loads(data)

            data_dict = {}
            for track in obj['recenttracks']['track']:
                if '@attr' in track and 'nowplaying' in track['@attr'] and track['@attr']['nowplaying'] == 'true':
                    lastplayed_trackname = track['name']
                    lastplayed_artist = track['artist']['#text']
                    lastplayed_album = track['album']['#text']
                    lastplayed_image_url = track['image'][3]['#text']

                    data_dict = {
                        "lastplayed_trackname": lastplayed_trackname,
                        "lastplayed_artist": lastplayed_artist,
                        "lastplayed_album": lastplayed_album,
                        "lastplayed_image_url": lastplayed_image_url,
                    }
            print(data_dict)
            data_bytes = json.dumps(data_dict).encode('utf-8')

            PubSubPublishMessageOperator(
                task_id='publish_to_pubsub',
                topic='lastfm_topic',
                messages=[{"data": data_bytes}], 
                project_id=project_id,
                gcp_conn_id='gcp_conn'
            ).execute(context={})

            time.sleep(2)

lastfm_to_pubsub = get_data_and_send_to_pubsub()

create_topic >> lastfm_to_pubsub
