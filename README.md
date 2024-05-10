# slack
MQ Repo for Slack App

## Setup
The project provides two seperate lambda functions:
    - an **intermediary function** serving as a middleman between Slack and command processing to ensure commands don't timeout; and
    - a **commands function** for processing commands sent to the Slack application and responding as needed.

### Intermediary function
The AWS lambda function requires the following additional permissions:
- *Lambda:InvokeFunction* for the commands Lambda function

### Commands function
The AWS lambda function requires the following additional permissions:
- *Lambda:InvokeFunction, Lambda:GetFunction* for itself

### API Gateway
The gateway should have a POST method that has its integration type as 'Lambda function' with Lambda proxy integration enabled. The Lambda function to be invoked should be set to the intermediary function.