import requests
import redis
import time
import dotenv
import os


dotenv.load_dotenv()

host = os.getenv('REDIS_HOST')
port = os.getenv('REDIS_PORT')

r = redis.Redis(host=host, port=port)

while True:
    url = 'https://data.cdc.gov/resource/9mfq-cb36.json?submission_date=2022-01-15'
    results = requests.get(url).json()
    confirmed = sum([int(result['tot_cases']) for result in results])

    r.set('confirmed', confirmed)
    time.sleep(15 * 60)
