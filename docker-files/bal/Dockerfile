# Use an openjdk 8 image as the base image
FROM openjdk:8-jdk

# Set the working directory to /app
WORKDIR /app

# Copy the WAR file to the /app directory
COPY blockchain-access-layer.war .

# Download and install Apache Tomcat 8
RUN apt-get update && \
    apt-get install -y wget && \
    wget https://archive.apache.org/dist/tomcat/tomcat-8/v8.5.56/bin/apache-tomcat-8.5.56.tar.gz && \
    tar xzf apache-tomcat-8.5.56.tar.gz && \
    mv apache-tomcat-8.5.56 tomcat

# Remove the downloaded tar file
RUN rm apache-tomcat-8.5.56.tar.gz

# Copy the WAR file to the Tomcat webapps directory
RUN mv blockchain-access-layer.war tomcat/webapps/

RUN mkdir /app/plugins

# Set the environment variable for the Tomcat home directory
ENV CATALINA_HOME /app/tomcat

ENV JAVA_OPTS -Dpf4j.pluginsDir=/app/plugins

EXPOSE 9092
# Start Tomcat
CMD ["/app/tomcat/bin/catalina.sh", "run"]