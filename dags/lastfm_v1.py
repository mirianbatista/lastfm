from datetime import date
from google.cloud import pubsub_v1
from google.api_core.exceptions import NotFound
import urllib.request
import json
import time

from airflow import DAG
from airflow.providers.google.cloud.operators.pubsub import PubSubCreateTopicOperator, PubSubPublishMessageOperator
from airflow.decorators import task

with DAG(
    'lastfm_v2',
    description='Meu Lastfm',
    schedule_interval = '* * * * * *',
    default_args={"start_date": date.today().strftime("%Y-%m-%d")},
    tags=['lastfm']
) as dag:
    
    # publisher = pubsub_v1.PublisherClient()
    project_id = 'project_id'
    topic_name = 'lastfm_topic'
    # topic_path = publisher.topic_path(project_id, topic_name)

    create_topic = PubSubCreateTopicOperator(
    task_id='create_topic',
    project_id=project_id,
    topic=topic_name,
    gcp_conn_id='gcp_conn',
    fail_if_exists=False)

    @task
    def get_data_and_send_to_pubsub():
        while True:
            lastfm_username = "lastfm_username"
            lastfm_public_key = "lastfm_public_key"

            url = "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user=" + lastfm_username + "&api_key=" + lastfm_public_key + "&format=json"
            data = urllib.request.urlopen(url).read().decode()
            obj = json.loads(data)

            lastplayed_trackname = obj['recenttracks']['track'][0]['name']
            lastplayed_artist = obj['recenttracks']['track'][0]['artist']['#text']
            lastplayed_album = obj['recenttracks']['track'][0]['album']['#text']
            lastplayed_image_url = obj['recenttracks']['track'][0]['image'][3]['#text']

            data_dict = {
                "lastplayed_trackname": lastplayed_trackname,
                "lastplayed_artist": lastplayed_artist,
                "lastplayed_album": lastplayed_album,
                "lastplayed_image_url": lastplayed_image_url
            }
            print(data_dict)
            
            data_bytes = json.dumps(data_dict).encode('utf-8')

            # publisher.publish(topic_path, data_bytes)

            time.sleep(10)

lastfm_to_pubsub = get_data_and_send_to_pubsub()

create_topic >> lastfm_to_pubsub
