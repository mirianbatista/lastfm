from datetime import datetime
from google.cloud import pubsub_v1
from google.api_core.exceptions import NotFound
import urllib.request
import json

from airflow import DAG
from airflow.providers.google.cloud.operators.pubsub import PubSubCreateTopicOperator, PubSubPublishMessageOperator
from airflow.decorators import task

with DAG(
    'lastfm_v1',
    description='Meu Lastfm',
    schedule_interval = '* * * * * *',
    start_date = datetime.now(),
    tags=['lastfm']
) as dag:
    
    project_id = 'project_id'
    topic_name = 'lastfm_topic'

    create_topic = PubSubCreateTopicOperator(
    task_id='create_topic',
    project_id=project_id,
    topic=topic_name,
    gcp_conn_id='gcp_conn',
    fail_if_exists=False)

    @task
    def get_data():
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
        
        return data_dict

    @task
    def publish_to_pubsub(data):
        data_bytes = json.dumps(data).encode('utf-8')

        publish_task = PubSubPublishMessageOperator(
            task_id='publish_to_pubsub',
            topic='lastfm_topic',
            messages=[{"data": data_bytes}], 
            project_id='project_id',
            gcp_conn_id='gcp_conn'
        )
        return publish_task.execute(context={})

    request_lastfm = get_data()
    send_to_pubsub = publish_to_pubsub(request_lastfm)


create_topic >> request_lastfm >> send_to_pubsub
