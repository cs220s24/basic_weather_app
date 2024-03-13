import requests
import redis
import time
import dotenv
import os


dotenv.load_dotenv()

host = os.getenv('REDIS_HOST')
port = os.getenv('REDIS_PORT')
api_key = os.getenv('API_KEY')

r = redis.Redis(host=host, port=port)

while True:
    url = 'http://api.weatherapi.com/v1/current.json'

    params = {
        'key': api_key,
        'q': '18018',
    }

    results = requests.get(url, params=params).json()

    temp_f = results['current']['temp_f']

    r.set('temp_f', temp_f)
    # Flush the buffer to ensure it is printed immediately
    print('Saved {}. Sleeping for 15 minutes'.format(temp_f), flush=True)
    time.sleep(15 * 60)
