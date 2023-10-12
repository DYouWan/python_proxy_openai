import os
import logging
import requests
from flask import Flask, request, Response

app = Flask(__name__)


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    if path == "":
        return proxy_default()
    else:
        return proxy_openai(path)


def proxy_openai(path) -> bytes:
    url = f"https://api.openai.com/{path}"
    headers = {key: value for (
        key, value) in request.headers.items() if key != 'Host'}

    data = request.get_data()
    # app.logger.info(data)
    rsp = requests.request(request.method, url, headers=headers, data=data)
    # app.logger.info(rsp.content)
    return rsp.content


def proxy_default() -> Response:
    env_file_path = os.path.join(os.getcwd(), '.env')
    with open(env_file_path, 'r') as env_file:
        content = env_file.read()
    return Response(content, mimetype='text/plain')


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
