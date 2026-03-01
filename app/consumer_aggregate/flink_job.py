import json
import boto3
from datetime import datetime
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.window import TumblingEventTimeWindows
from pyflink.common import Time, WatermarkStrategy, Duration
from pyflink.datastream.functions import ProcessWindowFunction, ProcessFunction
from pyflink.common.typeinfo import Types

KAFKA_BOOTSTRAP = 'kafka:9092'
KAFKA_TOPIC = 'visit_events'
KAFKA_GROUP_ID = 'flink_aggregation_group'
S3_ENDPOINT = 'http://localstack:4566'
S3_BUCKET = 'aggregated-events'
AWS_ACCESS_KEY_ID = 'test'
AWS_SECRET_ACCESS_KEY = 'test'


class PostcodeAggregationFunction(ProcessWindowFunction):
    """Aggregate events in window: count page views per postcode."""

    def process(self, key, context, elements):
        count = sum(1 for _ in elements)
        window_start = context.window().start

        postcode = key
        datetime_str = datetime.fromtimestamp(window_start / 1000).isoformat()

        result = {
            'postcode': postcode,
            'datetime': datetime_str,
            'count': count
        }

        yield json.dumps(result)


class S3WriterProcessFunction(ProcessFunction):
    """Process function to write aggregated results to S3."""

    def __init__(self):
        self.s3_client = None

    def open(self, runtime_context):
        """Initialize S3 client."""
        self.s3_client = boto3.client(
            's3',
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        try:
            self.s3_client.create_bucket(Bucket=S3_BUCKET)
            print(f"Created bucket: {S3_BUCKET}")
        except Exception as e:
            print(f"Bucket {S3_BUCKET} may already exist: {e}")

    def process_element(self, value, ctx):
        """Write each aggregation result to S3."""
        try:
            data = json.loads(value)
            postcode = data['postcode'].replace(' ', '')
            datetime_str = data['datetime'].replace(':', '-')

            key = f"postcode={postcode}/window={datetime_str}.json"

            self.s3_client.put_object(
                Bucket=S3_BUCKET,
                Key=key,
                Body=value
            )

            print(f"Written to S3: {key}")
        except Exception as e:
            print(f"Error writing to S3: {e}")

        yield value


def parse_event(json_str):
    """Parse JSON event and extract postcode and timestamp."""
    event = json.loads(json_str)
    return {
        "postcode": event["postcode"],
        "timestamp": int(event["timestamp"] * 1000),
    }

def main():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(1) # would increase this as necessary in prod to add more process per postcode groups

    env.enable_checkpointing(10000) # enables resisiance, but could leads to dupes

    kafka_source = KafkaSource.builder() \
        .set_bootstrap_servers(KAFKA_BOOTSTRAP) \
        .set_topics(KAFKA_TOPIC) \
        .set_group_id(KAFKA_GROUP_ID) \
        .set_starting_offsets(KafkaOffsetsInitializer.earliest()) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

    watermark_strategy = WatermarkStrategy \
        .for_bounded_out_of_orderness(Duration.of_seconds(5)) \
        .with_timestamp_assigner(
            lambda event, ts: event["timestamp"]
        )

    stream = env.from_source(
        kafka_source,
        watermark_strategy,
        "Kafka Source"
    )

    parsed_stream = stream.map(
        parse_event,
        output_type=Types.MAP(Types.STRING(), Types.LONG())
    )

    keyed_stream = parsed_stream.key_by(
        lambda event: event["postcode"]
    )

    windowed_stream = keyed_stream.window(
        TumblingEventTimeWindows.of(Time.minutes(1))
    )

    aggregated_stream = windowed_stream.process(
        PostcodeAggregationFunction(),
        output_type=Types.STRING()
    )

    aggregated_stream.process(
        S3WriterProcessFunction(),
        output_type=Types.STRING()
    )

    env.execute("Postcode Aggregation Job")


if __name__ == '__main__':
    main()
