# Takes a docker image with java 21
FROM openjdk:21-jdk-slim

# Install network tools
RUN apt-get update && apt-get install -y iputils-ping dnsutils telnet && rm -rf /var/lib/apt/lists/*

# Install JMeter
COPY apache-jmeter-5.6.3.tgz /tmp/
RUN mkdir /opt/jmeter && tar -xzf /tmp/apache-jmeter-5.6.3.tgz -C /opt/jmeter --strip-components=1

# Create report directories
RUN mkdir -p files/results/html_report

# Set working directory
WORKDIR /opt/jmeter

# Run the test
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


# jmeter -n -t files/test.jmx -q files/test.properties -l results/results.jtl -e -o results/html_report
