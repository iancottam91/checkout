FROM flink:1.18-scala_2.12-java11

USER root

RUN apt-get update && \
    apt-get install -y python3 python3-pip wget openjdk-11-jdk-headless && \
    ln -s /usr/bin/python3 /usr/bin/python && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget -P /opt/flink/lib/ https://repo1.maven.org/maven2/org/apache/flink/flink-sql-connector-kafka/3.1.0-1.18/flink-sql-connector-kafka-3.1.0-1.18.jar

COPY requirements.txt /opt/flink/
ENV JAVA_HOME=/usr/lib/jvm/java-11-openjdk-arm64
RUN pip3 install -r /opt/flink/requirements.txt

COPY flink_job.py /opt/flink/job/

WORKDIR /opt/flink

USER flink

CMD ["/bin/bash", "-c", "/opt/flink/bin/start-cluster.sh && python3 /opt/flink/job/flink_job.py"]
