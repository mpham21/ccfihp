# Collaborative Care for In-Home Patients

___

This project is seeks to provide an IoT messaging platform to support collaborative care for in home patients.

## Architecture Description

![](/Users/matthewpham/Library/Application Support/typora-user-images/image-20200304161206528.png)





##Installation/Set Up

____

This set up outlined in context of a POC of a simulated heart rate and a medication dispenser. This can be modified to fit the use case.

The set up of the messaging platform can be broken up into two parts:

1. Cloud set up
2. Device set up

### Cloud set up

####Setting up response stream

To set up the response stream, the following resources need to be created

1. SNS topic to allow messages to be published to and disseminated to end users
2. IoT Rule to reroute trigger messages to AWS Lambda 
3. A Lambda function to handle messages 

#####SNS topic

1. Open AWS SNS Console
2. Go to "Topics" in the side bar
3. Create a topic for medical professionals
4. Add subscriptions to the topic (medical professional endpoints)
5. Create a topic for non-medical stakeholders 
6. Add subscription to the topic (non-medical stakeholders)

##### IoT Rule & Lambda function

Using the rules engine within the IoT Core, we can reroute messages published to a topic to a lambda function to allow us to respond with more complex actions. From the AWS IoT Console we can set up rules

1. Open AWS IoT Core Console
2. Go to "Act" in the side bar
3. Select "Rules" in the side bar
4. "Create" a new rule
5. Add query:

```sql
SELECT * FROM 'health_tracker/dt_stream' WHERE message.heart_rate > 80	
```

6. From the "select actions" menu select "send message to a Lambda function" and "configure action"
7. Create a new lambda function
   1. Set run time to "Python 3.8"
   2. Open drop down "Choose or create an execution role"
   3. "Create a new role from AWS policy templates"
   4. add "Amazon SNS publish policy" template to the role
8. upload "heart_rate_notification.py" to the lambda function
9. Update topic and region variables in "heart_rate_notification.py" to match the SNS topics made previously

#### Setting up data storage stream

To set up the data storage stream, the following resources need to be created

1. IoT Analytics 
   1. Channel
   2. Pipeline 
   3. Data Store
2. IoT rule to reroute telemetry data to data storage

#### IoT Analytics

1. Open AWS IoT Analytics Console
2. Use "Quick create" to createt all required components, use a prefix to denote device data to be stored and the appropriate MQTT topic, in this case "health_tracker/dt_stream"

This process should create a channel, pipeline, data store as well as an IoT rule to reroute the telemetry data. This data store can then be queried to create data sets to be used in AWS QuickSight.

### Device set up



#### Provisioning devices

To provision devices, the following resources are required

1. IoT Thing
2. Thing Policy
3. Device private key
4. Device certificate
5. Root certificate

This can all be done in the IoT Core

##### IoT Core

1. Open AWS IoT Console

2. Select "onboard" from side bar

3. Complete process and download device certificate and private key

4. To update what topics the device can publish and subscribe to, modify it's thing policy

   (For the sample devices, thing policies are included in their associated folders

#### Programming devices

To program on devices, the AWS IoT SDK should be installed on the device and is required for the demonstrated devices. In addition, the demo scripts were run on a raspberry pi to make use of the GPIO ports.

```bash
pip install AWSIoTPythonSDK
```

The "skeleton_device.py" provides a basis for devices to be programmed and provides a method to connect MQTT Client and basic routines for publishing device data. Note, endpoints and certificates need to be updated to reflect your own IoT devices.

## Usage

To run the sample demonstration, run 

Suggested best practices

Topic naming conventions

Standardised message format

