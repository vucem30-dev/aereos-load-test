# For this test to run we need 5 files:
# test.jmx
# test.properties
# master.xml
# house.xml
# manifiesto.xml
# The first three files are the JMeter test plan and the properties file.
# The last three files are the XML TEMPLATE files that will be used to generate the test data.
docker run -it --rm \
  --name aereos \
  -v $(pwd):/opt/jmeter/files \
  gustavoarellano/jmeter-vucem3-privados-aereos-load-test
