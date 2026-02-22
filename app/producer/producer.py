import json
import time
import random
from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'kafka:9092'
}
producer = Producer(conf)
topic = "visit_events"

while True:

    event = {
        "user_id": random.randint(1, 5000),
        "postcode" : "SW19", # generate some variety here
        "webpage": "www.website.com/index.html", # generate some variety here
        "timestamp": time.time()
    }

    producer.produce(topic, json.dumps(event).encode('utf-8'))

    print("Produced:", event)

    producer.flush()

    time.sleep(1)

