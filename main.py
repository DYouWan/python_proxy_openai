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

    app.logger.info("123")
    app.logger.info(path)

    first_slash_index = path.index('/', 0)  # 找到从索引 8 开始的第一个斜杠
    path_header = str[:first_slash_index]
    path_route = str[first_slash_index+1:]

    if path_header == "p1":
        return proxy_openai(path_route)
    elif path_header == "p2":
        return proxy_openai(path[7:])
    else:
        return proxy_default()


def proxy_openai(path) -> bytes:
    url = f"https://api.openai.com/v1/{path}"
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
