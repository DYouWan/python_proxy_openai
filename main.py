from flask import Flask, request, Response
import requests
import os
import gzip
import logging

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
        response = requests.request(
            request.method, url, headers=headers, data=data, allow_redirects=False
        )

        app.logger.info(response.headers.get("Content-Encoding"))
        app.logger.info(response.content)

        # 检查响应的内容类型是否为 JSON
        if response.headers.get("Content-Type") == "application/json":
            # 使用原始数据
            uncompressed_data = response.content
        else:
            # 其他情况（如 gzip 压缩），使用原始数据或进行相应处理
            uncompressed_data = response.content

        # 将 OpenAI API 的响应转发给客户端
        return Response(uncompressed_data, response.status_code, headers=response.headers.items())


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
