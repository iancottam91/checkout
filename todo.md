# To do

## infra

- [x] create an s3 bucket to write raw and aggregated data
- [x] create a kafka instance to receive events
- [x] create a kafka topic
- [ ] think about a prod deploy:

## code
- [x] create a test producer (1.15 events per second to mimic 100k events per day)
    - add code for random postcode and website
- [x] create a consumer to write raw events (use basic container)
    - straight forward writes
- [x] create a consumer to aggregate events and write aggregates (use flink) ++


## Decisions
- Combined the kafka controller and broker for simpler local set up (talk about prod set up)
- Write While True because..
- Used full docker and local stack..
- Used flink for aggregates as wanted to see what it offers over simple python apps running in ECS as I've used in the past

## To Productionise:

### Kafka
- partitions for my topic based on postcodeID
- separate broker and controller containers (3 controllers, at least 3 brokers) 
- used a managed service
- env vars to switch between prod and local

# Flink
- increase parallelism
- ensure checkout pointing is written to persistant storage using 'get_checkpoint_config' (not in mem as local set up)
- improve check pointing to be exactly once
- use a managed service


