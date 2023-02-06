# Rasa Assistant Example

This is a Rasa chatbot example demonstrating how to build an AI assistant. Below is an example conversation, showing the bot helping a user open a support ticket and query its status.

Here is an example of a conversation you can have with this bot:

```
Coming soon ...
```

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Rasa Assistant Example](#rasa-assistant-example)
  - [Setup](#setup)
    - [Install the dependencies](#install-the-dependencies)
  - [Running the bot](#running-the-bot)
  - [Things you can ask the bot](#things-you-can-ask-the-bot)
  - [Example conversations](#example-conversations)
  - [Testing the bot](#testing-the-bot)
  - [Rasa X Deployment](#rasa-x-deployment)
    - [Action Server Image](#action-server-image)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Setup

### Install the dependencies

In a Python3 virtual environment run:

```bash
pip install -r requirements.txt
```

To install development dependencies, run:

```bash
pip install -r requirements-dev.txt
pre-commit install
```

## Running the bot

Use `rasa train` to train a model.

Then, to run, first set up your action server in one terminal window:

```bash
rasa run actions
```

In another window, run the duckling server (for entity extraction):

```bash
docker run -p 8000:8000 rasa/duckling
```

Then to talk to the bot, run:

```bash
rasa shell --debug
```

Note that `--debug` mode will produce a lot of output meant to help you understand how the bot is working
under the hood. You can also add this flag to the action server command. To simply talk to the bot, you can remove this flag.

## Things you can ask the bot

[//]: # (The bot has two main skills:)

[//]: # (1. Opening an incident in ServiceNow.)

[//]: # (2. Checking the status of incidents in ServiceNow by email address of the caller. It will prompt the user to re-use previously provided &#40;during the chat session&#41; email addresses, if any exist.)

[//]: # (For the purposes of illustration, the bot recognizes the following as requests to open an incident:)

[//]: # ()
[//]: # (1. Asking to open an incident directly e.g. "I want to open an incident")

[//]: # (2. Asking about a problem resetting their password e.g. "I can't reset my password")

[//]: # (3. Asking about a problem with outlook/email e.g. "I can't log in to my outlook")

Take a look at `data/nlu.md` to see what the bot is currently trained to recognize.

It can also respond to requests for help (e.g. "help me").

## Example conversations

(Coming soon ...)

[//]: # (```)

[//]: # (Your input ->  help me reset my password)

[//]: # (    What is your email address?)

[//]: # (Your input ->  idontexist@example.com)

[//]: # (    Sorry, "idontexist@example.com" isn't in our incident management system. Please try again.)

[//]: # (    What is your email address?)

[//]: # (Your input ->  abraham.lincoln@example.com)

[//]: # (    ? What is the priority of this issue?)

[//]: # (Your input -> 3: high &#40;/inform{"priority":"high"}&#41;)

[//]: # (    What is the problem description for the issue?)

[//]: # (Your input ->  Password stuck in a loop)

[//]: # (    ? Should I open an incident with the following details?)

[//]: # (    email: abraham.lincoln@example.com)

[//]: # (    problem description: Password stuck in a loop)

[//]: # (    title: Problem resetting password)

[//]: # (    priority: high)

[//]: # (Your input ->  1: Yes &#40;/affirm&#41;)

[//]: # (    Successfully opened up incident INC0010008 for you.  Someone will reach out soon.)

[//]: # (Your input ->  Can I check the status of my tickets?)

[//]: # (    Would you like to use the last email address you used, abraham.lincoln@example.com?)

[//]: # (Your input ->  Yes please)

[//]: # (    Incident INC0010002: "Email Log in problem", opened on 2020-05-21 09:57:06 is currently in progress)

[//]: # (    Incident INC0010008: "Problem resetting password", opened on 2020-05-21 12:12:49 is currently awaiting triage)

[//]: # (Your input ->  thanks)

[//]: # (    You're welcome!)

[//]: # (```)

## Testing the bot

You can test the bot on the test conversations by running  `rasa test`.
This will run [end-to-end testing](https://rasa.com/docs/rasa/user-guide/testing-your-assistant/#end-to-end-testing) on the conversations in `tests/conversation_tests.md`.

## Rasa X Deployment

To [deploy helpdesk-assistant](https://rasa.com/docs/rasa/user-guide/how-to-deploy/), it is highly recommended to make use of the
[one line deploy script](https://rasa.com/docs/rasa-x/installation-and-setup/one-line-deploy-script/) for Rasa X. As part of the deployment, you'll need to set up [git integration](https://rasa.com/docs/rasa-x/installation-and-setup/integrated-version-control/#connect-your-rasa-x-server-to-a-git-repository) to pull in your data and
configurations, and build or pull an action server image.

### Action Server Image

See the Dockerfile for what is included in the action server image,

To build the image:

```bash
docker build . -t <name of your custom image>:<tag of your custom image>
```

To test the container locally, you can then run the action server container with:

```bash
docker run -p 5055:5055 <name of your custom image>:<tag of your custom image>
```

Once you have confirmed that the container works as it should, you can push the container image to a registry with `docker push`

It is recommended to use an [automated CI/CD process](https://rasa.com/docs/rasa/user-guide/setting-up-ci-cd) to keep your action server up to date in a production environment.
