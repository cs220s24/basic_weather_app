from flask import Flask
import redis
import dotenv
import os

app = Flask(__name__)
dotenv.load_dotenv()

host = os.getenv('REDIS_HOST')
port = os.getenv('REDIS_PORT')

r = redis.Redis(host=host, port=port)


@app.route('/')
def home():
    confirmed = int(r.get('confirmed'))
    return 'confirmed: {}'.format(confirmed)


if __name__ == '__main__':
   app.run()
