import os, json, base64, logging
from flask_api import FlaskAPI
from flask import request
from backends.big_query import BqClient

app = FlaskAPI(__name__)
os.environ.setdefault('FLASK_APP', 'main.py')
os.environ.setdefault('GOOGLE_APPLICATION_CREDENTIALS', 'backends/credentials.json')


@app.route('/')
def hello():
    return 'Flask microservice PubSub BQ streaming handler'


@app.route("/pub-sub/", methods=['POST'])
def pob_sub():
    if request.data.get("message"):
        attributes = json.loads(request.data["message"].get("attributes").get("attrs"))
        data = request.data["message"].get("data")
        if not attributes:
            logging.warning("No attributes supplied")
            return "", 400
        if not data:
            logging.warning("No data supplied")
            return "", 400
        if not (attributes.get("dataset") or attributes.get("table")):
            logging.warning("No dataset or table supplied")
            return "", 400

        try:
            data = base64.b64decode(request.data["message"].get("data"))
            data = json.loads(data)
            table = attributes.get("table")
            data_set = attributes.get("dataset")
        except Exception as e:
            logging.error("Unexpected error: %s" % e)
            return "", 500
        BqClient().insert_row(data_set, table, data)
    else:
        logging.error("No pub-sub message body was found")
    return "", 200