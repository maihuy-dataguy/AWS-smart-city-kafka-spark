# AWS-smart-city-kafka-spark

## Introduction
This project provides a comprehensive data pipeline solution to extract, transform, and load (ETL) Reddit data into a Redshift data warehouse. The pipeline leverages a combination of tools and services including Spark Streaming, Apache Kafka, Amazon S3, AWS Glue, Amazon Athena, and Amazon Redshift. Kafka and Spark are containerized using Docker for ease of deployment and scalability to load data into S3 Storage for production.

## System Architecture
![System Architecture](https://github.com/maihuy-dataguy/AWS-smart-city-kafka-spark/blob/main/pics/aws%20smart-city.png)

The project is designed with the following Technology Stack:

- **Data Source** : Assumed data fetched from IOT devices, illustrating the information about the vehicle travelling from London to Birmingham
- **Apache Kafka**: Managing streaming data through metadata fetched from zookeeper, broker.
- **Apache Spark**: Processing streaming data from Kafka and write data into S3 Storage
- **Docker**: For deploying containers such as zookeeper, broker from kafka and master node, worker nodes from spark
- **Simple Storage Service (S3)**: sink storage written from Spark streaming, object storage service can be regarded as a data lake
- **AWS Glue**: Manage ETL jobs, we are going to transform data through Spark and load back into S3. Create metadata tables definition stored in data catalog by running crawlers. 
- **AWS Athena**: For querying the transformed data beneath S3. Querying through database and metadata tables created from AWS Glue crawlers
- **Amazon Redshift**: For data warehousing, we can query and make statistics from external table created from external database AWS Glue Data Catalog.
- **BI Tools**: we can connect to tableau, looker, power bi through Redshift endpoint, AWS Athena or Data catalog connection.

## Prerequisites
- AWS Account with appropriate permissions for S3, Glue, Athena, and Redshift.
- Docker Installation
- Python-3.12 , Spark(3.5.4) (to this point)

## Getting started
1. Clone the repository:
    ```bash
    git clone https://github.com/maihuy-dataguy/AWS-smart-city-kafka-spark.git
    ```
2. Create a virtual environment.
    ```bash
    virtualvenv env
    ```
3. Activate the virtual environment.
     ```bash
    source venv/bin/activate
    ```
4. Install the dependencies.
    ```bash
    pip install -r requirements.txt
    ```
5. Input AWS configurations needed for Spark streaming sink 
     ```bash
     mv config/config.conf.example config/config.conf
    ```
    
   Input these configuration in config.conf file

    ```bash
    
    reddit_clientconfiguration = {
    "AWS_ACCESS_KEY": "",
    "AWS_SECRET_KEY": "",
    "BUCKET_NAME": ""
    }

    ```
6. Starting the containers
     ```bash
     docker compose up -d
    ```
7. Submit Spark streaming job to master node container
    ```bash
      docker exec -it awssmartcityde-spark-master-1 spark-submit --master spark://spark-master:7077 \
                 --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.1,org.apache.hadoop:hadoop-aws:3.3.1,com.amazonaws:aws-java-sdk:1.11.469 \
                 jobs/spark-stream-consumer.py
    ```
8. Can use kafka CLI to check topic created and consumed for testing through broker container using docker desktop 
   ```bash
       kafka-topics --bootstrap-servers broker:29092 --list
    ```
   ```bash
       kafka-console-consumer --topic vehicle_data --bootstrap-servers broker:29092 --from-beginning
   ```
9. Check written data in bucketname/data from S3

    ![System Architecture](https://github.com/maihuy-dataguy/AWS-smart-city-kafka-spark/blob/main/pics/S3_data.png)
   
