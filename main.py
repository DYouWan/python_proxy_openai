from flask import Flask, request
import requests
import logging
import os

app = Flask(__name__)

OPENAI_API_HOST = "api.openai.com"

# 配置日志记录
logging.basicConfig(filename='app.log', level=logging.INFO)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def proxy(path):

    # 记录请求的日志
    app.logger.info(f"请求地址：{request.url}")

    if path.startswith('/v1'):
        url = f"https://{OPENAI_API_HOST}/{path}"
        headers = request.headers
        data = request.get_data()

        response = requests.request(
            request.method, url, headers=headers, data=data)
        return response.content, response.status_code, response.headers.items()
    else:
        env_file_path = os.path.join(os.getcwd(), '.env')
        with open(env_file_path, 'r') as env_file:
            content = env_file.read()
        return content


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
