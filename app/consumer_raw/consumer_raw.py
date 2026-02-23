import json
import boto3
import uuid
from confluent_kafka import Consumer

BUCKET = "raw-events"

s3 = boto3.client(
    "s3",
    endpoint_url="http://localstack:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)

# create a bucket (should do this outside of the container in prod)
s3.create_bucket(Bucket=BUCKET)

conf = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'group1',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
consumer.subscribe(["visit_events"])

while True:

    msg = consumer.poll(1)

    if msg is None:
        continue

    raw_event = json.loads(msg.value())

    user = raw_event["user_id"]

    print("Consumed:", raw_event)
    print("Consumed:", user)

    key = str(uuid.uuid4())

    # Save to S3
    s3.put_object(
        Bucket=BUCKET,
        Key=key,
        Body=json.dumps(raw_event)
    )
