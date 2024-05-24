# slack
MQ Repo for Slack App

## Setting up slack
This section follows how to setup the slack aspect of the application.

The required scopes of the bot token are:
- `channels:history`
- `chat:write`
- `commands`
- `groups:history`
- `im:history`
- `mpim:history`
- `users:read`

Follow [Setup](#setup) to setup the API Gateway.
The deployed URL should be used for the slash commands 'Request URL', with the currently supported slash commands:
- /greetings
- /summarise
- /recap
- /question



<a name="setup"></a>
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

## Uploading repo to AWS
This stage involves updating the intermediary function and the commands function.

### Intermediary function
Zip the contents of the intermediary-function folder and upload it to the lambda function created.
```bash
$ (cd intermediary-function && zip -r ../intermediary-function.zip)
```

Set the environment variables to be:
- `AWS_LAMBDA_FUNC` = `name-of-commands-function`, e.g. slack-commands

### Commands function
Zip the contents of the commands-function folder along with the required packages, then upload it to the lambda function created.
```bash
$ cd commands-lambda
$ pip install --target . -r requirements.txt
$ zip -r ../commands-lambda.zip .
```

Set the environment variables to be:
- `RAPID_API_KEY` = `rapid-analysis-key`
- `SLACK_BOT_TOKEN` = `slack-bot-token`
- `SLACK_SIGNING_SECRET` = `slack-signing-secret`