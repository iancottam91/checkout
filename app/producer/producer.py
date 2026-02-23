import json
import time
import random
import string

from confluent_kafka import Producer

conf = {
    'bootstrap.servers': 'kafka:9092'
}
producer = Producer(conf)
topic = "visit_events"

def generate_uk_postcode():
    # Possible outward code formats
    outward_formats = [
        "A9", "A9A", "A99",
        "AA9", "AA9A", "AA99"
    ]
    
    format_choice = random.choice(outward_formats)
    
    postcode = ""
    
    for char in format_choice:
        if char == "A":
            postcode += random.choice(string.ascii_uppercase)
        elif char == "9":
            postcode += random.choice(string.digits)
    
    # Inward code is always: 9AA
    inward = (
        random.choice(string.digits) +
        random.choice(string.ascii_uppercase) +
        random.choice(string.ascii_uppercase)
    )
    
    return postcode + " " + inward

def generate_webaddres():
    protocols = ["http", "https"]
    tlds = [".com", ".co.uk"]
    domain = ''
    domain = domain.join(random.choice(string.ascii_lowercase) for _ in range(random.randint(5, 12)))
    protocol = random.choice(protocols)
    tld = random.choice(tlds)


    return f"{protocol}://www.{domain}{tld}"

if __name__ == "__main__":
    while True:

        webpage = generate_webaddres()
        postcode = generate_uk_postcode()

        event = {
            "user_id": random.randint(1, 5000),
            "postcode" : postcode, # generate some variety here (rand )
            "webpage": webpage, # generate some variety here
            "timestamp": time.time()
        }

        producer.produce(topic, json.dumps(event).encode('utf-8'))

        print("Produced:", event)

        producer.flush()

        time.sleep(1)

