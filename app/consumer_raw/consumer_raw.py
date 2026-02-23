import json
import boto3

BUCKET = "raw-events"

s3 = boto3.client(
    "s3",
    endpoint_url="http://localstack:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
)


s3.create_bucket(Bucket=BUCKET)


raw_event = {}

raw_event['webpage'] = "abc"
raw_event['user_id'] = "123"

# Save to S3
s3.put_object(
    Bucket=BUCKET,
    Key="aggregates.json",
    Body=json.dumps(raw_event)
)

print("Event:", raw_event)