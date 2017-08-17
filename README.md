# google-pubsub-bigquery-handler
Ready to deploy Google App Engine microservice using gcloud SDK. The service handle PubSub messages via PUSH and insert message into BigQuery tables.

# Supports
  - One or multiple rows per message
  - Bigquery insertion in background thread
  - Dataset/table target specified per message

# Pre-requisites
  - python 2.7/pip installed
  - gcloud SDK installed

# Installation

Clone repository
```sh
$ git clone https://github.com/andresjaor/google-pubsub-bigquery-handler.git
```

Create lib folder
```sh
$ pip install -t lib -r requirements.txt
```

# Setup
  - Create your BigQuery dataset - table schema
  - Create a PubSub topic
  - Create a PubSub subscriber for the topic and in "delivery type" option chose "push into an endpoint url". Put there the GAE url endpoint e.g.(**https://{{project}}.appspot.com/pub-sub**)
  - Generate a JSON service account key in APIs & services/credentials, copy and paste it into **credentials.json** file.
  
# deploy
```sh
$ gcloud app deploy
```

# Usage
PubSub messages has data and attributes fields. In data field put your json string data representation, in attributes define dataset and table. Publish your message using [google pubsub api](https://cloud.google.com/pubsub/docs/reference/libraries#client-libraries-install-python). Every message published will be handle by PubSub GAE microservice and data will be inserted.

Basic example with python client
```py
from google.cloud import pubsub
import json
attr = str(json.dumps({"dataset": dataset, "table": table}))
payload = json.dumps([{'column1': data1, 'column2': data2},
                      {'column1': data1, 'column2': data2}])
client = pubsub.Client()
topic = client.topic('topic_name')
topic.publish(payload, attrs=attr)
```
**Important: dictionary key names on payload must be equal to column names of BQ table.**
