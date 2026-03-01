# Processor app

## Prerequisites

- Docker
- AWS CLI

## How to get set up

To start all containers run `docker compose up -d`
To stop all containers run `docker compose down`

## Check it's working (integration style tests):

### localstack

- Run `curl localhost:4566/_localstack/health` to see if localstack is health and running
- Run `aws --endpoint-url=http://localhost:4566 s3 ls` to check our buckets for raw and aggregate data

Check if data is being written raw to our buckets:

```
aws --endpoint-url=http://localhost:4566 s3 ls s3://raw-events
```

Check if data is being written to our aggregate buckets (after 60 seconds there should be data):

```
aws --endpoint-url=http://localhost:4566 s3 ls s3://aggregated-events --recursive
```

Read a particular aggregate file:

```
aws --endpoint-url=http://localhost:4566 s3 cp s3://aggregated-events/<path-to-file>
aws --endpoint-url=http://localhost:4566 s3 cp s3://aggregated-events/postcode=ZW9F0WD/window=2026-02-26T21-19-00.json -
```

### flink

Check logs with:

```
docker logs flink-aggregator
```

### kafka

Check running topics with:

```
docker exec -it checkout-kafka opt/kafka/bin/kafka-topics.sh \
--list \
--bootstrap-server kafka:9092
```

Note: there should be a topic at start up called 'visit_events' when running the docker set up locally,
as this will be autocreated by our test consumer.

- Write a test event to the topic: 

```
docker exec -it checkout-kafka opt/kafka/bin/kafka-console-producer.sh \
--topic visit_events \
--bootstrap-server kafka:9092
```

- Check events are being written to the topic: 

```
docker exec -it checkout-kafka opt/kafka/bin/kafka-console-consumer.sh \
--topic visit_events \
--from-beginning \
--bootstrap-server kafka:9092
```

- Create a topic with (although this is done automatically): 

```
docker exec -it checkout-kafka opt/kafka/bin/kafka-topics.sh \
--create \
--topic events \
--partitions 3 \
--replication-factor 1 \
--bootstrap-server kafka:9092
```

## Run unit tests

From the root folder:
```
python -m pytest tests/test_producer.py -v 
```