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
    temp_f = float(r.get('temp_f'))
    return 'temp_f: {}'.format(temp_f)


if __name__ == '__main__':
    if os.getenv('REDIS_HOST') is None:
        print('REDIS_HOST is not set')
        exit(1)

    if os.getenv('REDIS_PORT') is None:
        print('REDIS_PORT is not set')
        exit(1)

    app.run(host='0.0.0.0', port=8000)
