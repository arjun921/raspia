import sys
import Adafruit_DHT
import redis
import json
import os
import time

redisClient = redis.StrictRedis(
            host = os.environ.get('REDIS_HOST'),
            port = os.environ.get('REDIS_PORT'),
            password = os.environ.get('REDIS_PWD')
        )
try:
    redisClient.ping()
    print('Connected!')
except Exception as e:
    print("error: {}".format(e))



while True:
    humidity, temperature = Adafruit_DHT.read_retry(11, 4)
    temperature = float("{0:0.1f}".format(temperature))
    data = {
            'timestamp': time.asctime(time.localtime(time.time())),
            'Temp': temperature, 
            'Humidity' : humidity
        }
    print(data)
    try:
        redisClient.lpush('room_data',json.dumps(data))
        time.sleep(5)
    except Exception as e:
        print(e)
