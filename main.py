from flask import Flask, request
import requests
import os

app = Flask(__name__)

OPENAI_API_HOST = "api.openai.com"


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):
    url = f"https://{OPENAI_API_HOST}/{path}"
    headers = request.headers
    data = request.get_data()

    response = requests.request(
        request.method, url, headers=headers, data=data)
    return response.content, response.status_code, response.headers.items()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
