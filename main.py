import os
import logging
import requests
from flask import Flask, request, Response

app = Flask(__name__)

# 配置日志记录器
logging.basicConfig(level=logging.INFO)  # 设置日志记录级别为 INFO

OPENAI_API_HOST = "api.openai.com"


@app.route('/', defaults={'path': ''}, methods=['GET', 'POST', 'PUT', 'DELETE'])
@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy(path):
    if path == "":
        env_file_path = os.path.join(os.getcwd(), '.env')
        with open(env_file_path, 'r') as env_file:
            content = env_file.read()
        return Response(content, mimetype='text/plain')
    else:
        url = f"https://{OPENAI_API_HOST}/{path}"
        headers = {key: value for (
            key, value) in request.headers.items() if key != 'Host'}

        data = request.get_data()
        app.logger.info("请求OpenAi数据格式: ", data)
        rsp = requests.request(request.method, url, headers=headers, data=data)
        app.logger.info("OpenAi返回的数据格式: ", rsp.content)

        # 创建 Flask 响应对象
        flask_response = Response(rsp.content)
        app.logger.info("Flask响应对象: ", flask_response)

        # 复制原始响应的头信息到 Flask 响应对象
        for header, value in rsp.headers.items():
            flask_response.headers[header] = value

        return flask_response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
