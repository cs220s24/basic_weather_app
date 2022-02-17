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
    response = requests.get('https://covid19-api.com/totals')
    confirmed = response.json()[0]['confirmed']

    r.set('confirmed', confirmed)
    time.sleep(15 * 60)