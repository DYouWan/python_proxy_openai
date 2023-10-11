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

    first_slash_index = path.index('/', 0) 
    path_header = path[:first_slash_index]
    path_route = path[first_slash_index+1:]

    if path_header == "p1":
        return proxy_openai(path_route)
    elif path_header == "p2":
        return proxy_wikipedia(path_route)
    else:
        return proxy_default()


def proxy_openai(args) -> bytes:
    url = f"https://api.openai.com/v1/{args}"
    headers = {key: value for (
        key, value) in request.headers.items() if key != 'Host'}

    data = request.get_data()
    app.logger.info(data)
    rsp = requests.request(request.method, url, headers=headers, data=data)
    app.logger.info(rsp.content)
    return rsp.content


def proxy_wikipedia(args) -> bytes:
    url = f"https://en.wikipedia.org{args}"
    app.logger.info(url)
    headers = {key: value for (
        key, value) in request.headers.items() if key != 'Host'}

    data = request.get_data()
    rsp = requests.request(request.method, url, headers=headers, data=data)
    return rsp.content


def proxy_default() -> Response:
    env_file_path = os.path.join(os.getcwd(), '.env')
    with open(env_file_path, 'r') as env_file:
        content = env_file.read()
    return Response(content, mimetype='text/plain')


logging.basicConfig(level=logging.INFO)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
