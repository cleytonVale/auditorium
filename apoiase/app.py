import json

import requests
from flask import Flask, jsonify
from flask_cors import CORS

import config


app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)


@app.route('/')
def home():
    if not config.APOIASE_URL:
        error = dict(error='Apoia.se URL not set as env variable!')
        return jsonify(error), 500

    response = requests.get(config.APOIASE_URL)
    if response.status_code == 200:
        page = json.loads(response.text)
        users = page.get('supports', {}).get('users', [])
        names = map(serializer, users)
        names = [name for name in names if name]
        return jsonify(names)


def serializer(users):
    private=users.get('privateSupport')
    if not private:
        return dict(name=users.get('_id').get('name'))



if __name__ == '__main__':
    app.run()
