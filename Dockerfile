# Takes a docker image with java 21
FROM openjdk:21-jdk-slim

# Install network tools
RUN apt-get update && apt-get install -y iputils-ping dnsutils telnet && rm -rf /var/lib/apt/lists/*

# Install JMeter
COPY apache-jmeter-5.6.3.tgz /tmp/
RUN mkdir /opt/jmeter && tar -xzf /tmp/apache-jmeter-5.6.3.tgz -C /opt/jmeter --strip-components=1

# Set working directory
WORKDIR /opt/jmeter

# Run the test
ENTRYPOINT ["./bin/jmeter", "-n", "-t", "files/test.jmx", "-q", "files/test.properties"]