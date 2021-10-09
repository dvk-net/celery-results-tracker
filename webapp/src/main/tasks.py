import requests as r
import uuid
import time
from random import randint
from celery import shared_task
from django.conf import settings

CAT_URL = "http://thecatapi.com/api/images/get?format=src&type=gif"

@shared_task
def download_a_cat():
    resp = r.get(CAT_URL)
    file_ext = resp.headers.get('Content-Type').split('/')[1]
    file_name = settings.BASE_DIR / 'cats' / (str(uuid.uuid4())+ "." + file_ext)
    with open(file_name, 'wb') as f:
        for chunk in resp.iter_content(chunk_size=128):
            f.write(chunk)
    return True


@shared_task
def cpu_task():
    time_to_sleep = randint(5, 70)
    time.sleep(time_to_sleep)
    return f"I slept for {time_to_sleep} secs"