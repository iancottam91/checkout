# To do

## infra

- [x] create an s3 bucket to write raw and aggregated data
- [x] create a kafka instance to receive events
- [x] create a kafka topic
- [ ] sort a prod deploy:
    - partitions for my topic,
    - separate broker and controller containers,
    - env vars to switch between prod and local

## code
- [x] create a test producer (1.15 events per second to mimic 100k events per day)
    - add code for random postcode and website
- [x] create a consumer to write raw events (use basic container)
    - straight forward writes
- [ ] create a consumer to aggregate events and write aggregates (use flink) ++

- [ ] tests
    - full e2e as minimum would be nice
